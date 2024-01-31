import time
import logging
import sqlite3
import requests
from bs4 import BeautifulSoup
from lxml import etree
from threading import Thread
from urllib import robotparser, error, parse
from utils.pagedownloader import download_page
from utils.linksextractor import extract_links

class WebCrawler:
    def __init__(self, base_url, max_urls=50, n_threads=1, politeness_delay=3, max_url_per_page=5):
        """
        Initializes the WebCrawler.
        """
        self.base_url = base_url
        self.max_urls = max_urls
        self.visited_urls = {} # {url: time}
        self.urls_to_crawl = [base_url]
        self.visited_sitemaps = set()
        self.n_threads = n_threads
        self.robots_parsers = {}
        self.politeness_delay = politeness_delay
        self.max_url_per_page = max_url_per_page

        logging.info(f"Initialized WebCrawler with base URL {base_url} and {max_urls} max URLs.")

    def add_url_to_crawl(self, url):
        """
        Adds a URL to the list of URLs to crawl if it hasn't been visited or added already.
        Do not add XML URLs to avoid parsing sitemaps twice
        """
        if url not in self.visited_urls and url not in self.urls_to_crawl and not url.endswith(".xml"):
            self.urls_to_crawl.append(url)

    def parse_robots(self, url, thread_prefix=""):
        """
        Checks if the URL can be crawled and parses the sitemaps if available.
        """
        # Checking if the URL can be crawled
        logging.info(f"{thread_prefix}Checking if {url} can be crawled.")
        robots_url = parse.urljoin(url, "/robots.txt")
        if robots_url in self.robots_parsers:
            rp = self.robots_parsers[robots_url]
        else:
            rp = robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            self.robots_parsers[robots_url] = rp

        # Checking if a sitemap is available
        sitemaps = []
        robots_content = requests.get(robots_url).text
        for line in robots_content.split('\n'):
            if line.startswith('Sitemap:'):
                sitemaps.append(line.split(': ')[1].strip())
        
        # Parsing sitemaps
        for sitemap_url in sitemaps:
            if sitemap_url in self.visited_sitemaps:
                continue

            self.visited_sitemaps.add(sitemap_url)
            logging.info(f"{thread_prefix}Found sitemap {sitemap_url}. Parsing sitemap...")
            sitemap_content = requests.get(sitemap_url).content
            xml_parser = etree.XMLParser(recover=True) 
            root = etree.fromstring(sitemap_content, parser=xml_parser)

            # Extracting URLs from the sitemap
            urls = [loc.text for loc in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
            logging.info(f"{thread_prefix}Found {len(urls)} URLs in the sitemap {sitemap_url}.")

            for url in urls:
                self.add_url_to_crawl(url)

        # Return True if the URL can be crawled
        return rp.can_fetch("*", url)

    def crawl(self):
        """
        Initiates the crawling process.
        """
        while self.urls_to_crawl and len(self.visited_urls) < self.max_urls:
            # Compute number of threads to start
            n_current_threads = min(self.n_threads, len(self.urls_to_crawl))
            n_current_threads = min(n_current_threads, self.max_urls - len(self.visited_urls))
            current_urls = self.urls_to_crawl[:n_current_threads]
            self.urls_to_crawl = self.urls_to_crawl[n_current_threads:]
            logging.info(f"Starting {n_current_threads} thread(s)...")

            # Start the threads
            threads = []
            for i in range(n_current_threads):
                thread_name = f"{i+1}/{n_current_threads}"
                thread = Thread(target=self.parse_page, args=(current_urls[i], thread_name))
                thread.start()
                threads.append(thread)

            # Wait for the threads to finish
            for thread in threads:
                thread.join()

            # Respect the politeness policy
            logging.info("Waiting for 3 seconds to respect the politeness policy...")
            time.sleep(self.politeness_delay)

            
    def parse_page(self, current_url, thread_name = None):
        """
        Parses the page and extracts the links.
        """
        # Add a prefix to the log messages if the crawler is multi-threaded
        thread_prefix = ""
        if thread_name:
            thread_prefix = "[Thread " + thread_name + "] "
         
        # Chesck if the URL can be crawled based on robots.txt rules
        if not self.parse_robots(current_url, thread_prefix):
            logging.info(f"{thread_prefix}Skipping {current_url} based on robots.txt rules.")
            return

        # Download the page
        page_content = download_page(current_url)[:self.max_url_per_page]
        logging.info(f"{thread_prefix}Downloading HTML from {current_url}.")

        if page_content:
            # Extract links from the page
            links_on_page = extract_links(page_content)
            added_links = 0

            # Add new links to the list of URLs to crawl
            for link in links_on_page:
                absolute_link = link if link.startswith("http") else self.base_url + link
                if absolute_link not in self.visited_urls and absolute_link not in self.urls_to_crawl:
                    self.add_url_to_crawl(absolute_link)
                    added_links += 1

            # Mark the current URL as visited
            self.visited_urls[current_url] = time.time()
            logging.info(f"{thread_prefix}Successfully downloaded HTML/XML from {current_url}. Added {added_links} new links.")
        else:
            logging.error(f'{thread_prefix}Error while downloading HTML/XML from {current_url}.')
   
    def save_visited_urls(self, output_file, db_file=None):
        """
        Saves the visited URLs to a file.
        """
        with open(output_file, 'w') as f:
            for url in self.visited_urls:
                f.write(url + '\n')
            logging.info(f"Successfully saved {len(self.visited_urls)} URLs to {output_file}.")
            
        if db_file:
            try:
                conn = sqlite3.connect("output/visited_urls.db")
                cursor = conn.cursor()

                # Create the table if it doesn't exist
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS webpages
                    (url text, age real)"""
                )

                # Insert the URLs into the table
                for url in self.visited_urls:
                    cursor.execute("INSERT INTO webpages VALUES (?, ?)", (url, self.visited_urls[url]))
                    conn.commit()
                conn.close()
                logging.info(f"Successfully saved {len(self.visited_urls)} URLs to {db_file}.")
            
            except Exception as e:
                logging.error(f"Error while saving the visited URLs to the database: {e}")

# Example usage
if __name__ == '__main__':
    example_base_url = "https://ensai.fr"
    web_crawler = WebCrawler(example_base_url, max_urls=5)
    web_crawler.crawl()
    print(web_crawler.visited_urls)
