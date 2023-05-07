### API Document

## Overview

This API provides functionality for uploading files and ingesting feeds. The API is built using Flask, Flask-RESTful, and Flasgger for interactive API documentation. It supports the following endpoints:

`/api/upload`: Upload a file.
`/api/ingest_feed`: Ingest a feed.


## Authentication

This API does not require authentication.

## API Endpoints

# Upload a file

URL: `/api/upload`

Method: `POST`

Description: Upload a file to the server

Parameters:

`file`: The file to be uploaded. (required)

Responses:

`200 OK`: File uploaded and read successfully.
`400 Bad Request`: No file provided.

Example Request: 

`curl -X POST -H "Content-Type: multipart/form-data" -F "file=@example.txt" http://localhost:5000/api/upload`


# Ingest a feed

URL: `/api/ingest_feed`

Method: `POST`

Description: Ingest a feed from the provided URL.

Parameters:

`feed_url`: The URL of the feed to ingest. (required)

Responses:

`200 OK`: Feed ingestion initiated. Processing in the background.
`400 Bad Request`: No feed URL provided.

Example Request

`curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "feed_url=https://example.com/feed" http://localhost:5000/api/ingest_feed`


# Interactive API Documentation

To explore the API interactively, you can visit the Flasgger-generated documentation at:

`http://localhost:5000/apidocs`

This interactive documentation allows you to view the available endpoints, their parameters, and test them directly from your browser.




