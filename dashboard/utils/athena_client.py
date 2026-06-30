import time
from pathlib import Path

import boto3
import pandas as pd


DATABASE = "inventoryiq"
WORKGROUP = "primary"
REGION = "us-east-1"
OUTPUT_LOCATION = "s3://inventoryiq-athena-results-sandeep/"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUERY_DIR = PROJECT_ROOT / "athena_queries"

athena = boto3.client("athena", region_name=REGION)


def run_query(query: str) -> pd.DataFrame:
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": DATABASE},
        ResultConfiguration={"OutputLocation": OUTPUT_LOCATION},
        WorkGroup=WORKGROUP,
    )

    query_execution_id = response["QueryExecutionId"]

    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = result["QueryExecution"]["Status"]["State"]

        if state == "SUCCEEDED":
            break

        if state in ["FAILED", "CANCELLED"]:
            reason = result["QueryExecution"]["Status"].get("StateChangeReason", "No reason provided")
            raise RuntimeError(f"Athena query {state}: {reason}")

        time.sleep(1)

    results = athena.get_query_results(QueryExecutionId=query_execution_id)

    rows = results["ResultSet"]["Rows"]
    columns = [col.get("VarCharValue", "") for col in rows[0]["Data"]]

    data = []
    for row in rows[1:]:
        data.append([col.get("VarCharValue", None) for col in row["Data"]])

    return pd.DataFrame(data, columns=columns)


def run_sql_file(file_name: str) -> pd.DataFrame:
    query_path = QUERY_DIR / file_name

    with open(query_path, "r") as file:
        query = file.read()

    return run_query(query)