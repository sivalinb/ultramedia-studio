import argparse
import csv
from pathlib import Path

from sqlalchemy import select

from .config import get_settings
from .database import Database, Race, TimingEvent

REQUIRED_TIMING_COLUMNS = {
    "athlete_bib",
    "athlete_name",
    "checkpoint",
    "mile",
    "elapsed_seconds",
    "position_overall",
}


def ingest_timing_csv(database: Database, race_id: str, csv_path: Path) -> int:
    """Ingest a rights-cleared timing export; network scraping is intentionally out of scope."""
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_TIMING_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Timing CSV missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)
    with database.session() as db:
        if db.scalar(select(Race.id).where(Race.id == race_id)) is None:
            raise ValueError(f"Unknown race: {race_id}")
        for row in rows:
            db.add(
                TimingEvent(
                    race_id=race_id,
                    athlete_bib=row["athlete_bib"],
                    athlete_name=row["athlete_name"],
                    checkpoint=row["checkpoint"],
                    mile=float(row["mile"]),
                    elapsed_seconds=int(row["elapsed_seconds"]),
                    position_overall=int(row["position_overall"]),
                )
            )
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a governed race timing CSV")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--race-id", default="wser-demo")
    args = parser.parse_args()
    database = Database(get_settings().database_url)
    database.create_all()
    count = ingest_timing_csv(database, args.race_id, args.csv_path)
    print(f"Ingested {count} timing events for {args.race_id}")


if __name__ == "__main__":
    main()
