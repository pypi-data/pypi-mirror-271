from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType
from pyspark.sql.functions import udf


# Initialize Spark Session
spark = SparkSession.builder.appName("Anonymizer").getOrCreate()
sc = spark.sparkContext

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


def anonymize_column(df: DataFrame, column: str) -> DataFrame:
    # Each task creates its own analyzer and anonymizer
    broadcasted_analyzer = sc.broadcast(analyzer)
    broadcasted_anonymizer = sc.broadcast(anonymizer)

    def anonymize_text(text):
        # Analyze the text to detect personal information
        analyzer = broadcasted_analyzer.value
        anonymizer = broadcasted_anonymizer.value
        analyzer_results = analyzer.analyze(text=text, language="en")
        anonymized_result = anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results,
            operators={"DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"})}
        )
        return anonymized_result.text

    # Define a UDF that applies the anonymization function
    anonymize_udf = udf(anonymize_text, StringType())

    # Apply the anonymization UDF to the specified column
    return df.withColumn(column, anonymize_udf(df[column]))