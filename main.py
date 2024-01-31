import argparse
import logging
from webcrawler import WebCrawler

# Parsing the command-line arguments
parser = argparse.ArgumentParser(description="Web Crawler")
parser.add_argument("-m", "--max_urls", type=int, default=5, help="Maximum number of URLs to crawl")
parser.add_argument("-b", "--base_url", type=str, default="https://ensai.fr", help="Base URL to start crawling from")
parser.add_argument("-o", "--output_path", type=str, default="output/visited_urls.txt", help="Path to the output file")
parser.add_argument("-d", "--db_path", type=str, default="output/visited_urls.db", help="Path to the SQLite database file")
parser.add_argument("-t", "--n_threads", type=int, default=5, help="Number of threads to use")
parser.add_argument("-p", "--politeness_delay", type=int, default=5, help="Politeness delay in seconds")
args = parser.parse_args()

# Setting up the logger
open("output/logs.log", "w").close() # Clearing the log file
logging.basicConfig(
   level=logging.INFO, 
   format="%(asctime)s - %(levelname)s - %(message)s",
   filename="output/logs.log")

# Create instance of the WebCrawler class and start crawling
web_crawler = WebCrawler(
   args.base_url, 
   max_urls=args.max_urls, 
   n_threads=args.n_threads,
   politeness_delay=args.politeness_delay)
web_crawler.crawl()

# Save the visited URLs to a file
output_file = "visited_urls.txt"
web_crawler.save_visited_urls(args.output_path, args.db_path)