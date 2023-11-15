# finnhub_data_extraction
This is a sample Repo for extracting data from finnhub using API

## install poetry
`pip3 install poetry`

## start a new shell and activate the virtual environment.
`poetry shell`

## Run the docker compose file
`docker compose -f zk-single-kafka-multiple.yml up -d`

## Enable the relative path
`export PYTHONPATH="${PYTHONPATH}:/path/to/your/project/"`

## Run producer and consumer codes
- `poetry run python3 -m finnhub_producer`
- `poetry run python3 -m finnhub_consumer`

## Run Spark Job

- `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 `<source/to/app.py>``