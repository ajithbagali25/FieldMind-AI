from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse
from PIL import Image
import io
from pathlib import Path

from backend.ai_engine import analyze_image

app = FastAPI(
    title="FieldMind AI",
    description="Private on-device AI field assistant",
    version="0.1.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"


@app.get("/")
def home():
    return FileResponse(str(FRONTEND_FILE))


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze-image")
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    question: str = Form("What do you see in this image?")
):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    image_bytes = await file.read()

    try:
        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        )

    try:
        result = analyze_image(
            image,
            question
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

    return {
        "filename": file.filename,
        "question": question,
        "analysis": result
    }
from PIL import Image
import io
from pathlib import Path

from backend.ai_engine import analyze_image

app = FastAPI(
    title="FieldMind AI",
    description="Private on-device AI field assistant",
    version="0.1.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_FILE = BASE_DIR / "frontend" / "index.html"


@app.get("/")
def home():
    return FileResponse(str(FRONTEND_FILE))


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze-image")
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    question: str = Form("What do you see in this image?")
):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    image_bytes = await file.read()

    try:
        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        )

    try:
        result = analyze_image(
            image,
            question
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

    return {
        "filename": file.filename,
        "question": question,
        "analysis": result
    }
from PIL import Image
import io

from backend.ai_engine import analyze_image

app = FastAPI(
    title="FieldMind AI",
    description="Private on-device AI field assistant",
    version="0.1.0"
)


@app.get("/")
def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/analyze-image")
async def analyze_image_endpoint(
    file: UploadFile = File(...),
    question: str = Form("What do you see in this image?")
):

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file."
        )

    image_bytes = await file.read()

    try:
        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        )

    try:
        result = analyze_image(
            image,
            question
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )

    return {
        "filename": file.filename,
        "question": question,
        "analysis": result
    }