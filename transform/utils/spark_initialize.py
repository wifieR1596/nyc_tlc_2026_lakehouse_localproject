from pyspark.sql import SparkSession

def get_spark_session(app_name: str = "tlc_lakehouse_project") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .master("local[2]")
        .config("spark.driver.memory", "4g")
        .config("spark.sql.session.timeZone", "UTC")
        .getOrCreate()
    )
