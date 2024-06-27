import unittest
from unittest.mock import patch, mock_open
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from src.data_processing.house_data_converter import HouseDataConverter  # Adjusted import

class TestHouseDataConverter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local[1]").appName("TestHouseDataConverter").getOrCreate()
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
        self.mock_file_path = 'mock_file_path'
        self.mock_config_path = 'mock_config_path'
        self.mock_data = [
            ("$500,000", "$3,000/mo", "3 beds", "2 baths", "2,000 sqft", "Single Family", "123 Main St, City, ST 12345"),
            ("$250,000", "$1,500/mo", "2 beds", "1 bath", "1,000 sqft", "Condo", "456 Elm St, Town, TS 67890")
        ]
        self.schema = StructType([
            StructField("Price", StringType(), True),
            StructField("Rent Estimate", StringType(), True),
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

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_remove_nulls_and_dups(self, mock_file):
        self.converter.__remove_nulls_and_dups()
        self.assertEqual(self.converter.df.count(), 2)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_clean_price(self, mock_file):
        self.converter.__clean_price()
        expected_data = [(500000,), (250000,)]
        expected_schema = StructType([StructField("Price", IntegerType(), True)])
        expected_df = self.spark.createDataFrame(expected_data, schema=expected_schema)
        self.assertEqual(self.converter.df.select("Price").collect(), expected_df.collect())

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_clean_rent_estimate(self, mock_file):
        self.converter.__clean_rent_estimate()
        expected_data = [(3000.0,), (1500.0,)]
        expected_schema = StructType([StructField("Rent Estimate", FloatType(), True)])
        expected_df = self.spark.createDataFrame(expected_data, schema=expected_schema)
        self.assertEqual(self.converter.df.select("Rent Estimate").collect(), expected_df.collect())

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_clean_bed_and_bath(self, mock_file):
        self.converter.__clean_bed_and_bath()
        expected_data = [(3, 2), (2, 1)]
        expected_schema = StructType([
            StructField("Beds", IntegerType(), True),
            StructField("Baths", IntegerType(), True)
        ])
        expected_df = self.spark.createDataFrame(expected_data, schema=expected_schema)
        self.assertEqual(self.converter.df.select("Beds", "Baths").collect(), expected_df.collect())

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_clean_sq_ft(self, mock_file):
        self.converter.__clean_sq_ft()
        expected_data = [(2000,), (1000,)]
        expected_schema = StructType([StructField("SqFt", IntegerType(), True)])
        expected_df = self.spark.createDataFrame(expected_data, schema=expected_schema)
        self.assertEqual(self.converter.df.select("SqFt").collect(), expected_df.collect())

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_clean_home_type(self, mock_file):
        self.converter.__clean_home_type()
        expected_data = [(1,), (2,)]
        expected_schema = StructType([StructField("Home Type", IntegerType(), True)])
        expected_df = self.spark.createDataFrame(expected_data, schema=expected_schema)
        self.assertEqual(self.converter.df.select("Home Type").collect(), expected_df.collect())

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_extract_address(self, mock_file):
        self.converter.__extract_address()
        expected_data = [("123 Main St", "City", "ST", 12345), ("456 Elm St", "Town", "TS", 67890)]
        expected_schema = StructType([
            StructField("Street", StringType(), True),
            StructField("City", StringType(), True),
            StructField("State Label", StringType(), True),
            StructField("Zip Code", IntegerType(), True)
        ])
        expected_df = self.spark.createDataFrame(expected_data, schema=expected_schema)
        self.assertEqual(self.converter.df.select("Street", "City", "State Label", "Zip Code").collect(), expected_df.collect())

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
        'home_type_mapping': {
            'Single Family': 1, 'Condo': 2, 'Townhouse': 3, 'Multi Family': 4
        }
    }))
    def test_remove_outliers(self, mock_file):
        self.converter.__remove_outliers()
        self.assertEqual(self.converter.df.count(), 2)

if __name__ == "__main__":
    unittest.main()
