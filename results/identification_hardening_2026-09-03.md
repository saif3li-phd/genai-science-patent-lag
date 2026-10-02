# Identification hardening, mature sample (filings through 2024-06-30)

Patents: 55,539. Script: `code/identification_hardening.py`.

## A. Narrow pre-periods

Pre-period shortened toward 2023; post period held at 2023 to 2024-06-30.

| Pre-period | Patents | Fresh-science share DiD (pp) | SE | p |
|---|---:|---:|---:|---:|
| 2018 to 2022 (paper) | 55,539 | -5.56 | 1.58 | 0.0004 |
| 2019 to 2022 | 49,455 | -5.88 | 1.76 | 0.0008 |
| 2020 to 2022 | 40,428 | -5.36 | 1.88 | 0.0043 |
| 2021 to 2022 | 29,107 | -6.46 | 2.23 | 0.0037 |

## B. Continuous citation-age outcomes, no threshold

| Outcome | Unit | DiD | SE | p |
|---|---|---:|---:|---:|
| fresh share | percentage points | -5.5599 | 1.5772 | 0.0004 |
| mean age | years | +0.1398 | 0.7831 | 0.8583 |
| median age | years | +0.3523 | 0.7574 | 0.6418 |
| citation-weighted age (pair level) | years | +0.3882 | 0.7421 | 0.6009 |

## C. Breakdown sensitivity to a differential pre-trend

Fitted treated-specific linear pre-trend on 2018 to 2022: **+0.077 points per year** (SE 0.617, p = 0.901). The sign is positive, so the treated classes were gaining fresh science before 2023, which works against the post-2023 decline rather than producing it.

Removing that fitted trend from the post period leaves **-5.81 pp** (SE 1.59, p = 0.0003) against -5.56 pp unadjusted.

Breakdown value: the mean post-period patent is filed 1.22 years after 2022, so a differential pre-trend of **-4.55 points per year** in the treated classes, sustained through the post period, would be needed to account for the entire estimate. The trend actually observed before 2023 is +0.077, of the opposite sign.

