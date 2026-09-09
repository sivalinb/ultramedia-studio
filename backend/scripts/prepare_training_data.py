"""Export corrected, consenting editorial examples with original evidence."""

import argparse
from pathlib import Path

from sqlalchemy import select

from ultramedia.database import Database, EditorialRevision, GenerationRecord, StoryDraft
from ultramedia.dataset import example_record, sha, write_dataset


def build_examples(database_url):
    database = Database(database_url)
    database.create_all()
    rows = []
    with database.session() as db:
        for record in db.scalars(select(GenerationRecord)):
            story = db.get(StoryDraft, record.story_id)
            review = db.scalar(
                select(EditorialRevision).where(
                    EditorialRevision.story_id == story.id, EditorialRevision.revision == record.revision
                )
            )
            if not review or story.status != "approved" or not review.training_consent or not review.rights_basis:
                continue
            provenance = {
                **record.provenance,
                "human_approved": True,
                "reviewer": review.reviewer,
                "review_revision": review.revision,
                "rights_basis": review.rights_basis,
                "training_consent": True,
            }
            rows.append(
                example_record(story.id, record.provenance["group_id"], record.inputs, record.output, provenance)
            )
    groups = sorted({r["group_id"] for r in rows}, key=sha)
    if len(rows) < 20 or len(groups) < 3:
        raise ValueError("Export requires 20 consenting, approved examples from at least three independent race groups")
    train_end = max(1, int(len(groups) * 0.7))
    validation_end = min(len(groups) - 1, max(train_end + 1, int(len(groups) * 0.85)))
    group_split = {
        g: "train" if i < train_end else "validation" if i < validation_end else "test" for i, g in enumerate(groups)
    }
    for row in rows:
        row["split"] = group_split[row["group_id"]]
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--database-url", default="sqlite:///ultramedia.db")
    parser.add_argument("--output", type=Path, default=Path("training_data/reviewed"))
    args = parser.parse_args()
    print(write_dataset(build_examples(args.database_url), args.output, "editor_reviewed"))


if __name__ == "__main__":
    main()
