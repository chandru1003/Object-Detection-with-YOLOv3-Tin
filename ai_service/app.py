from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import logging

app = Flask(__name__)

# Load YOLOv3-tiny model (.pt format)
model = YOLO("models/yolov3-tiny.pt")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai_service")


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Service with Ultralytics YOLOv3-tiny is running"}), 200


@app.route("/detect", methods=["POST"])
def detect_objects():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Read image
        image_data = file.read()
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Run detection
        results = model.predict(img, conf=0.5)

        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = float(box.conf[0])

                detections.append({
                    "class": label,
                    "confidence": round(conf, 2),
                    "bbox": [int(x1), int(y1), int(x2), int(y2)]
                })

                # Draw on image
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)),
                              (0, 255, 0), 2)
                cv2.putText(img, f"{label} {conf:.2f}",
                            (int(x1), int(y1) - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2)

        # Convert annotated image to Base64
        _, buffer = cv2.imencode(".jpg", img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        return jsonify({
            "detections": detections,
            "output_image_base64": img_base64
        }), 200

    except Exception as e:
        logger.exception("Error during detection")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
