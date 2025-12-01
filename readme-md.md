# 🫁 Pneumonia Detection System

An AI-powered web application for detecting pneumonia from chest X-ray images using deep learning. Designed specifically for deployment in low-resource healthcare settings where access to radiological expertise may be limited.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-orange.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Information](#model-information)
- [Security Considerations](#security-considerations)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

---

## 🎯 Overview

The Pneumonia Detection System is a web-based diagnostic assistance tool that uses a deep learning model (VGG16) to analyze chest X-ray images and predict the presence of pneumonia. The system provides visual explanations through Grad-CAM heatmaps, helping healthcare workers understand which regions of the X-ray influenced the AI's decision.

### Purpose

This system addresses the shortage of radiological expertise in low-resource healthcare settings by providing:
- **Fast Analysis**: Results in seconds
- **High Accuracy**: 96% accuracy with VGG16 model
- **Visual Explanation**: Grad-CAM heatmaps showing areas of concern
- **Accessibility**: Simple interface requiring minimal technical expertise
- **History Tracking**: For authenticated users to monitor cases over time

### Target Users

- Healthcare workers in rural or remote clinics
- Medical facilities with limited access to radiologists
- Community health centers in low-resource areas
- Medical education and training programs

---

## ✨ Features

### Core Functionality

- **🔍 AI-Powered Detection**: VGG16 deep learning model with 96% accuracy
- **📊 Confidence Scoring**: Transparent confidence levels for each prediction
- **🎨 Grad-CAM Visualization**: Color-coded heatmaps showing model focus areas
- **⚡ Fast Processing**: Results delivered in seconds
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

### Authentication & User Management

- **🔐 Google OAuth**: Quick sign-in with Google accounts
- **📧 Email/Password**: Traditional authentication option
- **👤 Guest Access**: Use without registration (no history saved)
- **🔒 Secure Sessions**: Password hashing and session management

### History & Data Management

- **📋 Classification History**: View past analyses (authenticated users)
- **🖼️ Image Archive**: Store original X-rays and heatmaps
- **🗑️ Data Deletion**: Users can delete their records
- **📅 Timestamp Tracking**: Record when each analysis was performed

### User Experience

- **🌓 Theme Support**: Light, dark, and system-adaptive themes
- **🖱️ Drag & Drop**: Intuitive file upload
- **📤 File Preview**: See uploaded image before analysis
- **⚠️ Clear Feedback**: Color-coded results and informative messages
- **🔤 Professional UI**: Clean, medical-grade interface

---

## 🛠 Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Authentication**: Flask-Login, Authlib (OAuth)
- **Database**: SQLite (development), PostgreSQL-ready
- **Security**: Werkzeug password hashing

### Machine Learning
- **Framework**: TensorFlow 2.15.0
- **Model**: VGG16 (96% accuracy)
- **Visualization**: Grad-CAM (Gradient-weighted Class Activation Mapping)
- **Image Processing**: OpenCV, Pillow

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Custom styling with CSS variables
- **JavaScript**: Vanilla JS for interactivity
- **Design**: Responsive, mobile-first approach

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│  (HTML/CSS/JS - Responsive Web Application)         │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│              Flask Application                       │
│  ┌──────────────────────────────────────────────┐  │
│  │  Authentication Layer                        │  │
│  │  - Google OAuth / Email-Password             │  │
│  │  - Session Management                        │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Image Processing Pipeline                   │  │
│  │  - Upload & Validation                       │  │
│  │  - Resize & Normalization                    │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  AI Model Inference                          │  │
│  │  - VGG16 Prediction                          │  │
│  │  - Grad-CAM Generation                       │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Data Management                             │  │
│  │  - History Storage                           │  │
│  │  - File Management                           │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│              Data Layer                              │
│  ┌────────────────┐      ┌────────────────────┐    │
│  │  SQLite DB     │      │  File Storage       │    │
│  │  - Users       │      │  - X-ray Images     │    │
│  │  - History     │      │  - Heatmaps         │    │
│  └────────────────┘      └────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

## 📥 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum (8GB recommended)
- Modern web browser

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/pneumonia-detection.git
cd pneumonia-detection
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Directory Structure

```bash
# Create necessary directories
mkdir -p static/uploads
mkdir -p models
```

### Step 5: Add Model File

Place your trained VGG16 model file in the `models/` directory:
```
models/pneumonia_vgg16_0.96(21Nov25).keras
```

---

## ⚙️ Configuration

### 1. Secret Key Configuration

Generate a secure secret key:

```python
import secrets
print(secrets.token_hex(32))
```

Update in `app.py`:
```python
app.secret_key = 'your-generated-secret-key-here'
```

### 2. Google OAuth Setup (Optional)

If you want to enable Google authentication:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API or People API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI:
   ```
   http://127.0.0.1:5000/auth/google/callback
   ```
6. Update in `app.py`:
   ```python
   client_id='YOUR_GOOGLE_CLIENT_ID',
   client_secret='YOUR_GOOGLE_CLIENT_SECRET',
   ```

**Note**: The system works fully without Google OAuth using email/password or guest access.

### 3. Environment Variables (Production)

For production deployment, use environment variables:

```bash
export SECRET_KEY='your-secret-key'
export GOOGLE_CLIENT_ID='your-client-id'
export GOOGLE_CLIENT_SECRET='your-client-secret'
export DATABASE_URL='postgresql://...'  # For PostgreSQL
```

Update `app.py` to read from environment:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY')
```

---

## 🚀 Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Basic Workflow

#### As a Guest User:

1. **Navigate** to `http://127.0.0.1:5000`
2. **Upload** a chest X-ray image (drag & drop or click to browse)
3. **Click** "Analyze X-Ray"
4. **View** results with prediction, confidence, and Grad-CAM heatmap

#### As an Authenticated User:

1. **Sign In** using Google OAuth or email/password
2. **Upload** and analyze X-ray images (same as guest)
3. **View History** to see all past analyses
4. **Delete** records as needed
5. **Logout** when finished

### Interpreting Results

**Prediction**: 
- `NORMAL` (Green) - No pneumonia detected
- `PNEUMONIA` (Red) - Pneumonia detected

**Confidence Score**: 
- Percentage indicating model certainty
- Higher values indicate more confident predictions

**Grad-CAM Heatmap**:
- **Blue/Purple**: Areas model paid less attention to
- **Green/Yellow**: Areas of moderate interest
- **Red**: Areas model focused on most (potential pneumonia indicators)

---

## 📁 Project Structure

```
pneumonia-detection/
├── app.py                          # Main Flask application
├── gradcam.py                      # Grad-CAM visualization logic
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── SETUP_INSTRUCTIONS.md           # Detailed setup guide
├── pneumonia_detection.db          # SQLite database (auto-created)
│
├── models/
│   └── pneumonia_vgg16_0.96(21Nov25).keras    # VGG16 model
│
├── static/
│   ├── style.css                   # Main stylesheet
│   ├── auth.css                    # Authentication page styles
│   ├── script.js                   # Frontend JavaScript
│   └── uploads/                    # Uploaded images and heatmaps
│
└── templates/
    ├── index.html                  # Main detection page
    ├── login.html                  # Login page
    ├── register.html               # Registration page
    └── history.html                # History page
```

---

## 🤖 Model Information

### VGG16 Architecture

The system uses a VGG16-based convolutional neural network, fine-tuned specifically for pneumonia detection from chest X-rays.

**Model Specifications**:
- **Architecture**: VGG16 (Visual Geometry Group)
- **Input Size**: 224×224 pixels (RGB)
- **Training Dataset**: Chest X-ray images (pneumonia vs normal)
- **Accuracy**: 96%
- **Output**: Binary classification (Normal vs Pneumonia)

### Grad-CAM Visualization

Gradient-weighted Class Activation Mapping (Grad-CAM) provides visual explanations by highlighting regions that contributed most to the model's prediction.

**How It Works**:
1. Gradients flow back from the prediction to the last convolutional layer
2. Weights are computed based on gradient importance
3. A heatmap is generated showing influential regions
4. The heatmap is overlaid on the original X-ray

**Benefits**:
- Interpretability for healthcare workers
- Verification that model focuses on clinically relevant areas
- Educational tool for understanding AI decision-making
- Trust building through transparency

---

## 🔒 Security Considerations

### Implemented Security Measures

1. **Password Security**
   - Passwords hashed using Werkzeug's security utilities
   - No plain-text password storage

2. **Session Management**
   - Secure session cookies
   - Flask-Login session management
   - Session expiry handling

3. **Input Validation**
   - File type validation (images only)
   - File size limits (16MB maximum)
   - SQL injection prevention through parameterized queries

4. **Data Isolation**
   - User data strictly isolated per account
   - Authorization checks on all protected routes

5. **HTTPS Ready**
   - Configuration ready for SSL/TLS in production

### Security Best Practices for Deployment

- Always use HTTPS in production
- Regularly update dependencies
- Use environment variables for secrets
- Implement rate limiting for authentication
- Regular security audits
- Backup database regularly
- Monitor authentication logs

---

## 🌐 Deployment

### Local Development

Already covered in [Installation](#installation) and [Usage](#usage) sections.

### Production Deployment Options

#### Option 1: Traditional Server (Ubuntu/Linux)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv nginx

# Clone and setup
git clone https://github.com/yourusername/pneumonia-detection.git
cd pneumonia-detection
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY='...'
export GOOGLE_CLIENT_ID='...'
export GOOGLE_CLIENT_SECRET='...'

# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Configure Nginx as reverse proxy and enable SSL.

#### Option 2: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t pneumonia-detection .
docker run -p 5000:5000 pneumonia-detection
```

#### Option 3: Cloud Platforms

- **Heroku**: Use Procfile and requirements.txt
- **AWS EC2**: Deploy as traditional server
- **Google Cloud Run**: Deploy as container
- **Azure App Service**: Deploy Python web app

### Database Migration for Production

Replace SQLite with PostgreSQL:

```bash
pip install psycopg2-binary
```

Update `app.py`:
```python
import os
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Google OAuth Error 400: redirect_uri_mismatch

**Solution**:
- Ensure redirect URI in Google Console matches: `http://127.0.0.1:5000/auth/google/callback`
- Access app at `http://127.0.0.1:5000` not `localhost:5000`
- Wait 5-10 minutes after updating Google Console

#### 2. Model Not Found Error

**Solution**:
```bash
# Verify model file exists
ls models/pneumonia_vgg16_0.96(21Nov25).keras

# Check path in app.py matches filename exactly
```

#### 3. Permission Denied on Upload Directory

**Solution**:
```bash
# Linux/Mac
chmod 755 static/uploads

# Windows
# Right-click folder → Properties → Security → Edit permissions
```

#### 4. Database Locked Error

**Solution**:
- SQLite has limited concurrent access
- For production with multiple users, migrate to PostgreSQL
- Or delete `pneumonia_detection.db` to reset

#### 5. Memory Issues with Large Images

**Solution**:
- The system limits uploads to 16MB
- For lower memory systems, reduce in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add comments for complex logic
- Test thoroughly before submitting PR
- Update documentation for new features

### Areas for Contribution

- Additional model architectures or improvements
- Multi-language support for international deployment
- Mobile application development
- Performance optimizations
- Accessibility enhancements
- Documentation translations
- Bug fixes and security improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**IMPORTANT MEDICAL DISCLAIMER**

This pneumonia detection system is designed as an **assistive diagnostic tool** for healthcare professionals and should **NOT** be used as a replacement for professional medical diagnosis, advice, or treatment.

### Key Points:

- This tool is intended for **educational and supportive purposes only**
- Results should be **interpreted by qualified healthcare professionals**
- The system provides predictions with confidence levels, but **no AI system is 100% accurate**
- Always **consult with medical professionals** for diagnosis and treatment decisions
- This tool is particularly designed to **assist** healthcare workers in low-resource settings, not replace clinical judgment
- **Do not make medical decisions** based solely on this system's output

### Limitations:

- The model was trained on a specific dataset and may not generalize to all populations
- Image quality, patient positioning, and X-ray technique affect accuracy
- The system cannot detect other lung conditions or complications
- False positives and false negatives are possible

### Recommended Use:

Use this system as a:
- **Screening tool** to prioritize cases for review
- **Second opinion** alongside clinical assessment
- **Educational resource** for training healthcare workers
- **Triage support** in resource-limited settings

Always prioritize patient safety and follow established medical protocols in your jurisdiction.

---

## 📞 Support and Contact

For questions, issues, or feedback:

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/pneumonia-detection/issues)
- **Email**: your.email@example.com
- **Documentation**: See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

---

## 🙏 Acknowledgments

- VGG16 architecture by Visual Geometry Group, Oxford
- Grad-CAM visualization technique by Selvaraju et al.
- TensorFlow and Keras teams
- Flask and Python communities
- Healthcare workers in low-resource settings who inspire this work

---

## 📊 Project Status

- **Version**: 1.0.0
- **Status**: Active Development
- **Last Updated**: December 2024
- **Maintainer**: Your Name

---

**Made with ❤️ for improving healthcare access in low-resource settings**