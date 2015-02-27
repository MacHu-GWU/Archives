##encoding=UTF8

"""
This script is to crawl url in taskplan file. All record will be stored in pipeline folder as json
file. Then there's another program can regularly push data in pipeline into database
"""

from util.archive import Archive, Parser
from util.LINEARSPIDER import *
from util.DATA import *
from util.SQLITE import *
from util.GADGET import *
import itertools
import sys

def crawl(year):
    """This script is to download record from query result page
    for pagenum from 1 to max_pagenumber:
        crawl all records with state-lastname-pagenum combination.
    
    We use a database table to record which combination is already crawled. The key is:
        "state&lastname&pagenum"
    """
    ### === initiate constant
    arc = Archive()
    parser = Parser()
    spider = Crawler()
    spider.set_referer("http://www.archives.com/member/")
    if not spider.login(url = "http://www.archives.com/member/", # login
                        payload = {"__uid":"efdevices@theeagleforce.net","__pwd":"MYpasswd"}):
        raise Exception("Failed to log in")
    insert_obj = crawlplan.insert()

    task = load_pk(fname)
    saving_interval = 100 # dump to disk every how many http request
    cycler = itertools.cycle(range(saving_interval))
    
    for key, max_pagenum in task.items():
        for pagenum in range(1, max_pagenum + 1):
            state, lastname = key.split("&&") # get state and lastname
            crawlplan_key = "%s&&%s&&%s" % (state, lastname, pagenum) # create crawlplan key
            
            result = engine.select(Select(crawlplan.all).where(crawlplan.key == crawlplan_key))
            if count_generator(result) == 0: # if key is not found, so we should crawl it
                print("\nCrawling %s - %s page %s..." % (state, lastname, pagenum))
                url = arc.generate_query_url(lastname, "US", state, 2, year, 0, 250, pagenum)
                html = spider.html(url)
                if html:
                    record_list = list()
                    for record in parser.records(html): # 测试从查询结果中摘取出死亡记录的结果
                        record_list.append(record)
                    safe_dump_js(record_list, r"pipeline\%s&&%s.json" % (year, crawlplan_key),
                                 enable_verbose = False)
                    engine.insert_record(insert_obj, (crawlplan_key,))
                    print("\tSuccuess!")
                    if next(cycler) == (saving_interval - 1):
                        engine.commit()
                else:
                    log.write("got bad html", "%s-%s page %s" % (state, lastname, pagenum))

if __name__ == "__main__":
    year = int(sys.argv[1])
    fname = r"taskplan\task%s.p" % year
    databasename = r"crawlplan\crawlplan%s.db" % year
    
    ### configure database
    metadata = MetaData()
    engine = Sqlite3Engine(databasename)
    engine.autocommit(False)
    datatype = DataType()
    crawlplan = Table("crawlplan", metadata,
        Column("key", DataType.text, primary_key=True))
    metadata.create_all(engine)
    
    ### start crawl
    log = Log()
    crawl(year)
