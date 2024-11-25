# Chatbot Project

## Project Overview

This project is a **web-based chatbot** developed using **Django**, which integrates with **Dialogflow** and uses **spaCy** for Natural Language Processing (NLP). The chatbot is designed to answer user queries about companies stored in a **MySQL** database. The web interface is built using **HTML**, **CSS**, and **JavaScript**.

## Project Structure

The project is structured as follows:
- **Django Project Name**: `chatbot_project`
- **App Name**: `chatbot`

### Files & Folders:
- `chatbot_project/`: The main Django project directory.
- `chatbot/`: The app directory containing the views, URLs, models, etc.
- `chatbot/static/`: Contains the CSS and JavaScript files for the web interface.
- `chatbot/templates/`: Contains the HTML files for the web interface.
- `chatbot/chatbot_logic.py`: This file contains the logic for handling user queries and integrating with Dialogflow and spaCy.

## Detailed Explanation

### 1. **Views.py** (in `chatbot` app)

The `views.py` file in the `chatbot` app handles incoming HTTP requests and responses. It processes the requests from the user and displays the chatbot interface. The views are responsible for:
- Rendering the chatbot interface in the browser.
- Processing user input and calling the chatbot logic for generating responses.

**Synonyms for Entities**:
Instead of relying strictly on predefined entities, you can use **synonyms**. For example, if a user queries about 'Microcontrollers', the bot could understand 'Microchips', 'Embedded Controllers', etc., as synonyms and still retrieve accurate results.
  
### 2. **Urls.py** (in `chatbot` app)

The `urls.py` file maps URLs to the views in your app. It handles the routing of requests and directs them to the appropriate view functions. For example:
- **Home URL**: This renders the main page where the user can interact with the chatbot.

### 3. **Chatbot Logic (chatbot_logic.py)**

The `chatbot_logic.py` file contains the core logic for the chatbot. It integrates with:
- **Dialogflow** for understanding user queries and detecting intents.
- **spaCy** for natural language processing, extracting entities (such as company names and locations), and handling fallback scenarios.
  
In this file, we connect to Dialogflow's API to detect the intent of the user's query and use spaCy for additional processing when necessary. It interacts with the **MySQL** database to provide relevant data about companies based on user queries. The queries include asking about companies from specific industries, locations, or products.

# Electronica Data Database Setup

This document provides details about the MySQL database used in the project.

## Database Information
- **Database Name**: `electronica_data`
- **Table Name**: `companies`

## Table Schema
The `companies` table contains information about various companies and their details. Below is the schema for the `companies` table:

| Column Name       | Data Type        | Description                                      |
|--------------------|------------------|--------------------------------------------------|
| `id`              | INT (Primary Key, Auto Increment) | Unique identifier for each company.            |
| `company_name`    | VARCHAR(500)     | Name of the company.                            |
| `industry_category` | VARCHAR(1000)  | Industry category of the company.               |
| `address`         | VARCHAR(500)     | Address of the company.                         |
| `email`           | VARCHAR(500)     | Email address of the company.                   |
| `phone`           | VARCHAR(500)     | Phone number of the company.                    |
| `website`         | VARCHAR(500)     | Official website URL of the company.            |
| `linkedin`        | VARCHAR(500)     | LinkedIn profile URL of the company.            |
| `youtube`         | VARCHAR(500)     | YouTube channel URL of the company.             |
| `instagram`       | VARCHAR(500)     | Instagram profile URL of the company.           |
| `facebook`        | VARCHAR(500)     | Facebook page URL of the company.               |
| `twitter`         | VARCHAR(500)     | Twitter profile URL of the company.             |
| `products_services` | TEXT           | Description of the products and services offered by the company. |
| `company_profile` | TEXT             | Detailed profile of the company.                |

## my database file
 file name: 727_companies_database.sql

## Sample Outputs

Here are some example interactions with the chatbot:

### 1. **Query**: How many companies are listed under the 'Semiconductors' industry?

**Bot**: There are 263 companies in the 'Semiconductors' industry.

### 2. **Query**: List all companies that manufacture 'Microcontrollers'.

**Bot**: Companies manufacturing 'Microcontrollers': IC-Direct GmbH, ABOV Semiconductor etc .....

### 3. **Query**: Provide the contact details of companies located in 'Germany'.

**Bot**:  Company Name: IC-Direct GmbH Address: Max-Planck-Strasse 12, 81675 München, Germany Email: sales@ic-direct.com Phone: 0049 89 4142419-0 Website: https://www.ic-direct.com/

Company Name: 3M Deutschland GmbH Address: Carl-Schurz-Str. 1, 41453 Neuss, Germany Email: Nill Phone: 0049 2131 140 Website: http://www.3mdeutschland.de/3M/de_DE/elektronik-de/

Company Name: ACCRETECH (Europe) GmbH Address: Landsberger Str. 396, 81241 München, Germany Email: info@accretech.eu Phone: 0049 89 250064-200 Website: http://www.accretech.eu/

etc....



## Running the Project

Follow the steps below to set up and run the chatbot project locally:

1. **Open Terminal**: Start the terminal or command prompt.
   
2. **Navigate to Project Directory**:
   ```bash
   cd chatbot_project
3. ## setup virtual environment 
    python -m venv venv
    # On Windows
    venv\Scripts\activate
4. ## Install Dependencies:
    pip install -r requirements.txt

5. ## Apply Migrations:
    python manage.py migrate

6. ## Run Server:
    python manage.py runserver