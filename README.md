# Shop Inventory Analysis

## Quickstart

1. Download input files: `coding_challenge_inventory.csv`, `coding_challenge_meta.csv` and `coding_challenge_prices.csv` into `etl/inputs/`.
2. Run `docker compose up -d`.
3. Navigate to http://127.0.0.1:8000/docs in order to see the API docs and execute requests.

## ETL

ETL process is implemented using Jupyter Notebook. While it's not the usual way how the production-grade
software is implemented, it's the perfect tool for R&D activities on data. Notebook is executed on the
input data stored in `etc/inputs/` in headless mode using `papermill`. Resulting notebook is converted
to html and saved a `etl/outputs/output.html` together with the results (as CSVs) in the same directory.
Generated notebook describes the processing approach and assumptions for inputs.

Loading into DB (postgres 17) is conducted via `etl/db-init.sql` script that creates the tables, and
then loads generated data inside.

In order to browse loaded data one can use `psql` shell executed directly on the container:

```
$ docker compose exec db psql -U postgres
```

## API
