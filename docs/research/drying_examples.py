"""Worked examples for the dust dry-ground clock (docs/research/ALERT_THRESHOLDS.md §2.3).

How long does a wet surface take to dry? This script estimates it for a few
typical weather patterns.

Method
------
Hourly drying is estimated with the ASCE standardized reference ET equation,
which is the same Penman-Monteith form the NWS uses for its FRET forecasts.

- Solar radiation is estimated from sky cover with Kasten & Czeplak (1980):
  Rs = Rso * (1 - 0.75 * c**3.4).
- Wind is taken as measured at 10 m, which is how the NWS forecasts it.

Surface moisture is tracked as a small "bucket":

- Rain is added to the bucket, which is capped at CAP_MM.
- Each hour, K_DRY * ET0 is subtracted from the bucket.
- No drying is counted while the air temperature is at or below 0 °C (frozen ground).
- Dust alerts are allowed again once the bucket is empty, but never sooner than
  FLOOR_H after FLOOR_MIN_IN or more of rain in any 24 h, or MIN_HOLD_H after
  any lighter measurable rain. The holds count from the last hour of rain.

These are illustrative profiles, not observations. Requires: pip install refet numpy
"""
import math

import numpy as np
import refet
from refet import calcs

CAP_MM = 6.35   # 0.25 in: deeper wetting doesn't keep the surface damp any longer (judgment)
K_DRY = 1.0     # bare, trafficked surface vs. the grass reference (judgment; calibrate)
FLOOR_H = 24          # hold after >= FLOOR_MIN_IN of rain in any 24 h, whatever the clock says (product rule)
FLOOR_MIN_IN = 0.10   # in any 24 h; lighter rain gets the shorter MIN_HOLD_H (decided Nov 20)
MIN_HOLD_H = 6        # hold after any measurable rain (>= 0.01 in), whatever the clock says (decided Nov 20)


def et0_hour(t_c, tdew_c, wind_ms, sky, lat, lon, elev, doy, utc_hour):
    """Reference ET for one hour, in mm."""
    ra = calcs.ra_hourly(np.array([math.radians(lat)]), np.array([math.radians(lon)]),
                         doy, np.array([utc_hour + 0.5]), "asce")
    rso = calcs.rso_simple(ra, np.array([elev]))
    rs = rso * (1 - 0.75 * sky ** 3.4)
    et = refet.Hourly(tmean=t_c, tdew=tdew_c, rs=rs, uz=wind_ms, zw=10, elev=elev,
                      lat=lat, lon=lon, doy=doy, time=utc_hour).eto()
    return max(float(et[0]), 0.0)


def f2c(f):
    return (f - 32) * 5 / 9


def hours_to_dry(sc, rain_in, start_local=6, max_hours=240):
    """Hours from the end of the rain until the bucket is empty."""
    bucket = min(rain_in * 25.4, CAP_MM)
    tmin, tmax = f2c(sc["tmin_f"]), f2c(sc["tmax_f"])
    mean, amp = (tmax + tmin) / 2, (tmax - tmin) / 2
    for h in range(max_hours):
        local = (start_local + h) % 24
        t = mean + amp * math.cos(2 * math.pi * (local - 15) / 24)   # min ~03:00, max 15:00
        if t <= 0:
            continue                                                   # frozen: no drying
        utc = (local + sc["utc_offset"]) % 24
        doy = sc["doy"] + (start_local + h + sc["utc_offset"]) // 24
        bucket -= K_DRY * et0_hour(t, min(f2c(sc["tdew_f"]), t), sc["wind_mph"] * 0.44704,
                                   sc["sky"], sc["lat"], sc["lon"], sc["elev"], doy, utc)
        if bucket <= 0:
            return h + 1
    return None


SCENARIOS = [
    dict(name="Desert summer, clear (Las Vegas, Jul)", lat=36.08, lon=-115.15, elev=660, doy=196,
         utc_offset=7, tmax_f=105, tmin_f=82, tdew_f=35, wind_mph=10, sky=0.1),
    dict(name="Santa Maria fall, dry offshore wind (Nov)", lat=34.95, lon=-120.43, elev=73, doy=320,
         utc_offset=8, tmax_f=80, tmin_f=50, tdew_f=20, wind_mph=15, sky=0.0),
    dict(name="Santa Maria spring, windy, clear (Apr)", lat=34.95, lon=-120.43, elev=73, doy=105,
         utc_offset=7, tmax_f=68, tmin_f=45, tdew_f=40, wind_mph=15, sky=0.2),
    dict(name="Santa Maria winter, cloudy after storm (Jan)", lat=34.95, lon=-120.43, elev=73, doy=15,
         utc_offset=8, tmax_f=58, tmin_f=46, tdew_f=47, wind_mph=6, sky=0.8),
    dict(name="High plains winter, cold, dry, clear (Denver, Jan)", lat=39.75, lon=-104.99, elev=1610,
         doy=15, utc_offset=7, tmax_f=38, tmin_f=20, tdew_f=12, wind_mph=10, sky=0.1),
    dict(name="High plains winter, below freezing all day (Jan)", lat=39.75, lon=-104.99, elev=1610,
         doy=15, utc_offset=7, tmax_f=28, tmin_f=12, tdew_f=8, wind_mph=10, sky=0.1),
]

def hours_until_alerts_allowed(sc, rain_in):
    """The later of the drying clock and the hold (24 h for >= 0.10 in, 6 h for lighter rain)."""
    clock = hours_to_dry(sc, rain_in)
    if clock is None:
        return None
    return max(clock, FLOOR_H if rain_in >= FLOOR_MIN_IN else MIN_HOLD_H)


if __name__ == "__main__":
    print(f"Rain ends 06:00 local. Cap {CAP_MM} mm, K {K_DRY}. Holds: {FLOOR_H} h after >= {FLOOR_MIN_IN} in, "
          f"{MIN_HOLD_H} h after lighter rain.")
    print("Hours until dust alerts are allowed again; the drying clock alone is in brackets.\n")
    fmt = lambda x: f"{x} h" if x is not None else "frozen"
    print(f"{'Scenario':52} {'0.01 in':>8} {'0.10 in':>14} {'0.25 in+':>14}")
    for sc in SCENARIOS:
        cells = [fmt(hours_until_alerts_allowed(sc, 0.01))]
        for r in (0.10, 0.25):
            cells.append(f"{fmt(hours_until_alerts_allowed(sc, r))} ({fmt(hours_to_dry(sc, r))})")
        print(f"{sc['name']:52} {cells[0]:>8} {cells[1]:>14} {cells[2]:>14}")
