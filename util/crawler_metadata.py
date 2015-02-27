##encoding=UTF8

"""
import:
    from util.crawler_metadata import engine, crawlplan
"""

from .SQLITE import *

metadata = MetaData()
engine = Sqlite3Engine(r"crawlplan\crawlplan.db")
engine.autocommit(False)
datatype = DataType()
crawlplan = Table("crawlplan", metadata,
    Column("key", DataType.text, primary_key=True))
metadata.create_all(engine)