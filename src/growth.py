"""Yearly CO2 absorption = change in CO2 stock over one year of growth.

    absorbed this year = stock(now)        - stock(one year ago)
    absorbed next year = stock(next year)  - stock(now)

Height is re-estimated from the new DBH every time, so both grow together.
"""
from . import allometry as al
from . import config as cfg


def absorption_this_year_kg(dbh_cm, growth_cm=None):
    """CO2 gained over the PAST year (stock now minus stock one year ago)."""
    g = cfg.DBH_GROWTH_CM_PER_YEAR if growth_cm is None else growth_cm
    return al.co2_stock_kg(dbh_cm) - al.co2_stock_kg(dbh_cm - g)


def absorption_next_year_kg(dbh_cm, growth_cm=None):
    """CO2 gained over the NEXT year (stock next year minus stock now)."""
    g = cfg.DBH_GROWTH_CM_PER_YEAR if growth_cm is None else growth_cm
    return al.co2_stock_kg(dbh_cm + g) - al.co2_stock_kg(dbh_cm)
