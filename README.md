# 🖼️ Object Detection with YOLOv3-Tiny

This project implements a microservice-based object detection system using **YOLOv3-Tiny** with Ultralytics.  
It contains two main services:
- **AI Service (Flask)** → Runs object detection and returns detections + annotated image (Base64).
- **UI Service (Streamlit)** → Simple web interface to upload an image and view detection results.

---

## 🚀 Features

- Uses YOLOv3-Tiny model (`.pt`) for lightweight detection.
- Flask API returns:
  - JSON detections (`class`, `confidence`, `bbox`).
  - Annotated image encoded in Base64.
- Streamlit UI for uploading and testing images.
- Dockerized for easy deployment with `docker-compose`.
- Outputs saved as JSON + annotated images for submission.

---

## 🔧 Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Internet access (to download model if not already included)

Dependencies:
- `ultralytics`
- `flask`
- `opencv-python`
- `numpy`
- `pillow`
- `streamlit`
- `requests`

---

## 📖 Steps to Solution

1. **Model Selection**  
   Used **YOLOv3-Tiny** from Ultralytics for faster inference on CPU.  

2. **AI Service (Backend)**  
   - Implemented using Flask.
   - Exposes `/detect` endpoint that accepts an uploaded image.
   - Runs inference with YOLOv3-Tiny.
   - Returns JSON detections and Base64-encoded annotated image.

3. **UI Service (Frontend)**  
   - Implemented in Streamlit.
   - Allows uploading images and calling AI service.
   - Displays both raw detections and annotated output image.

4. **Containerization**  
   - Each service has its own Dockerfile.
   - A `docker-compose.yml` file orchestrates both services.
   - Communication between containers uses the service name (`ai_service`).

5. **Output Saving**  
   - JSON files: detections with bounding boxes.
   - Annotated images: bounding boxes drawn around detected objects.

---

## 🐳 Running with Docker

### Build & Run
```bash
docker-compose up --build
