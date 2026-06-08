import os
from pathlib import Path
from dagster import Definitions, AssetExecutionContext, define_asset_job, ScheduleDefinition
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

# ==============================================================================
# CONFIGURACIÓN DE RUTAS DINÁMICAS (Compatibilidad Windows Local / Render Linux)
# ==============================================================================
# BASE_DIR apunta a la raíz del proyecto (MARKETPLACE_DW_PROJECT)
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta al proyecto de dbt
DBT_PROJECT_DIR = BASE_DIR / "dbt"

# Ruta exacta al ejecutable de dbt dentro del entorno virtual dbt_env_39
DBT_EXECUTABLE_PATH = BASE_DIR / "dbt_env_39" / "bin" / "dbt"

# ==============================================================================
# INICIALIZACIÓN DEL PROYECTO DBT
# ==============================================================================
dbt_project = DbtProject(project_dir=DBT_PROJECT_DIR)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_assets_def(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

# ==============================================================================
# TRABAJOS Y PLANIFICACIONES (SCHEDULES)
# ==============================================================================
marketplace_dw_job = define_asset_job(name="marketplace_dw_job", selection="*")

marketplace_schedule = ScheduleDefinition(
    job=marketplace_dw_job,
    cron_schedule="0 0 * * *", 
    execution_timezone="America/Bogota"
)

# ==============================================================================
# DEFINICIÓN DEL DEPLOY DE DAGSTER
# ==============================================================================
defs = Definitions(
    assets=[dbt_assets_def],
    schedules=[marketplace_schedule],
    resources={
        "dbt": DbtCliResource(
            project_dir=os.fspath(DBT_PROJECT_DIR),
            dbt_executable=os.fspath(DBT_EXECUTABLE_PATH)  # <-- Corrección del ejecutable
        ),
    },
)