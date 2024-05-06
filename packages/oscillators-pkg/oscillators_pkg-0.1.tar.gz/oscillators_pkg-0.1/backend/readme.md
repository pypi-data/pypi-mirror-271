Django Application Setup Guide
==============================

Local Setup
-----------

### Prerequisites

Before you begin, make sure you have the following installed:

*   Python (3.6 or higher)
*   pip (Python package manager)
*   virtualenv (optional but recommended)

### Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/Pradeep-Kumar-Rebbavarapu/CS-208-PROJECT-ODE-GRAPHER
    ```

3.  Navigate to the project directory:
    ```bash
    cd backend
    ```

4.  Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```

5.  Activate Virtual Environment:
    ```bash
    venv\Scripts\activate
    ```

6.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

7.  Run the development server:
    ```bash
    python manage.py runserver
    ```

8.  Open your browser and navigate to [http://localhost:8000](http://localhost:8000) to view the application.

Docker Setup
------------

### Prerequisites

Before you begin, make sure you have Docker installed on your system.

### Installation

1.  Build the Docker image:

    docker build -t django-app .

3.  Run the Docker container:

    docker run -p 8000:8000 django-app

5.  Open your browser and navigate to [http://localhost:8000](http://localhost:8000) to view the application.

Additional Resources
--------------------

*   [Django Documentation](https://docs.djangoproject.com/en/stable/)
*   [Docker Documentation](https://docs.docker.com/)