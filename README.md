# Healthcare Backend API

A backend system for a healthcare application built with Django, Django REST Framework (DRF), and PostgreSQL. This API allows users to register, log in securely using JWT authentication, and manage patient and doctor records with strict user-data isolation.

## 🚀 Features
* **JWT Authentication:** Secure user registration and login using `djangorestframework-simplejwt`.
* **Data Isolation:** Patients are strictly tied to the authenticated user who created them. Users cannot view, edit, or delete patients belonging to other users.
* **Doctor Management:** A shared directory of doctors that authenticated users can manage.
* **Patient-Doctor Mapping:** Securely assign doctors to patients with duplicate-assignment prevention (`unique_together` constraints).
* **Environment Configuration:** Sensitive data (Database credentials, Secret Key) are secured using `.env`.
* **Relational Database:** fully integrated with PostgreSQL.

## 🛠️ Tech Stack
* **Framework:** Django 4.1+ / Python 3
* **API:** Django REST Framework (DRF)
* **Database:** PostgreSQL (with `psycopg2-binary`)
* **Authentication:** JSON Web Tokens (JWT)
* **Environment Management:** `python-dotenv`

Local Setup Instructions
1. Prerequisites
Ensure you have the following installed on your machine:

Python 3.10+

PostgreSQL (Running locally)


2. Open your PostgreSQL CLI (psql) or pgAdmin and create an empty database:

        CREATE DATABASE healthcare_db;

3. # Create virtual environment
        python3 -m venv venv

     # Activate (Mac/Linux)
        source venv/bin/activate
     # Activate (Windows)
        venv\Scripts\activate

    # Install required packages
        pip install -r requirements.txt