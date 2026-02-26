import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

urls = [
    "https://modelscope.github.io/sirchmunk-web/blog/in-context-search/",
    "https://modelscope.github.io/sirchmunk-web/blog/technical-deep-dive/",
    "https://modelscope.github.io/sirchmunk-web/blog/v2.0.0/",
    "https://modelscope.github.io/sirchmunk-web/blog/v1.0.0/"
]

output_dir = "/Users/bowhead/agentic_rag/Sirchmunk/raw_blog"
os.makedirs(output_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

for url in urls:
    print(f"Fetching {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to find the exact content div for Hugo Blox/Academic
    content = soup.find('div', class_='article-style')
    if not content:
        content = soup.find('div', class_='article-container')
    if not content:
        content = soup.find('article')
    if not content:
        content = soup.find('main')
    
    if content:
        # fix relative image links
        for img in content.find_all('img'):
            src = img.get('src')
            if src and not src.startswith('http'):
                if src.startswith('/'):
                    img['src'] = "https://modelscope.github.io" + src
                else:
                    img['src'] = url.rstrip('/') + '/' + src
                    
        # fix relative text links
        for a in content.find_all('a'):
            href = a.get('href')
            if href and not href.startswith('http') and not href.startswith('#'):
                if href.startswith('/'):
                    a['href'] = "https://modelscope.github.io" + href
                else:
                    a['href'] = url.rstrip('/') + '/' + href
    
    markdown_text = md(str(content) if content else str(soup.body), heading_style="ATX", strip=['script', 'style'])
    
    filename = url.strip('/').split('/')[-1] + '.md'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write((markdown_text or '').strip())

    print(f"Saved {filepath}")

# clean up .txt files
for f in os.listdir(output_dir):
    if f.endswith('.txt'):
        os.remove(os.path.join(output_dir, f))
        print(f"Removed old .txt file: {f}")
