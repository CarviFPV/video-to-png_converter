# MP4 to PNG Frame Extractor

A full-stack web application that extracts all frames from MP4 videos and produces PNG images packaged into a ZIP file. Built with a React + Vite frontend, a Python + Flask backend, and containerized with Docker.

## Features

- Upload video files (MP4, AVI, MOV, MKV)
- Extract all frames from uploaded videos using OpenCV
- Download extracted frames as a ZIP archive
- Dockerized backend and frontend for easy deployment
- Progress reporting and basic file validation (max 500MB)

## Repository layout

```
mp4-to-png/
├── backend/              # Python Flask API
│   ├── app.py            # Main application logic
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Backend container config
│   └── .gitignore
├── frontend/             # React + Vite application
│   ├── src/              # React source files
│   ├── index.html        # HTML template
│   ├── package.json      # Node dependencies
│   ├── Dockerfile        # Frontend container config
│   └── nginx.conf        # Nginx config used in production image
├── docker-compose.yml    # Compose orchestration for local/dev
└── README.md             # This file
```

## Quick start

Prerequisites:
- Docker Desktop or Docker Engine + Docker Compose
- Git

Run locally using Docker Compose:

```powershell
git clone <your-repo-url>
cd mp4-to-png
docker-compose up --build
```

Open the frontend at http://localhost and the backend API at http://localhost:5000.

To stop:

```powershell
docker-compose down
```

## Usage

1. Upload a supported video file (MP4, AVI, MOV, MKV).
2. Click Extract Frames and wait for processing to complete.
3. Download the resulting ZIP file containing PNG frames.

## Development

### Backend (without Docker)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The backend will run on http://localhost:5000 by default.

### Frontend (without Docker)

```powershell
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000 by default.

## API Endpoints

- GET /health
  - Health check, returns {"status": "healthy"}
- POST /extract
  - Multipart form upload with field `video`. Returns extraction metadata and an ID to download the ZIP.
- GET /download/:download_id
  - Download the ZIP containing extracted frames for the given ID.

## Configuration

Environment variables used by the backend (examples):
- `FLASK_ENV` (set to `production` in production)
- max upload size is configured in the backend source (`app.py`)

The frontend uses `VITE_API_URL` to point to the backend during development or production if needed.

## Supported formats

- Input: MP4, AVI, MOV, MKV
- Output: PNG images

## Technologies / Versions

- Frontend: React 19, Vite 7, Axios
- Backend: Python 3.14, Flask 3.1.2, OpenCV (opencv-python-headless), Gunicorn
- DevOps: Docker, Docker Compose, Nginx (production frontend)

## Limitations

- Max upload size: 500MB (configurable)
- Processing time depends on video length, frame rate and available CPU

## Troubleshooting

If containers fail to start:
- Ensure ports 80 and 5000 are free
- Check logs with `docker-compose logs` and `docker ps -a`

If upload or extraction fails:
- Verify file size and format
- Check backend logs for errors

## License

This project is available under the MIT License.

## Contributing

Issues and pull requests are welcome. Please include reproduction steps and logs where appropriate.
