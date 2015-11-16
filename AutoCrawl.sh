#!/bin/sh
cd ~/workspace/CSUNewsSpider/
git reset --hard
git pull
scrapy crawl CSUNews
scrapy crawl CSUAcademic
scrapy crawl CSUJobs

