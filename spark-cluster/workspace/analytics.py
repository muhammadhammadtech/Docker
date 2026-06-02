from pyspark.sql import SparkSession
import os
import csv

spark = SparkSession.builder \
    .appName("TextAnalytics") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

INPUT_DIR = "/workspace/input"
OUTPUT_DIR = "/workspace/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

input_files = [
    os.path.join(INPUT_DIR, f)
    for f in os.listdir(INPUT_DIR)
    if f.endswith(".txt")
]

print("\n" + "="*60)
print("Files found:", input_files)
print("="*60 + "\n")

summary_rows = []
all_words_rdd = spark.sparkContext.emptyRDD()

for filepath in input_files:
    filename = os.path.basename(filepath)
    lines_rdd = spark.sparkContext.textFile(filepath)

    line_count = lines_rdd.count()
    words_rdd = lines_rdd.flatMap(lambda line: line.lower().split())
    word_count = words_rdd.count()

    line_lengths = lines_rdd.map(lambda line: len(line))
    avg_line_length = line_lengths.sum() / line_count if line_count > 0 else 0

    filtered_words = words_rdd.filter(lambda w: len(w) >= 4)
    word_freq = filtered_words.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
    top_word_pair = word_freq.takeOrdered(1, key=lambda x: -x[1])
    top_word = top_word_pair[0][0] if top_word_pair else "N/A"

    summary_rows.append({
        "filename": filename,
        "line_count": line_count,
        "word_count": word_count,
        "avg_line_length": round(avg_line_length, 2),
        "top_word": top_word
    })

    all_words_rdd = all_words_rdd.union(filtered_words)

output_csv = os.path.join(OUTPUT_DIR, "summary.csv")
with open(output_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["filename","line_count","word_count","avg_line_length","top_word"])
    writer.writeheader()
    writer.writerows(summary_rows)

print("\n" + "="*60)
print("Per-File Summary:")
print("="*60)
for row in summary_rows:
    print(f"  File: {row['filename']}")
    print(f"    Lines: {row['line_count']} | Words: {row['word_count']} | Avg Length: {row['avg_line_length']} | Top Word: {row['top_word']}")
print(f"\nCSV written to: {output_csv}")

print("\n" + "="*60)
print("TOP 10 WORDS ACROSS ALL FILES:")
print("="*60)
global_freq = all_words_rdd.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)
top10 = global_freq.takeOrdered(10, key=lambda x: -x[1])
for word, cnt in top10:
    print(f"  {word:<25} {cnt}")
print("="*60 + "\n")

spark.stop()
