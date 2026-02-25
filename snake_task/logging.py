"""CSV logging utilities for experiment runs."""

import csv
import os
from typing import Any, Mapping, Optional
from config import RATE_DECIMALS

FIELDNAMES: list[str] = [
	"participant_id",
	"version",
	"session_date",
	"session_time",
	"difficulty",
	"snake_length",
	"score",
	"score_per_ms",
	"hits_per_ms",
	"collisions_per_ms",
	"target_hit",
	"collisions",
]

def _float_or_none(value: Any) -> Optional[float]:
	"""Safely convert a value to float or return None.

	Args:
		value: Any value that may represent a number (string, int, float),
		or may be None/empty.

	Returns:
		A float if conversion succeeds, otherwise ``None`` for None/empty
		or when conversion raises a ValueError/TypeError.
	"""
	try:
		if value is None:
			return None
		if value == "":
			return None
		return float(value)
	except (TypeError, ValueError):
		return None

def _migrate_log_file(path: str) -> None:
	"""Migrate an existing CSV log to the current FIELDNAMES.

	This function reads the existing CSV at `path`. If the header already
	matches `FIELDNAMES` no action is taken. Otherwise it reads all rows,
	rewrites them to a temporary file using the current `FIELDNAMES`,
	backfilling fields where possible (for example splitting a legacy
	`session_datetime` into `session_date` and `session_time`, and deriving
	per-ms rates from a legacy `survival_time`). The original file is
	replaced with the migrated temporary file at the end.

	Args:
		path: Path to the CSV file to migrate.

	Returns:
		None
	"""
	with open(path, "r", newline="", encoding="utf-8") as handle:
		reader = csv.reader(handle)
		existing_header = next(reader, None)
		if existing_header is None:
			return
		if existing_header == FIELDNAMES:
			return

	with open(path, "r", newline="", encoding="utf-8") as handle:
		dict_reader = csv.DictReader(handle)
		rows = list(dict_reader)

	tmp_path = f"{path}.tmp"
	with open(tmp_path, "w", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
		writer.writeheader()
		for row in rows:
			out = {name: row.get(name, "") for name in FIELDNAMES}
			if out.get("session_date", "") in ("", None) and out.get("session_time", "") in ("", None):
				date_part, time_part = _split_session_datetime(row.get("session_datetime"))
				if date_part:
					out["session_date"] = date_part
				if time_part:
					out["session_time"] = time_part
			denom_sec = _float_or_none(row.get("survival_time"))
			if denom_sec and denom_sec > 0:
				denom_ms = denom_sec * 1000.0

				if out.get("score_per_ms", "") in ("", None):
					score = _float_or_none(row.get("score"))
					if score is not None:
						out["score_per_ms"] = f"{(score / denom_ms):.{RATE_DECIMALS}f}"

				if out.get("hits_per_ms", "") in ("", None):
					hits = _float_or_none(row.get("target_hit"))
					if hits is not None:
						out["hits_per_ms"] = f"{(hits / denom_ms):.{RATE_DECIMALS}f}"

				if out.get("collisions_per_ms", "") in ("", None):
					collisions = _float_or_none(row.get("collisions"))
					if collisions is not None:
						out["collisions_per_ms"] = f"{(collisions / denom_ms):.{RATE_DECIMALS}f}"
			writer.writerow(out)

	os.replace(tmp_path, path)

def ensure_log_file(path: str) -> None:
	"""Ensure the CSV exists and matches the expected header.

	Args:
		path: CSV file path.
	"""
	os.makedirs(os.path.dirname(path), exist_ok=True)
	if not os.path.exists(path):
		with open(path, "w", newline="", encoding="utf-8") as handle:
			writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
			writer.writeheader()
		return
	_migrate_log_file(path)

def append_log(path: str, row: Mapping[str, Any]) -> None:
	"""Append one row of results to the CSV log.

	Args:
		path: CSV file path.
		row: Mapping of field name to value.
	"""
	ensure_log_file(path)
	with open(path, "a", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
		writer.writerow(row)

def append_blank_row(path: str) -> None:
	"""Append a blank row (visual separator) to the CSV log.

	Args:
		path: CSV file path.
	"""
	ensure_log_file(path)
	with open(path, "a", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle)
		writer.writerow([])

def _split_session_datetime(value: Any) -> tuple[str, str]:
	"""Split a session datetime string into date and time parts.

	Args:
		value: A session datetime value (often a string) in formats like
			"M/D/YYYY  H:MM:SS AM/PM" or similar.

	Returns:
		A tuple ``(date_str, time_str)``. If the input is None or empty,
		returns two empty strings. If only a single token is present, the
		token is returned as the date and the time is an empty string.
	"""
	if value is None:
		return "", ""
	text = str(value).strip()
	if not text:
		return "", ""
	parts = text.split()
	if len(parts) < 2:
		return text, ""
	return parts[0], " ".join(parts[1:])