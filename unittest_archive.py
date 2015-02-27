##encoding=UTF8

"""

"""

from __future__ import print_function
from util.archive import Archive, Parser
from util.LINEARSPIDER import *

arc = Archive()
parser = Parser()
spider = Crawler()
spider.set_referer("http://www.archives.com/member/")
if not spider.login(url = "http://www.archives.com/member/", # 登录
                    payload = {"__uid":"efdevices@theeagleforce.net","__pwd":"MYpasswd"}):
    raise Exception("Failed to log in")

url = arc.generate_query_url("Carlson", "US", "VA", 2, 2014, 0, 10, 1) # generate query url
html = spider.html(url)
print(parser.num_of_records(html)) # 测试从html中找出该查询一共有多少条记录
for record in parser.records(html): # 测试从查询结果中摘取出死亡记录的结果
    print(record)