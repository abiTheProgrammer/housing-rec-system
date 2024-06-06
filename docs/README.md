# Housing Recommendation System

## Overview

The Housing Recommendation System is a Model designed to recommend Houses to a User based on the User's financial needs. Houses can additionally be filtered and rated to provide feedback to the model to further improve recommendations.

## Features

**User Financial Needs**: Input user financial status and expectations such as ...

**Recommendations**: House recommendations based on User needs and House features such as ...

**Feedback Loop**: Continuous improvement through user feedback and interaction to improve model behavior.

**Recommendation Filtering**: Recommend houses filtered by the user based on preferences like house location, type, bedrooms, square feet, and more.

## Steps

**1. Web Scrape Housing Data from https://www.mls.com/**

    1. Extract Links for Each State:
            For each of the 50 states, extract the URLs that link to the state's
            housing information. This includes categories like cities, rural
            areas, and foreclosures. **

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
            Store the housing data somewhere.

**2. Clean and Preprocess Data**

**3. EDA and Feature Engineering**

**4. Build Recommendation System**

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

**4. Run the script**:

```sh
python3 src/data_processing/house_scraper.py
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
