# API-client
## Getting Started

### Prerequisites

- Python (version 3.9 or higher)
- pip (package installer for Python)

### Installing dependencies
`pip install -r requirements.txt`

### Env files
`create .env file and copy the contents from .env.dist`
`specify the path to the server in SERVER_API=`

### Apply migrations
`python manage.py migrate`

### Run the django development server
`python manage.py runserver (PORT)`

The Django development server will run locally, and you can access the frontend at http://localhost:(PORT).
