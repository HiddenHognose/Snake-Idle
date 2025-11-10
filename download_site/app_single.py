#!/usr/bin/env python3
"""
Single-file Flask application for Snake Idle download site.
Contains all HTML, CSS, and JavaScript inline.
"""
from flask import Flask, send_file, jsonify
from flask import render_template_string, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['VERSIONS_FILE'] = 'versions.json'

# Ensure downloads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Embedded HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snake Idle - Downloads</title>
    <style>
{{ css }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐍 Snake Idle</h1>
            <p class="subtitle">Hatch Your Collection!</p>
        </header>

        <main>
            <section class="about-coder">
                <h2>About the Coder</h2>
                <div class="coder-content">
                    <div class="coder-photo">
                        <img src="/static/coder_photo.jpeg" alt="HiddenHognose">
                    </div>
                    <div class="coder-text">
                        <p class="coder-greeting">Hey! My name's <strong>HiddenHognose</strong>, and I'm a small single-person game dev!</p>
                        <p>This game (which I referred to while coding it as "snake cookie clicker") was made specifically with <strong>Emily & Ed from Snake Discovery</strong> in mind.</p>
                    </div>
                </div>
            </section>

            <section class="info">
                <h2>System Requirements</h2>
                <ul>
                    <li>Python 3.8 or higher</li>
                    <li>Pygame library</li>
                    <li>Windows, Linux, or macOS</li>
                </ul>
            </section>

            <section class="intro">
                <h2>Download the Game</h2>
                <p>Choose a version below to download and start hatching snakes!</p>
            </section>

            <section class="versions">
                {% if versions %}
                    {% for version in versions %}
                    <div class="version-card {% if version.legacy %}legacy-version{% endif %}">
                        <div class="version-header">
                            <h3>{% if version.legacy %}Legacy: {% endif %}Version {{ version.version }}</h3>
                            <span class="version-date">{{ version.date }}</span>
                        </div>
                        <div class="version-info">
                            <p class="version-description">{{ version.description }}</p>
                            <div class="version-details">
                                <span class="file-size">{{ version.size }}</span>
                                {% if version.platform %}
                                <span class="platform">{{ version.platform }}</span>
                                {% endif %}
                            </div>
                        </div>
                        <div class="version-actions">
                            <a href="/download/{{ version.version }}" class="download-btn">
                                Download
                            </a>
                            {% if version.changelog %}
                            <button class="changelog-btn" onclick="toggleChangelog('{{ version.version }}')">
                                Changelog
                            </button>
                            {% endif %}
                        </div>
                        {% if version.changelog %}
                        <div class="changelog" id="changelog-{{ version.version }}" style="display: none;">
                            <h4>What's New:</h4>
                            <ul>
                                {% for change in version.changelog %}
                                <li>{{ change }}</li>
                                {% endfor %}
                            </ul>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-versions">
                        <p>No versions available yet. Check back soon!</p>
                    </div>
                {% endif %}
            </section>
        </main>

        <footer>
            <p>&copy; 2024 Snake Idle. All rights reserved.</p>
        </footer>
    </div>

    <script>
        function toggleChangelog(version) {
            const changelog = document.getElementById('changelog-' + version);
            if (changelog.style.display === 'none') {
                changelog.style.display = 'block';
            } else {
                changelog.style.display = 'none';
            }
        }
    </script>
</body>
</html>"""

# Embedded CSS
CSS_STYLES = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1a5f3f 0%, #2d8659 50%, #1a5f3f 100%);
    color: #fff;
    min-height: 100vh;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    text-align: center;
    padding: 40px 20px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 15px;
    margin-bottom: 40px;
    backdrop-filter: blur(10px);
}

header h1 {
    font-size: 3em;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.subtitle {
    font-size: 1.2em;
    opacity: 0.9;
}

main {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 15px;
    padding: 30px;
    margin-bottom: 30px;
}

.about-coder {
    background: rgba(0, 0, 0, 0.2);
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 30px;
}

.about-coder h2 {
    margin-bottom: 20px;
    color: #ffd700;
    text-align: center;
}

.coder-content {
    display: flex;
    gap: 30px;
    align-items: center;
    flex-wrap: wrap;
}

.coder-photo {
    flex-shrink: 0;
}

.coder-photo img {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 50%;
    border: 4px solid rgba(255, 215, 0, 0.5);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.coder-text {
    flex: 1;
    min-width: 300px;
}

.coder-text p {
    margin-bottom: 15px;
    font-size: 1.1em;
    line-height: 1.8;
}

.coder-greeting {
    font-size: 1.2em !important;
    font-weight: bold;
}

.coder-text strong {
    color: #ffd700;
}

.info {
    background: rgba(0, 0, 0, 0.2);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 30px;
}

.info h2 {
    margin-bottom: 15px;
    color: #ffd700;
}

.info ul {
    list-style-position: inside;
    padding-left: 10px;
}

.info li {
    margin-bottom: 8px;
}

.intro {
    text-align: center;
    margin-bottom: 30px;
    margin-top: 20px;
}

.intro h2 {
    font-size: 2em;
    margin-bottom: 10px;
}

.versions {
    display: grid;
    gap: 20px;
    margin-bottom: 40px;
}

.version-card {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 25px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.version-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.4);
}

.version-card.legacy-version {
    border-color: rgba(200, 200, 200, 0.3);
    background: rgba(255, 255, 255, 0.05);
    opacity: 0.9;
}

.version-card.legacy-version .version-header h3 {
    color: #ccc;
}

.version-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.version-header h3 {
    font-size: 1.8em;
    color: #ffd700;
}

.version-date {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9em;
}

.version-info {
    margin-bottom: 20px;
}

.version-description {
    margin-bottom: 10px;
    font-size: 1.1em;
}

.version-details {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
}

.file-size, .platform {
    background: rgba(255, 255, 255, 0.1);
    padding: 5px 12px;
    border-radius: 5px;
    font-size: 0.9em;
}

.platform {
    background: rgba(100, 200, 255, 0.2);
}

.version-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.download-btn, .changelog-btn {
    padding: 12px 30px;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
    font-weight: bold;
}

.download-btn {
    background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
    color: #1a5f3f;
    box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.download-btn:hover {
    background: linear-gradient(135deg, #ffed4e 0%, #ffd700 100%);
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.5);
}

.changelog-btn {
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.changelog-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

.changelog {
    margin-top: 20px;
    padding: 15px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    border-left: 4px solid #ffd700;
}

.changelog h4 {
    margin-bottom: 10px;
    color: #ffd700;
}

.changelog ul {
    list-style-position: inside;
    padding-left: 10px;
}

.changelog li {
    margin-bottom: 5px;
}

.no-versions {
    text-align: center;
    padding: 40px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
}

footer {
    text-align: center;
    padding: 20px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9em;
}

@media (max-width: 768px) {
    header h1 {
        font-size: 2em;
    }
    
    .version-header {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .version-actions {
        width: 100%;
    }
    
    .download-btn, .changelog-btn {
        flex: 1;
        text-align: center;
    }
    
    .coder-content {
        flex-direction: column;
        text-align: center;
    }
    
    .coder-photo {
        margin: 0 auto;
    }
}"""

def load_versions():
    """Load version information from JSON file"""
    if os.path.exists(app.config['VERSIONS_FILE']):
        with open(app.config['VERSIONS_FILE'], 'r') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    """Main download page"""
    versions = load_versions()
    # Sort: non-legacy first (newest first), then legacy
    non_legacy = [v for v in versions if not v.get('legacy', False)]
    legacy = [v for v in versions if v.get('legacy', False)]
    non_legacy.sort(key=lambda x: x.get('version', '0'), reverse=True)
    versions = non_legacy + legacy
    
    # Render template with embedded CSS
    return render_template_string(HTML_TEMPLATE.replace('{{ css }}', CSS_STYLES), versions=versions)

@app.route('/download/<version>')
def download(version):
    """Download a specific version"""
    versions = load_versions()
    version_info = next((v for v in versions if v['version'] == version), None)
    
    if not version_info:
        return "Version not found", 404
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], version_info['filename'])
    
    if not os.path.exists(file_path):
        return "File not found", 404
    
    return send_file(file_path, as_attachment=True, download_name=version_info['filename'])

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (like coder photo)"""
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_dir, filename)

@app.route('/api/versions')
def api_versions():
    """API endpoint to get all versions"""
    versions = load_versions()
    non_legacy = [v for v in versions if not v.get('legacy', False)]
    legacy = [v for v in versions if v.get('legacy', False)]
    non_legacy.sort(key=lambda x: x.get('version', '0'), reverse=True)
    versions = non_legacy + legacy
    return jsonify(versions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

