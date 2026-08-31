import io
from unittest.mock import patch

import pytest

from model import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def make_image_upload(filename="note.jpg", mimetype="image/jpeg"):
    return {"imageFile": (io.BytesIO(b"fake-image-bytes"), filename, mimetype)}


def test_missing_file_returns_400(client):
    response = client.post("/image_text_recognition", data={})
    assert response.status_code == 400
    assert response.get_json()["error"] == "No file uploaded"


def test_unsupported_extension_returns_400(client):
    response = client.post(
        "/image_text_recognition",
        data=make_image_upload(filename="notes.txt", mimetype="text/plain"),
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.get_json()["error"]


def test_unsupported_mime_type_returns_400(client):
    response = client.post(
        "/image_text_recognition",
        data=make_image_upload(filename="notes.jpg", mimetype="application/octet-stream"),
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    assert "Unsupported MIME type" in response.get_json()["error"]


@patch("model.search_results", return_value=[["https://example.com"]])
@patch("model.keyword_classifier", return_value=([4.0], ["sample keyword"]))
@patch("model.recognize_text", return_value=("sample text", 0.91, 0.88))
def test_successful_processing_returns_structured_json(
    _mock_ocr, _mock_keywords, _mock_search, client
):
    response = client.post(
        "/image_text_recognition",
        data=make_image_upload(),
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["text"] == "sample text"
    assert payload["avg_block_confidence"] == 91.0
    assert payload["avg_paragraph_confidence"] == 88.0
    assert payload["keywords"] == ["sample keyword"]


@patch("model.recognize_text", return_value=("", 0.0, 0.0))
def test_no_text_returns_422(_mock_ocr, client):
    response = client.post(
        "/image_text_recognition",
        data=make_image_upload(),
        content_type="multipart/form-data",
    )
    assert response.status_code == 422
    assert "No text detected" in response.get_json()["error"]


@patch("model.recognize_text", side_effect=RuntimeError("provider failure"))
def test_ocr_provider_error_returns_502(_mock_ocr, client):
    response = client.post(
        "/image_text_recognition",
        data=make_image_upload(),
        content_type="multipart/form-data",
    )
    assert response.status_code == 502
    assert "OCR service" in response.get_json()["error"]
