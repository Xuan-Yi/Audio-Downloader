# Audio-Downloader

In an age where music streaming is the default and ownership is optional, **Audio-Downloader** takes a small step back to the "download-and-keep" era. 
While streaming platforms dominate modern listening habits, there is still something practical, and mildly nostalgic, about locally stored audio.

## Requirements

* **FFmpeg**: [pydub](https://github.com/jiaaro/pydub) requires [ffmpeg](https://ffmpeg.org/download.html) to be installed on your system path.
  ```powershell
  # Install FFmpeg first if you have not installed.
  scoop install ffmpeg
  ```

## Installation & Execution

### Option 1: Using uv (Recommended)
> This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management.
```powershell
# Install uv first if you have not installed.
scoop install uv

# Install dependencies and run automatically
uv run main.py
```

### Option 2: Using pip

```powershell
# Install dependencies
pip install PyQt6 pydub requests pandas openpyxl mutagen pytubefix

# Run the application
python main.py
```

## Introduction

A YouTube audio downloader built with **PyQt6** and **pytubefix**.

* **Supported formats**: flac, mp3, wav, and m4a.
* **Features**: Batch downloading, user-friendly UI, and export/import music list.

### Basics

1. Paste a YouTube URL into the search bar.
2. Select your desired format and output directory.
3. Click "Add" to enqueue the song.
4. Manage your downloads in the queue area; you can remove pending or finished tasks anytime.

### Import/Export music list

You can batch import songs using a spreadsheet (xlsx or csv). The program automatically skips the header row.

* Import your list via **File > Import .xlsx**. (Supports both .xlsx and .csv)
* Export your list via **File > Export as .xlsx**. (Supports both .xlsx and .csv)

**Template:**
 | Title        | Artist         | Youtube URL                           |
 | ------------ | -------------- | ------------------------------------- |
 | Song Title   | Artist Name    | <https://www.youtube.com/watch?v=...> |
 | Another Song | Another Artist | <https://www.youtube.com/watch?v=...> |
 > Title and Artist are optional, but **Youtube URL** is required.

## Copyright

* **App Icon**: [headset icons](https://www.flaticon.com/free-icons/headset) created by smalllikeart - Flaticon
