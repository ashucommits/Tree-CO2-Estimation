"""Tree size -> biomass -> carbon -> CO2.

Chain used:
    crown diameter -> DBH, height   (rules of thumb, see config.py)
    DBH, height    -> above-ground biomass (Chave et al. 2014)
    + roots        -> total biomass
    x 0.47         -> carbon
    x 3.67         -> CO2
"""
import numpy as np

from . import config as cfg


def dbh_from_crown(crown_m):
    """Estimate DBH (cm) from crown diameter (m)."""
    return cfg.DBH_PER_CROWN * np.asarray(crown_m, dtype=float)


def height_from_dbh(dbh_cm):
    """Estimate height (m) from DBH (cm).

    Same crown-based rule as in config.py, written in terms of DBH so it can be
    re-used when the tree grows: crown = DBH / DBH_PER_CROWN.
    """
    crown = np.asarray(dbh_cm, dtype=float) / cfg.DBH_PER_CROWN
    return cfg.HEIGHT_INTERCEPT + cfg.HEIGHT_PER_CROWN * crown


def above_ground_biomass_kg(dbh_cm, height_m, wood_density=None):
    """Chave et al. (2014): AGB = 0.0673 * (rho * D^2 * H) ^ 0.976  (kg)."""
    rho = cfg.WOOD_DENSITY if wood_density is None else wood_density
    d = np.asarray(dbh_cm, dtype=float)
    h = np.asarray(height_m, dtype=float)
    return 0.0673 * (rho * d ** 2 * h) ** 0.976


def co2_stock_kg(dbh_cm, height_m=None, wood_density=None):
    """Total CO2 stored in a tree (kg). If height is not given it is estimated."""
    if height_m is None:
        height_m = height_from_dbh(dbh_cm)
    agb = above_ground_biomass_kg(dbh_cm, height_m, wood_density)
    total_biomass = agb * (1 + cfg.BELOW_GROUND_FRACTION)
    carbon = total_biomass * cfg.CARBON_FRACTION
    return carbon * cfg.CO2_PER_CARBON
