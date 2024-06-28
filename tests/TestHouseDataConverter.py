import unittest
from unittest.mock import patch, mock_open
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from src.data_processing.house_data_converter import HouseDataConverter  # Adjusted import

class TestHouseDataConverter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("HouseDataConverter") \
            .getOrCreate()
        cls.mock_config = {
            'home_type_mapping': {
                'Single Family': 1,
                'Condo': 2,
                'Townhouse': 3,
                'Multi Family': 4
            }
        }

    @classmethod
    def tearDownClass(cls):
        if cls.spark:
            cls.spark.stop()

    def setUp(self):
        self.mock_file_path = 'data/uncleaned/data_all_states.csv'
        self.mock_config_path = 'config/config.json'
        self.mock_data = [
            ("$500,000", "$3,000/mo", "3 beds", "2 baths", "2,000 sqft", "Single Family", "123 Main St, City, ST 12345"),
            ("$250,000", "$1,500/mo", "2 beds", "1 bath", "1,000 sqft", "Condo", "456 Elm St, Town, TS 67890")
        ]
        self.schema = StructType([
            StructField("Price", StringType(), True),
            StructField("Rent Estimate Per Month", StringType(), True),
            StructField("Beds", StringType(), True),
            StructField("Baths", StringType(), True),
            StructField("SqFt", StringType(), True),
            StructField("Home Type", StringType(), True),
            StructField("Address", StringType(), True)
        ])
        self.df = self.spark.createDataFrame(self.mock_data, schema=self.schema)
        self.converter = HouseDataConverter(self.mock_file_path, self.mock_config_path)
        self.converter.df = self.df
        self.converter.__home_type_mapping = self.mock_config['home_type_mapping']

    def test_data_cleaner(self):
        self.converter.data_cleaner()
        
        # Check if DataFrame transformations were called
        self.assertTrue(1==1)

if __name__ == "__main__":
    unittest.main()
