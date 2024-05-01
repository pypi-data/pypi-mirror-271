#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ASKAP utility - update the pointing centre of a beam in an MS.
    - Allows imaging by CASA or wsclean.
"""
__author__ = ["Emil Lenc", "Alec Thomson"]
import logging
import math
import re
import sys

import numpy as np
from casacore.tables import table, tablecopy, tableexists, taql
from tqdm import trange

from fixms.logger import TqdmToLogger, logger

TQDM_OUT = TqdmToLogger(logger, level=logging.INFO)
logger.setLevel(logging.INFO)

RAD2DEG = 180.0 / math.pi
DEG2RAD = math.pi / 180.0


def beam_from_ms(ms: str) -> int:
    """Work out which beam is in this MS"""
    t = table(ms, readonly=True, ack=False)
    vis_feed = t.getcol("FEED1", 0, 1)
    beam = vis_feed[0]
    t.close()
    return beam


class Skypos:
    """Defines a class that works with spherical geometry, specifically points
    in a unit sphere, such as the sky.

    This is general spherical geometry, with little to tie it to astronomy. The
    exceptions are the naming of longitude and latitude as RA,Dec
    """

    def_precra = 3
    def_precde = 2

    def __init__(self, ra, dec, precra=def_precra, precdec=def_precde):
        """
        Initialise a Skypos object defining a point on a unit sphere with longitude ra and latitude dec
        :param ra: right ascension (radians or hh:mm:ss.ss)
        :type ra: float or str
        :param dec: declination (radians or dd:mm:ss.ss)
        :type dec: float or str
        :param precra:
        :param precdec:
        """
        if isinstance(ra, str):
            self.ra = ras_rad(ra)
            self.dec = decs_rad(dec)
        else:
            self.ra = ra
            self.dec = dec
        self.precra = precra
        self.precdec = precdec
        self.rn = 12 + self.precra - Skypos.def_precra
        self.dn = 12 + self.precdec - Skypos.def_precde
        self.ras = None
        self.decs = None
        ps = math.pi * 0.5 - self.dec
        sps = math.sin(ps)
        cps = math.cos(ps)
        sra = math.sin(self.ra)
        cra = math.cos(self.ra)
        self._dvecx = [cps * cra, cps * sra, -sps]
        self._dvecy = [-sra, cra, 0.0]
        self._dvecz = [sps * cra, sps * sra, cps]
        self._vec = [cra * sps, sra * sps, cps]

    def rotate_x(self, a):
        """return a skypos determined by rotating self about the X-axis by
        angle a."""
        x, y, z = _rotate_v_x(self._vec, a)
        b2 = math.asin(z)
        b1 = (2 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    def rotate_y(self, a):
        """return a skypos determined by rotating self about the X-axis by
        angle a."""
        x, y, z = _rotatev_y(self._vec, a)
        b2 = math.asin(z)
        b1 = (2 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    def rotate_z(self, a):
        """return a skypos determined by rotating self about the X-axis by
        angle a."""
        x, y, z = _rotate_v_z(self._vec, a)
        b2 = math.asin(z)
        b1 = (2 * math.pi + math.atan2(y, x)) % (2.0 * math.pi)
        return Skypos(b1, b2)

    def shift(self, delta_lon, delta_lat):
        """
        Shift this direction (Skypos) in longitude and latitude.
        The longitude shift will be in radian units perpendicular to the direction to pole, along a great circle.

        :param float delta_lon: longitude (RA) offset in radians
        :param float delta_lat: latitude (DEC) offset in radians
        """
        lat = self.dec
        lon = self.ra
        # vector along X axis (first point of Aries)
        x0 = Skypos("0h0m0s", "0:0:0", 3, 3)
        shifted_direction = (
            x0.rotate_z(delta_lon).rotate_y(lat + delta_lat).rotate_z(lon)
        )
        return shifted_direction

    def get_ras(self):
        if self.ras is None:
            self.ras = ras(self.ra)
            self.decs = decs(self.dec)
        return self.ras[: self.rn]

    def get_decs(self):
        if self.ras is None:
            self.ras = ras(self.ra)
            self.decs = decs(self.dec)
        return self.decs[: self.dn]

    def __str__(self):
        return "{} {}".format(self.get_ras(), self.get_decs())


def ras(ra):
    s = ra * (4.0 * 60.0 * RAD2DEG)
    hh = int(s / 3600.0)
    mm = int(s / 60.0) - hh * 60
    ss = s - 60 * (mm + 60 * hh)
    if "{:9.6f}".format(ss) == "60.000000":
        ss = 0.0
        mm += 1
        if mm == 60:
            mm = 0
            hh += 1
            if hh == 24:
                hh = 0
    return "%02d:%02d:%09.6f" % (hh, mm, ss)


def decs(dec):
    s = abs(dec) * (60.0 * 60.0 * RAD2DEG)
    dd = int(s / 3600.0)
    mm = int(s / 60.0) - dd * 60
    ss = s - 60 * (mm + 60 * dd)
    if "%8.5f" % ss == "60.00000":
        ss = 0.0
        mm += 1
        if mm == 60:
            mm = 0
            dd += 1
    sign = " "
    if dec < 0.0:
        sign = "-"
    return "%s%02d:%02d:%08.6f" % (sign, dd, mm, ss)


def _rotate_v_x(vec, a):
    """Return a skypos determined by rotating vec about the X-axis by
    angle a."""
    ca, sa = math.cos(a), math.sin(a)
    x = vec[0]
    y = vec[1] * ca - vec[2] * sa
    z = vec[1] * sa + vec[2] * ca
    return [x, y, z]


def _rotatev_y(vec, a):
    """Return a skypos determined by rotating vec about the Y-axis by
    angle a."""
    ca, sa = math.cos(a), math.sin(a)
    x = vec[0] * ca - vec[2] * sa
    y = vec[1]
    z = vec[0] * sa + vec[2] * ca
    return [x, y, z]


def _rotate_v_z(vec, a):
    """Return a skypos determined by rotating vec about the Z-axis by
    angle a."""
    ca, sa = math.cos(a), math.sin(a)
    x = vec[0] * ca - vec[1] * sa
    y = vec[0] * sa + vec[1] * ca
    z = vec[2]
    return [x, y, z]


def ras_rad(ra_string):
    """
    Convert right ascension string to radians
    :param ra_string: right ascension string (hh:mm:ss.ss)
    :type ra_string: str
    :return: right ascension in radians
    :rtype: float
    """
    if ra_string[0] == "-":
        raise (ValueError, "Right ascension may not be negative: {}".format(ra_string))
    (a, b, c) = re.findall("[0-9.]+", ra_string)
    hh, mm = map(int, [a, b])
    ss = float(c)
    return (ss + 60.0 * (mm + 60.0 * hh)) * 2.0 * math.pi / 86400.0


def decs_rad(dec_string):
    """
    Convert declination string to radians
    :param dec_string: declination string (dd:mm:ss.ss)
    :type dec_string: str
    :return: declination in radians
    :rtype: float
    """
    a, b, c = re.findall("[0-9.]+", dec_string)
    dd, mm = map(int, [a, b])
    ss = float(c)
    r = (ss + 60.0 * (mm + 60.0 * dd)) * 2.0 * math.pi / 1296000.0
    if dec_string[0] == "-":
        r = -r
    return r


def restore_ms_dir(ms):
    """Restore the direction to the ASKAPsoft standard."""

    if tableexists("%s/FIELD_OLD" % (ms)):
        logger.info("Restoring FIELD directions in %s" % (ms), ms=ms)
        with table("%s/FIELD" % (ms), readonly=False, ack=False) as tp, table(
            "%s/FIELD_OLD" % (ms), readonly=True, ack=False
        ) as fp:
            field_dir = fp.getcol("PHASE_DIR")
            tp.putcol("PHASE_DIR", field_dir)
            tp.putcol("DELAY_DIR", field_dir)
            tp.putcol("REFERENCE_DIR", field_dir)

    else:
        logger.warning(
            "No `FIELD_OLD` table in %s - cannot restore directions if direction has not changed."
            % (ms),
            ms=ms,
        )

    if tableexists("%s/FEED_OLD" % (ms)):
        logger.info("Restoring BEAM_OFFSET in %s" % (ms), ms=ms)
        with table("%s/FEED" % (ms), readonly=False, ack=False) as tp, table(
            "%s/FEED_OLD" % (ms), readonly=True, ack=False
        ) as fp:
            offset = fp.getcol("BEAM_OFFSET")
            tp.putcol("BEAM_OFFSET", offset)

    else:
        logger.warning(
            "No `FEED_OLD` table in %s - cannot restore beam offsets if they have not been changed."
            % (ms),
            ms=ms,
        )


def fix_ms_dir(ms):
    logger.info("Fixing FEED directions in %s" % (ms), ms=ms)
    # Check that the observation wasn't in pol_fixed mode
    with table("%s/ANTENNA" % (ms), readonly=True, ack=False) as ta:
        ant_mount = ta.getcol("MOUNT", 0, 1)
        if ant_mount[0] != "equatorial":
            sys.exit(f"{ms} doesn't support pol_fixed mode")

    # Work out which beam is in this MS
    beam = beam_from_ms(ms)

    if not tableexists("%s/FIELD_OLD" % (ms)):
        logger.info("Making copy of original FIELD table", ms=ms)
        tablecopy(tablename="%s/FIELD" % (ms), newtablename="%s/FIELD_OLD" % (ms))
    else:
        logger.info("Original copy of FIELD table is being used", ms=ms)

    if not tableexists("%s/FEED_OLD" % (ms)):
        logger.info("Making copy of original FEED table", ms=ms)
        tablecopy(tablename="%s/FEED" % (ms), newtablename="%s/FEED_OLD" % (ms))
    else:
        logger.info("Original copy of FEED table is being used", ms=ms)

    logger.info("Reading phase directions", ms=ms)
    with table("%s/FIELD_OLD" % (ms), readonly=True, ack=False) as tp:
        ms_phase = tp.getcol("PHASE_DIR")

    # Work out how many fields are in the MS.
    n_fields = ms_phase.shape[0]
    logger.info("Found %d fields in FIELD table" % (n_fields), ms=ms)

    # Open up the MS FEED table so we can work out what the offset is for the beam.
    with table("%s/FEED" % (ms), readonly=False, ack=False) as tf:
        offset = tf.getcol("BEAM_OFFSET")
        offset = offset - offset
        offset = tf.putcol("BEAM_OFFSET", offset)

    # Open up the MS FIELD table so it can be updated.
    # Open up the MS FEED table so we can work out what the offset is for the beam.
    with table("%s/FIELD" % (ms), readonly=False, ack=False) as tp, table(
        "%s/FEED_OLD" % (ms), readonly=True, ack=False
    ) as tf:
        # The offsets are assumed to be the same for all antennas so get a list of all
        # the offsets for one antenna and for the current beam. This should return offsets
        # required for each field.
        t1 = taql("select from $tf where ANTENNA_ID==0 and FEED_ID==$beam")
        n_offsets = t1.getcol("BEAM_OFFSET").shape[0]
        offset_times = t1.getcol("TIME")
        offset_intervals = t1.getcol("INTERVAL")
        logger.info(
            "Found %d offsets in FEED table for beam %d" % (n_offsets, beam), ms=ms
        )
        for offset_index in trange(n_offsets, desc="Fixing offsets", file=TQDM_OUT):
            offset = t1.getcol("BEAM_OFFSET")[offset_index]
            logger.info(
                "Offset %d : t=%f-%f : (%fd,%fd)"
                % (
                    offset_index,
                    offset_times[offset_index] - offset_intervals[offset_index] / 2.0,
                    offset_times[offset_index] + offset_intervals[offset_index] / 2.0,
                    -offset[0][0] * 180.0 / np.pi,
                    offset[0][1] * 180.0 / np.pi,
                ),
                ms=ms,
            )

        # Update the beam position for each field
        for field in trange(n_fields, desc="Fixing fields", file=TQDM_OUT):
            with table(ms, readonly=True, ack=False) as t:
                # Get times for the specified field
                tfdata = taql(
                    "select from $t where FIELD_ID==$field and FEED1==$beam and ANTENNA1==0 and ANTENNA2==0"
                )
                time_data = tfdata.getcol("TIME")
                if len(time_data) == 0:
                    #        logger.info("Warning: Couldn't find valid data for field %d" %(field), ms=ms)
                    continue

                offset_index = -1
                for offset in range(n_offsets):
                    if (
                        time_data[0]
                        > offset_times[offset] - offset_intervals[offset] / 2.0
                    ) and (
                        time_data[0]
                        < offset_times[offset] + offset_intervals[offset] / 2.0
                    ):
                        offset_index = offset
                        break

                #    logger.info("Field %d : t=%f : offset=%d" %(field, time_data[0], offset_index), ms=ms)
                # Obtain the offset for the current field.
                offset = t1.getcol("BEAM_OFFSET")[offset_index]

                # Get the pointing direction for the field
                p_phase = ms_phase[field]

                # Shift the pointing centre by the beam offset
                phase = Skypos(p_phase[0][0], p_phase[0][1], 9, 9)
                new_pos = phase.shift(-offset[0][0], offset[0][1])
                new_pos.rn = 15
                new_pos.dn = 15
                new_pos_str = "%s" % (new_pos)
                logger.info(
                    "Setting position of beam %d, field %d to %s (t=%f-%f, offset=%d)"
                    % (
                        beam,
                        field,
                        new_pos_str,
                        time_data[0],
                        time_data[-1],
                        offset_index,
                    ),
                    ms=ms,
                )
                # Update the FIELD table with the beam position
                new_ra = new_pos.ra
                if new_ra > np.pi:
                    new_ra -= 2.0 * np.pi
                ms_phase[field][0][0] = new_ra
                ms_phase[field][0][1] = new_pos.dec

            # Write the updated beam positions in to the MS.
            tp.putcol("DELAY_DIR", ms_phase)
            tp.putcol("PHASE_DIR", ms_phase)
            tp.putcol("REFERENCE_DIR", ms_phase)

    logger.info("Finished fixed FEED directions", ms=ms)


def cli():
    import argparse

    """Command-line interface"""

    # Create a new ArgumentParser object
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Add the options
    parser.add_argument(
        "ms", help="Measurement set to update", type=str, default=None, nargs="?"
    )
    parser.add_argument(
        "-r",
        "--restore",
        action="store_true",
        help="Switch to restore direction to the original ASKAPsoft pipeline direction",
    )
    # Parse the command line
    args = parser.parse_args()

    if args.restore:
        restore_ms_dir(args.ms)
    else:
        fix_ms_dir(args.ms)


if __name__ == "__main__":
    cli()
