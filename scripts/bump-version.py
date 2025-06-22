#!/usr/bin/env python3
"""
Version management script for AIWand

Usage:
    python scripts/bump-version.py patch  # 0.1.0 -> 0.1.1
    python scripts/bump-version.py minor  # 0.1.0 -> 0.2.0  
    python scripts/bump-version.py major  # 0.1.0 -> 1.0.0
"""

import sys
import os
import re
from pathlib import Path


def get_current_version():
    """Get current version from __init__.py"""
    init_path = Path("src/aiwand/__init__.py")
    with open(init_path, "r") as f:
        content = f.read()
        match = re.search(r'__version__ = ["\'](.+)["\']', content)
        if match:
            return match.group(1)
    raise RuntimeError("Version not found in __init__.py")


def bump_version(current_version, bump_type):
    """Bump version based on type"""
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError("bump_type must be 'major', 'minor', or 'patch'")


def update_version_in_file(file_path, old_version, new_version):
    """Update version in a file"""
    with open(file_path, "r") as f:
        content = f.read()
    
    content = content.replace(f'__version__ = "{old_version}"', f'__version__ = "{new_version}"')
    content = content.replace(f"__version__ = '{old_version}'", f"__version__ = '{new_version}'")
    
    with open(file_path, "w") as f:
        f.write(content)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/bump-version.py {patch|minor|major}")
        sys.exit(1)
    
    bump_type = sys.argv[1].lower()
    if bump_type not in ['patch', 'minor', 'major']:
        print("Error: bump_type must be 'patch', 'minor', or 'major'")
        sys.exit(1)
    
    try:
        current_version = get_current_version()
        new_version = bump_version(current_version, bump_type)
        
        print(f"Bumping version: {current_version} -> {new_version}")
        
        # Update version in __init__.py
        update_version_in_file("src/aiwand/__init__.py", current_version, new_version)
        
        print(f"✅ Version updated to {new_version}")
        print("\nNext steps:")
        print("1. Update CHANGELOG.md with new changes")
        print("2. Commit changes: git add . && git commit -m 'Bump version to {}'".format(new_version))
        print("3. Build and publish: python -m build && python -m twine upload dist/*")
        print("4. Push to GitHub: git push")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 