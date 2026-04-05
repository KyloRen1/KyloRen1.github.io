#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build script to generate Pelican site and custom index.html"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def rebuild_assets_dir(repo_root: Path) -> None:
    """Build a root /assets folder expected by existing content URLs."""

    static_dir = repo_root / 'static'
    theme_dir = repo_root / 'theme'
    assets_dir = repo_root / 'assets'

    if assets_dir.exists():
        shutil.rmtree(assets_dir)
    assets_dir.mkdir(parents=True, exist_ok=True)

    if static_dir.exists():
        for path in static_dir.rglob('*'):
            if not path.is_file():
                continue
            destination = assets_dir / path.relative_to(static_dir)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)

    # Ensure compiled theme files are present at the expected /assets URLs.
    for filename in ('main.css', 'particle-network.js', 'scroll-nav.js'):
        source = theme_dir / filename
        if source.exists():
            shutil.copy2(source, assets_dir / filename)

def build_site():
    """Build the Pelican site with custom index handling"""
    
    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    theme_dir = script_dir / 'theme'
    
    # Run Pelican
    print("Building Pelican site...")
    pelican_cmd = [
        sys.executable, '-m', 'pelican',
        str(script_dir / 'content'),
        '-o', str(repo_root),
        '-s', str(script_dir / 'pelicanconf.py')
    ]
    result = subprocess.run(pelican_cmd, cwd=str(script_dir))
    
    if result.returncode != 0:
        print("Pelican build failed!")
        return False

    # Populate /assets to keep legacy links in templates and markdown working.
    rebuild_assets_dir(repo_root)
    
    # Generate custom index.html
    print("Generating index.html...")
    env = Environment(loader=FileSystemLoader(str(theme_dir / 'templates')))
    template = env.get_template('index.html')
    
    # Load config for template variables
    import importlib.util
    spec = importlib.util.spec_from_file_location("pelicanconf", str(script_dir / 'pelicanconf.py'))
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    # Render template
    context = {
        'AUTHOR': config.AUTHOR,
        'SITENAME': config.SITENAME,
        'SITESUBTITLE': config.SITESUBTITLE,
        'SITEURL': config.SITEURL,
        'SOCIAL': config.SOCIAL,
    }
    
    html = template.render(**context)
    
    # Write index.html
    index_path = repo_root / 'index.html'
    index_path.write_text(html)
    print(f"Created {index_path}")
    
    return True

if __name__ == '__main__':
    success = build_site()
    sys.exit(0 if success else 1)