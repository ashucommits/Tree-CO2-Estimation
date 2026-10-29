"""Step 1 of the project: CO2 estimate from the 31 MANUALLY measured trees.

Run from the repo root:
    python -m src.run_manual
"""
import pandas as pd

from . import allometry as al
from . import config as cfg
from . import growth as gr


def run(csv_path="data/manual_trees.csv", out_path="outputs/results_manual.csv"):
    trees = pd.read_csv(csv_path)
    trees["est_DBH_cm"] = al.dbh_from_crown(trees["crown_diameter_m"])
    trees["est_height_m"] = al.height_from_dbh(trees["est_DBH_cm"])
    trees["CO2_stock_kg"] = al.co2_stock_kg(trees["est_DBH_cm"], trees["est_height_m"])
    trees["CO2_absorbed_this_year_kg"] = gr.absorption_this_year_kg(trees["est_DBH_cm"])
    trees["CO2_absorbed_next_year_kg"] = gr.absorption_next_year_kg(trees["est_DBH_cm"])
    trees.round(2).to_csv(out_path, index=False)
    return trees


def sensitivity(trees):
    """How much does the answer change if our assumptions change?"""
    print("\nSensitivity of this-year absorption (tons CO2/year):")
    original = cfg.DBH_PER_CROWN
    for ratio in (3.5, 4.0, 4.5):
        cfg.DBH_PER_CROWN = ratio
        dbh = al.dbh_from_crown(trees["crown_diameter_m"])
        total = gr.absorption_this_year_kg(dbh).sum() / 1000
        print(f"  DBH = {ratio} x crown   -> {total:.2f}")
    cfg.DBH_PER_CROWN = original
    dbh = al.dbh_from_crown(trees["crown_diameter_m"])
    for g in (0.4, 0.6, 0.9):
        total = gr.absorption_this_year_kg(dbh, growth_cm=g).sum() / 1000
        print(f"  growth = {g} cm/year -> {total:.2f}")


if __name__ == "__main__":
    t = run()
    print(f"Trees: {len(t)}")
    print(f"Total CO2 stock:           {t.CO2_stock_kg.sum() / 1000:.1f} tons")
    print(f"Absorbed this year:        {t.CO2_absorbed_this_year_kg.sum() / 1000:.2f} tons")
    print(f"Projected absorption next: {t.CO2_absorbed_next_year_kg.sum() / 1000:.2f} tons")
    print(f"Average per tree:          {t.CO2_absorbed_this_year_kg.mean():.1f} kg/year")
    sensitivity(t)
    print("\nSaved: outputs/results_manual.csv")
