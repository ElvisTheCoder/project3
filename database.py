from sqlalchemy import create_engine, text, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import os
import pandas as pd
import requests
import json

dbpath = "HousingInflation.sqlite"

# Create a base class for declarating class definitions to produce Table objects
Base = declarative_base()

class HousingInflation(Base): 
    __tablename__ = "HousingInflation"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    Year = Column(String)
    Value = Column(Integer)
    percentagechange = Column(Float)


def LoadHousingData():
    #Load your SQLITE database
    engine = create_engine(f'sqlite:///{dbpath}')
    session = Session(engine)


    #Pull the data into pandas. We are filtering by the period    

    try:
    #SQL Alchemy 1.X version 
        query = session.query(HousingInflation).statement
        data = pd.read_sql(query, session.bind)    
    except:
        #SQL Alchemy 2.0 version 
        query  = text(str(session.query(HousingInflation)))
        data = pd.read_sql(query, engine.connect())

    return data


if __name__ == "__main__":
    import pandas as pd
    from sqlalchemy.orm import Session


    if os.path.exists(dbpath):
        os.remove(dbpath)

    engine = create_engine(f'sqlite:///{dbpath}')
    Base.metadata.create_all(engine)

    session = Session(engine)

    SFHousingData = pd.read_csv('HousingData.csv')

    Filtered = SFHousingData[(SFHousingData['Series ID'] == 'CUUSS49BSAH') & (SFHousingData['Period'] == 'S02')]

    Final = Filtered[['Series ID','Year','Value']]

    Final['Percentage_Change'] = ''

    Final['City'] = ''

    Final['Value'] = Final['Value'].astype('Float64')

    Final = Final.reset_index(drop=True)

    Final['Percentage_Change'] = Final['Value'].pct_change()

    Final['City'] =  'San Francisco'

    Final = Final[(Final['Year']) >= 2000]

    Final = Final.rename(columns={'Series ID': 'Seriesid'})

    Final = Final[['Seriesid', 'City','Year','Value','Percentage_Change']]

    Final = Final.reset_index()
    
    for index,row in Final.iterrows():
        print()
        id_row = row['index']
        city_row = row['City']
        Year_row = row['Year']
        Value_row = row['Value']
        percentagechange_row = row['Percentage_Change']
        session.add(HousingInflation(id=id_row, 
                                 city=city_row,
                                 Year= Year_row,
                                 Value=Value_row,
                                 percentagechange=percentagechange_row))
    session.commit()


    results = session.query(HousingInflation).all()

#data = pd.read_sql(session.query(Grade).statement, session.bind)
    data = LoadHousingData()

    print(data.head())

    session.close()
    