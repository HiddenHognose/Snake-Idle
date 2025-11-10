# Quick Start Guide

## First Time Setup

1. **Install Flask:**
   ```bash
   pip install flask
   ```
   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   cd download_site
   python app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5000`

## Adding Your First Version

### Option 1: Use the helper scripts (Recommended)

1. **Package the game:**
   ```bash
   cd download_site
   python package_game.py 1.0.0
   ```
   This creates `downloads/snake_idle_v1.0.0.zip`

2. **Add version info:**
   ```bash
   python add_version.py
   ```
   Follow the prompts to enter version details.

### Option 2: Manual

1. **Create a zip file** with your game files and place it in `downloads/`

2. **Edit `versions.json`** and add an entry:
   ```json
   {
     "version": "1.0.0",
     "date": "2024-01-15",
     "description": "Initial release",
     "filename": "snake_idle_v1.0.0.zip",
     "size": "2.5 MB",
     "platform": "All Platforms",
     "changelog": [
       "Initial release",
       "Full game features"
     ]
   }
   ```

## Testing

1. Start the server: `python app.py`
2. Visit `http://localhost:5000`
3. Click "Download" on a version to test the download
4. Check that files are served correctly

## Production Deployment

For a production server:

1. **Use Gunicorn:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Or use systemd service** (Linux):
   Create `/etc/systemd/system/snake-idle-downloads.service`:
   ```ini
   [Unit]
   Description=Snake Idle Download Site
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/download_site
   ExecStart=/usr/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Set up Nginx reverse proxy:**
   ```nginx
   server {
       listen 80;
       server_name downloads.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## File Structure

```
download_site/
├── app.py                 # Flask application
├── versions.json          # Version metadata
├── requirements.txt       # Python dependencies
├── package_game.py        # Script to package game
├── add_version.py         # Script to add versions
├── downloads/             # Game files go here
├── templates/
│   └── index.html         # Main page template
└── static/
    └── style.css          # Styling
```

## Tips

- Keep `versions.json` in version control
- Don't commit large game files to git (use `.gitignore`)
- Use descriptive version numbers (semantic versioning: MAJOR.MINOR.PATCH)
- Always test downloads before deploying
- Consider adding analytics to track downloads

