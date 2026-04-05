#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Build script to generate Pelican site and custom index.html"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def resolve_output_root(repo_root: Path) -> Path:
    """Resolve output folder from BUILD_OUTPUT_DIR env var."""
    output_dir = os.environ.get('BUILD_OUTPUT_DIR', '').strip()
    if not output_dir:
        return repo_root

    output_path = Path(output_dir)
    if not output_path.is_absolute():
        output_path = repo_root / output_path

    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def publish_assets(output_root: Path) -> None:
    """Publish static assets under /assets for templates that use /assets/* URLs."""
    theme_root = output_root / 'theme'
    assets_src = theme_root / 'assets'
    assets_dst = output_root / 'assets'

    assets_dst.mkdir(parents=True, exist_ok=True)

    # Copy directory-backed assets first (images, PDFs, project/review folders).
    if assets_src.exists():
        shutil.copytree(assets_src, assets_dst, dirs_exist_ok=True)

    # Ensure root-level css/js files also exist at /assets/*. 
    for filename in ('main.css', 'particle-network.js', 'scroll-nav.js'):
        src_file = theme_root / filename
        if src_file.exists():
            shutil.copy2(src_file, assets_dst / filename)


def publish_root_files(repo_root: Path, output_root: Path) -> None:
    """Copy root-level deployment files to output folder when needed."""
    for filename in ('CNAME', '.nojekyll'):
        src = repo_root / filename
        dst = output_root / filename
        if src.exists() and src.resolve() != dst.resolve():
            shutil.copy2(src, dst)

def build_site():
    """Build the Pelican site with custom index handling"""
    
    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    output_root = resolve_output_root(repo_root)
    theme_dir = script_dir / 'theme'
    
    # Run Pelican
    print("Building Pelican site...")
    pelican_cmd = [
        sys.executable, '-m', 'pelican',
        str(script_dir / 'content'),
        '-o', str(output_root),
        '-s', str(script_dir / 'pelicanconf.py')
    ]
    result = subprocess.run(pelican_cmd, cwd=str(script_dir))
    
    if result.returncode != 0:
        print("Pelican build failed!")
        return False

    print("Publishing assets...")
    publish_assets(output_root)
    publish_root_files(repo_root, output_root)
    
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
    index_path = output_root / 'index.html'
    index_path.write_text(html)
    print(f"Created {index_path}")
    
    return True

if __name__ == '__main__':
    success = build_site()
    sys.exit(0 if success else 1)
