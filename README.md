# Tree Inventory and CO2 Absorption Estimation

Estimate how many trees an area has, how much CO2 they absorb in a year, and how
much more they will absorb next year as they grow.

**Status: work in progress (proof-of-concept).** The pipeline is being developed and
tested on a 0.85 ha area of Pan Pacific Park (Los Angeles). The final target is the
UCP campus (Lahore).

## Pipeline

```
satellite image -> tree crowns -> crown diameter -> DBH, height
   -> biomass -> carbon -> CO2 stock -> yearly growth -> next-year projection
```

| Stage | Status |
|---|---|
| Manual tree marking + crown measurement (31 trees, Google Earth Pro) | Done |
| CO2 calculation and next-year projection (`src/`) | Done |
| Automatic tree detection (DeepForest) compared against manual marks | Next |
| Apply to UCP campus imagery | Planned |
| Map / dashboard, literature-based growth rates | Planned |

## How to run

```bash
pip install -r requirements.txt
python -m src.run_manual
```

This reads `data/manual_trees.csv` and writes `outputs/results_manual.csv`.

## Method

1. **Crown diameter** measured on the image with the Google Earth Pro ruler.
2. **DBH** (cm) = 4 x crown diameter (m). Rule of thumb, not calibrated.
3. **Height** (m) = 3 + 0.8 x crown diameter (m). Rough placeholder.
4. **Above-ground biomass** (Chave et al. 2014): `AGB = 0.0673 * (rho * D^2 * H)^0.976`, rho = 0.6.
5. **Roots** +26% (IPCC), **carbon** = 47% of biomass (IPCC), **CO2** = carbon x 3.67.
6. **Yearly absorption** = change in CO2 stock over one year of growth
   (assumed DBH growth: 0.6 cm/year; height is re-estimated from the new DBH).

All assumptions live in `src/config.py`.

## Prototype result (31 trees, 0.85 ha)

| | Value |
|---|---|
| Total CO2 stored | about 42.7 tons |
| Absorbed this year (modelled) | about 1.40 tons/year |
| Projected next year | about 1.44 tons/year (+2.5%) |
| Average per tree | about 45 kg CO2/year |

Sensitivity: DBH ratio 3.5 to 4.5 gives 1.23 to 1.57 tons/year; growth rate 0.4 to
0.9 cm/year gives 0.94 to 2.09 tons/year. Growth rate matters most.

## Limitations

- DBH, height and growth rate are assumptions, not calibrated with field data.
- Only 31 clearly separable trees were marked; overlapping canopies are not counted,
  so the real tree count is higher.
- Palms are not separated, and standard tree biomass equations do not apply to them directly.
- The Chave equation is pantropical; local or urban allometric equations would be better.
- "This year" absorption is modelled from the assumed growth rate, not measured.
- Test area is in Los Angeles (imagery date 6/9/2018), not in Pakistan.

## Repository layout

```
data/manual_trees.csv      31 trees: id, lat, lon, crown diameter, pixel position
data/images/               clean and annotated satellite image
src/config.py              all assumptions and constants
src/allometry.py           size -> biomass -> carbon -> CO2
src/growth.py              yearly absorption and next-year projection
src/run_manual.py          runs the manual-measurement pipeline
outputs/                   results
```
