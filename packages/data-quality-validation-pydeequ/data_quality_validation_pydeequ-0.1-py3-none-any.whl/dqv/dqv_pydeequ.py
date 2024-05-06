import yaml
import os
from data_quality_validation_pydeequ import DataQualityValidation
from pyspark.sql import SparkSession
from pathlib import Path
import pydeequ


class DqvPydeequ:
    """Class for performing data quality validation using PyDeequ and sending email notifications."""

    def __init__(
        self, 
        config_path: str, 
        source_path: str, 
        target_path: str, 
        **kwargs) -> None:
        """Initialize the DqvPydeequ class.

        Args:
            config_path (str): Path to configuration file.
            source_path (str): Path to source data.
            target_path (str): Path to target data.
            email_config (dict): Email configuration settings.
        """
        spark = (
            SparkSession.builder.appName("data_quality_validation_pydeequ")
                .enableHiveSupport()
                .config("spark.dynamicAllocation.enabled", "true")
                .config("spark.jars.packages", pydeequ.deequ_maven_coord)
                .config("spark.jars.excludes", pydeequ.f2j_maven_coord)
                .config("spark.default.parallelism", "10")
                .config("spark.sql.shuffle.partitions", "10")
                .config("spark.sql.files.ignoreCorruptFiles", "true")
                .getOrCreate()
        )
        with open(config_path, "r") as stream:
            data = yaml.safe_load(stream)
        config = data["DQ_ASSERTIONS"]["DIR1"]["PRODUCT_FILE"]
        print(config)
        try :
            bolosse = DataQualityValidation(
                spark,
                source_path,
                target_path,
                config,
            )
            bolosse.execute()
            spark.stop()
        except Exception as ex:
            print(ex)
            spark.stop()
            