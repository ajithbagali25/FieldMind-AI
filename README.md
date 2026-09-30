# FieldMind AI

## AI-Powered Private Field Assistant

FieldMind AI is a local AI-powered field assistant that helps users analyze real-world equipment and field situations using images and natural-language questions.

The system uses a vision-language AI model to understand the uploaded image and provide a practical field assessment.

## Problem

Field workers and users may face difficulty identifying visible equipment problems or understanding what action should be taken.

FieldMind AI provides a simple interface where users can upload an image and ask a question using text or voice.

## Solution

FieldMind AI processes the image locally through a vision-language model and generates a structured response containing:

- Observation
- Possible Issue
- Recommended Action
- Safety Note

The system is designed around privacy, local processing, and practical field assistance.

## Key Features

- Image-based field analysis
- Natural-language questions
- Voice input through the browser
- Vision-language AI analysis
- Structured field assessment
- Local AI inference
- No external AI API required for inference
- Simple browser-based interface

## Architecture

Image + Voice/Text Question
        |
        v
FastAPI Backend
        |
        v
Qwen3-VL-2B-Instruct
        |
        v
Field Assessment
        |
        +--> Observation
        +--> Possible Issue
        +--> Recommended Action
        +--> Safety Note

## AI Model

Model:

Qwen3-VL-2B-Instruct

The model is used as the vision-language reasoning component of FieldMind AI.

## Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn

### AI / Machine Learning
- PyTorch
- Transformers
- Qwen3-VL-2B-Instruct

### Image Processing
- Pillow
- NumPy
- OpenCV

### Frontend
- HTML
- CSS
- JavaScript
- Browser Speech Recognition API

## Privacy

FieldMind AI is designed for local inference. The application sends the uploaded image to the locally running AI model rather than depending on a cloud AI inference API.

This approach is intended to improve privacy and support environments where reliable internet connectivity may not be available.

## Snapdragon Optimization

The project is designed with on-device AI deployment in mind and can be further optimized and deployed on Snapdragon-powered PCs.

The current development environment was used for building and validating the application. Snapdragon-specific deployment and hardware optimization should be performed on compatible Snapdragon hardware.

## Running the Project

### 1. Create and activate the virtual environment

```bash
python -m venv .venv