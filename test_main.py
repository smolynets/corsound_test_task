import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from main import app

client = TestClient(app)

def create_image(file_format='JPEG'):
    """Helper function to create a test image."""
    image = Image.new('RGB', (100, 100), color='red')
    buf = io.BytesIO()
    image.save(buf, format=file_format)
    buf.seek(0)
    return buf

def create_text_file(file_name='test.txt', content='This is a test text file.'):
    """Helper function to create a test text file."""
    with open(file_name, 'w') as file:
        file.write(content)

def test_upload_valid_image():
    image_file = create_image('JPEG')
    response = client.post("/upload-image/", files={"file": ("test.jpg", image_file, "image/jpeg")})
    assert response.status_code == 200
    assert "predictions" in response.json()
    predictions = response.json()["predictions"]
    assert isinstance(predictions, list)
    assert len(predictions) > 0
    assert "class" in predictions[0]
    assert "probability" in predictions[0]

def test_upload_invalid_image_format():
    create_text_file()
    with open('test.txt', 'rb') as file:
        response = client.post("/upload-image/", files={"file": ("test.txt", file, "text/plain")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid image format. Only JPG and PNG are supported."}

def test_upload_corrupted_image():
    response = client.post("/upload-image/", files={"file": ("test.jpg", io.BytesIO(b"not an image"), "image/jpeg")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot identify the image. Make sure the file is a valid image."}
