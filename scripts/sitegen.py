#!/usr/bin/env python3
import os
import json
import shutil
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pdfminer.high_level import extract_text

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONTENT_EXTS = {'.pdf'}
SITE_DIR = os.path.join(REPO_ROOT, 'site')
FILES_DIR = os.path.join(SITE_DIR, 'files')
DOCS_DIR = os.path.join(SITE_DIR, 'docs')
TEMPLATES_DIR = os.path.join(REPO_ROOT, 'templates')
STATIC_DIR = os.path.join(REPO_ROOT, 'static')


def human_size(num_bytes: int) -> str:
	units = ['B', 'KB', 'MB', 'GB']
	size = float(num_bytes)
	for unit in units:
		if size < 1024:
			return f"{size:.1f} {unit}"
		size /= 1024
	return f"{size:.1f} TB"


def safe_slug(name: str) -> str:
	base = os.path.splitext(os.path.basename(name))[0]
	return ''.join(ch if ch.isalnum() or ch in ('-', '_') else '-' for ch in base).strip('-_').lower()


def find_pdfs(root: str) -> List[str]:
	pdfs = []
	for entry in os.listdir(root):
		path = os.path.join(root, entry)
		if os.path.isfile(path) and path.lower().endswith('.pdf'):
			pdfs.append(path)
	return pdfs


def extract_text_per_page(pdf_path: str) -> List[str]:
	# pdfminer.six high-level API extracts full text; to keep simple and
	# avoid content transformation, we extract full text and split on form feed.
	# If form feed not present, we fallback to a single page chunk.
	text = extract_text(pdf_path) or ''
	pages = [p.strip() for p in text.split('\f') if p.strip()]
	if not pages:
		pages = ['']
	return pages


def build_environment() -> Environment:
	return Environment(
		loader=FileSystemLoader(TEMPLATES_DIR),
		autoescape=select_autoescape(['html', 'xml'])
	)


def copy_static():
	os.makedirs(SITE_DIR, exist_ok=True)
	# Copy static assets
	dst_static = os.path.join(SITE_DIR, 'static')
	if os.path.exists(dst_static):
		shutil.rmtree(dst_static)
	shutil.copytree(STATIC_DIR, dst_static)


def render_templates(env: Environment, template_name: str, context: Dict[str, Any], out_path: str):
	tpl = env.get_template(template_name)
	os.makedirs(os.path.dirname(out_path), exist_ok=True)
	with open(out_path, 'w', encoding='utf-8') as f:
		f.write(tpl.render(**context))


def replicate_to_root():
	# Make root-level copies to support servers that serve repo root
	# Files
	for fname in ('index.html', 'index.json', 'robots.txt', 'sitemap.xml'):
		src = os.path.join(SITE_DIR, fname)
		dst = os.path.join(REPO_ROOT, fname)
		if os.path.exists(src):
			shutil.copy2(src, dst)
	# Directories
	for dname in ('static', 'docs', 'files'):
		src_dir = os.path.join(SITE_DIR, dname)
		dst_dir = os.path.join(REPO_ROOT, dname)
		if os.path.exists(src_dir):
			if os.path.exists(dst_dir):
				shutil.rmtree(dst_dir)
			shutil.copytree(src_dir, dst_dir)


def main():
	os.makedirs(SITE_DIR, exist_ok=True)
	os.makedirs(FILES_DIR, exist_ok=True)
	os.makedirs(DOCS_DIR, exist_ok=True)

	env = build_environment()
	build_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

	pdf_paths = find_pdfs(REPO_ROOT)
	documents: List[Dict[str, Any]] = []
	chunks: List[Dict[str, Any]] = []

	for pdf_path in sorted(pdf_paths):
		filename = os.path.basename(pdf_path)
		slug = safe_slug(filename)
		stat = os.stat(pdf_path)
		size_h = human_size(stat.st_size)
		# Copy original PDF to site/files
		dst_file = os.path.join(FILES_DIR, filename)
		shutil.copy2(pdf_path, dst_file)
		filename_url = urllib.parse.quote(filename)
		# Extract text into per-page list
		text_pages = extract_text_per_page(pdf_path)
		for idx, page_text in enumerate(text_pages, start=1):
			chunks.append({
				'slug': slug,
				'page': idx,
				'text': page_text,
				'filename': filename,
			})
		documents.append({
			'slug': slug,
			'title': os.path.splitext(filename)[0],
			'filename': filename,
			'filename_url': filename_url,
			'pages': len(text_pages),
			'size_bytes': stat.st_size,
			'size_human': size_h,
			'text_pages': text_pages,
		})

	# Render per-document pages
	for doc in documents:
		render_templates(env, 'doc.html', {
			'title': doc['title'],
			'base_path': '../',
			'build_time': build_time,
			'doc': doc,
		}, os.path.join(DOCS_DIR, f"{doc['slug']}.html"))

	# Render index
	render_templates(env, 'index.html', {
		'title': 'Repository Knowledge Base',
		'base_path': './',
		'build_time': build_time,
		'documents': documents,
	}, os.path.join(SITE_DIR, 'index.html'))

	# Write index.json for AI ingestion and client search
	with open(os.path.join(SITE_DIR, 'index.json'), 'w', encoding='utf-8') as f:
		json.dump({
			'generated_at': build_time,
			'documents': [
				{ 'slug': d['slug'], 'title': d['title'], 'pages': d['pages'], 'size_human': d['size_human'] }
				for d in documents
			],
			'chunks': chunks
		}, f, ensure_ascii=False)

	# robots and sitemap
	with open(os.path.join(SITE_DIR, 'robots.txt'), 'w', encoding='utf-8') as f:
		f.write('User-agent: *\nAllow: /\nSitemap: ./sitemap.xml\n')

	# sitemap.xml
	base_urls = ['index.html', 'index.json', 'robots.txt']
	urls = [f"./{u}" for u in base_urls]
	urls += [f"./docs/{d['slug']}.html" for d in documents]
	xml = [
		'<?xml version="1.0" encoding="UTF-8"?>',
		'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
	]
	for u in urls:
		xml.append('<url>')
		xml.append(f'<loc>{u}</loc>')
		xml.append('</url>')
	xml.append('</urlset>')
	with open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w', encoding='utf-8') as f:
		f.write('\n'.join(xml))

	copy_static()
	replicate_to_root()
	print(f"Generated site at {SITE_DIR} with {len(documents)} documents and replicated to repo root.")

if __name__ == '__main__':
	main()