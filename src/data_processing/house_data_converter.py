import os
import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, when, col, format_number, split, trim
from pyspark.sql.types import IntegerType, FloatType

class HouseDataConverter:
    """
    A class to handle the conversion and cleaning of house data.
    """
    def __init__(self, file_path: str, config_path: str):
        """
        Initializes the HouseDataConverter with the specified file and config paths.
        
        Args:
            file_path (str): The path to the directory containing the CSV file.
            config_path (str): The path to the configuration JSON file.
        """
        # Initialize Spark Session instance
        self.spark = SparkSession.builder \
            .appName("ReadScraperData") \
            .getOrCreate()
        # Load home_type_mapping for encoding from config file
        with open(config_path, 'r') as config:
            # self.__home_type_mapping = json.loads(config.read())['home_type_mapping']
            config_data = json.loads(config.read())
            self.__home_type_mapping = config_data['home_type_mapping']
            self.__rental_value_coming_soon = config_data['constants']['RENTAL_VALUE_COMING_SOON']
        
        # find the csv file inside the directory (if it exists)
        if os.listdir(file_path):
            for filename in os.listdir(file_path):
                if filename.endswith(".csv"):
                    file_path = os.path.join(file_path, filename)
                    break
            self.df = self.spark.read.option('header', 'true').csv(file_path)

    # top-level cleaner function
    def data_cleaner(self):
        """
        Cleans the house data by performing various transformations.
        Prints the data frame after all transformations are done.
        """
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
        """
        Drops any missing or duplicated data from the data frame.

        Returns:
            None: The function modifies the DataFrame in place.
        """
        self.df = self.df.dropna(how='any')
        self.df = self.df.dropDuplicates()
    
    def __clean_price(self):
        """
        Cleans the 'Price' column in the DataFrame.

        - Removes the dollar sign ('$') and commas (',') from the 'Price' column.
        - Casts the values to integer.

        Returns:
            None: The function modifies the DataFrame in place.
        """
        self.df = self.df.withColumn('Price', regexp_replace('Price', '[\$,]', '').cast(IntegerType()))

    def __clean_rent_estimate(self):
        """
        Cleans the 'Rent Estimate Per Month' column in the DataFrame.

        - Replaces the placeholder '*Rental Value Coming Soon' with None.
        - Removes dollar signs ('$'), commas (','), '/m', and 'Estimated Rental Value' from the 'Rent Estimate Per Month' column.
        - Casts the cleaned values to integer.

        Returns:
            None: The function modifies the DataFrame in place.
        """
        # self.df = self.df.withColumn('Rent Estimate Per Month', when(col('Rent Estimate Per Month') == '*Rental Value Coming Soon', None).otherwise(col('Rent Estimate Per Month')))
        self.df = self.df.withColumn('Rent Estimate Per Month', when(col(self.df_columns[2]) == self.__rental_value_coming_soon, None).otherwise(col(self.df_columns[2])))
        self.df = self.df.withColumn('Rent Estimate Per Month', regexp_replace('Rent Estimate Per Month', '[\$,/m Estimated Rental Value]', '').cast(IntegerType()))

    def __clean_bed_and_bath(self):
        """
        Cleans the 'Beds' and 'Baths' columns in the DataFrame.

        - Removes the text ' bed' and ' bath' from the 'Beds' and 'Baths' columns, respectively.
        - Casts the values to float.
        - Truncates the values to one decimal place.
        - Removes the trailing '.0' for whole numbers, retaining the '.5' for half beds or baths.

        Returns:
            None: The function modifies the DataFrame in place.
        """
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
        """
        Cleans the 'SqFt' column in the DataFrame.

        - Removes commas (','), 'sqft', and periods ('.') from the 'SqFt' column.
        - Casts the values to integer.

        Returns:
            None: The function modifies the DataFrame in place.
        """
        self.df = self.df.withColumn('SqFt', regexp_replace('SqFt', '[\,sqft.]', '').cast(IntegerType()))

    def __clean_home_type(self):
        """
        Cleans and encodes the 'Home Type' column in the DataFrame based on a predefined mapping.

        The home type mapping is as follows:
            - "Single-Family": "SF"
            - "Multi-Family": "MF"
            - "Condo": "CONDO"
            - "Mobile Home": "MH"
            - "Commercial": "COMM"

        - Converts the 'Home Type' column to encoded values according to the mapping.

        Returns:
            None: The function modifies the DataFrame in place.
        """
        # Convert home_type to encoded value
        home_type_expr = col("Home Type")
        # Chain the when conditions for each key in the home type mapping
        for key, value in self.__home_type_mapping.items():
            home_type_expr = when(self.df["Home Type"] == key, value).otherwise(home_type_expr)
        # Apply the mapping expression to the Home Type column
        self.df = self.df.withColumn("Home Type", home_type_expr)

    def __extract_address(self):
        """
        Extracts components of the 'Address' column into separate columns.

        - Splits the 'Address' column by commas into a list of address components.
        - Extracts and trims the street, city, state, and zip code from the split address.
        - Creates new columns: 'Street', 'City', 'State Label', and 'Zip Code'.
        - Drops the intermediate 'SplitAddress' column.

        Returns:
            None: The function modifies the DataFrame in place.
        """
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
        """
        Removes outliers from the DataFrame based on predefined criteria.

        - Filters out rows where the number of beds is less than or equal to 0.
        - Filters out rows where the number of baths is less than or equal to 0.
        - Filters out rows where the square footage ('SqFt') is less than 200.

        Returns:
            None: The function modifies the DataFrame in place.
        """
        self.df = self.df.filter((self.df["Beds"] > 0) & (self.df["Baths"] > 0) & (self.df["SqFt"] >= 200))

    def __del__(self):
        """
        Stops the SparkSession instance.
        """
        self.spark.stop()

# to run the file using "python3 <relative-path-of-file> <relative-path-to-data-file>"
if __name__ == "__main__":
    hdc = HouseDataConverter(sys.argv[len(sys.argv) - 1], config_path='config/config.json')
    hdc.data_cleaner()
    # export final dataframe (completed data processing) into csv file
    # coalesce into 1 csv file (change mode based on how data to be stored)
    hdc.df.coalesce(1).write.csv(f"data/final/final_housing_data.csv", header=True, mode="overwrite")
    del hdc