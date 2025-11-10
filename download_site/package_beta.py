#!/usr/bin/env python3
"""
Script to package the Beta_1 version from git commit
"""
import os
import shutil
import zipfile
import subprocess
import tempfile

def package_beta_version(commit_hash='524bae9', output_dir='downloads'):
    """Package the Beta_1 version from a specific commit"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the script's directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Create temporary directory for checkout
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Checking out commit {commit_hash}...")
        
        # Clone to temp directory
        result = subprocess.run(
            ['git', 'clone', project_root, temp_dir],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error cloning: {result.stderr}")
            return False
        
        # Checkout the specific commit
        result = subprocess.run(
            ['git', 'checkout', commit_hash],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Error checking out commit: {result.stderr}")
            return False
        
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
        
        # Create zip filename
        zip_filename = 'snake_idle_beta1.zip'
        zip_path = os.path.join(script_dir, output_dir, zip_filename)
        
        print(f"Packaging Beta_1 version...")
        print(f"Output: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add required files
            for item in files_to_include:
                item_path = os.path.join(temp_dir, item)
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
                item_path = os.path.join(temp_dir, item)
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
                item_path = os.path.join(temp_dir, item)
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
        
        print(f"\n✓ Beta_1 package created successfully!")
        print(f"  File: {zip_filename}")
        print(f"  Size: {size_mb:.2f} MB")
        return True

if __name__ == '__main__':
    package_beta_version()

