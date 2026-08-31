# Document Digitalization

A Flask-based web application that converts images of handwritten notes into structured digital text using Google Cloud Vision OCR. The application also extracts keywords from the recognized text and generates related search results.

## Project Preview

The repository includes example document images used to demonstrate the OCR workflow:

<p align="center">
  <img src="IMAGE_PRESENTATION/example1.jpg" alt="Example handwritten document used by the OCR application" width="45%" />
  <img src="IMAGE_PRESENTATION/random_example.jpg" alt="Second example document used by the OCR application" width="45%" />
</p>

The application takes an uploaded document image and turns it into machine-readable text, OCR confidence metrics, ranked keywords and related search results.

## Overview

The goal of this project is to make handwritten information easier to digitize, review, and explore. A user uploads an image through the web interface, and the backend processes it through an OCR and text-analysis pipeline.

The application returns:

- extracted text from the uploaded image
- OCR confidence scores at block and paragraph level
- ranked keywords identified with RAKE
- related web-search results based on the extracted keywords

## Results

The completed prototype demonstrates an end-to-end document-processing workflow rather than OCR in isolation. For each successfully processed upload, the backend:

1. extracts document text with Google Cloud Vision;
2. calculates average OCR confidence at block and paragraph level;
3. identifies and ranks meaningful phrases with RAKE;
4. uses those phrases to retrieve related search results;
5. returns the processed information to the browser as structured JSON.

This makes the project a practical example of combining a cloud AI service with NLP and a web application layer. The repository does not currently include a formal OCR benchmark dataset, so the project should be viewed as a working application prototype rather than a measured comparison of OCR accuracy.

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
├── IMAGE_PRESENTATION/    # Example document images
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

Potential improvements include stronger file-type validation, automated tests, improved frontend error handling, rate limiting for search requests, a formal OCR evaluation dataset, containerization and deployment so the application can be tested without a local setup.
