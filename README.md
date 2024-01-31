
## Usage

The Web Crawler is a tool for crawling and extracting information from web pages. Below are the available command-line options:

```bash
python your_script.py [-h] [-m MAX_URLS] [-b BASE_URL] [-o OUTPUT_PATH] [-d DB_PATH] [-t N_THREADS] [-p POLITENESS_DELAY]
```

### Options:

- `-h, --help`: Show the help message and exit.

- `-m MAX_URLS, --max_urls MAX_URLS`: Maximum number of URLs to crawl (default: 5).

- `-b BASE_URL, --base_url BASE_URL`: Base URL to start crawling from (default: "https://ensai.fr").

- `-o OUTPUT_PATH, --output_path OUTPUT_PATH`: Path to the output file for saving visited URLs (default: "output/visited_urls.txt").

- `-d DB_PATH, --db_path DB_PATH`: Path to the SQLite database file for storing visited URLs (default: "output/visited_urls.db").

- `-t N_THREADS, --n_threads N_THREADS`: Number of threads to use for parallel crawling (default: 5).

- `-p POLITENESS_DELAY, --politeness_delay POLITENESS_DELAY`: Politeness delay in seconds between successive requests (default: 5).

### Example:

```bash
python your_script.py -m 10 -b https://example.com -o output/visited_links.txt -d output/visited_links.db -t 8 -p 3
```

This command will start the web crawler with a maximum of 10 URLs, using "https://example.com" as the base URL, saving visited URLs to "output/visited_links.txt" and storing them in an SQLite database at "output/visited_links.db". The crawler will use 8 threads for parallel crawling with a politeness delay of 3 seconds between requests.
