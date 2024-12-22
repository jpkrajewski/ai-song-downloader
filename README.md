# AI Song Downloader 🎵
AI Song Downloader is a Python-based tool that uses AI to generate song titles based on prompts, fetch their YouTube URLs, and download them as MP3 files. It also supports downloading songs directly from YouTube playlists. The project is powered by Typer for the CLI and leverages advanced AI-based music recommendation.

# Features 🚀
- 🎧 Generate Song Titles from Prompts: Provide a creative prompt, and AI will suggest song titles.
- 🔗 Fetch YouTube URLs: Automatically search YouTube for the generated songs and retrieve their URLs.
- ⬇️ Download MP3 Files: Download songs in MP3 format with high-quality audio processing.
- 🎶 Support for YouTube Playlists: Directly download MP3s from a YouTube playlist URL.
- 🛠️ Customizable: Easily extendable to use different AI providers or custom YouTube URL extraction methods.

# Requirements 📋
Python 3.10+
UV for dependency management

# Installation 🛠️
Clone the repository:

```bash
git clone https://github.com/yourusername/ai-song-downloader.git
cd ai-song-downloader
```

# Usage 💻
The tool provides a command-line interface (CLI) to interact with the application.

### Commands
Get Songs from Prompt:

Use this command to generate song titles based on an AI prompt and download them as MP3s:

```bash
uv run main.py from-prompt "Your creative prompt here"
```

Example:

```bash
uv run aisd/src/cli.py from-prompt "summer party DJ mix"
```

### Download from Playlist:

Provide a YouTube playlist URL to download all songs as MP3 files:

```bash
uv run aisd/src/cli.py from-playlist "https://www.youtube.com/playlist?list=YOUR_PLAYL
```

# Development 🛠️
Run tests using pytest:

```bash
pytest
```

Run the pre-commit hooks:

```bash
pre-commit install
```

# Configuration 🔧
AI provider logic can be customized by implementing your own provider in the src/ai/providers directory.

# Acknowledgments 🙏
Inspired by the desire to blend AI with music downloading.
Built using Typer for CLI and UV for dependency management.
