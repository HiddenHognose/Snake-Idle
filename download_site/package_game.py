#!/usr/bin/env python3
"""
Script to package the game for distribution
"""
import os
import shutil
import zipfile
from datetime import datetime

def package_game(version, output_dir='downloads'):
    """Package the game into a zip file"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Files to include
    files_to_include = [
        'snake_idle_pygame.py',
        'requirements.txt',
        'README.md',
    ]
    
    # Directories to include
    dirs_to_include = [
        'images',
    ]
    
    # Optional files/dirs
    optional_items = [
        'background.png',
        'snaketummy.png',
        'education.png',
        'locked.png',
        'memes',
    ]
    
    # Check what exists
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create zip filename
    zip_filename = f'snake_idle_v{version}.zip'
    zip_path = os.path.join(output_dir, zip_filename)
    
    print(f"Packaging game version {version}...")
    print(f"Output: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add required files
        for item in files_to_include:
            item_path = os.path.join(root_dir, item)
            if os.path.exists(item_path):
                if os.path.isfile(item_path):
                    zipf.write(item_path, item)
                    print(f"  Added: {item}")
                else:
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.join(item, os.path.relpath(file_path, item_path))
                            zipf.write(file_path, arcname)
                    print(f"  Added directory: {item}/")
            else:
                print(f"  Warning: {item} not found, skipping")
        
        # Add required directories
        for item in dirs_to_include:
            item_path = os.path.join(root_dir, item)
            if os.path.exists(item_path):
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(item, os.path.relpath(file_path, item_path))
                        zipf.write(file_path, arcname)
                print(f"  Added directory: {item}/")
            else:
                print(f"  Warning: {item} not found, skipping")
        
        # Add optional items if they exist
        for item in optional_items:
            item_path = os.path.join(root_dir, item)
            if os.path.exists(item_path):
                if os.path.isfile(item_path):
                    zipf.write(item_path, item)
                    print(f"  Added (optional): {item}")
                else:
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.join(item, os.path.relpath(file_path, item_path))
                            zipf.write(file_path, arcname)
                    print(f"  Added directory (optional): {item}/")
    
    # Get file size
    size = os.path.getsize(zip_path)
    size_mb = size / (1024 * 1024)
    
    print(f"\n✓ Package created successfully!")
    print(f"  File: {zip_filename}")
    print(f"  Size: {size_mb:.2f} MB")
    print(f"\nNext steps:")
    print(f"  1. Run: python add_version.py")
    print(f"  2. Enter version: {version}")
    print(f"  3. Enter filename: {zip_filename}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python package_game.py <version>")
        print("Example: python package_game.py 1.0.0")
        sys.exit(1)
    
    version = sys.argv[1]
    package_game(version)

