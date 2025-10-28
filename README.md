# HNG-project Stage 2
This is a task given to develop 6 API endpoints which process fetch data of multiple countries and cache them in a database.

### Tech Stack
These are the main technologies used:
- Python
- FastAPI
- MySQL

## Getting Started
### Prerequisites
- Python version 3.10+

### Installation
**git clone https://github.com/AOKTunbosun/HNG_tech_Stage_2**

### Installing dependencies
Run the following commands:
- **pip install pipenv**
- **pipenv install**

### Running locally
**Navigate to the database.py and comment out the DATABASE_URL with environment variable**
**Uncomment the DATABASE_URL with sqlite**
In terminal run:
**uvicorn main:app --reload --port 8000**

### Environment variables needed
*COUNTRY_DETAILS_API*
*COUNTRY_EXCHANGE_DETAILS_API*
