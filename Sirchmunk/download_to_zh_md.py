import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

urls = [
    ("in-context-search", "https://modelscope.github.io/sirchmunk-web/zh/blog/in-context-search/"),
    ("technical-deep-dive", "https://modelscope.github.io/sirchmunk-web/zh/blog/technical-deep-dive/"),
    ("v2.0.0", "https://modelscope.github.io/sirchmunk-web/zh/blog/v2.0.0/"),
    ("v1.0.0", "https://modelscope.github.io/sirchmunk-web/zh/blog/v1.0.0/")
]

output_dir = "/Users/bowhead/agentic_rag/Sirchmunk/raw_blog"
os.makedirs(output_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

for slug, url in urls:
    print(f"Fetching {url}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    article = soup.find('article')
    if not article:
        print(f"Could not find article for {url}")
        continue
        
    title_element = article.find('h1')
    prose = article.find('div', class_='prose')
    
    # We might miss the hero image if it's outside prose.
    # Let's find images inside article but before prose.
    hero_imgs = []
    if prose:
        for element in article.find_all('img'):
            if element not in prose.find_all('img'):
                hero_imgs.append(element)
    
    # build a new container to markdownify
    content = BeautifulSoup("<div></div>", "html.parser").div
    if title_element:
        content.append(title_element)
        
    for img in hero_imgs:
        content.append(img)
        
    if prose:
        content.append(prose)
    else:
        # Fallback to article if no prose found
        content = article

    # fix relative image links
    for img in content.find_all('img'):
        src = img.get('src')
        if src and not src.startswith('http') and not src.startswith('#') and not src.startswith('data:'):
            if src.startswith('/'):
                img['src'] = "https://modelscope.github.io" + src
            else:
                img['src'] = url.rstrip('/') + '/' + src
                
    # fix relative text links
    for a in content.find_all('a'):
        href = a.get('href')
        if href and not href.startswith('http') and not href.startswith('#') and not href.startswith('mailto:'):
            if href.startswith('/'):
                a['href'] = "https://modelscope.github.io" + href
            else:
                a['href'] = url.rstrip('/') + '/' + href
    
    # remove duplicate empty lines and some markdownify artifacts
    markdown_text = md(str(content), heading_style="ATX", strip=['script', 'style'])
    
    filepath = os.path.join(output_dir, slug + '.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write((markdown_text or '').strip())

    print(f"Saved {filepath}")
