##encoding=UTF-8

"""
This script is to find out how many page for every state&&lastname combination.
After this, then we can crawl record page by page. (250 record perpage)

How to use:
    cd to project directory, then enter this in command line:
        python3 dev01_taskplan.py 2000
        
    format:
        python_interpreter this_script_name year
"""

from __future__ import print_function
from util.archive import Archive, Parser
from util.LINEARSPIDER import *
from util.DATA import *
from util.GADGET import *
import util.constant
import itertools
import math
import sys
import random

def taskplan(year):
    """This function take year as input, to tell the death record crawler how much pages(250 record
    per page) in a year-state-lastname combination of a query. So the crawler then able to get 
    record page by page. I use a pickle3 file to store the index information.
    
    For example:
        task2000.p = dict({"state&lastname": max_pagenum})
    """
    ### === initiate constant
    arc = Archive()
    parser = Parser()
    spider = Crawler()
    spider.set_referer("http://www.archives.com/member/")
    if not spider.login(url = "http://www.archives.com/member/", # login
                        payload = {"__uid":"efdevices@theeagleforce.net","__pwd":"MYpasswd"}):
        raise Exception("Failed to log in")
    try:
        task = load_pk(fname)
    except:
        task = dict()
    
    saving_interval = 100 # dump to disk every how many http request
    cycler = itertools.cycle(range(saving_interval))
    
    ### === crawl all 18839 lastnames and 50 states combination
    random.shuffle(util.constant.statenamelist)
    random.shuffle(util.constant.lastnamelist)
    
    for state in util.constant.statenamelist:
        for lastname in util.constant.lastnamelist:
            key = "%s&&%s" % (state, lastname) # key = lastname&&state
            if key not in task: # exam if it is already crawled
                print("Crawling %s - %s..." % (state, lastname))
                url = arc.generate_query_url(lastname, "US", state, 2, year, 0, 10, 1)
                html = spider.html(url)
                if html:
                    try:
                        num_of_records = parser.num_of_records(html)
                        max_pagenum = int(math.ceil(float(num_of_records)/250))+1
                        task[key] = max_pagenum
                        print("\tMaxpage = %s" % max_pagenum)
                        if next(cycler) == (saving_interval-1):
                            safe_dump_pk(task, fname)
                    except Exception as e:
                        log.write(str(e), "%s-%s" % (state, lastname))
                else:
                    log.write("got bad html", "%s-%s" % (state, lastname))
                    
if __name__ == "__main__":
    year = int(sys.argv[1])
    fname = r"taskplan\task%s.p" % year
    log = Log()
    taskplan(year)
