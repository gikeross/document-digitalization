import io
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from google.cloud import vision
from googlesearch import search
from rake_nltk import Rake

app = Flask(__name__, static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}


@app.route("/")
def index():
    return render_template("index.html")


def validate_upload(uploaded_file):
    if uploaded_file is None or uploaded_file.filename == "":
        return "No file uploaded"

    extension = Path(uploaded_file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return "Unsupported file type. Use PNG, JPG, JPEG, or WEBP."

    if uploaded_file.mimetype not in ALLOWED_MIME_TYPES:
        return "Unsupported MIME type. Upload a valid image file."

    return None


@app.errorhandler(413)
def file_too_large(_error):
    return jsonify({"error": "File too large. Maximum upload size is 8 MB."}), 413


@app.route("/image_text_recognition", methods=["POST"])
def image_text_recognition():
    uploaded_file = request.files.get("imageFile")
    validation_error = validate_upload(uploaded_file)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    temp_path = None
    try:
        suffix = Path(uploaded_file.filename).suffix.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            uploaded_file.save(temp_file.name)
            temp_path = temp_file.name

        doc_text, avg_block_confidence, avg_paragraph_confidence = recognize_text(temp_path)

        if not doc_text or not doc_text.strip():
            return jsonify({"error": "No text detected in the uploaded image."}), 422

        rating_list, keywords_list = keyword_classifier(doc_text)
        all_results = search_results(keywords_list)

        return jsonify({
            "text": doc_text,
            "avg_block_confidence": round(avg_block_confidence * 100, 2),
            "avg_paragraph_confidence": round(avg_paragraph_confidence * 100, 2),
            "rating": rating_list,
            "keywords": keywords_list,
            "search": all_results,
        })
    except RuntimeError as exc:
        app.logger.warning("OCR provider error: %s", exc)
        return jsonify({"error": "OCR service could not process the image."}), 502
    except Exception:
        app.logger.exception("Image processing failed")
        return jsonify({"error": "Image processing failed unexpectedly."}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def recognize_text(file_path):
    client = vision.ImageAnnotatorClient()

    with io.open(file_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise RuntimeError(response.error.message)

    total_block_confidence = 0.0
    total_paragraph_confidence = 0.0
    num_blocks = 0
    num_paragraphs = 0

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            total_block_confidence += block.confidence
            num_blocks += 1
            for paragraph in block.paragraphs:
                total_paragraph_confidence += paragraph.confidence
                num_paragraphs += 1

    avg_block_confidence = total_block_confidence / num_blocks if num_blocks else 0.0
    avg_paragraph_confidence = (
        total_paragraph_confidence / num_paragraphs if num_paragraphs else 0.0
    )

    return response.full_text_annotation.text, avg_block_confidence, avg_paragraph_confidence


def keyword_classifier(doc_text):
    rake = Rake()
    rake.extract_keywords_from_text(doc_text)

    ratings = []
    keywords = []
    for rating, phrase in rake.get_ranked_phrases_with_scores():
        if rating > 1:
            ratings.append(round(rating, 0))
            keywords.append(phrase)

    return ratings, keywords


def search_results(keywords_list, num_results=1):
    all_results = []
    for keyword in keywords_list:
        keyword_results = []
        for result in search(keyword, num_results=num_results):
            keyword_results.append(result)
            if len(keyword_results) >= num_results:
                break
        all_results.append(keyword_results)
    return all_results


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
