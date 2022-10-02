import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd

def connectZenithDb_v2():
    """returns a connection to a local SQL Server database (Zenith)
    using Windows authentication"""
    driver='{ODBC Driver 17 for SQL Server}'
    server='STEVE_XPS\SQLEXPRESS'
    database='Zenith'
    connection_string='driver='+driver+';server='+server+';database='+database+';Trusted_Connection=yes;'
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine=create_engine(connection_url)
    try:
        cnxn=engine.connect()
    except:
        return None            
    return cnxn

def connectZenithDb():
    """returns a connection to a local SQL Server database (Zenith)
    using Windows authentication"""
    driver='{ODBC Driver 17 for SQL Server}'
    server='STEVE_XPS\SQLEXPRESS'
    database='Zenith'
    try:
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+'; \
                      DATABASE='+database+';Trusted_Connection=yes;')
    except:
        return None            
    return cnxn

def filterBySize(cnxn, df, sizeFilters, rebalanceYear):
    minMCR=1
    maxMCR=1000
    for i,sf in enumerate(sizeFilters):
        if sf: maxMCR=(300,500,1000)[i]
    for i,sf in enumerate(list(reversed(sizeFilters))):
        if sf: minMCR=(501,301,1)[i]
    strQry='select StockID from yearEndMCR where yearEnd='\
                    +str(rebalanceYear)+' and MCR>='+str(minMCR)\
                        +' and MCR<='+str(maxMCR)
    df2=pd.read_sql(strQry,cnxn)       
    df=pd.merge(df,df2,on='StockID')
    return df
 
def filterByIndustry(cnxn,df,indFilters):
    if sum(indFilters)==1:
        strQry='select StockID from companysectors where IndustryNo='+str(indFilters.index(1)+1)
    else:
        indNumbers=[]
        for i, f in enumerate(indFilters):
            if f: indNumbers.append(i+1)
        strIndList=str(tuple(indNumbers))
        strQry='select StockID from companysectors where IndustryNo in '+strIndList
    df2=pd.read_sql(strQry,cnxn)
    df=pd.merge(df,df2,on='StockID')
    return df

def extractRatio(cnxn, ratioName, ratioType, rebalanceYear):
    if ratioType=='Financial':
        strQry='select a.StockID, '+ ratioName + \
        ' from outputTable a inner join financialRefDates b ' + \
        'on a.StockID=b.StockID and a.ReportMonth=month(b.reportDate) ' + \
        'and a.ReportYear=year(b.reportDate) ' + \
        'where year(b.rebalanceDate)=' + str(rebalanceYear)
    else:
        strQry='select StockID, '+ ratioName + \
        ' from outputTable_MktBased ' + \
        'where year(monthEnd)=' + str(rebalanceYear) + 'and month(monthEnd)=12'
    df=pd.read_sql(strQry, cnxn)
    return df                    

def extractAllRatios(cnxn, ratioType, rebalanceYear):
    if ratioType=='Financial':
        strQry='select a.* from outputTable a inner join financialRefDates b ' + \
        'on a.StockID=b.StockID and a.ReportMonth=month(b.reportDate) ' + \
        'and a.ReportYear=year(b.reportDate) ' + \
        'where year(b.rebalanceDate)=' + str(rebalanceYear)
    else:
        strQry='select *' + \
        ' from outputTable_MktBased ' + \
        'where year(monthEnd)=' + str(rebalanceYear) + 'and month(monthEnd)=12'
    df=pd.read_sql(strQry, cnxn)
    return df                    
          
def extractAllAccumIndexes(cnxn, StockIDList, performanceYear):
    """returns a pandas dataframe with columns which are the daily TR index
    of each stcok, indexed by date"""
    dfAll=extractRefDates(cnxn, performanceYear)
    for s in StockIDList:
        df=extractAccumIndex(cnxn,s,performanceYear)
        dfAll=dfAll.merge(df,'left','PriceDate')
    return dfAll

def extractRefDates(cnxn, performanceYear):
    """returns a series of tradings days from the last day of performanceYear-1
    to the last day of December performanceYear"""
    strQry='select PriceDate,  DateOffset from tradingdays '+\
        'where year(PriceDate)='+str(performanceYear)+\
        ' or PriceDate=(select max(PriceDate) from tradingdays '+\
        ' where year(PriceDate)='+\
        str(performanceYear-1)+') order by PriceDate'
    df=pd.read_sql(strQry, cnxn)
    df.set_index(['PriceDate'],inplace=True)
    return(df)    
    
def extractAccumIndex(cnxn, StockID, performanceYear):
    """returns a pandas series of the accum (TR) index of StockID
    from end of December performanceYear-1 to end of December performanceYear"""
    strQry1='select PriceDate,  AccumIndex from stockaccumindex where StockID='+\
        str(StockID)+' and PriceDate='+\
        '(select max(PriceDate) from tradingdays where year(PriceDate)='+\
        str(performanceYear-1)+')'
    df1=pd.read_sql(strQry1, cnxn)
    df1.set_index(['PriceDate'],inplace=True)
    strQry2='select PriceDate,  AccumIndex from stockaccumindex '+\
        'where stockID='+str(StockID)+' and year(PriceDate)='+str(performanceYear)
    df2=pd.read_sql(strQry2, cnxn)
    df2.set_index(['PriceDate'],inplace=True)
    df3=pd.concat([df1, df2])
    df3.columns=[str(StockID)]
    return df3

def extractIndexData(cnxn, yearRange):
    """Returns a pandas dataframe with the daily S&P200 accumulation
    index level and return"""
    strQry1='select PriceDate, AccumIndex, DailyRet from SP200Data where PriceDate='+\
        '(select max(PriceDate) from tradingdays where year(PriceDate)='+\
        str(yearRange[0]-1)+')'
    df1=pd.read_sql(strQry1, cnxn)
    df1.set_index(['PriceDate'],inplace=True)
    strQry2='select PriceDate, AccumIndex, DailyRet from SP200Data '+\
        'where year(PriceDate) between '+str(yearRange[0])+' and '+str(yearRange[1])
    df2=pd.read_sql(strQry2, cnxn)
    df2.set_index(['PriceDate'],inplace=True)
    df3=pd.concat([df1, df2])
    return df3
    
