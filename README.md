# Web Crawler Project

## Description
This project implements a web crawler in Python. The crawler downloads pages from a starting URL, extracts links from these pages, and continues the process up to a certain number of URLs. The project uses multithreading to improve crawling efficiency and stores data of visited URLs in an SQLite database.

## Features
- **Multi-threaded Crawling**: Allows processing multiple pages simultaneously.
- **Respect for _robots.txt_ Rules**: The crawler checks the _robots.txt_ file of sites to ensure it is allowed to explore them.
- **Sitemap Analysis**: Attempts to read the _sitemap.xml_ file for more efficient URL discovery.
- **Crawler Politeness**: Waits for a defined time between requests to avoid overloading web servers.
- **Data Storage**: Records visited URLs and their visit dates in an SQLite database.
- **Detailed Logs**: Records detailed report in _output/logs.log_.

## Project Structure
The project directory is organized as follows:

```
|-- main.py
|-- README.md
|-- requirements.txt
|-- webcrawler.py
|-- output
  |-- logs.log
  |-- visited_urls.db
  |-- visited_urls.txt
|-- utils
  |-- linksextractor.py
  |-- pagedownloader.py
```

### Files:

- `main.py`: Main file to launch the crawler.
- `README.md`: Documentation file providing an overview of the project.
- `requirements.txt`: Lists the dependencies needed to run the project.
- `webcrawler.py`: Contains the main logic of the crawler.
- `logs.log`: Log file capturing crawler activity.
- `visited_urls.db`: SQLite database file storing visited URLs.
- `visited_urls.txt`: Text file containing a list of visited URLs.
- `linksextractor.py`: Script for extracting links from pages.
- `pagedownloader.py`: Script for downloading web pages.

## Installation and Execution

### Installing Dependencies
Run the following command to install the required dependencies:
```
pip install -r requirements.txt
```

### Launching the Crawler
Here is an example command to start the crawler:

```
python main.py -m 10 -b https://example.com -o output/visited_links.txt -d output/visited_links.db -t 8 -p 3
```

This command will start the web crawler with a maximum of 10 URLs, using "https://example.com" as the base URL, saving visited URLs to "output/visited_links.txt" and storing them in an SQLite database at "output/visited_links.db". The crawler will use 8 threads for parallel crawling with a politeness delay of 3 seconds between requests.