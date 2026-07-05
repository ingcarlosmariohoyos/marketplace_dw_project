import os
from dagster import Definitions
from dagster_dbt import DbtCliResource
from dagster_project.assets.bronze import create_bronze_tables, load_raw_to_bronze
from dagster_project.assets.dbt_assets import dbt_assets_def, DBT_PROJECT_DIR
from dagster_project.assets.gold import create_foreign_keys
from dagster_project.jobs import marketplace_dw_job, marketplace_schedule

defs = Definitions(
    assets=[create_bronze_tables, load_raw_to_bronze, dbt_assets_def, create_foreign_keys],
    schedules=[marketplace_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(DBT_PROJECT_DIR)),
    },
)