# KimCartoon Batch Downloader

A browser-based script to batch download episodes from KimCartoon.si.

## Features

- Batch download episodes from KimCartoon.si
- Select quality preferences (720p, 480p, etc.)
- Multiple output formats (plain links, wget/aria2 format, HTML page)
- Automatic retry on failures
- Captcha detection and handling

## Usage

1. Open KimCartoon.si in your browser
2. Open the browser's developer console (F12 or right-click -> Inspect -> Console)
3. Copy and paste the following code:

```javascript
$.getScript(
  "https://cdn.jsdelivr.net/gh/Dhairya3391/kimcartoon-downloader@main/kimcartoon.js"
);
```

4. Follow the prompts to:
   - Select start episode number
   - Select end episode number
   - Choose video quality preferences
   - Select output format

## Output Formats

- 0: Simple list of links
- 1: List with filenames (for wget, aria2 helper scripts)
- 2: HTML page with links

## Requirements

- Modern web browser
- jQuery (already included on KimCartoon.si)
- Internet connection

## Note

This script is for personal use only. Please respect the website's terms of service and copyright laws.

# kimcartoon-downloader
