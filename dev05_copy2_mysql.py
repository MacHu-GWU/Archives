##encoding=UTF8

"""
WARNING!! This script has to run in python27, because python3 doens't support Python MySqldb

I created a MySQL database on the VM 10.0.80.194
 
Can you please move your data from your sqllite db to this MySQL instance?  The data file for this instance sits on the E drive which has 200GB of space.
 
Let me know if you need any help with any of this.
 
Username: development
Password: DevTeam01!
Schema:  bdrecords
Port:  3306
"""

from __future__ import print_function
from sqlalchemy import *
from sqlalchemy.sql import select

##################
# Mysql Metadata #
##################
engine_mysql = create_engine("mysql+mysqldb://development:DevTeam01!@localhost:3306/bdrecords", pool_recycle=3600)
conn_mysql = engine_mysql.connect()
metadata_mysql = MetaData()
archive_mysql = Table("archive", metadata_mysql, # death record database
    Column("lastname", String(64), primary_key=True),
    Column("state", String(64), primary_key=True),
    Column("name", String(64), primary_key=True),
    Column("death_date", Date, primary_key=True),
    Column("birth_date", Date),
    Column("location", String(64)),
    Column("resident", String(64)),
    Column("collection", String(64)),
    )
metadata_mysql.create_all(engine_mysql)
ins = archive_mysql.insert()

###################
# Sqlite metadata #
###################
engine_sqlite = create_engine(r"sqlite:///C:\Users\Sanhe.Hu\workspace\py33\py33_projects\Archives\archive.db" )
conn_sqlite = engine_sqlite.connect()
metadata_sqlite = MetaData()
metadata_sqlite.reflect(engine_sqlite)
archive_sqlite = metadata_sqlite.tables["archive"]

#########################################
# move data from sqlite3 db to Mysql db #
#########################################

for record in conn_sqlite.execute(select([archive_sqlite])):
    record = dict(record)
    try:
        conn_mysql.execute(ins, record)
    except:
        pass
