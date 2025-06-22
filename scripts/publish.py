#!/usr/bin/env python3
"""
Publishing script for AIWand

This script automates the build and publish process for PyPI.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Command: {cmd}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def get_current_version():
    """Get current version from __init__.py"""
    init_path = Path("src/aiwand/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()
        import re
        match = re.search(r'__version__ = ["\'](.+)["\']', content)
        if match:
            return match.group(1)
    raise RuntimeError("Version not found in __init__.py")


def check_git_status():
    """Check if git working directory is clean"""
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("❌ Git working directory is not clean. Please commit your changes first.")
        print("Uncommitted changes:")
        print(result.stdout)
        sys.exit(1)
    print("✅ Git working directory is clean")


def main():
    print("🪄 AIWand Publishing Script")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("src/aiwand/__init__.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Get current version
    try:
        version = get_current_version()
        print(f"📦 Current version: {version}")
    except Exception as e:
        print(f"❌ Error getting version: {e}")
        sys.exit(1)
    
    # Check git status
    check_git_status()
    
    # Check if build and twine are installed
    try:
        subprocess.run("python -m build --version", shell=True, check=True, capture_output=True)
        subprocess.run("python -m twine --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ build and twine are required. Installing...")
        run_command("pip install build twine", "Installing build tools")
    
    # Clean previous builds
    if Path("dist").exists():
        print("🧹 Cleaning previous builds...")
        shutil.rmtree("dist")
    
    if Path("build").exists():
        shutil.rmtree("build")
        
    for egg_info in Path(".").glob("src/*.egg-info"):
        shutil.rmtree(egg_info)
    
    # Run tests
    run_command("python test_install.py", "Running installation tests")
    
    # Build the package
    run_command("python -m build", "Building package")
    
    # Check if dist files were created
    dist_files = list(Path("dist").glob("*"))
    if not dist_files:
        print("❌ No distribution files were created")
        sys.exit(1)
    
    print(f"📦 Built files:")
    for file in dist_files:
        print(f"  - {file}")
    
    # Ask for confirmation
    print(f"\n🚀 Ready to publish version {version} to PyPI")
    print("This will:")
    print("1. Upload to PyPI")
    print("2. Create a git tag")
    print("3. Push to GitHub")
    
    response = input("\nProceed? (y/N): ").lower().strip()
    if response != 'y':
        print("❌ Publishing cancelled")
        sys.exit(0)
    
    # Upload to PyPI
    run_command("python -m twine upload dist/*", "Uploading to PyPI")
    
    # Create git tag
    run_command(f"git tag v{version}", f"Creating git tag v{version}")
    
    # Push to GitHub
    run_command("git push", "Pushing to GitHub")
    run_command("git push --tags", "Pushing tags to GitHub")
    
    print("\n🎉 Publishing completed successfully!")
    print(f"✅ Version {version} is now live on PyPI")
    print(f"✅ Git tag v{version} created and pushed")
    print(f"🔗 PyPI: https://pypi.org/project/aiwand/{version}/")
    print(f"🔗 GitHub: https://github.com/onlyoneaman/aiwand/releases/tag/v{version}")


if __name__ == "__main__":
    main() 