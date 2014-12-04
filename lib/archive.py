##encoding=utf8

from __future__ import print_function
from .pk import obj2str
from bs4 import BeautifulSoup as BS4
import re
import random

class Archive(object):
    def __init__(self):
        self.template = ("http://www.archives.com/member/Default.aspx?_act=VitalSearchResult"
                         "&LastName=%s" # lastname
                         "&Country=%s" # country
                         "&State=%s" # state
                         "&RecordType=%s" # recordtype
                         "&DeathYear=%s" # deathyear
                         "&DeathYearSpan=%s" # deathyearspan
                         "&activityID=%s" # activityID
                         "&ShowSummaryLink=1"
                         "&pagesize=%s" # pagesize 
                         "&pageNumber=%s" # pagenumber
                         "&pagesizeAP=10&pageNumberAP=1")
        self.activityID_list = [
                                "1ea327cc-2ff3-4c69-95c8-03514f8da579", # update on 2014-12-04
                                "5f9abce4-617a-47df-953d-cc8a95ad58a6",
                                "3f8573d2-3f37-4e80-943f-c67b3273d99c",
                                "8ba94eaa-6883-49f4-a157-ec410a8e6dc0",
                                "defa1e74-8b16-40d6-8061-e2dd325fc5d9",
                                
                                ]
        
    def generate_query_url(self, lastname, country, state, recordtype, 
                           deathyear, deathyearspan, pagesize, pagenumber):
        return self.template % (lastname, country, state, recordtype, 
                           deathyear, deathyearspan, random.choice(self.activityID_list), pagesize, pagenumber)

class Parser(object):
    def num_of_records(self, html):
        html = str(html)
        s = re.findall(r'(?<=>Showing 1-10 of ).{1,10}(?=</span>)', html)[0]
        s = s.replace(',', '')
        return int(s)

    def records(self, html):
        soup = BS4(html)
        resultVital = soup.find("div", id = "resultVital")
        for resultBox in resultVital.find_all("div", class_ = "resultBox"):
            
            resultRows = resultBox.find_all("div", class_ = "resultRow")
            resultRows.pop()
            
            record = dict()
            for resultRow in resultRows:
                field = resultRow.find("div", class_ = "field").text
                fieldValue = resultRow.find("div", class_ = "fieldValue").text
                record[field] = fieldValue
            item = obj2str(record)
            yield item
                
if __name__ == "__main__":
    arc = Archive()
    url = arc.generate_query_url("Carlson", "US", "VA", 2, 2014, 0, 
                         "9ffab73d-793a-4afb-816d-2f4ea0c0184d", 10, 1)
    print(url)