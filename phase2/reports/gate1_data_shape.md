# Gate 1 data-shape report

Table: `data/wdc_lspc2017_offers.csv.gz`  
Provenance: `data/MANIFEST.json`

Shape is reported under the as-distributed triple: `key` = WDC cluster id
(product identity), `label` = WDC category, `surface_string` = offer title.
Gate 2 re-derives Framing A and Framing B keys from this same table.

## Totals

- Total rows (distinct offers): 15,179
- Distinct keys (clusters): 2,485
- Distinct surface strings: 14,033
- Label cardinality (categories): 15

## Key recurrence

| occurrences | keys | share |
| --- | --- | --- |
| 1 | 50 | 2.0% |
| 2 | 232 | 9.3% |
| 3+ | 2,203 | 88.7% |

## Distinct surface forms per key

- min 1, median 5, max 140
- keys with more than one surface form: 93.6%

## Labels

- `Computers_and_Accessories`: 4,518
- `Jewelry`: 3,936
- `Camera_and_Photo`: 3,394
- `Shoes`: 2,760
- `Other_Electronics`: 177
- `Office_Products`: 152
- `not found`: 53
- `Sports_and_Outdoors`: 46
- `Cellphones_and_Accessories`: 41
- `Video_Games`: 36
- `Luggage_and_Travel_Gear`: 26
- `Automotive`: 14
- `Musical_Instruments`: 12
- `Tools_and_Home_Improvement`: 10
- `Toys_and_Games`: 4

## Example rows

| key | forms in key | surface_string | label |
| --- | --- | --- | --- |
| 517 | 7 |  "Sandisk 32GB Extreme Plus SDSDQXN-032G microSDHC Card r60MB/s w40MB/s Limited Stock" | Camera_and_Photo |
| 517 | 7 |  "Sandisk SDSDQXP-032G CVL 32GB 8p MSDHC Class 10 r95mb/S 633x U3 Micro Secure Digital Hig | Camera_and_Photo |
| 1201 | 8 |  "672631-B21 HP 16GB (1x16GB) SDRAM DIMM" "Null" | Computers_and_Accessories |
| 1201 | 8 |  "HP 16GB DDR3 SDRAM Memory Module - 16 GB (1 x GB) 1600 MHz DDR3-1600 PC3-12800 Registere | Computers_and_Accessories |
| 2328 | 3 |  "ALPHA 6000 + 16-50 55-210 NOIR" | Camera_and_Photo |
| 2328 | 3 |  "Sony A6000 + 16-50mm f/3.5-5.6 55-210mm f/4.5-6.3 Zwart - Prijzen "@NL Tweakers"@NL | Camera_and_Photo |
| 3020 | 9 |  "Kingston HyperX Predator SSD M.2 480GB - Specificaties "@NL Tweakers"@NL | Computers_and_Accessories |
| 3020 | 9 |  "SSD Kingston M.2 PCIe 480Go" | Computers_and_Accessories |
| 3036 | 10 |  " DVC Premium Tape 80min "@en, "DVC 80min"@en Prices - CNET"@en | Camera_and_Photo |
| 3036 | 10 |  "Sony Mini DV Cassette Without Chip" " Sony Chip - DVM80PRL Audio/Video Media CDW.com | Camera_and_Photo |
| 34181 | 1 |  "DKNY NY2287 Stanhope watch" | Jewelry |
| 146308 | 1 |  " Nike WMNS Air Footscape Woven | Shoes |
| 146308 | 1 |  " Nike WMNS Air Footscape Woven | Shoes |
| 172933 | 1 |  "Canon Lens Hood EW-75 II for 20mm"@en 20mm - Accessories Lenses"@en | Camera_and_Photo |
| 300416 | 1 |  " Casio Ladies' Junior Collection Watch"@en "Ladies' Watch (LQ-139LB-2B2ER) - WATCH SHOP. | Jewelry |
| 318478 | 1 |  "Nikon EN-EL4A Rechargeable Battery"@en " Nikon Battery \| Digital SLR Camera Aden "@en C | Camera_and_Photo |
