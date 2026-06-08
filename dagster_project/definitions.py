import os
from pathlib import Path
# Agregamos in_process_executor a las importaciones de dagster
from dagster import Definitions, AssetExecutionContext, define_asset_job, ScheduleDefinition, in_process_executor
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

# ==============================================================================
# CONFIGURACIÓN DE RUTAS DINÁMICAS
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DBT_PROJECT_DIR = BASE_DIR / "dbt"
DBT_EXECUTABLE_PATH = BASE_DIR / "dbt_env_39" / "bin" / "dbt"

# ==============================================================================
# EN PRODUCCIÓN (RENDER): Generar el manifest.json si no existe antes de arrancar
# ==============================================================================
MANIFEST_PATH = (DBT_PROJECT_DIR / "target" / "manifest.json").resolve()

if not MANIFEST_PATH.exists():
    import subprocess
    print("Manifest no encontrado. Generando manifest.json de forma dinámica...")
    subprocess.run(
        [os.fspath(DBT_EXECUTABLE_PATH), "parse"],
        cwd=os.fspath(DBT_PROJECT_DIR),
        check=True
    )

# Ahora inicializamos el DbtProject de forma segura
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
        "dbt": DbtCliResource(
            project_dir=os.fspath(DBT_PROJECT_DIR),
            dbt_executable=os.fspath(DBT_EXECUTABLE_PATH)
        ),
    },
    # CONFIGURACIÓN DE EJECUTOR: Corre de forma síncrona dentro del proceso principal
    # para mitigar el límite de 512 MB de RAM en Render.
    executor_def=in_process_executor,
)