from athena_client import run_sql_file

df = run_sql_file("executive_kpis_athena.sql")

print(df)