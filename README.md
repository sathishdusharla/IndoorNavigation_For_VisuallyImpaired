# NavSight: Indoor Navigation for the Visually Impaired

![Project Banner](https://img.shields.io/badge/AI%20Project-NavSight-blueviolet?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

**NavSight** is an AI-powered indoor navigation system designed to assist visually impaired individuals in real-time. It uses computer vision and voice feedback to detect objects, elevations (stairs/ramps), and rooms, helping users navigate complex indoor environments safely and independently.

---

## 🧠 Key Features

- 🔍 **Object Detection** using YOLOv3 + OpenCV (e.g., doors, obstacles, staircases)
- 📷 **Real-Time Elevation Recognition** for stairs, slopes, etc.
- 🧾 **Offline QR-based Room Detection**
- 🎤 **Voice Assistant Integration** for user commands and emergency alerts
- 🔊 **Live Audio Feedback** to guide the user step-by-step
- 📡 **Guardian Notification System** (future enhancement)

---

## 📄 Publication

This project has been **published in JETIR (Journal of Emerging Technologies and Innovative Research)**.

> 📘 **Title**: *NavSight: An AI‑Powered Indoor Navigation System*  
> 🗓️ **Published**: May 2025, Volume 12 Issue 5  
> 🔗 [Read the Paper (JETIR)](https://www.jetir.org/view?paper=JETIR2505010)

---

## 📁 Project Structure

```bash
├── dataset/                    # Training and test datasets
├── models/                     # YOLO weights or custom-trained models
├── qr_code_module/             # QR room recognition
├── voice_assistant/            # Audio output and speech recognition
├── elevation_detection/        # Stair/ramp classifier
├── main.py                     # Entry point for real-time demo
├── requirements.txt            # Required packages
├── README.md                   # This file
