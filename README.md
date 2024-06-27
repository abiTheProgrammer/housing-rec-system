# Housing Recommendation System

## Overview

The Housing Recommendation System is a Model designed to recommend Houses to a User based on the User's financial needs. Houses can additionally be filtered and rated to provide feedback to the model to further improve recommendations.

## Features

**User Financial Needs**: Input user financial status and expectations such as ...

**Recommendations**: House recommendations based on User needs and House features such as location, price, rent estimate, and more.

**Feedback Loop**: Continuous improvement through user feedback and interaction to improve model behavior.

**Recommendation Filtering**: Recommend houses filtered by the user based on preferences like house location, type, bedrooms, square feet, and more.

## Steps

**1. Web Scrape Housing Data from https://www.mls.com/**

    1. Extract Links for Each State:
            For each of the 50 states, extract the URLs that link to the state's
            housing information. This includes categories like cities, rural
            areas, and foreclosures.

    2. Extract Links for Each Category within Each State:
            For each state, navigate to the categories: cities, rural areas
            (if present), and foreclosures. Extract the URLs that link to
            these categories.

    3. Extract Links for Each Location within Each Category:
            Within each category, there are different locations (e.g., cities,
            towns) where homes are listed for sale. Extract the URLs for these locations.

    4. Extract Housing Listings from Each Location:
            Navigate to each location's URL and scrape the house listings.
            For each house listing, extract relevant information such as:
            - Price
            - Address
            - Number of bedrooms
            - Number of bathrooms
            - Square feet
            - Type of House (Single, Mobile, Condo, etc)

    5. Store Data:
            Convert each listing into a dataframe row. Append row to final dataframe.
            Export dataframe with raw scraped data as csv file to further preprocess data
            and conduct EDA. (Update with cloud storage solution)

**2. Exploratory Data Analysis (EDA)**

Conduct preliminary analysis on data points in jupyter notebooks before deciding on
what criteria to filter on. Rigorously test on inputs and datafiles and check if
outputs match. Examine features like SqFt, Address, Rent Estimate, and more.
Identify patterns in data, new features to be engineered and define criteria to
filter.

**3. Clean, Preprocess Data, and Feature Engineering**

    1. Clean and Preprocess Data:
            Remove Duplicates, NULL values. Convert Price to INT and Rent Estimate to INT.
            If no Rental Value hasn't been updated, store as NULL. Convert Beds, Baths to FLOAT
            and SqFt to INT. Convert Home Type values to encoded values in config file.

    2. Feature Extract Data:
            Extract Street, City, State Label, Zip Code from Address.

    3. Final Cleanup:
            Remove any final outliers.

    4. Export Data:
            Export final cleaned dataframe as csv file. (Update with cloud storage solution)

**4. Build Recommendation System**

    1. Add Rating column to dataset:
        Rating of House Listing determines strength of recommendation.
        Quantifiable column to recommend houses to users after filtering for prices, and more.

    2. Recommendation Apprach:
        a. Collaborative-based Filtering:
                User 1 likes Houses A, B, C.
                User 2 likes Houses A, B, D.
                User 1 may like D and User 2 may like C.
        b. Content-based Filtering:
                User X likes House A.
                House E has similar content as A.
                User X may like House E as well.
        c. Hybrid (a + b)

    3. User Generated Feedback:
        Liking/Disliking a house listing changes its rating.
        This enhances the recommendation algorithm by re-training on updated ratings,
        improving its accuracy.

## Setup

**1. Clone Github Repo**:

```sh
git clone <URL>
cd housing-rec-system
```

**2. Create and Activate Virtual Enviornment**:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Dependencies**:

```sh
pip install -r requirements.txt
```

- If JRE (Java Runtime Environment) not present, download from https://www.oracle.com/java/technologies/downloads/ (Required for PySpark)

**4. Run Program**:

(Update with script that runs the Data Pipeline)

**Data Pipeline**

- Populate raw csv file with data from website:

```sh
python3 src/data_processing/house_scraper.py
```

- Clean and convert raw scraped csv file to exportable dataset:

```sh
python3 src/data_processing/house_data_converter.py data/uncleaned/data_all_states.csv
```

## EC2 Setup

**1. Login to AWS console**

**2. Create Amazon Linux EC2 Virtual Instance. Select free tier**

**3. Create a new key pair. Download it as keypair1.pem**

**4. Connect to your EC2 instance using the pem file.**

**5. Install git using these commands:**

```sh
   sudo yum update -y
   sudo yum install git -y
   git config --global user.name “Your Name”
   git config --global user.email “your_email@example.com”
```

**6. Then, clone git repository.**

```sh
   git clone <URL>
```

## Running tests

```sh
python -m unittest discover -s tests -p "*.py"
```

## High Level Workflow Diagram

![Flowchart](docs/Workflow%20Diagram.png)

## Other Qustions/Comments/Ideas:

    Q1. When do we add the rating column and with what initial values?
    Q2. How do we store the data and what cloud service to use? Where are venv dependencies stored?
    Q3. Create a script to run the Data Pipeline?
