from sqlalchemy import MetaData
from pipig import app
from pipig.data import db


metadata = db.metadata

for t in metadata.sorted_tables:
    print t