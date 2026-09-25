# International Ground Data Repository (IGDR)

**Maintained by [Midwest Stratospheric Data Systems](https://www.midwestsds.com)**  
GitHub: [Midwest-Stratospheric](https://github.com/Midwest-Stratospheric)

## Purpose

The International Ground Data Repository (IGDR) is a living, open archive that aggregates and organizes publicly available stratospheric, upper-air, and ground-based atmospheric weather data from sources around the world — plus first-party **Casey, Illinois surface radiation** from the Aerostratospheric GMC-800.

Over time, this repository will grow into a comprehensive, versioned collection of public datasets to support research, education, citizen science, and open atmospheric monitoring. It complements the flight data released by Midwest Stratospheric Data Systems (MSDS) in the [msds-data](https://github.com/Midwest-Stratospheric/msds-data) repository and the UOGW ground layer.

All third-party data here is sourced from public domain or openly licensed government and research archives. We do not claim ownership of the original observations — we curate, index, snapshot, and make them more discoverable and persistent. First-party GMC-800 files are MSDS/Aerostratospheric observations of ionizing radiation at a fixed station.

## Radiation data (first-party)

Casey, Illinois hosts a **fixed GQ GMC-800** Geiger–Müller counter used as a surface radiation / weather station.

| Field | Value |
|-------|-------|
| Station id | `MSDS-GMC800-CASEY` |
| Latitude | 39.2974 N |
| Longitude | 87.9818 W (−87.9818) |
| Variables | CPM, µSv/h |
| Station file | [`stations/msds-gmc800-casey.json`](./stations/msds-gmc800-casey.json) |
| Latest snapshot | [`snapshots/2026-09-16/gmc-800-casey.json`](./snapshots/2026-09-16/gmc-800-casey.json) |
| Canonical hourly package | [UOGW `layers/ground/casey/gmc-800/latest.json`](https://github.com/Midwest-Stratospheric/Unified-Open-Global-Weather/blob/main/layers/ground/casey/gmc-800/latest.json) |

This is **background ionizing radiation** (beta / gamma / X-ray indication from the GMC-800), time-stamped and locked to the coordinates above. It is a research series, not a regulatory or emergency-alert product.

## Core Data Sources

- **NOAA Integrated Global Radiosonde Archive (IGRA)**  
  The largest publicly available collection of quality-controlled, globally-distributed historical and near-real-time radiosonde and pilot balloon observations.  
  → [NCEI IGRA](https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive)  
  Updated daily for ~800–900 stations worldwide.

- **NOAA / NCEI Upper-Air BUFR and related streams**  
  Global upper-air reports from the National Weather Service Telecommunications Gateway.

- **Copernicus / ECMWF Comprehensive Upper-air Observation Network (CUON)**  
  Merged historical balloon observations.

- **Aerostratospheric / MSDS Casey GMC-800**  
  First-party fixed-site surface radiation (CPM, µSv/h) at 39.2974 N, −87.9818 W.

- **Other open sources**  
  QBO tropical stratospheric winds, ozone sonde networks, satellite-derived stratospheric products (SWOOSH, etc.), and regional meteorological agency open data where available.

## Repository Structure (evolving)

```
/
├── README.md                 # This file
├── sources/                  # Documentation of data sources and access methods
├── snapshots/                # Daily or periodic curated snapshots / indexes
│   └── YYYY-MM-DD/
├── stations/                 # Station metadata (includes msds-gmc800-casey.json)
├── indexes/                  # Machine-readable catalogs of available data
└── docs/                     # Guides, citation information, methodology
```

## Daily Updates

This repository is designed to receive automated daily contributions that:
- Capture recent public radiosonde / upper-air updates
- Maintain indexes of available global stations and latest observations
- Preserve historical snapshots for long-term accessibility
- Link back to authoritative sources for full bulk downloads
- Ingest first-party Casey GMC-800 radiation history when a new Data Viewer export is curated

## Citation & License

When using data from this repository, always cite the original data providers (primarily NOAA NCEI IGRA and related programs) in addition to acknowledging Midwest Stratospheric Data Systems as the curator of this open archive. For GMC-800 files, cite Aerostratospheric / MSDS and GQ Electronics as the instrument maker.

IGRA citation example:  
Durre, Imke; Yin, Xungang; Vose, Russell S.; Applequist, Scott; Arnfield, Jeff; Korzeniewski, Bryant; Hundermark, Bruce. (2016) Integrated Global Radiosonde Archive (IGRA), Version 2. NOAA National Centers for Environmental Information. DOI:10.7289/V5X63K0Q.

Repository content (indexes, documentation, curated snapshots) is released under Creative Commons Attribution 4.0 International (CC BY 4.0) unless otherwise noted.

## Collaboration

IGDR feeds the ground layer of UOGW and the radiation panel on xDataHub, our public open atmospheric data dashboard: https://www.midwestsds.com/msds-data-hub.html. Station operators and researchers who want to pair their own ground or radiation series with ours, or help check these snapshots, are welcome to reach out about data collaboration: email space@aerostratospheric.com or book a 15 minute intro at https://calendly.com/aerostratospheric/15min

## Contact

Midwest Stratospheric Data Systems  
Casey, Illinois, USA  
launchcontrol@midwestsds.com  
https://www.midwestsds.com

---
*Building an open stratospheric data commons, one day at a time.*
