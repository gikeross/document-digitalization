# Document Digitalization

A Flask-based web application that converts images of handwritten notes into structured digital text using Google Cloud Vision OCR. The application also extracts keywords from the recognized text and generates related search results.

## Overview

The goal of this project is to make handwritten information easier to digitize, review, and explore. A user uploads an image through the web interface, and the backend processes it through an OCR and text-analysis pipeline.

The application returns:

- extracted text from the uploaded image
- OCR confidence scores at block and paragraph level
- ranked keywords identified with RAKE
- related web-search results based on the extracted keywords

## Tech Stack

- **Python** — application logic and text-processing pipeline
- **Flask** — web application and API endpoints
- **Google Cloud Vision** — document text detection / OCR
- **RAKE-NLTK** — keyword extraction
- **googlesearch** — related search-result retrieval
- **HTML / CSS / JavaScript** — user interface

## How It Works

1. The user uploads an image containing handwritten or printed notes.
2. Flask stores the upload in a temporary file.
3. Google Cloud Vision performs document text detection.
4. The application calculates average OCR confidence scores.
5. RAKE extracts and ranks relevant phrases from the recognized text.
6. The extracted keywords are used to retrieve related search results.
7. The temporary upload is removed after processing.
8. The processed information is returned to the frontend as JSON.

## Project Structure

```text
document-digitalization/
├── model.py               # Flask backend, OCR and keyword-processing logic
├── requirements.txt       # Python dependencies
├── .gitignore             # Local, environment and credential exclusions
├── templates/             # HTML templates
├── static/                # Frontend assets and styling
├── IMAGE_PRESENTATION/    # Presentation assets
├── FINAL_project.pptx     # Project presentation
└── README.md
```

## Running the Project Locally

Clone the repository and create an isolated environment:

```bash
git clone https://github.com/gikeross/document-digitalization.git
cd document-digitalization
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Google Cloud Vision requires authentication. Keep the service-account JSON file outside the repository and set its path in your shell:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
```

Then start the Flask application:

```bash
python model.py
```

Open the local Flask address shown in the terminal and upload an image for processing.

To enable Flask debug mode during local development only:

```bash
export FLASK_DEBUG=true
python model.py
```

## Security and Repository Hygiene

Credentials are not stored in source code. Local environment files, virtual environments, macOS metadata and common credential filenames are excluded through `.gitignore`.

If a service-account key has ever been committed to Git history, removing the file from the current branch is not enough: revoke that key in Google Cloud and create a new one.

## Skills Demonstrated

This project combines several parts of an end-to-end data application: API integration, OCR, natural-language processing, backend development, temporary file handling, secure configuration and frontend/backend communication.

## Future Improvements

Potential improvements include stronger file-type validation, automated tests, improved frontend error handling, rate limiting for search requests, containerization and deployment so the application can be tested without a local setup.
