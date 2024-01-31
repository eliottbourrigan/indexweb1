from bs4 import BeautifulSoup
from lxml import etree

def extract_links(content):
    """
    Extracts links from HTML content.
    """
    # Parse HTML with BeautifulSoup
    links = []
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extracting links from anchor tags
    for anchor_tag in soup.find_all('a', href=True):
        links.append(anchor_tag['href'])
    
    return links

# Example usage
if __name__ == '__main__':
    # Extracting links from example HTML content
    example_html_content = """<body><a href="https://ensai.fr/page1"></a></body>"""
    extracted_links = extract_links(example_html_content)
    print(' '.join(extracted_links))