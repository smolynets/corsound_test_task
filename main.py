from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image, UnidentifiedImageError
import torch
import io
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

preprocessor = AutoImageProcessor.from_pretrained("google/mobilenet_v2_1.0_224")
model = AutoModelForImageClassification.from_pretrained("google/mobilenet_v2_1.0_224")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Request completed with status code {response.status_code}")
    return response

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    logger.info("Image upload endpoint called")
    if file.content_type not in ["image/jpeg", "image/png"]:
        logger.error(f"Invalid image format: {file.content_type}")
        raise HTTPException(status_code=400, detail="Invalid image format. Only JPG and PNG are supported.")
    
    try:
        image = Image.open(io.BytesIO(await file.read()))
    except UnidentifiedImageError:
        logger.error("Cannot identify the image. Make sure the file is a valid image.")
        raise HTTPException(status_code=400, detail="Cannot identify the image. Make sure the file is a valid image.")
    except Exception as e:
        logger.exception(f"An error occurred while reading the image: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while reading the image: {e}")

    try:
        inputs = preprocessor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits

        top_k = 3
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        top_k_probs, top_k_indices = torch.topk(probabilities, top_k)

        predictions = []
        for i in range(top_k):
            predicted_class_idx = top_k_indices[0, i].item()
            probability = top_k_probs[0, i].item()
            predicted_class_label = model.config.id2label[predicted_class_idx]
            predictions.append({
                "class": predicted_class_label,
                "probability": probability
            })

        logger.info("Image processed and predictions generated")
        return JSONResponse(content={"predictions": predictions})
    except Exception as e:
        logger.exception(f"An error occurred during model inference: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during model inference: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
