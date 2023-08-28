from sqlalchemy import create_engine, text, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import os
import pandas as pd
import requests
import json



# Create a base class for declarating class definitions to produce Table objects
Base = declarative_base()

class HousingInflation(Base): 
    __tablename__ = "HousingInflation"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    Year = Column(String)
    Value = Column(Integer)
    percentagechange = Column(Float)

class InterestRates(Base):
    __tablename__ = "InterestRates" 
    id = Column(Integer, primary_key = True)
    year = Column(String)
    Interest_Rates = Column(Float)

dbpath = "HousingInflation.sqlite"
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
dbpath2 = "InterestRates.sqlite"
def LoadInterestData():
    #Load your SQLITE database
    engine = create_engine(f'sqlite:///{dbpath}')
    session = Session(engine)


    #Pull the data into pandas. We are filtering by the period    

    try:
    #SQL Alchemy 1.X version 
        query = session.query(InterestRates).statement
        data = pd.read_sql(query, session.bind)    
    except:
        #SQL Alchemy 2.0 version 
        query  = text(str(session.query(InterestRates)))
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

    #ETL processes for housing data
    HousingData = pd.read_csv('HousingDataAustin.csv')
    HousingData['DATE'] = HousingData['DATE'].astype('datetime64[D]')
    HousingData = HousingData[(HousingData['DATE']>'1999') & (HousingData['DATE'].dt.month == 10)]
    HousingData['Year'] = HousingData['DATE'].dt.year
    Indexed_Home_Price = 100638

    HousingData['Value'] = Indexed_Home_Price*HousingData['ATNHPIUS12420Q']
    HousingData['Percentage_Change'] = HousingData['Value'].pct_change()
    HousingData = HousingData[(HousingData['DATE']>'2000')]

    HousingData['City'] = 'Austin'


    HousingData = HousingData[['City','Year','Value','Percentage_Change']]

    SFHousingData = pd.read_csv('HousingDataSF.csv')

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

    Final = Final[['City','Year','Value','Percentage_Change']]

    Merged = Final.append(HousingData)

    Merged = Merged.reset_index()
   
   #ETL Processes for interest rate data 

    InflationData = pd.read_csv('InterestRates.csv')

    InflationData[['Year','Month','Day']] = InflationData['DATE'].str.split(pat = '-',expand=True)

    InflationData = InflationData.reset_index()

    InflationData = InflationData[(InflationData['Month'] == '12')]

    InflationData = InflationData.rename(columns={'INTDSRUSM193N':'Interest Rates'})

    FinalFrame = InflationData[['Year','Interest Rates']]

    FinalFrame = FinalFrame.reset_index(drop=True)

    FinalFrame =FinalFrame.reset_index()

    
    for index,row in Merged.iterrows():
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
        
    for index,interest_row in FinalFrame.iterrows():
        session.add(InterestRates(id = interest_row['index'],
                                  year = interest_row['Year'],
                                  Interest_Rates = interest_row['Interest Rates']
                                  ))

    session.commit()


    results = session.query(HousingInflation).all()

#data = pd.read_sql(session.query(Grade).statement, session.bind)
    data = LoadHousingData()

    interestdata = LoadInterestData()

    print(interestdata.head())

    session.close()
    