#!/usr/bin/env python3
"""Reference scorer for the calibration interview rubric."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Score pre-committed calibration predictions against actual answers."
        )
    )
    parser.add_argument("predictions", type=Path, help="JSON file of predicted answers")
    parser.add_argument("answers", type=Path, help="JSON file of actual answers")
    parser.add_argument(
        "--bar",
        type=float,
        default=90.0,
        help="Pass bar on a 100-point scale (default: 90)",
    )
    return parser.parse_args()


def load_json_list(path: Path, required_fields: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list")

    items: list[dict[str, str]] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"{path} item {index} must be an object")
        missing = [field for field in required_fields if field not in item]
        if missing:
            raise ValueError(
                f"{path} item {index} is missing required fields: {', '.join(missing)}"
            )
        items.append({field: str(item[field]) for field in required_fields})
    return items


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def score_reasoning(predicted_reasoning: str, actual_reasoning: str) -> tuple[int, list[str]]:
    # Reference heuristic only: count distinct overlapping keywords and cap at 4.
    predicted_tokens = set(tokenize(predicted_reasoning))
    actual_tokens = set(tokenize(actual_reasoning))
    overlap = sorted(predicted_tokens & actual_tokens)
    return min(4, len(overlap)), overlap


def main() -> int:
    args = parse_args()

    try:
        predictions = load_json_list(
            args.predictions,
            ("question", "predicted_decision", "predicted_reasoning"),
        )
        answers = load_json_list(
            args.answers,
            ("question", "actual_decision", "actual_reasoning"),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    predictions_by_question = {
        item["question"]: item for item in predictions
    }

    total_points = 0
    max_points = len(answers) * 10

    print("Calibration scoring breakdown")
    print("=" * 30)

    for index, answer in enumerate(answers, start=1):
        prediction = predictions_by_question.get(answer["question"])
        decision_points = 0
        reasoning_points = 0
        overlap: list[str] = []

        if prediction is None:
            predicted_decision = "(missing prediction)"
        else:
            predicted_decision = prediction["predicted_decision"]
            if prediction["predicted_decision"] == answer["actual_decision"]:
                decision_points = 6
            reasoning_points, overlap = score_reasoning(
                prediction["predicted_reasoning"],
                answer["actual_reasoning"],
            )

        question_points = decision_points + reasoning_points
        total_points += question_points

        print(f"{index}. {answer['question']}")
        print(f"   Predicted decision: {predicted_decision}")
        print(f"   Actual decision:    {answer['actual_decision']}")
        print(f"   Decision points:    {decision_points}/6")
        if overlap:
            print(
                "   Reasoning points:   "
                f"{reasoning_points}/4 (overlap: {', '.join(overlap)})"
            )
        else:
            print(f"   Reasoning points:   {reasoning_points}/4")
        print(f"   Question score:     {question_points}/10")
        print()

    normalized_score = (total_points / max_points) * 100 if max_points else 0.0
    status = "PASS" if normalized_score >= args.bar else "FAIL"

    print(f"Total points: {total_points}/{max_points}")
    print(f"Total score:  {normalized_score:.1f}/100")
    print(f"Pass bar:     {args.bar:.1f}/100")
    print(status)

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
