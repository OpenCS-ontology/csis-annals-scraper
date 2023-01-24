# csis-annals-scraper
This repository contains tools to scrape  Annals of Computer Science and Information Systems website. 
When used it will produce folders looking like this: `Volume_1/pdfs` with downloaded articles and 
and `Volume_1/ttls` with OWL files containing information describing articles (like author, title, number of pages etc.).
<br />
<hr style="border:2px solid gray">
# Issues <br />
It is possible to encounter connection errors then using GROBID or CrossRef. The only solution is to restart program from last scraped volume. 
<hr style="border:2px solid gray">
# IMPORTANT <br /> 
Before every scraping application deletes folder 
Volume_1 directory (or Volume_2, Volume_3...) if it exists.

To use this application type those commands when you are in project directory: <br />
`docker build -t grobid grobid_service/` <br />
`docker build -t scrape scrape/` <br />

`docker-compose -f "docker-compose.yml" up -d` <br />
`docker-compose run --rm -it scrape /bin/bash` <br />
`cd /home/scrape` <br />
Using `python main.py --help` you can print help. <br />
You can specify volumes to scrape `python main.py --volumes 1,2,3` or scrape all of them using `python main.py` (more info under  `python main.py --help`).
Result will be in `Volume_1` directory (or `Volume_2`, `Volume_3`...) etc.

Documentation is in `scrape/build/index.html`