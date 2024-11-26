# README

## Project Overview

This project is developed by Nicolà Bertolazzi (I4AA) for the Flask laboratory.

Please note that this is an unfinished application. The project will continue to be developed individually throughout the remainder of the semester, and the current version is not yet complete.


## Description

This application manages data for the NBA.  

---

## Requirements

To run the application and import data, the following are required:

- **Python**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Pip**: Python's package installer, which comes pre-installed with Python. Ensure it's updated by running:
  ```bash
  python -m pip install --upgrade pip
  ```
- **MongoDB**: A NoSQL database to store application data. You can download and install it from the [MongoDB website](https://www.mongodb.com/try/download/community). Alternatively, you can use **MongoDB Atlas** for a cloud-based solution.


---

## Folder Structure

### `/app`
The main application folder, containing the core of the Flask project:
- **`configs/`**: Configuration files for the application (e.g., database, app settings).
- **`routes/`**: Flask route definitions for handling application endpoints.
- **`services/`**: Logic and services that support the application.
- **`static/`**: Static files (e.g., CSS, JavaScript, assets).
- **`templates/`**: HTML templates for the Flask application.
- **`validators/`**: Input validation utilities for forms and APIs.
- **`__init__.py`**: Application setup and initialization.

### `/data`
Contains datasets to populate the **MongoDB database**.

### `/extra`
Contains data, scripts, or other files used for testing and experimentation. 
This folder is **not essential** for the application to run.

### `/tests`
In the `tests` directory, you can find the tests created using Selenium, along with a subfolder containing the necessary setup to execute them using Python.

---

## Configuration

- **`.env`**: Stores sensitive data such as database credentials and environment variables.  
- **`configs/`**: Houses configuration settings for the application.

**Important Note: Teams Logos Storage Path**  
The path for saving the **teams-logo** is specified in the `.env` file. Please be aware that this location is temporary and will be changed once a NAS or cloud storage solution is available. Make sure to check the `.env` for the current path configuration.

--- 

## How to Run

To run the application, follow these steps:

1. Create the virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - On **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

---