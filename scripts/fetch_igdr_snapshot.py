#!/usr/bin/env python3
"""
Build a daily lightweight IGDR snapshot index for International-Ground-Data-Repository.

Pulls live public metadata from NOAA NCEI IGRA (status, station list, directory listings)
and writes snapshots/YYYY-MM-DD/index.json. Designed for GitHub Actions.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

UA = {"User-Agent": "Midwest-Stratospheric/IGDR-daily-snapshot/1.0"}


def fetch_text(url: str, timeout: int = 90) -> str | None:
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"WARN fetch failed {url}: {e}", file=sys.stderr)
        return None


def parse_station_count(text: str | None) -> int:
    if not text:
        return 0
    count = 0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 3:
            try:
                float(parts[1])
                float(parts[2])
                count += 1
            except ValueError:
                continue
    return count


def list_tarballs(html: str | None, pattern: str) -> list[str]:
    if not html:
        return []
    found = sorted(set(re.findall(pattern, html, flags=re.I)))
    return found


def main() -> int:
    now = datetime.now(timezone.utc)
    date = now.strftime("%Y-%m-%d")
    # Prefer previous calendar day for "daily archive" semantics if early UTC morning
    if now.hour < 6:
        archive_date = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        archive_date = date

    print(f"Building IGDR snapshot for {archive_date} (UTC now {now.isoformat()})")

    status_txt = fetch_text("https://www.ncei.noaa.gov/pub/data/igra/status.txt") or \
                 fetch_text("https://www1.ncdc.noaa.gov/pub/data/igra/status.txt")

    station_list = fetch_text("https://www.ncei.noaa.gov/pub/data/igra/igra2-station-list.txt") or \
                   fetch_text("https://www1.ncdc.noaa.gov/pub/data/igra/igra2-station-list.txt")
    station_count = parse_station_count(station_list)

    y2d_html = fetch_text("https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-y2d/")
    por_html = fetch_text("https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/archive/")

    y2d_tars = list_tarballs(y2d_html, r'href="(IGRA[^"\']+\.tar)"')
    if not y2d_tars:
        y2d_tars = list_tarballs(y2d_html, r'href="([A-Za-z0-9_\-\.]+\.tar)"')

    por_tars = list_tarballs(por_html, r'href="(IGRA_v2\.2_data-por[^"\']+\.tar)"')
    derived_tars = list_tarballs(por_html, r'href="(IGRA_v2\.2_derived-por[^"\']+\.tar)"')

    # Infer latest end date from filenames when possible (e_YYYYMMDD)
    latest_end = None
    for name in y2d_tars + por_tars:
        m = re.search(r"_e(\d{8})_", name)
        if m:
            try:
                d = datetime.strptime(m.group(1), "%Y%m%d").date()
                if latest_end is None or d > latest_end:
                    latest_end = d
            except ValueError:
                pass

    latest_por_str = latest_end.isoformat() if latest_end else "unknown (see NCEI)"

    network_notes = [
        "IGRA v2.2 continues daily updates incorporating TAC + BUFR sources for ~800–900 active stations.",
        f"Station list parse counted {station_count} entries from the public igra2-station-list.txt.",
        "Full bulk multi-GB tarballs remain at NCEI; this index is a lightweight daily reference only.",
        "No bulk archives are downloaded into this repository.",
    ]
    if status_txt:
        # Keep a short excerpt of status for transparency
        excerpt = " ".join(status_txt.strip().split())[:400]
        if excerpt:
            network_notes.append(f"NCEI status excerpt: {excerpt}")

    record = {
        "date": archive_date,
        "repository": "International-Ground-Data-Repository",
        "curator": "Midwest Stratospheric Data Systems",
        "description": "Daily snapshot index of publicly available global upper-air / stratospheric radiosonde data sources",
        "primary_source": {
            "name": "NOAA Integrated Global Radiosonde Archive (IGRA) v2.2",
            "provider": "NOAA NCEI",
            "stations_historical": ">2800",
            "stations_listed": station_count,
            "stations_updating": "~800-900",
            "update_frequency": "Daily for recent soundings; bulk POR and Y2D tarballs typically refreshed daily",
            "latest_bulk_period_of_record_end": latest_por_str,
            "latest_year_to_date_files": y2d_tars[:8],
            "latest_por_files": por_tars[:8],
            "latest_derived_por_files": derived_tars[:8],
            "access": {
                "landing_page": "https://www.ncei.noaa.gov/products/weather-balloon/integrated-global-radiosonde-archive",
                "recent_soundings_https": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-y2d/",
                "period_of_record_https": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/data-por/",
                "derived_parameters_https": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/derived-por/",
                "monthly_means_https": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/access/monthly-por/",
                "archive_tarballs": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/archive/",
                "station_list": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/doc/igra2-station-list.txt",
                "readme": "https://www.ncei.noaa.gov/data/integrated-global-radiosonde-archive/doc/igra2-readme.txt",
                "status": "https://www.ncei.noaa.gov/pub/data/igra/status.txt",
            },
        },
        "related_sources": [
            {"name": "NWSTG Global Upper Air BUFR", "update": "Daily", "access": "https://www.ncei.noaa.gov/data/nws-global-upper-air-bufr/"},
            {"name": "ECMWF Global Upper Air BUFR", "update": "Monthly", "access": "https://www.ncei.noaa.gov/data/ecmwf-global-upper-air-bufr/"},
            {"name": "NWS-Managed Upper Air Observations in BUFR (US/Caribbean/Pacific)", "access": "https://www.ncei.noaa.gov/data/us-radiosonde-bufr/"},
            {"name": "Copernicus CUON", "access": "https://cds.climate.copernicus.eu/datasets/insitu-comprehensive-upper-air-observation-network"},
            {"name": "RATPAC (Radiosonde Atmospheric Temperature Products for Assessing Climate)", "access": "https://www.ncei.noaa.gov/products/weather-balloon/radiosonde-atmospheric-temperature-products"},
        ],
        "network_notes": network_notes,
        "notes": "Full bulk multi-GB tarballs remain at NCEI; this index is a lightweight daily reference for availability, periods of record, and access links only. Do not download the large archives into this repository.",
        "generated_by": "Midwest Stratospheric Data Systems automated curation",
        "timestamp_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ok": station_count > 0 or bool(y2d_tars) or bool(status_txt),
    }

    out_dir = Path(f"snapshots/{archive_date}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Lightweight status for health monitor
    Path("status").mkdir(exist_ok=True)
    with open("status/last_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "date": archive_date,
                "ok": record["ok"],
                "station_count": station_count,
                "y2d_file_count": len(y2d_tars),
                "generated_at_utc": record["timestamp_utc"],
                "path": str(out_path),
            },
            f,
            indent=2,
        )
        f.write("\n")

    print(f"Wrote {out_path}")
    print(f"  stations listed: {station_count}")
    print(f"  y2d tarballs found: {len(y2d_tars)}")
    print(f"  ok: {record['ok']}")
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
