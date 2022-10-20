# Spider for Crawling Google Searches and Scraping Business Recorder News Articles

This is a small spider for crawling Google search results from the Business Recorder site and scrape the articles to a JSON file.

Google does not allow automated searches (https://policies.google.com/terms/archive/20020906?hl=en) and the Business Recorder site's own search results are not as good (*even though they use Google's Programmable Search - probably some setting issue*). So this manual spider will take input search term and load the search results in the Chrome browser. The urls of the search results can then be collected and scraped.

The spider will only run Google search and scrape news articles from Business Recorder site (https://www.brecorder.com/news). The xpath and other search parameters are set for this purpose only. For scraping any other website, these will have to be modified in the script. 

*This was originally designed to collect data for a NLP project so the parameters are very specific.*

## Framework

It uses Selenium and Scrapy for crawling and scraping. Tkinter for the interface.

## Instructions

This uses Selenium on Chrome and requires the chrome driver (https://chromedriver.chromium.org/downloads). The path to the chrome driver on the local disk must be added in the script at the specified location.

1. Enter the search term along with date limits 'Before' and 'After' in the format YYYY-MM-DD. Date limits are optional.
2. Once results show, press 'Get URLs' to load the urls for scraping.
3. 'Save URLs' will save urls to a binary file. 'Update URLs' will load previously saved urls. Although the program will handle duplicates when saving and updating, don't worry too much about duplicate urls, Scrapy will automatically ignore scraping duplicate links.
4. 'Link Nos.' specifies which link serial on the page is to be added. The count starts from 0, i.e. the first link in the search results is 0. It can take input as comma separated or dashed range or both e.g. "0-3, 5, 7-9". If link no.s is not specified, all urls are loaded to be scraped.
5. 'Get Articles' will start Scrapy process and save the count, date, url and article content to a JSON file.
6. 'Reset' will reset the loaded urls. Urls saved to file will still persist and can be loaded with 'Update URLs' button.
7. Some stats show at the bottom of the interface which help keep track of collected urls. If they can't be seen, expand the window.

## Ideal UX

Ideally, the user should collect all the required links and then run the 'Get Articles'. If all the links cannot be loaded in a single sitting, save them and, in the next sitting, update to load saved urls and continue.

It would also be helpful to look into Google search operators and how to improve search results, if already not an expert! :) ;)

## Minimal Error Handling

At this time there is minimal error handling in this small program, so if it stops responding at some point without giving any notice, please see the log output. Or just save urls at frequent intervals to not lose search data and restart the program if it stops responding.

## Future TODO

1. add support for other websites
2. better error handling
3. better interface, giving more control over url lists and scraped items.
4. add support for other browsers

