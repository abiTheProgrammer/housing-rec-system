# Import relative modules
import os
import seaborn as sns
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, split, trim, when
from pyspark.sql.types import IntegerType

# Initialize Spark session
spark = SparkSession.builder.appName("EDA").getOrCreate()

# Go back a directory to access src
os.chdir("..")

from src.data_processing.house_data_converter import HouseDataConverter

hdc = HouseDataConverter("data/raw/Rhode-Island_hd.csv")
df = hdc.df
df.show()

# Start EDA using Spark DataFrame

# Drop duplicates
dropped_df = df.dropDuplicates()
dropped_df.show()

# Drop NA
dropped_df = dropped_df.dropna()
dropped_df.show()

dropped_df.select("Price").distinct().show()

# all the unique values in the 'Address' column
dropped_df.select("Address").distinct().show()

# all the unique values in the 'Rent Estimate' column
dropped_df.select("Rent Estimate").distinct().show()

# all the rows that have the value '*Rental Value Coming Soon' in 'Rent Estimate'
dropped_df.filter(dropped_df["Rent Estimate"] == "*Rental Value Coming Soon").show()

# all the unique values in the 'Beds' column
dropped_df.select("Beds").distinct().show()

# all the unique values in the 'Baths' column
dropped_df.select("Baths").distinct().show()

# all the unique values in the 'Sq. Ft' column
dropped_df.select("Sq. Ft").distinct().show()

# all the rows that have the value '0 sqft.' in 'Sq. Ft'
dropped_df.filter(dropped_df["Sq. Ft"] == "0 sqft.").show()

# all the unique values in the 'Home Type' column
dropped_df.select("Home Type").distinct().show()

# dropping all the rows that have either a 'Rent Estimate' value of '*Rental Value Coming Soon' or a 'Sq. Ft' value of '0 sqft.'
dropped_df = dropped_df.filter((dropped_df["Rent Estimate"] != "*Rental Value Coming Soon") & (dropped_df["Sq. Ft"] != "0 sqft."))
dropped_df.show()

def clean_and_convert(df):
    # remove the dollar sign and commas out from all 'Price' values
    # eg: '$360,675' becomes '360675'
    df = df.withColumn('Price', regexp_replace('Price', '[\$,]', '').cast(IntegerType()))
    # remove 'sqft.' and comma from 'Sq. Ft' values
    df = df.withColumn('Sq. Ft', regexp_replace('Sq. Ft', '[\,sqft.]', '').cast(IntegerType()))
    return df

# Apply the function to clean and convert the DataFrame
dropped_df = clean_and_convert(dropped_df)
dropped_df.show()

def extract_address(df):
    # Step 1: Split by commas
    split_df = split(dropped_df["Address"], ",")
    # Step 2: Trim whitespace from split parts
    split_df = [trim(c) for c in split_df]
    # Step 3: Split the third part (state and zip code) by space
    state_zip_split = split(split_df[2], " ")
    # Assign the parts to new columns
    df = df.withColumn("Street", split_df[0]) \
           .withColumn("City", split_df[1]) \
           .withColumn("State Label", state_zip_split[0]) \
           .withColumn("Zip Code", state_zip_split[1].cast(IntegerType()))
    # Drop the original Address column if no longer needed
    df = df.drop("Address")
    return df

dropped_df = extract_address(dropped_df)
dropped_df.show()

# all the unique 'Home Type' values shortened for simplicity
home_type_mapping = {
    'Single-Family': 'SF',
    'Multi-Family': 'MF',
    'Condo': 'CON',
    'Mobile Home': 'MH',
    'Commercial': 'COMM'
}

# Apply the mapping to the "Home Type" column
home_type_expr = when(dropped_df["Home Type"] == "Single-Family", "SF") \
    .when(dropped_df["Home Type"] == "Multi-Family", "MF") \
    .when(dropped_df["Home Type"] == "Condo", "CON") \
    .when(dropped_df["Home Type"] == "Mobile Home", "MH") \
    .when(dropped_df["Home Type"] == "Commercial", "COMM")

dropped_df = dropped_df.withColumn("Home Type", home_type_expr)
dropped_df.show()

# making a boxplot for the 'Price' column to check for any outliers
pandas_df = dropped_df.toPandas()
sns.boxplot(x=pandas_df["Price"])
plt.title("Price")
plt.show()

def drop_outliers(df):
    # 0 beds is an outlier
    df = df.filter(df["Beds"] > 0)
    # 0 baths is an outlier
    df = df.filter(df["Baths"] > 0)
    # anything less than 200 sq. ft is an outlier
    df = df.filter(df["Sq. Ft"] >= 200)
    return df

dropped_df = drop_outliers(dropped_df)
dropped_df.show()
