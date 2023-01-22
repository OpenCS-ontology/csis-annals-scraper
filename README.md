# csis-annals-scraper
Scraper for the Annals of Computer Science and Information Systems website <br />

To use this application type those commands when you are in project directory: <br />
`docker build -t grobid grobid_service/` <br />
`docker build -t scrape scrape/` <br />

`docker-compose -f "docker-compose.yml" up -d` <br />
`docker-compose run --rm -it scrape /bin/bash` <br />
`cd /home/scrape` <br />
Using `python main.py --help` you can print help <br />
to use with default arguments type `python main.py`
Result will be in `Volume_1` directory (or `Volume_2`, `Volume_3`..) etc.

Documentation is in `scrape/build/index.html`