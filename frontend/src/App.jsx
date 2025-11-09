import { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      // Check file size (500MB max)
      if (selectedFile.size > 500 * 1024 * 1024) {
        setError('File size exceeds 500MB limit')
        setFile(null)
        return
      }
      setFile(selectedFile)
      setError(null)
      setResult(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a video file')
      return
    }

    const formData = new FormData()
    formData.append('video', file)

    setUploading(true)
    setError(null)
    setProgress(0)

    try {
      const response = await axios.post(`${API_URL}/extract`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          setProgress(percentCompleted)
        },
      })

      setResult(response.data)
      setUploading(false)
      setProgress(0)
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during extraction')
      setUploading(false)
      setProgress(0)
    }
  }

  const handleDownload = () => {
    if (result && result.download_id) {
      window.location.href = `${API_URL}/download/${result.download_id}`
    }
  }

  const handleReset = () => {
    setFile(null)
    setResult(null)
    setError(null)
    setProgress(0)
    // Reset file input
    const fileInput = document.getElementById('video-input')
    if (fileInput) fileInput.value = ''
  }

  return (
    <div className="App">
      <div className="container">
        <h1>🎬 MP4 to PNG Frame Extractor</h1>
        <p className="subtitle">Upload a video and extract all frames as PNG images</p>

        <div className="upload-section">
          <div className="file-input-wrapper">
            <input
              id="video-input"
              type="file"
              accept="video/mp4,video/avi,video/mov,video/x-matroska"
              onChange={handleFileChange}
              disabled={uploading}
            />
            <label htmlFor="video-input" className={uploading ? 'disabled' : ''}>
              {file ? `📁 ${file.name}` : '📂 Choose Video File'}
            </label>
          </div>

          {file && !result && (
            <div className="file-info">
              <p>
                <strong>Selected:</strong> {file.name}
              </p>
              <p>
                <strong>Size:</strong> {(file.size / (1024 * 1024)).toFixed(2)} MB
              </p>
            </div>
          )}

          {!result && (
            <button
              className="extract-btn"
              onClick={handleUpload}
              disabled={!file || uploading}
            >
              {uploading ? '⏳ Extracting...' : '🚀 Extract Frames'}
            </button>
          )}

          {uploading && (
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}>
                {progress}%
              </div>
            </div>
          )}

          {error && (
            <div className="error-message">
              <p>❌ {error}</p>
            </div>
          )}

          {result && (
            <div className="success-message">
              <h2>✅ Extraction Complete!</h2>
              <p>
                <strong>Frames extracted:</strong> {result.frame_count}
              </p>
              <p>{result.message}</p>
              <div className="action-buttons">
                <button className="download-btn" onClick={handleDownload}>
                  ⬇️ Download ZIP
                </button>
                <button className="reset-btn" onClick={handleReset}>
                  🔄 Extract Another Video
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="info-section">
          <h3>📋 Supported Formats</h3>
          <ul>
            <li>MP4</li>
            <li>AVI</li>
            <li>MOV</li>
            <li>MKV</li>
          </ul>
          <p className="note">
            <strong>Note:</strong> Maximum file size is 500MB
          </p>
        </div>
      </div>
    </div>
  )
}

export default App
