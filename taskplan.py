##encoding=utf8

from LinearSpider import *
from lib.archive import Archive, Parser
from lib.loaddata import load_lastnamelist, load_statelist
import math

year = 2000

def level1(url, spider):
    lastnamelist = load_lastnamelist()
    statelist = load_statelist()
    for state in statelist:
        for lastname in lastnamelist:
            yield "&&".join([state, lastname]), {}
        
def level2(url, spider):
    global year
    state, lastname = url.split("&&")
    arc, parser = Archive(), Parser()
    url = arc.generate_query_url(lastname, "US", state, 2, year, 0, 10, 1)
    html = spider.html(url)
    num_of_records = parser.num_of_records(html)
    for i in range(1, int(math.ceil(float(num_of_records)/250))+1):
        yield str(i), {"done": 0}
        
spider, pm = Crawler(), ProxyManager()
spider.set_referer("http://www.archives.com/member/")
# pm.download_proxy(300)
pm.load_pxy()
# pm.reset_health()
 
if not spider.login(url = "http://www.archives.com/member/", # 登录
                    payload = {"__uid":"husanhe@gmail.com","__pwd":"efa2014"}):
    raise Exception("Failed to log in")
 
spider.enable_proxy(pm)
spider.html("http://www.python.org/") # dummy
sch = Scheduler("nothing")
sch.bind(spider=spider, try_howmany=10, save_interval=20, local_file="task%s.p" % year)
sch.bind_link_extractor([level1, level2])
sch.start()

# task = load_pk("task%s.p" % year)
# prt_js(task)    