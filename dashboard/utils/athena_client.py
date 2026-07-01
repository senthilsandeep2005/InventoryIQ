import time
from pathlib import Path
import boto3
import pandas as pd
import streamlit as st



DATABASE = "inventoryiq"
WORKGROUP = "primary"
REGION = "us-east-1"
OUTPUT_LOCATION = "s3://inventoryiq-athena-results-sandeep/"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUERY_DIR = PROJECT_ROOT / "athena_queries"

athena = boto3.client(

    "athena",

    region_name=REGION,

    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],

    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],

)


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

        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break

        time.sleep(1)

    if state != "SUCCEEDED":
        reason = result["QueryExecution"]["Status"].get("StateChangeReason", "Unknown error")
        raise RuntimeError(f"Athena query {state}: {reason}")

    rows = []
    column_names = None
    next_token = None

    while True:
        if next_token:
            results = athena.get_query_results(
                QueryExecutionId=query_execution_id,
                NextToken=next_token
            )
        else:
            results = athena.get_query_results(QueryExecutionId=query_execution_id)

        result_rows = results["ResultSet"]["Rows"]

        if column_names is None:
            column_names = [col.get("VarCharValue", "") for col in result_rows[0]["Data"]]
            result_rows = result_rows[1:]

        for row in result_rows:
            rows.append([
                col.get("VarCharValue", None)
                for col in row.get("Data", [])
            ])

        next_token = results.get("NextToken")

        if not next_token:
            break

    return pd.DataFrame(rows, columns=column_names)

@st.cache_data(ttl=3600)
def run_sql_file(file_name: str) -> pd.DataFrame:
    query_path = QUERY_DIR / file_name

    with open(query_path, "r") as file:
        query = file.read()

    return run_query(query)