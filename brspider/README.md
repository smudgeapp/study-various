# Spider for Crawling Google Searches and Scraping Business Recorder News Articles


This is a small spider from crawling Google search results from the Business Recorder site and scrape the articles to a JSON file.

Google does not allow automated searches and the Business Recorder site's own search results are not as good (*even though they use Google's Programmable Search - probably some setting issue*). So this manual spider will take input search term and load the search results in the Chrome browser. The urls of the search results can then be collected and scraped.

The spider will only run Google search and scrape articles from Business Recorder site (brecorder.com/news). The xpath and other search parameters are set for this purpose only. For scraping any other website, these will have to be modified in the script. 

*This was originally designed to collect data for some NLP project so the parameters are very specific.*

## Framework

It uses Selenium and Scrapy for crawling and scraping. Tkinter for the interface.

## Instructions

1. Enter the search term along with date limits 'Before' and 'After' in the format YYYY-MM-DD.
2. Once results show, press 'Get URLs' to load the urls for scraping.
3. 'Save URLs' will save urls to a binary file. 'Update URLs' will load previously saved urls. Although the program will handle duplicates, don't worry too much about duplicate urls, Scrapy will automatically ignore scraping duplicate links.
4. 'Get Articles' will start Scrapy process and save the count, date, url and article content to a JSON file.
5. 'Reset' will reset the loaded urls. Urls saved to file will still persist and can be loaded with 'Update URLs' button.
6. Some stats show at the bottom of the interface which help keep track of collected urls.

## Minimal Error Handling

At this time there is minimal error handling in this small program, so if it stops responding at some point without giving any notice, please see the log output. Or just save urls at frequent intervals to not lose search data and restart the program when it stops responding.

## Future TODO

1. add support for other websites
2. better error handling
3. better interface, giving more control over url lists and scraped items.
4. add support for other browsers

