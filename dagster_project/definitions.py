import os
from pathlib import Path
from dagster import Definitions, AssetExecutionContext, define_asset_job, ScheduleDefinition
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

# ==============================================================================
# CONFIGURACIÓN DE RUTAS
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DBT_PROJECT_DIR = BASE_DIR / "dbt"

# DbtProject maneja el manifest automáticamente
dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
dbt_project.prepare_if_dev()

# ==============================================================================
# ASSETS, JOBS Y DEFINICIONES
# ==============================================================================
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_assets_def(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

marketplace_dw_job = define_asset_job(name="marketplace_dw_job", selection="*")

marketplace_schedule = ScheduleDefinition(
    job=marketplace_dw_job,
    cron_schedule="0 0 * * *",
    execution_timezone="America/Bogota"
)

defs = Definitions(
    assets=[dbt_assets_def],
    schedules=[marketplace_schedule],
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(DBT_PROJECT_DIR)),
    },
)