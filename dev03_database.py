##encoding=UTF8

"""
This script is to crawl url in taskplan file. All record will be stored in pipeline folder as json
file. Then there's another program can regularly push data in pipeline into database.
"""

from util.DATA import *
from util.SQLITE import *
from util.LIBRARIAN import *
import itertools
import os
import time

### configure database
metadata = MetaData()
engine = Sqlite3Engine("archive.db")
engine.autocommit(False)
datatype = DataType()
archive = Table("archive", metadata, # death record database
    Column("lastname", DataType.text, primary_key=True),
    Column("state", DataType.text, primary_key=True),
    Column("name", DataType.text, primary_key=True),
    Column("death_date", DataType.date, primary_key=True),
    Column("birth_date", DataType.date),
    Column("location", DataType.text),
    Column("resident", DataType.text),
    Column("collection", DataType.text),
    )
metadata.create_all(engine)

tw = TimeWrapper() # date string parser
insert_obj = archive.insert() # insert object
saving_interval = 10 # dump to disk every how many http request
cycler = itertools.cycle(range(saving_interval))
    
def json_filter(winfile):
    if winfile.basename.endswith(".json"):
        return True
    else:
        return False

def push2db():
    ### push data into database
    for winfile in FileCollections.from_path_by_criterion(r"pipeline", json_filter).iterfiles():
        year, state, lastname, pagenumber = winfile.fname.split("&&")
        records = load_js(winfile.abspath)
        for record in records:
            try:
                new_record = dict()
                new_record["lastname"] = lastname
                new_record["state"] = state
                new_record["name"] = record.get("Name:")
                new_record["death_date"] = tw.str2date(record.get("Death Date:") )
                try:
                    new_record["birth_date"] = tw.str2date(record.get("Birth Date:") )
                except:
                    pass
                new_record["location"] = record.get("Location:")
                new_record["resident"] = record.get("Residence:")
                new_record["collection"] = record.get("Collection:")
                
                row = Row.from_dict(new_record)
                try:
                    engine.insert_row(insert_obj, row)
                except:
                    pass
            except:
                pass
        os.remove(winfile.abspath)
        if next(cycler) == (saving_interval - 1):
            engine.commit()
    engine.commit()

if __name__ == "__main__":
    while 1:
        try:
            push2db()
        except:
            pass
        time.sleep(60) # process every 600 seconds