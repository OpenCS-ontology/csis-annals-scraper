FROM python:3.8-slim-buster

COPY requirements.txt /home/scrape/requirements.txt

RUN apt update \
    && apt upgrade -y \ 
    && apt-get install git -y \
    && apt-get install wget -y \
    && apt install unzip -y \
    && apt install chromium -y \
    && wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip \ 
    && unzip chromedriver_linux64.zip \ 
    && git clone https://github.com/kermitt2/grobid_client_python /home/grobid_client_python \
	&& cd /home/grobid_client_python \
	&& python3 setup.py install \
    && cd /home/scrape/ \ 
    && pip install -r requirements.txt \
	&& cd /home


#COPY dummy.sh /home/scrape/dummy.sh
#CMD ["./home/scrape/dummy.sh"]
#CMD ["./chromedriver"]