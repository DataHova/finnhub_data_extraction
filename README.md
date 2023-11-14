# finnhub_data_extraction
This is a sample Repo for extracting data from finnhub using API

## Run the docker compose file
`docker compose -f zk-single-kafka-multiple.yml up`

## Run producer and consumer codes
- `poetry run python3 finnhub_producer.py`
- `poetry run python3 finnhub_consumer.py`

## Run Spark Job

- `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 `<source/to/app.py>``