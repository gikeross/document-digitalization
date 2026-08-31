# Document Digitalization

A Flask-based web application that converts images of handwritten notes into structured digital text using Google Cloud Vision OCR. The application also extracts keywords from the recognized text and generates related search results.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/gikeross/document-digitalization)

## Project Preview

The repository includes example document images used to demonstrate the OCR workflow:

<p align="center">
  <img src="IMAGE_PRESENTATION/example1.jpg" alt="Example handwritten document used by the OCR application" width="45%" />
  <img src="IMAGE_PRESENTATION/random_example.jpg" alt="Second example document used by the OCR application" width="45%" />
</p>

The application takes an uploaded document image and turns it into machine-readable text, OCR confidence metrics, ranked keywords and related search results.

## User Experience

The frontend now includes drag-and-drop upload, client-side file validation, image preview, loading/success/error states, responsive result cards, clickable related links and a one-click copy action for extracted text.

Accepted formats are **PNG, JPG/JPEG and WEBP**, with an **8 MB** maximum upload size.

## Results

The completed prototype demonstrates an end-to-end document-processing workflow rather than OCR in isolation. For each successfully processed upload, the backend:

1. validates the uploaded image type and enforces an 8 MB size limit;
2. extracts document text with Google Cloud Vision;
3. calculates average OCR confidence at block and paragraph level;
4. identifies and ranks meaningful phrases with RAKE;
5. uses those phrases to retrieve related search results;
6. returns the processed information to the browser as structured JSON.

The API distinguishes common failure cases such as missing uploads, unsupported image types, files that are too large, images with no detected text, OCR-provider failures and unexpected server errors.

This makes the project a practical example of combining a cloud AI service with NLP and a web application layer. The repository does not currently include a formal OCR benchmark dataset, so the project should be viewed as a working application prototype rather than a measured comparison of OCR accuracy.

## Reliability and Testing

The repository includes automated Flask API tests under `tests/` covering upload validation, successful mocked OCR responses, no-text responses and OCR-provider failure handling. A GitHub Actions workflow runs the suite automatically on relevant pushes and pull requests.

```bash
pytest -q
```

## Tech Stack

- **Python** — application logic and text-processing pipeline
- **Flask** — web application and API endpoints
- **Google Cloud Vision** — document text detection / OCR
- **RAKE-NLTK** — keyword extraction
- **googlesearch** — related search-result retrieval
- **Gunicorn** — production WSGI server
- **Docker** — portable production runtime
- **pytest** — automated API testing
- **GitHub Actions** — continuous integration
- **HTML / CSS / JavaScript** — responsive user interface

## How It Works

1. The user selects or drops a supported image into the browser.
2. Client-side JavaScript validates the file and displays a preview.
3. Flask validates the filename, MIME type and maximum request size again server-side.
4. The upload is stored in a temporary file.
5. Google Cloud Vision performs document text detection.
6. The application calculates average OCR confidence scores.
7. RAKE extracts and ranks relevant phrases from the recognized text.
8. The extracted keywords are used to retrieve related search results.
9. The temporary upload is removed after processing.
10. Results are rendered into responsive cards in the browser.

## Project Structure

```text
document-digitalization/
├── model.py               # Flask backend, validation, OCR and NLP logic
├── requirements.txt       # Python and test dependencies
├── tests/                 # Flask API tests
├── .github/workflows/     # Continuous-integration workflow
├── Dockerfile             # Production container image
├── .dockerignore          # Container build exclusions
├── render.yaml            # Render deployment blueprint
├── templates/             # HTML templates
├── static/                # Frontend JavaScript and responsive styling
├── IMAGE_PRESENTATION/    # Example document images
├── FINAL_project.pptx     # Project presentation
└── README.md
```

## Running Locally

```bash
git clone https://github.com/gikeross/document-digitalization.git
cd document-digitalization
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
python model.py
```

## Running with Docker

```bash
docker build -t document-digitalization .
docker run --rm -p 8080:8080 \
  -e GOOGLE_APPLICATION_CREDENTIALS_JSON="$(cat /path/to/service-account.json)" \
  document-digitalization
```

Then open `http://localhost:8080`. The production container runs the application through Gunicorn and exposes `/health` for platform health checks.

## Cloud Deployment

The repository is deployment-ready through the included `Dockerfile` and `render.yaml` blueprint. The **Deploy to Render** button at the top opens this repository directly as a Render Blueprint deployment. Render supports public repositories directly and reads the included `render.yaml` configuration. Configure the service-account JSON as the secret environment variable:

```text
GOOGLE_APPLICATION_CREDENTIALS_JSON
```

Do **not** commit the credential file itself. The application parses the secret in memory and passes the credentials directly to Google Cloud Vision.

After reviewing the Blueprint in Render, enter the secret value, apply the deployment, and verify `/health` returns a successful response before testing OCR. Other Docker-capable platforms can use the same image and health endpoint.

## Security and Repository Hygiene

Credentials are not stored in source code. Local environment files, virtual environments, macOS metadata and common credential filenames are excluded through `.gitignore` and `.dockerignore`.

If a service-account key has ever been committed to Git history, revoke that key in Google Cloud and create a new one.

## Skills Demonstrated

This project combines API integration, OCR, natural-language processing, backend development, frontend UX, input validation, automated testing, continuous integration, Docker deployment, production WSGI serving, temporary file handling and secure configuration.

## Future Improvements

Useful next improvements include rate limiting for search requests, a formal OCR evaluation dataset, end-to-end browser tests and a public live-demo URL once a hosting account is connected.
