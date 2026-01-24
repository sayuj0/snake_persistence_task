import csv
import os


FIELDNAMES = [
	"participant_id",
	"session_datetime",
	"difficulty",
	"snake_length",
	"score",
	"survival_time",
	"target_hit",
	"collisions",
]


def ensure_log_file(path):
	os.makedirs(os.path.dirname(path), exist_ok=True)
	if not os.path.exists(path):
		with open(path, "w", newline="", encoding="utf-8") as handle:
			writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
			writer.writeheader()


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

