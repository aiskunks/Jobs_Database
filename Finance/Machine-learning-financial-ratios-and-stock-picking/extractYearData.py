# A function to extract and process all the data for each year
# It excludes financial & real estate firms
import pandas as pd
import numpy as np
def extractYearData(forecastYear, cnxn):
    # extract all financial ratios
    strQry1='select a.*, ' +str(forecastYear)+' as ForecastYear from outputTable a inner join financialRefDates b ' + \
            'on a.StockID=b.StockID and a.ReportMonth=month(b.reportDate) ' + \
            'and a.ReportYear=year(b.reportDate) ' + \
            'where year(b.rebalanceDate)=' + str(forecastYear-1)
    df1=pd.read_sql(strQry1,cnxn)

    # extract market-based ratios
    strQry2='select * from outputTable_MktBased where year(monthEnd)=' + str(forecastYear-1) + ' and month(monthEnd)=12'
    df2=pd.read_sql(strQry2,cnxn)

    # merge financial and market-based features
    features=df1.merge(df2,on='StockID')
    features.drop(columns=['ReportMonth', 'ReportYear', 'monthEnd'],inplace=True)
    features.dropna(axis=0,inplace=True)

    # limit study to companies in the top 500 by market cap
    features=features[features.MCR<501]

    # extract the industry of each stock and exclude real estate and financial companies
    strQry3='select StockID, IndustryNo from companysectors'
    df3=pd.read_sql(strQry3,cnxn)
    df3.dropna(inplace=True)
    inds=df3.astype({'IndustryNo': 'int32'})
    features=features.merge(inds,on='StockID')

    # exclude real estate (IndustryNo=1) and financial (IndustryNo=5) stocks
    features=features[(features['IndustryNo']!=1) & (features['IndustryNo']!=5)]
    features.drop(columns=['IndustryNo'],inplace=True)

    # extract stock returns
    # first, the TR index from end of December in the previous year
    strQry4='select StockID, AccumIndex as TR0 from stockaccumindex where PriceDate='+\
            '(select max(PriceDate) from tradingdays where year(PriceDate)='+str(forecastYear-1)+')'
    df4=pd.read_sql(strQry4,cnxn)
    # next, the TR index from end of December in the forecast year
    strQry5='select StockID, AccumIndex as TR1 from stockaccumindex where PriceDate='+\
            '(select max(PriceDate) from tradingdays where year(PriceDate)='+str(forecastYear)+')'
    df5=pd.read_sql(strQry5,cnxn)
    # merge the 2 dataframes
    stockReturns=df4.merge(df5,on='StockID')
    stockReturns['Return']=stockReturns['TR1']/stockReturns['TR0']-1
    stockReturns.drop(columns=['TR0','TR1'],inplace=True)
    allData=features.merge(stockReturns,on='StockID')

    # create the target variable: HighReturn=1 if the stock return is above the median
    allData['HighReturn']=0
    allData.loc[allData.Return>allData['Return'].median(),'HighReturn']=1
    
    #trim outliers; as defined per standard box plot definition (i.e. outside of 1st & 3rd quartiles +/- 1.5* i/q range)
    tempdf=allData.drop(columns=['StockID', 'ForecastYear', 'HighReturn'])
    q1=tempdf.quantile(0.25)
    q3=tempdf.quantile(0.75)
    iqr=q3-q1
    lower=q1-1.5*iqr
    upper=q3+1.5*iqr
    desc=pd.concat([q1,q3,iqr,lower,upper],axis=1).T
    desc.rename(index={0.25: 'q1', 0.75: 'q3', 0: 'iqr', 1:'lower', 2:'upper'},inplace=True)

    for v in tempdf.columns.values: # exclude 'Outperform'
            allData[v]=np.where(allData[v]>desc[v]['upper'],desc[v]['upper'],np.where(allData[v]<desc[v]['lower'],desc[v]['lower'],allData[v]))

    # also restrict B_P>0 and 0<D_A<1
    allData['B_P']=np.where(allData['B_P']<0,0,allData['B_P'])
    allData['D_A']=np.where(allData['D_A']<0,0,np.where(allData['D_A']>1,1,allData['D_A']))        

    return allData
