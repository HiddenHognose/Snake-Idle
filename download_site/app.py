from flask import Flask, render_template, send_file, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['VERSIONS_FILE'] = 'versions.json'

# Ensure downloads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def load_versions():
    """Load version information from JSON file"""
    if os.path.exists(app.config['VERSIONS_FILE']):
        with open(app.config['VERSIONS_FILE'], 'r') as f:
            return json.load(f)
    return []

def save_versions(versions):
    """Save version information to JSON file"""
    with open(app.config['VERSIONS_FILE'], 'w') as f:
        json.dump(versions, f, indent=2)

@app.route('/')
def index():
    """Main download page"""
    versions = load_versions()
    # Sort: non-legacy versions first (newest first), then legacy versions
    def sort_key(v):
        is_legacy = v.get('legacy', False)
        version = v.get('version', '0')
        # Return tuple: (is_legacy, -version_number) so legacy comes after
        # For non-legacy, we want newest first, so we'll sort by version descending
        # For legacy, we want them at the end
        return (is_legacy, version)
    
    # Sort: legacy versions go to the end, non-legacy sorted by version (newest first)
    versions.sort(key=lambda x: (x.get('legacy', False), x.get('version', '0')), reverse=False)
    # Now reverse non-legacy versions to get newest first
    non_legacy = [v for v in versions if not v.get('legacy', False)]
    legacy = [v for v in versions if v.get('legacy', False)]
    # Sort non-legacy by version descending (newest first)
    non_legacy.sort(key=lambda x: x.get('version', '0'), reverse=True)
    versions = non_legacy + legacy
    return render_template('index.html', versions=versions)

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

@app.route('/api/versions')
def api_versions():
    """API endpoint to get all versions"""
    versions = load_versions()
    # Sort: non-legacy first (newest first), then legacy
    non_legacy = [v for v in versions if not v.get('legacy', False)]
    legacy = [v for v in versions if v.get('legacy', False)]
    non_legacy.sort(key=lambda x: x.get('version', '0'), reverse=True)
    versions = non_legacy + legacy
    return jsonify(versions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

