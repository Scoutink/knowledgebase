#!/usr/bin/env python3
import os
import sys
import re
from bs4 import BeautifulSoup

"""
Purpose: Add a Table of Contents and stable anchors to an existing HTML file
without modifying the textual content. Output a WordPress-friendly HTML fragment.

Rules:
- Do not alter text nodes. We only add id attributes and a generated TOC block.
- Use existing headings (h1-h6). If none exist, we only decorate what's there.
- Generate anchor ids from heading text (slugify) and ensure uniqueness.
- Insert a TOC at the top wrapped in a <nav class="kb-toc"> with nested lists.
- Wrap entire content in <div class="kb-wrapper"> to avoid theme collisions.

Usage:
  python3 scripts/wp_kb_structure.py /path/to/full-kb.html > /path/to/full-kb.wp.html
"""


def slugify(text: str) -> str:
	text = text.strip().lower()
	# replace non-alphanumerics with '-'
	text = re.sub(r"[^a-z0-9]+", "-", text)
	text = text.strip('-')
	return text or 'section'


def unique_id(base: str, used: set) -> str:
	candidate = base
	index = 2
	while candidate in used:
		candidate = f"{base}-{index}"
		index += 1
	used.add(candidate)
	return candidate


def build_toc(headings):
	# headings: list of (level, id, text)
	# Build nested lists according to heading levels
	html = []
	html.append('<nav class="kb-toc" aria-label="Table of contents">')
	html.append('<h2>Contents</h2>')
	html.append('<ol class="kb-toc-list">')
	prev_level = 1
	stack = [1]
	for level, hid, text in headings:
		while level > prev_level:
			html.append('<ol>')
			stack.append(level)
			prev_level += 1
		while level < prev_level:
			html.append('</ol>')
			stack.pop()
			prev_level -= 1
		html.append(f'<li><a href="#${hid}">{text}</a></li>'.replace('#$', '#'))
	# close remaining lists
	while prev_level > 1:
		html.append('</ol>')
		prev_level -= 1
	html.append('</ol>')
	html.append('</nav>')
	return ''.join(html)


def main():
	if len(sys.argv) < 2:
		print('Usage: python3 scripts/wp_kb_structure.py /path/to/full-kb.html', file=sys.stderr)
		sys.exit(1)
	in_path = sys.argv[1]
	if not os.path.exists(in_path):
		print(f'Error: file not found: {in_path}', file=sys.stderr)
		sys.exit(2)

	with open(in_path, 'r', encoding='utf-8') as f:
		html = f.read()

	soup = BeautifulSoup(html, 'html.parser')

	# Collect headings
	headings = []
	used_ids = set()
	for tag in soup.find_all(re.compile(r'^h[1-6]$')):
		text = tag.get_text(strip=True)
		if not text:
			continue
		base = slugify(text)
		if tag.has_attr('id') and tag['id']:
			base = slugify(tag['id'])
		hid = unique_id(base, used_ids)
		tag['id'] = hid  # set id, leave text untouched
		headings.append((int(tag.name[1]), hid, text))

	# Build TOC if headings exist
	toc_html = build_toc(headings) if headings else ''

	# Wrap content
	wrapper = soup.new_tag('div', attrs={'class': 'kb-wrapper'})
	# Insert toc at top
	if toc_html:
		# Using a placeholder container to insert raw HTML
		toc_container = soup.new_tag('div')
		toc_container.append(BeautifulSoup(toc_html, 'html.parser'))
		wrapper.append(toc_container)

	# Move body children into wrapper (or entire soup if fragment)
	if soup.body:
		for child in list(soup.body.children):
			wrapper.append(child.extract())
		soup.body.clear()
		soup.body.append(wrapper)
	else:
		# Fragment: wrap the whole soup
		for child in list(soup.children):
			wrapper.append(child.extract())
		soup.clear()
		soup.append(wrapper)

	# Output
	sys.stdout.write(str(soup))

if __name__ == '__main__':
	main()