##How to use

For example, if you want to crawl death record data in year 2000:

CD to project dir:

	cd C:\Users\Sanhe.Hu\workspace\py33\py33_projects\Archives

Run this command to do taskplan:
	
	python3 dev01_taskplan 2000

Run this command to crawl data stored in taskplan\task2000.p

	python3 dev02_crawl_record 2000

Run a database automate ETL process:

	python3 dev03_database

Then all death record data are automatically going to archive.db

##Design

###taskplan

taskplan is a dictionary include info that, a result of query of #lastname + #statename has how many pages. (250 records per page)

task2000.p data model:

	dict({lastname&&statename: max_page_number})

###crawlrecord

I use crawlplan.db to indicate which #lastname + #statename combination has been crawled.

###pipeline

while the crawler downloading data to a json file like this:
	
	pipeline\year&&lastname&&statename&&page_number.json

the ETL process is monitoring the folder and keep moving data to database
