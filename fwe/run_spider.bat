@echo off
set /p crawler= "Type in the crawler to start: "
echo Starting %crawler%
scrapy crawl %crawler%
pause 