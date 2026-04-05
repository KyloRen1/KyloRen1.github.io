#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build script to generate Pelican site and custom index.html"""

import os
import sys
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

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
