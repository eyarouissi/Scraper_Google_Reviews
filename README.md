# Scraper_Google_Reviews

A scraper that scrapes reviews from google reviews

## Features

+ Python FastAPI backend.
+ MongoDB database.


```console
pip3 install -r requirements.txt
```

To run the starter:

First, unstall package `scrapy`:

```console
pip install scrapy
```

Next, to get the list of reviews:

```console
scrapy crawl google -o reviews.csv
```
