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
- **HTML / CSS** — user interface

## How It Works

1. The user uploads an image containing handwritten or printed notes.
2. Flask temporarily stores the uploaded file.
3. Google Cloud Vision performs document text detection.
4. The application calculates average OCR confidence scores.
5. RAKE extracts and ranks relevant phrases from the recognized text.
6. The extracted keywords are used to retrieve related search results.
7. The processed information is returned to the frontend as JSON.

## Project Structure

```text
Document_digitalization/
├── model.py               # Flask backend, OCR and keyword-processing logic
├── templates/             # HTML templates
├── static/                # Frontend assets and styling
├── IMAGE_PRESENTATION/    # Presentation assets
├── FINAL_project.pptx     # Project presentation
└── README.md
```

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/gikeross/Document_digitalization.git
cd Document_digitalization
```

Install the Python dependencies required by `model.py`, including Flask, Google Cloud Vision, pandas, RAKE-NLTK and googlesearch.

Google Cloud Vision also requires valid application credentials. The current project code references a local credential path, so update the `GOOGLE_APPLICATION_CREDENTIALS` configuration for your own environment before running the application.

Start the Flask server:

```bash
python model.py
```

Then open the local Flask address in your browser and upload an image for processing.

## Skills Demonstrated

This project combines several parts of an end-to-end data application: API integration, OCR, natural-language processing, backend development, temporary file handling and frontend/backend communication.

## Future Improvements

Potential improvements include moving configuration into environment variables, adding a dependency file, improving error handling, expanding OCR evaluation, and deploying the application so it can be tested without a local setup.
