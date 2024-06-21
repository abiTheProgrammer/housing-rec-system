import os
import sys
from pyspark.sql import SparkSession

class HouseDataConverter:
    def __init__(self, file_path: str):
        # Initialize Spark Session instance
        self.spark = SparkSession.builder \
            .appName("ReadScraperData") \
            .getOrCreate()
        # find the csv file inside the directory (if it exists)
        if os.listdir(file_path):
            for filename in os.listdir(file_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(file_path, filename)
                    break
            self.df = self.spark.read.option('header', 'true').csv(file_path)

    def __del__(self):
        self.spark.stop()

# to run the file using "python3 <relative-path-of-file> <relative-path-to-data-file>"
if __name__ == "__main__":
    hdc = HouseDataConverter(sys.argv[len(sys.argv) - 1])
    del hdc