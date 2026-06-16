"""
analytics.py — PySpark Text Analytics Job

Reads all .txt files from INPUT_DIR, computes per-file statistics
(line count, word count, average line length, top word), writes a
summary CSV to OUTPUT_DIR, and prints the top-10 words across all files.

Configuration (environment variables):
    INPUT_DIR       Path to input text files  (default: /workspace/input)
    OUTPUT_DIR      Path for output files      (default: /workspace/output)
    MIN_WORD_LEN    Minimum word length to include in frequency counts (default: 4)
"""

import csv
import logging
import os
import sys
from typing import List, Dict, Any

from pyspark.sql import SparkSession
from pyspark import RDD

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration via environment variables
# ---------------------------------------------------------------------------
INPUT_DIR: str = os.environ.get("INPUT_DIR", "/workspace/input")
OUTPUT_DIR: str = os.environ.get("OUTPUT_DIR", "/workspace/output")
MIN_WORD_LEN: int = int(os.environ.get("MIN_WORD_LEN", "4"))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_input_files(input_dir: str) -> List[str]:
    """Return sorted list of .txt file paths inside *input_dir*."""
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"INPUT_DIR does not exist: {input_dir!r}")
    files = sorted(
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".txt")
    )
    return files


def analyse_file(
    sc,
    filepath: str,
    min_word_len: int,
) -> tuple[Dict[str, Any], "RDD"]:
    """
    Analyse a single text file.

    Returns
    -------
    summary : dict
        Per-file statistics.
    filtered_words_rdd : RDD
        RDD of words with length >= min_word_len (for global aggregation).
    """
    filename = os.path.basename(filepath)
    lines_rdd: RDD = sc.textFile(filepath)

    line_count: int = lines_rdd.count()

    if line_count == 0:
        log.warning("File %s is empty — skipping word analysis.", filename)
        return (
            {
                "filename": filename,
                "line_count": 0,
                "word_count": 0,
                "avg_line_length": 0.0,
                "top_word": "N/A",
            },
            sc.emptyRDD(),
        )

    words_rdd: RDD = lines_rdd.flatMap(lambda line: line.lower().split())
    word_count: int = words_rdd.count()

    avg_line_length: float = round(
        lines_rdd.map(len).sum() / line_count, 2
    )

    filtered_words: RDD = words_rdd.filter(lambda w: len(w) >= min_word_len)
    word_freq: RDD = filtered_words.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
    top_word_pair = word_freq.takeOrdered(1, key=lambda x: -x[1])
    top_word: str = top_word_pair[0][0] if top_word_pair else "N/A"

    summary: Dict[str, Any] = {
        "filename": filename,
        "line_count": line_count,
        "word_count": word_count,
        "avg_line_length": avg_line_length,
        "top_word": top_word,
    }
    return summary, filtered_words


def write_summary_csv(output_path: str, rows: List[Dict[str, Any]]) -> None:
    """Write per-file summary rows to *output_path* as CSV."""
    fieldnames = ["filename", "line_count", "word_count", "avg_line_length", "top_word"]
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log.info("Summary CSV written to: %s", output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # --- Discover input files -------------------------------------------
    try:
        input_files = get_input_files(INPUT_DIR)
    except FileNotFoundError as exc:
        log.error(exc)
        sys.exit(1)

    if not input_files:
        log.warning("No .txt files found in %s — nothing to do.", INPUT_DIR)
        sys.exit(0)

    log.info("Found %d input file(s): %s", len(input_files), input_files)

    # --- Prepare output directory ----------------------------------------
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Spark session -----------------------------------------------------
    spark = (
        SparkSession.builder
        .appName("TextAnalytics")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    sc = spark.sparkContext

    try:
        summary_rows: List[Dict[str, Any]] = []
        per_file_rdds: List[RDD] = []

        for filepath in input_files:
            summary, filtered_words = analyse_file(sc, filepath, MIN_WORD_LEN)
            summary_rows.append(summary)
            per_file_rdds.append(filtered_words)

        # --- Per-file summary --------------------------------------------
        sep = "=" * 60
        log.info("%s", sep)
        log.info("Per-File Summary:")
        log.info("%s", sep)
        for row in summary_rows:
            log.info(
                "  %s | Lines: %d | Words: %d | Avg Length: %.2f | Top Word: %s",
                row["filename"],
                row["line_count"],
                row["word_count"],
                row["avg_line_length"],
                row["top_word"],
            )

        # --- Write CSV ---------------------------------------------------
        output_csv = os.path.join(OUTPUT_DIR, "summary.csv")
        write_summary_csv(output_csv, summary_rows)

        # --- Global top-10 words -----------------------------------------
        # Union all per-file RDDs in one call to avoid lineage explosion
        all_words_rdd: RDD = sc.union(per_file_rdds)
        global_freq: RDD = all_words_rdd.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
        top10 = global_freq.takeOrdered(10, key=lambda x: -x[1])

        log.info("%s", sep)
        log.info("TOP 10 WORDS ACROSS ALL FILES:")
        log.info("%s", sep)
        for word, cnt in top10:
            log.info("  %-25s %d", word, cnt)
        log.info("%s", sep)

    finally:
        spark.stop()
        log.info("SparkSession stopped.")


if __name__ == "__main__":
    main()
