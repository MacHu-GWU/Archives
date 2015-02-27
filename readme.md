#Design

###taskplan
task2000.p

	dict({lastname&&statename: max_page_number})

###crawlplan
crawl2000.p
	
	set({lastname&&statename&&page_number})

###pipeline
lastname&&statename&&page_number.json