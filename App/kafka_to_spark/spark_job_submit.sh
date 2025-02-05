#!/bin/bash

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 kafka_to_spark.py kafka:9092 topic1 topic2