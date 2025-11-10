#!/usr/bin/env python3
"""
Helper script to add a new version to the download site
"""
import json
import os
import sys
from datetime import datetime

VERSIONS_FILE = 'versions.json'

def get_file_size(filename):
    """Get human-readable file size"""
    size = os.path.getsize(filename)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def add_version():
    """Interactive script to add a new version"""
    print("Add New Version to Download Site")
    print("=" * 40)
    
    # Load existing versions
    if os.path.exists(VERSIONS_FILE):
        with open(VERSIONS_FILE, 'r') as f:
            versions = json.load(f)
    else:
        versions = []
    
    # Get version info
    version = input("Version number (e.g., 1.0.1): ").strip()
    if not version:
        print("Version number is required!")
        return
    
    # Check if version already exists
    if any(v['version'] == version for v in versions):
        response = input(f"Version {version} already exists. Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return
        versions = [v for v in versions if v['version'] != version]
    
    description = input("Description: ").strip()
    if not description:
        description = f"Version {version} release"
    
    filename = input("Filename in downloads/ directory: ").strip()
    if not filename:
        print("Filename is required!")
        return
    
    # Check if file exists
    filepath = os.path.join('downloads', filename)
    if not os.path.exists(filepath):
        print(f"Warning: File {filepath} does not exist!")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return
        size = "Unknown"
    else:
        size = get_file_size(filepath)
    
    platform = input("Platform (optional, press Enter to skip): ").strip()
    if not platform:
        platform = "All Platforms"
    
    # Get changelog
    print("\nEnter changelog items (one per line, empty line to finish):")
    changelog = []
    while True:
        item = input("  - ").strip()
        if not item:
            break
        changelog.append(item)
    
    # Create version entry
    version_entry = {
        "version": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "filename": filename,
        "size": size,
        "platform": platform
    }
    
    if changelog:
        version_entry["changelog"] = changelog
    
    # Add to versions list
    versions.append(version_entry)
    
    # Save
    with open(VERSIONS_FILE, 'w') as f:
        json.dump(versions, f, indent=2)
    
    print(f"\n✓ Version {version} added successfully!")
    print(f"  File: {filename}")
    print(f"  Size: {size}")

if __name__ == '__main__':
    try:
        add_version()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)

