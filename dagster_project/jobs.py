from dagster import define_asset_job, ScheduleDefinition

marketplace_dw_job = define_asset_job(name="marketplace_dw_job", selection="*")

marketplace_schedule = ScheduleDefinition(
    job=marketplace_dw_job,
    cron_schedule="0 0 * * *",
    execution_timezone="America/Bogota"
)