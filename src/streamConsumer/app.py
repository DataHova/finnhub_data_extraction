from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.types import *
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, DoubleType, LongType
from pyspark.sql.functions import from_json, col
import os

from dotenv import load_dotenv
load_dotenv()

topic = os.getenv('topic')

# Create a Spark Session with the Kafka package included
spark = SparkSession \
    .builder \
    .master("spark://localhost:7077") \
    .appName("KafkaStreamProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()
    # .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1") \
    

# Define the schema for the nested 'data' array
data_schema = StructType([
    StructField('c', ArrayType(StringType(), containsNull=True), nullable=True),
    StructField('p', DoubleType(), nullable=False),
    StructField('s', StringType(), nullable=False),
    StructField('t', LongType(), nullable=False),
    StructField('v', DoubleType(), nullable=False)
])

# Define the top-level schema for the stream
schema = StructType([
    StructField('data', ArrayType(data_schema), nullable=False),
    StructField('type', StringType(), nullable=False)
])

# Read from Kafka
kafkaStreamDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", topic) \
    .option("startingOffsets", "earliest") \
    .option("header", "true") \
    .load()
#  .schema(schema) \
    
# Process the stream and Parse the JSON data using the schema defined above
parsed_df = kafkaStreamDF \
            .selectExpr("CAST(value AS STRING)") \
            .withColumn("jsonData", from_json(col("value"), data_schema)) \
            .select("jsonData.*")

# Now you can select the data you need from the jsonData column
# flattened_df = parsed_df.select(
#     col("jsonData.data.c").alias("c"),
#     col("jsonData.data.p").alias("p"),
#     col("jsonData.data.s").alias("s"),
#     col("jsonData.data.t").alias("t"),
#     col("jsonData.data.v").alias("v"),
#     col("jsonData.type")
# )

# flattened_df.show()
              

# Process and start the streaming query
query = parsed_df.writeStream \
                .outputMode("append") \
                .format("console") \
                .start() \
                .awaitTermination()


# Consume and Output the Stream
# query = valuesDF.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()

# query.awaitTermination()



# cleanUp
# query.stop()


# Converting the Unix millis to seconds
# from pyspark.sql.functions import col
# from pyspark.sql.types import TimestampType

# # Assuming unix_millis is in milliseconds
# df_with_timestamp = df.withColumn("timestamp", (col("unix_millis") / 1000).cast(TimestampType()))
