@echo off
set /p crawler= "Type in the crawler to start: "
echo Starting %crawler%
cd ..
cd crawling
scrapy crawl %crawler%
pause 