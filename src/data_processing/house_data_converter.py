import os
import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, when, col, format_number, split, trim
from pyspark.sql.types import IntegerType, FloatType

class HouseDataConverter:
    def __init__(self, file_path: str, config_path: str):
        # Initialize Spark Session instance
        self.spark = SparkSession.builder \
            .appName("ReadScraperData") \
            .getOrCreate()
        # Load home_type_mapping for encoding from config file
        with open(config_path, 'r') as config:
            self.__home_type_mapping = json.loads(config.read())['home_type_mapping']
        # find the csv file inside the directory (if it exists)
        if os.listdir(file_path):
            for filename in os.listdir(file_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(file_path, filename)
                    break
            self.df = self.spark.read.option('header', 'true').csv(file_path)

    # top-level cleaner function
    def data_cleaner(self):
        self.__remove_nulls_and_dups()
        self.__clean_price()
        self.__clean_rent_estimate()
        self.__clean_bed_and_bath()
        self.__clean_sq_ft()
        self.__clean_home_type()
        # extract features like street, city, state, zipcode from address
        self.__extract_address()
        # remove any final outliers
        self.__remove_outliers()
        # "truncate=false" to display all content of rows, and "n=df.count" to display all rows
        print(self.df.show(truncate=False, n=self.df.count()))
    
    def __remove_nulls_and_dups(self):
        self.df = self.df.dropna(how='any')
        self.df = self.df.dropDuplicates()
    
    def __clean_price(self):
        self.df = self.df.withColumn('Price', regexp_replace('Price', '[\$,]', '').cast(IntegerType()))

    def __clean_rent_estimate(self):
        self.df = self.df.withColumn('Rent Estimate Per Month', when(col('Rent Estimate Per Month') == '*Rental Value Coming Soon', None).otherwise(col('Rent Estimate Per Month')))
        self.df = self.df.withColumn('Rent Estimate Per Month', regexp_replace('Rent Estimate Per Month', '[\$,/m Estimated Rental Value]', '').cast(IntegerType()))

    def __clean_bed_and_bath(self):
        # if there is a half bed or half bath, show one decimal, if not show no decimals
        # cast to float
        self.df = self.df.withColumn('Beds', regexp_replace('Beds', ' bed', '').cast(FloatType()))
        self.df = self.df.withColumn('Baths', regexp_replace('Baths', ' bath', '').cast(FloatType()))
        # truncate to one decimal
        self.df = self.df.withColumn('Beds', format_number(col('Beds'), 1))
        self.df = self.df.withColumn('Baths', format_number(col('Baths'), 1))
        # Remove .0 for whole numbers, keep .5 baths/beds
        self.df = self.df.withColumn('Beds', regexp_replace('Beds', '\.0$', ''))
        self.df = self.df.withColumn('Baths', regexp_replace('Baths', '\.0$', ''))

    def __clean_sq_ft(self):
        self.df = self.df.withColumn('SqFt', regexp_replace('SqFt', '[\,sqft.]', '').cast(IntegerType()))

    def __clean_home_type(self):
        # Convert home_type to encoded value
        home_type_expr = col("Home Type")
        # Chain the when conditions for each key in the home type mapping
        for key, value in self.__home_type_mapping.items():
            home_type_expr = when(self.df["Home Type"] == key, value).otherwise(home_type_expr)
        # Apply the mapping expression to the Home Type column
        self.df = self.df.withColumn("Home Type", home_type_expr)

    def __extract_address(self):
        # Split by commas and create new column
        self.df = self.df.withColumn("SplitAddress", split(self.df["Address"], ","))
        # Extract city, state, zip and trim all whitespace
        self.df = self.df.withColumn("Street", trim(self.df["SplitAddress"][0])) \
            .withColumn("City", trim(self.df["SplitAddress"][1])) \
            .withColumn("State Label", trim(split(trim(self.df["SplitAddress"][2]), " ")[0])) \
            .withColumn("Zip Code", trim(split(trim(self.df["SplitAddress"][2]), " ")[1]).cast(IntegerType()))
        # Drop unnecessary address column
        self.df = self.df.drop("SplitAddress")

    def __remove_outliers(self):
        self.df = self.df.filter((self.df["Beds"] > 0) & (self.df["Baths"] > 0) & (self.df["SqFt"] >= 200))

    def __del__(self):
        self.spark.stop()

# to run the file using "python3 <relative-path-of-file> <relative-path-to-data-file>"
if __name__ == "__main__":
    hdc = HouseDataConverter(sys.argv[len(sys.argv) - 1], config_path='config/config.json')
    hdc.data_cleaner()
    # export final dataframe (completed data processing) into csv file
    # coalesce into 1 csv file (change mode based on how data to be stored)
    hdc.df.coalesce(1).write.csv(f"data/final/final_housing_data.csv", header=True, mode="overwrite")
    del hdc