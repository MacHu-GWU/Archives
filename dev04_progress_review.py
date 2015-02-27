##encoding=UTF-8

"""

4,000,000 record per day
0.15GB per 1000,000 record

"""
from util.DATA import *
from dev03_database import engine, archive

# for year in range(2000, 2003+1):
#     fname = "task%s.p" % year

# 2015-02-24 12:06:00, 12885 records
# 2015-02-24 12:19:00, 772959 records
engine.prt_howmany(archive)