from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, lower, regexp_replace, trim, col, udf, array
from pyspark.sql import functions as F
from pyspark.ml.feature import StopWordsRemover
import json
import spacy
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize Spark session
spark = SparkSession.builder.appName("NERKafkaSparkStreaming").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.shuffle.partitions", "4")

# Function to remove emojis
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # other miscellaneous symbols
                               u"\U000024C2-\U0001F251"  # enclosed characters
                               u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
                               u"\U0001FA70-\U0001FAFF"  # chess symbols
                               u"\U00002600-\U000026FF"  # miscellaneous symbols
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Function to extract named entities
def extract_entities(text):
    named_entities = ["PERSON", "ORG", "GPE", "LOC", "EVENT", "WORK_OF_ART"]
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_.upper() in named_entities and len(ent.text.split()) == 1]

# Register UDFs
remove_emojis_udf = F.udf(lambda text: remove_emojis(text))
extract_entities_udf = F.udf(lambda text: extract_entities(text), F.ArrayType(F.StringType()))

# Stop words remover
stopwords_remover = StopWordsRemover(inputCol="words", outputCol="filtered_text")

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "topic1") \
    .load()

# Preprocess the data
preprocessed_df = df \
    .selectExpr("CAST(value AS STRING) AS json_string") \
    .selectExpr("json_tuple(json_string, 'body') AS text") \
    .withColumn("text", lower(trim("text"))) \
    .withColumn("text", regexp_replace("text", "[\\n\\.\\,\\!\\?\\-]", " ")) \
    .withColumn("text", remove_emojis_udf("text")) \
    .withColumn("text", regexp_replace("text", "\\s+", " ")) \
    .withColumn("words", F.split("text", " ")) \
    .transform(lambda df: stopwords_remover.transform(df)) \
    .withColumn("filtered_text", F.expr("filter(filtered_text, x -> x != '')")) \
    .withColumn("entities", extract_entities_udf("text"))

preprocessed_df = preprocessed_df.withColumn("entities", F.expr("filter(entities, x -> x NOT IN ('n\\'t', 'un', 'etc', 'i', '\\\\'))"))

# Count entities
entity_counts = preprocessed_df \
    .select(explode("entities").alias("entity")) \
    .groupBy("entity").count()

# Function to print and send data to Kafka (optional for debug)
def print_and_send_to_kafka(df, epoch_id):
    for row in df.collect():
        entity = row['entity']
        count = row['count']
        print(f"ENTITY COUNT: Entity: {entity}, Count: {count}")

# Query to write to Kafka
query_kafka = entity_counts \
    .select(F.to_json(F.struct("entity", "count")).alias("value")) \
    .writeStream \
    .outputMode("update") \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("topic", "topic2") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .start()

# Query to print to console
console_query = entity_counts \
    .select("entity", "count") \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

# Await termination
query_kafka.awaitTermination()
console_query.awaitTermination()
