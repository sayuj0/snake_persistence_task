import csv
import os

from config import RATE_DECIMALS


FIELDNAMES = [
	"participant_id",
	"session_datetime",
	"difficulty",
	"snake_length",
	"score",
	"score_per_ms",
	"survival_time",
	"target_hit",
	"collisions",
]


def _float_or_none(value):
	try:
		if value is None:
			return None
		if value == "":
			return None
		return float(value)
	except (TypeError, ValueError):
		return None


def _migrate_log_file(path):
	# If the CSV exists but has an older header, rewrite it with the new header.
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
		writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
		writer.writeheader()
		for row in rows:
			# Preserve blank rows (DictReader won't return them)
			out = {name: row.get(name, "") for name in FIELDNAMES}
			if out.get("score_per_ms", "") in ("", None):
				score = _float_or_none(out.get("score"))
				survival_time = _float_or_none(out.get("survival_time"))
				if score is not None and survival_time and survival_time > 0:
					out["score_per_ms"] = f"{(score / (survival_time * 1000.0)):.{RATE_DECIMALS}f}"
			writer.writerow(out)

	os.replace(tmp_path, path)


def ensure_log_file(path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	if not os.path.exists(path):
		with open(path, "w", newline="", encoding="utf-8") as handle:
			writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
			writer.writeheader()
		return
	_migrate_log_file(path)


def append_log(path, row):
	ensure_log_file(path)
	with open(path, "a", newline="", encoding="utf-8") as handle:
		writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
		writer.writerow(row)


def append_blank_row(path):
	ensure_log_file(path)
	with open(path, "a", newline="", encoding="utf-8") as handle:
		writer = csv.writer(handle)
		writer.writerow([])

