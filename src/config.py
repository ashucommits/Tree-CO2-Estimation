"""Central place for all constants and assumptions.

Every number here is an ASSUMPTION or a literature default. If you change one,
the whole pipeline changes, so keep them all in this one file.
"""

# --- Image scale (derived by matching the 31 pin lat/lon to their pixel positions) ---
# One pixel in data/images/park_clean.jpg is about 6.7 cm on the ground.
METERS_PER_PIXEL = 0.067

# --- Allometry (crown -> size): ROUGH rules of thumb, not calibrated ---
DBH_PER_CROWN = 4.0        # DBH (cm) = 4 x crown diameter (m)
HEIGHT_INTERCEPT = 3.0     # height (m) = 3 + 0.8 x crown diameter (m)
HEIGHT_PER_CROWN = 0.8

# --- Biomass (Chave et al. 2014, pantropical equation) ---
WOOD_DENSITY = 0.6             # g/cm^3, generic value (not species specific)
BELOW_GROUND_FRACTION = 0.26   # roots = 26% of above-ground biomass (IPCC range 0.24-0.26)
CARBON_FRACTION = 0.47         # carbon = 47% of biomass (IPCC default)
CO2_PER_CARBON = 3.67          # molecular weight ratio CO2 : C (44/12, rounded)

# --- Growth ---
DBH_GROWTH_CM_PER_YEAR = 0.6   # assumed yearly DBH increase (to be replaced by literature values)
