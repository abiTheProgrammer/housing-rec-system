# Housing Recommendation System

## Overview

The Housing Recommendation System is a Model designed to recommend Houses to a User based on the User's financial needs. Houses can additionally be filtered and rated to provide feedback to the model to further improve recommendations.

## Features

**User Financial Needs**: Input user financial status and expectations such as ...

**Recommendations**: House recommendations based on User needs and House features such as ...

**Feedback Loop**: Continuous improvement through user feedback and interaction to improve model behavior.

**Recommendation Filtering**: Recommend houses filtered by the user based on preferences like house location, type, bedrooms, square feet, and more.

## Steps

**1. Collect User and Housing Data from different Data Sources (Web Scrape/Real Estate Data/Housing Web App APIs)**

**2. Clean and Preprocess Data**

**3. EDA and Feature Engineering**

**4. Build Recommendation System**

## Setup

**1. Clone Github Repo**:

```sh
git clone https://github.com/abiTheProgrammer/housing-rec-system.git
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

**4. Run the script:**

```sh
python3 src/data_processing/house_scraper.py
```

## EC2 Setup

**1. Login into AWS console**

**2. Create Amazon Linux EC2 Virtual Instance. Select free tier**

**3. Create a new key pair. Download it as keypair1.pem**

**4. Connect to your EC2 instance using the pem file.**

**5. Install git using this command:**
```sh
   sudo yum update -y
   sudo yum install git -y
   git config --global user.name “Your Name”
   git config --global user.email “your_email@example.com”
```
 **6. Then, download your repository.**
 ```sh
    git clone https://github.com/abiTheProgrammer/housing-rec-system.git
```

