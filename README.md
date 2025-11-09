# 🎬 MP4 to PNG Frame Extractor

A full-stack web application that extracts all frames from MP4 videos and downloads them as PNG images in a ZIP file. Built with React/Vite frontend, Python/Flask backend, and fully containerized with Docker.

## ✨ Features

- 📤 **Upload Video Files**: Support for MP4, AVI, MOV, and MKV formats
- 🖼️ **Frame Extraction**: Extracts all frames from videos using OpenCV
- 📦 **ZIP Download**: Downloads all extracted frames as PNG files in a convenient ZIP archive
- 🐳 **Docker Ready**: Fully containerized application with Docker Compose
- 🎨 **Modern UI**: Beautiful, responsive React interface with real-time progress tracking
- ⚡ **Fast Processing**: Efficient frame extraction with Python backend
- 🔒 **File Validation**: Checks file types and size limits (500MB max)

## 🏗️ Architecture

```
mp4-to-png/
├── backend/              # Python Flask API
│   ├── app.py           # Main application logic
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile       # Backend container config
│   └── .gitignore
├── frontend/            # React/Vite application
│   ├── src/
│   │   ├── App.jsx      # Main React component
│   │   ├── App.css      # Styling
│   │   ├── main.jsx     # Entry point
│   │   └── index.css    # Global styles
│   ├── index.html       # HTML template
│   ├── vite.config.js   # Vite configuration
│   ├── nginx.conf       # Nginx config for production
│   ├── package.json     # Node dependencies
│   ├── Dockerfile       # Frontend container config
│   └── .gitignore
├── docker-compose.yml   # Container orchestration
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine + Docker Compose (Linux)
- Git

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mp4-to-png
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Open your browser and navigate to: `http://localhost`
   - The backend API is available at: `http://localhost:5000`

4. **Stop the application**
   ```bash
   docker-compose down
   ```

## 🎯 Usage

1. **Upload a Video**
   - Click on "Choose Video File" button
   - Select an MP4, AVI, MOV, or MKV file (max 500MB)

2. **Extract Frames**
   - Click "Extract Frames" button
   - Wait for the extraction process to complete
   - Monitor the progress bar

3. **Download Results**
   - Once extraction is complete, click "Download ZIP"
   - Your frames will be downloaded as `frames.zip`
   - Each frame is saved as `frame_XXXXXX.png`

4. **Extract Another Video**
   - Click "Extract Another Video" to start over

## 🛠️ Development

### Running Backend Locally (without Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend will run on `http://localhost:5000`

### Running Frontend Locally (without Docker)

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:3000`

## 📝 API Endpoints

### Backend API

- **GET /health**
  - Health check endpoint
  - Returns: `{"status": "healthy"}`

- **POST /extract**
  - Extract frames from uploaded video
  - Body: `multipart/form-data` with `video` file
  - Returns: 
    ```json
    {
      "success": true,
      "frame_count": 150,
      "download_id": "uuid",
      "message": "Successfully extracted 150 frames"
    }
    ```

- **GET /download/:download_id**
  - Download the ZIP file containing extracted frames
  - Returns: ZIP file download

## 🔧 Configuration

### Environment Variables

**Backend:**
- `FLASK_ENV`: Set to `production` for production mode
- Max upload size: 500MB (configurable in `app.py`)

**Frontend:**
- `VITE_API_URL`: API base URL (defaults to `/api` in production)

### Docker Configuration

**Ports:**
- Frontend: `80` (mapped to host port 80)
- Backend: `5000` (mapped to host port 5000)

**Volumes:**
- Backend uploads and outputs are persisted in local directories

## 🎨 Supported Formats

**Input Video Formats:**
- MP4 (`.mp4`)
- AVI (`.avi`)
- MOV (`.mov`)
- MKV (`.mkv`)

**Output Format:**
- PNG images (`.png`)

## 📦 Technologies Used

**Frontend:**
- React 18
- Vite 5
- Axios
- Modern CSS with gradients

**Backend:**
- Python 3.11
- Flask 3.0
- OpenCV (opencv-python-headless)
- Gunicorn

**DevOps:**
- Docker
- Docker Compose
- Nginx (for serving frontend in production)

## ⚠️ Limitations

- Maximum file size: 500MB
- Processing time depends on video length and system resources
- Temporary files are automatically cleaned up after download

## 🐛 Troubleshooting

**Issue: Container won't start**
- Check if ports 80 and 5000 are available
- Run `docker-compose logs` to see error messages

**Issue: Upload fails**
- Ensure file is under 500MB
- Check that file format is supported
- Verify backend container is running: `docker ps`

**Issue: Extraction takes too long**
- Large videos with high frame rates will take longer
- Check CPU/memory resources in Docker Desktop

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 👨‍💻 Author

Your Name

## 🌟 Acknowledgments

- OpenCV for video processing capabilities
- React and Vite for the modern frontend framework
- Flask for the lightweight Python backend
