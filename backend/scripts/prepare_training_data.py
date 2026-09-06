import argparse
import json
import random
import sqlite3
from pathlib import Path

SYSTEM_PROMPT = (
    "You are the UltraMedia race journalist. Write concise, factual endurance-sports stories. "
    "Use only supplied evidence, retain citation IDs, never infer medical condition or emotion, "
    "and always require editorial approval."
)


def build_examples(database_path: Path) -> list[dict]:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        "SELECT athlete_bib, signal_type, headline, body, social_caption, citations "
        "FROM story_drafts WHERE status = 'approved' ORDER BY created_at"
    ).fetchall()
    connection.close()
    examples = []
    for row in rows:
        citations = json.loads(row["citations"])
        user = json.dumps(
            {
                "athlete_bib": row["athlete_bib"],
                "signal_type": row["signal_type"],
                "evidence": citations,
            }
        )
        assistant = json.dumps(
            {
                "headline": row["headline"],
                "body": row["body"],
                "social_caption": row["social_caption"],
                "citation_ids": [item["id"] for item in citations],
            }
        )
        examples.append(
            {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": assistant},
                ]
            }
        )
    return examples


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build QLoRA train/validation data from approved stories")
    parser.add_argument("--database", type=Path, default=Path("ultramedia.db"))
    parser.add_argument("--output", type=Path, default=Path("training_data"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    examples = build_examples(args.database)
    if len(examples) < 20:
        raise SystemExit("At least 20 human-approved drafts are required before fine-tuning")
    random.Random(args.seed).shuffle(examples)
    split = max(1, int(len(examples) * 0.9))
    write_jsonl(args.output / "train.jsonl", examples[:split])
    write_jsonl(args.output / "validation.jsonl", examples[split:])
    print(f"Prepared {split} train and {len(examples) - split} validation examples")


if __name__ == "__main__":
    main()
