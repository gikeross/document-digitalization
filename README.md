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

1. validates the uploaded image type and enforces an 8 MB size limit;
2. extracts document text with Google Cloud Vision;
3. calculates average OCR confidence at block and paragraph level;
4. identifies and ranks meaningful phrases with RAKE;
5. uses those phrases to retrieve related search results;
6. returns the processed information to the browser as structured JSON.

The API now distinguishes common failure cases such as missing uploads, unsupported image types, files that are too large, images with no detected text, OCR-provider failures and unexpected server errors.

This makes the project a practical example of combining a cloud AI service with NLP and a web application layer. The repository does not currently include a formal OCR benchmark dataset, so the project should be viewed as a working application prototype rather than a measured comparison of OCR accuracy.

## Reliability and Testing

The repository includes automated Flask API tests under `tests/`. They cover:

- missing-file validation
- unsupported file extensions
- invalid MIME types
- successful OCR-response formatting using mocks
- no-text responses
- OCR-provider failure handling

A GitHub Actions workflow runs the test suite automatically on relevant pushes and pull requests.

Run the tests locally with:

```bash
pytest -q
```

## Tech Stack

- **Python** — application logic and text-processing pipeline
- **Flask** — web application and API endpoints
- **Google Cloud Vision** — document text detection / OCR
- **RAKE-NLTK** — keyword extraction
- **googlesearch** — related search-result retrieval
- **pytest** — automated API testing
- **GitHub Actions** — continuous integration
- **HTML / CSS / JavaScript** — user interface

## How It Works

1. The user uploads a PNG, JPG/JPEG, or WEBP image.
2. Flask validates the filename, MIME type and maximum request size.
3. The upload is stored in a temporary file.
4. Google Cloud Vision performs document text detection.
5. The application calculates average OCR confidence scores.
6. RAKE extracts and ranks relevant phrases from the recognized text.
7. The extracted keywords are used to retrieve related search results.
8. The temporary upload is removed after processing.
9. The processed information is returned to the frontend as JSON.

## Project Structure

```text
document-digitalization/
├── model.py               # Flask backend, validation, OCR and NLP logic
├── requirements.txt       # Python and test dependencies
├── tests/                 # Flask API tests
├── .github/workflows/     # Continuous-integration workflow
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

This project combines several parts of an end-to-end data application: API integration, OCR, natural-language processing, backend development, input validation, automated testing, continuous integration, temporary file handling, secure configuration and frontend/backend communication.

## Future Improvements

The next useful improvements would be client-side validation and clearer frontend error messages, rate limiting for search requests, a formal OCR evaluation dataset, containerization and deployment so the application can be tested without a local setup.
