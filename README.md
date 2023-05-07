# EC530_Final_Project

# Email: zhangta6@bu.edu

## Intro
This is the repository of EC530 Final Project, The application features Google OAuth2 authentication, file uploading and reading, feed ingestion, and processing. 

## Architecture

The project has the following structure:


.
├── app.py                     # Flask API and routes

├── api/

│   ├── __init__.py
│   ├── upload_api.py          # Upload file API endpoint
│   ├── ingest_feed_api.py     # Ingest feed API endpoint
│   └── analyzer.py            # Document and feed analyzer

├── gui.py                     # PyQt5-based GUI

├── templates/
│   ├── login.html             # Login template
│   └── register.html          # Registration template

├── static/
│   └── css/                   # Stylesheets

├── tests/
│   └── test_app.py            # Unit tests for app.py

├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies

## Main Components
`app.py`: Contains the Flask API and routes, serving as the main entry point for the application.

`api/`: Contains the API endpoints and the document/feed analyzer.
upload_api.py: Implements the file upload API endpoint.

`ingest_feed_api.py`: Implements the feed ingestion API endpoint.
analyzer.py: Provides functionality for analyzing uploaded documents and ingested feeds.

`gui.py`: Implements a PyQt5-based graphical user interface for the application.

`templates/`: Contains the HTML templates for the login and registration pages.

`static/`: Contains static files, such as stylesheets.

`tests/`: Contains unit tests for the application.
test_app.py: Unit tests for app.py.

## User Story
- As a user, I want to be able to log in using my Gmail account so that I can access my saved data.

- As a user, I want to be able to upload a document so that I can analyze its contents.

- As a developer, I want to have clear and comprehensive documentation for each component of the system so that I can easily maintain and extend the system.

- As a developer, I want to have error messages and logging in place so that I can easily debug the system in case of any issues.


## Prerequist 
- Python 3.8+
- Redis
- (optional)pip3

## Installation

### Steps
1. Clone the repository:

    `git clone https://github.com/cesdium2011/EC530_Final_Project.git`

2. Change the current directory to the project folder:

    `cd /your-directory/EC530_Final_Project`

3. Create a virtual environment and activate it:

    `python -m venv venv`

    `source venv/bin/activate` 
    
    On Windows, use `venv\Scripts\activate`

4. Install the required packages:

    `pip install -r requirement.txt`

5. Configure the environment variables for the Google OAuth2 client ID and secret:

    MacOS:

    `export GOOGLE_OAUTH2_CLIENT_ID="your_client_id.apps.googleusercontent.com"`

    `export GOOGLE_OAUTH2_CLIENT_SECRET="your_client_secret"`

    Windows: 

    `set GOOGLE_OAUTH2_CLIENT_ID="your_client_id.apps.googleusercontent.com"`

    `set GOOGLE_OAUTH2_CLIENT_SECRET="your_client_secret"`





## Usage

1. Start the Redis server.

2. Run the Flask application:

    `python app.py`

3. In a separate terminal, run the Celery worker:

    `celery -A app.celery worker --loglevel=info`

4. In another terminal, run the PyQt5 GUI:

    `python gui.py`

5. Open your browser and navigate to http://localhost:5000 to access the web application.


## Contributing
We welcome contributions to this project. If you're interested in contributing, please follow these steps:

1. Fork the repository.
2. Create a branch with a descriptive name, e.g., add-new-feature.
3. Implement your changes and commit them to your branch.
4. Push your changes to your forked repository.
5. Open a pull request describing the changes you've made.

### License 
This project is licensed under the MIT License. See the LICENSE file for more details.