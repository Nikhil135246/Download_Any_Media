# YouTube Downloader GUI

A standalone desktop application for downloading YouTube videos and audio with a clean, user-friendly interface. **No installation required** - just download and run!

## 🚀 Quick Start (For Users)

**[Download the latest release](https://github.com/Nikhil135246/Download_Any_Media/releases)** - Get the ready-to-use executable

1. Download `YouTube-Downloader.exe` from the releases page
2. Double-click to run - no installation needed!
3. Paste any YouTube URL and download

## ✨ Features

- **🎯 Zero Installation**: Self-contained executable with all dependencies bundled
- **🔧 No Setup Required**: FFmpeg included - works on any Windows PC
- **🎨 Custom Icon**: Professional download icon in Windows Explorer
- **📁 Smart Downloads**: Automatically organizes videos and audio in separate folders
- **⚡ Simple Interface**: Clean GUI with easy-to-use controls
- **🎵 Multiple Download Options**:
  - Single video download (best quality with automatic merging)
  - Single audio download (MP3 format)
  - Playlist video downloads
  - Playlist audio downloads (MP3 format)
- **⚙️ Configurable Settings**: Choose custom download directories
- **📊 Real-time Progress**: See download progress and status updates
- **🛡️ Error Handling**: Comprehensive error reporting and logging
- **🌍 Universal Compatibility**: Works on any Windows PC (7, 10, 11)

## 💻 For Developers

Want to modify the code or build your own version?

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Nikhil135246/Download_Any_Media.git
   cd Download_Any_Media
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Download FFmpeg binaries (for bundling):
   ```bash
   # Run the download script
   download_ffmpeg.bat
   ```

### Development

Run the application in development mode:
```bash
uv run python main.py
```

## 📖 How to Use

1. **📋 Paste URL**: Enter a YouTube video or playlist URL
2. **🎯 Select Option**: Choose your preferred download format
3. **📁 Configure Path**: Use File → Settings to set your download directory (optional)
4. **⬇️ Download**: Click the Download button and watch the magic happen!

### 🎬 Download Options

- **v - Download video**: Downloads the best quality video with audio merged
- **🎵 m - Download audio only MP3**: Extracts audio and converts to MP3
- **📺 vp - Download playlist videos**: Downloads all videos in a playlist
- **🎶 mp - Download playlist audios**: Downloads all audios from a playlist as MP3

### ⚙️ Settings

Access settings via File → Settings to configure:
- **📂 Output Directory**: Choose where files are saved (default: `Downloads/YouTube-Downloads/`)
- Videos are saved to: `{output_directory}/Videos/`
- Audio files are saved to: `{output_directory}/Music/`

## 🔧 Technical Details

- **🖥️ GUI Framework**: Built with **PySide6** for modern, responsive interface
- **⬇️ Download Engine**: Uses **yt-dlp** for reliable YouTube content downloading
- **🎥 Video Processing**: **FFmpeg bundled** - no separate installation needed
- **⚡ Performance**: Threaded downloads keep the UI responsive
- **🎯 Smart Formats**: Optimal yt-dlp settings (`bestvideo+bestaudio/best`) for automatic merging
- **💾 Settings**: Persistent settings storage using QSettings
- **📦 Bundling**: PyInstaller packages everything into a single executable

## 🛠️ Building Standalone Executable

For developers who want to create their own bundled executable:

### Prerequisites
```bash
uv add --dev pyinstaller
```

### Build Process
1. **Download FFmpeg** (required for bundling):
   ```bash
   download_ffmpeg.bat
   ```

2. **Build the executable**:
   ```bash
   uv run pyinstaller YouTube-Downloader.spec
   ```

3. **Find your executable**: The bundled EXE will be created in `dist/YouTube-Downloader.exe` (~186 MB)

### 🎨 What's Bundled

Your executable includes:
- ✅ **All Python dependencies** (PySide6, yt-dlp, etc.)
- ✅ **FFmpeg binaries** (ffmpeg.exe, ffprobe.exe) 
- ✅ **Custom download icon** (48x48 resolution)
- ✅ **Smart path detection** (works from any location)

### 🔧 Icon Notes
- **Custom Icon**: Professional download icon appears in Windows Explorer, taskbar, and shortcuts
- **Cache Refresh**: If you see old icons after building, restart Windows or run `clear_icon_cache.bat`

## 📋 Requirements

### For Users
- ✅ **Windows 7/10/11** (64-bit)
- ✅ **No additional software needed** - everything is bundled!

### For Developers  
- **Python 3.8+**
- **Dependencies**: PySide6, yt-dlp, PyInstaller
- **FFmpeg**: Downloaded automatically via `download_ffmpeg.bat`

## 📸 Screenshots

> Add screenshots of your application here to show users what to expect!

## 🤝 Contributing

Found a bug or want to add a feature? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the **MIT License**.

## 🙏 Acknowledgments

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - Powerful YouTube downloading library
- **[FFmpeg](https://ffmpeg.org/)** - Essential multimedia framework
- **[PySide6](https://wiki.qt.io/Qt_for_Python)** - Modern Python GUI framework

---

**⭐ If this project helped you, please give it a star on GitHub!**
