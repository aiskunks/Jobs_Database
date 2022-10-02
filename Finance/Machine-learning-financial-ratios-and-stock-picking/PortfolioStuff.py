import pandas as pd
import numpy as np
import math
from scipy.stats import t
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression

from ZenithDatabaseInteractions import extractRatio, filterBySize, \
filterByIndustry, extractAllAccumIndexes

def getPortfolios(cnxn,FactorAbbrs, FactorTypes, LSind, indFilters, sizeFilters, yearRange):
    """returns a list of 4 items which are respectively:
        1) a list of the long portfolios (pandas series), one for each year
        2) a list of the short portfolios (pandas series), one for each year
        3) a list of the count of long portfolio holdings by year
        4) a list of the count of short portfolio holdings by year"""
    longPortfolios=[]
    shortPortfolios=[]
    longCount=[]
    shortCount=[]
    for y in range(yearRange[0],yearRange[1]+1):
        p=getPortfolio(cnxn,FactorAbbrs, FactorTypes, LSind, indFilters, sizeFilters, y-1)
        longPortfolios.append(p[0])
        shortPortfolios.append(p[1])
        longCount.append(p[0].shape[0])
        shortCount.append(p[1].shape[0])
    return [longPortfolios,shortPortfolios,longCount,shortCount]

def getPortfolio(cnxn,FactorAbbrs, FactorTypes, LSind, indFilters, sizeFilters, rebalanceYear):
    """return a list of 2 pandas series: the first containing the long
    portfolio IDs and the 2nd the short portfolio IDs"""
    qryResult=[]
#   get the data for each factor
#    for fa in FactorAbbrs:
    for fa, ft in zip(FactorAbbrs, FactorTypes):
        df=extractRatio(cnxn, fa, ft, rebalanceYear)
#       remove observations with missing values
        df.dropna(inplace=True)
        qryResult.append(df)
#   if there are 2 factors, merge the DataFrames
    if len(FactorAbbrs)==2:
        df2=pd.merge(qryResult[0], qryResult[1], on='StockID')
    else:
        df2=qryResult[0]
    if sizeFilters:
        df2=filterBySize(cnxn, df2, sizeFilters, rebalanceYear)
    if indFilters:
        df2=filterByIndustry(cnxn, df2, indFilters)
#   rank all observations by each factor
    for i, fa in enumerate(FactorAbbrs):
        boolAsc=False if LSind[i]==1 else True
        df2[fa+'_rank']=df2[fa].rank(ascending=boolAsc)
#   now allocate to long and short portfolios
    if len(FactorAbbrs)==1:
        df2['Long']=(df2[FactorAbbrs[0]+'_rank']<=float(df2.shape[0])/3.0)
        df2['Short']=(df2[FactorAbbrs[0]+'_rank']>=1+df2.shape[0]-float(df2.shape[0])/3.0)
    else:
        df2['Long']=(df2[FactorAbbrs[0]+'_rank']<=float(df2.shape[0])/3.0) & (df2[FactorAbbrs[1]+'_rank']<=float(df2.shape[0])/3.0)
        df2['Short']=(df2[FactorAbbrs[0]+'_rank']>=1+df2.shape[0]-float(df2.shape[0])/3.0) & (df2[FactorAbbrs[1]+'_rank']>=1+df2.shape[0]-float(df2.shape[0])/3.0)
    return [df2[df2['Long']]['StockID'], df2[df2['Short']]['StockID']]

def calcAllPortfolioValues(cnxn, Holdings):
    """Returns a list of two pandas time series which are the daily total return
    indexes of the long and short portfolios respectively"""
    lngValues=[]
    shrtValues=[]
    for i, (lngPort,shrtPort,yr) in enumerate(Holdings):
        if i==0:
            lng=calcPortfolioValue(cnxn, lngPort, yr, 1)
            shrt=calcPortfolioValue(cnxn, shrtPort, yr, 1)
            lngValues.append(lng)
            shrtValues.append(shrt)
        else:
            lng=calcPortfolioValue(cnxn, lngPort, yr, lng[-1])
            shrt=calcPortfolioValue(cnxn, shrtPort, yr, shrt[-1])
            lngValues.append(lng[1:]) # don't include end of prev year if not 1st year
            shrtValues.append(shrt[1:])
    lngFullSeries=pd.concat(lngValues)
    shrtFullSeries=pd.concat(shrtValues)
    return [lngFullSeries, shrtFullSeries]

def calcPortfolioValue(cnxn, Hldngs, yr, StartValue):
    """Returns a pandas series of portfolio values (TR index) for year yr
    given the Stock IDs in Hldngs and a starting value of StartValue"""
    df=extractAllAccumIndexes(cnxn, list(Hldngs), yr)
#   remove columns where first entry is not available: bad data    
    bcs=zip(list(df.columns.values), list(df.isna().iloc[0]))
    bad_cols=[c[0] for c in bcs if c[1]]
    df.drop(columns=bad_cols,inplace=True)
#   now deal with missing values in the middle
    idxList=list(df.index.values)
    maxIdx= idxList[-1] # last index value (a datetime)
    cols=list(df.columns.values)
    lvi=[df[c].last_valid_index() for c in cols] # list of "last valid indexes"
    # fill missing values with previous values
    df.fillna(method='ffill',inplace=True)
    # but replace the missing values at the end
    for i,l in enumerate(lvi):
        if l<maxIdx:
            n=idxList.index(l)
            df.loc[idxList[n+1:],cols[i]]=np.nan
    # rescale each series to 1.0 at the beginning
    df=cleanStockReturns(df)
    x=df.iloc[:,1:].divide(df.iloc[0,1:]/StartValue)
    # if any series finishes early, replace with average of all the others
    x['PortfolioValue']=x.iloc[:,1:].mean(axis=1)
    return x['PortfolioValue']

def cleanStockReturns(df):
    """Returns a cleaned DataFrame of stock TR indexes after winsorizing
    daily extreme returns to the Median +/-10% and resetting initial TR index to 1"""
    df2=df.iloc[:,1:].pct_change(fill_method=None)
    df3=df2.iloc[1:,].transform(lambda x: winsorizeReturns(x,x.median(),0.2),axis='columns')
    df3=pd.concat([df2.iloc[0:1,:].fillna(0),df3])
#    df3.iloc[0,:]=0
    df3=df3.applymap(lambda x: x+1).cumprod()
    df4=pd.merge(df[['DateOffset']],df3,on='PriceDate')
    return df4

def winsorizeReturns(x,y,lim):
    """Winsorize x values to the range [y-lim, y+lim]"""
    x2=[y+lim if z>y+lim else z for z in x]
    x3=[y-lim if z<y-lim else z for z in x2]
    return x3

def calcPortfolioReturns(portfolioValues):
    lng=portfolioValues[0].to_frame()
    shrt=portfolioValues[1].to_frame()
    lng['Long ret']=lng.pct_change()
    shrt['Short ret']=shrt.pct_change()
    allData=pd.merge(lng,shrt,on='PriceDate')
    allData['Long minus Short']=allData['Long ret']-allData['Short ret']
    return allData

def calcPerformanceStats(portReturns, indexData):
    nd=portReturns.shape[0]-1
    d=portReturns[['Long ret','Short ret','Long minus Short']]
    mn=d.mean()*100
    std=d.std()*100
    stderr=std/math.sqrt(nd)
    tstats=mn/stderr
    pValues=[1-t.cdf(tstats['Long ret'],nd-1), t.cdf(tstats['Short ret'],nd-1),\
                1-t.cdf(tstats['Long minus Short'],nd-1)]
    # calculate alphas, betas and residual volatility
    [aL, irL]=calcInvestPerformance(d['Long ret'][1:],indexData[1:]) # 1st row contains NaNs
    [aS, irS]=calcInvestPerformance(d['Short ret'][1:],indexData[1:])
    [aLS, irLS]=calcInvestPerformance(d['Long minus Short'][1:],indexData[1:])
    return[list(mn), list(tstats), pValues, (aL, aS, aLS), (irL, irS, irLS)]

def calcInvestPerformance(portRet, bmRet):
    """Returns the alpha, beta and residual volatility given portfolio and benchmark returns"""
    y=portRet.values
    y=y.reshape(y.shape[0],1)
    x=bmRet.values
    x=x.reshape(x.shape[0],1)
    ols=LinearRegression().fit(x,y)
    alpha=250*ols.intercept_.item() # annualised
    #beta=ols.coef_.item()
    y_hat=ols.predict(x)
    resids=y-y_hat
    resid_ssq=np.sum(resids**2)
    resid_vol=math.sqrt(resid_ssq/(portRet.shape[0]-2))
    resid_vol=resid_vol*math.sqrt(250) # annualised
    infoRatio=alpha/resid_vol
    return[alpha, infoRatio]
    
def plotPortfolioValues(portfolioValues,bmValues,FactorAbbrs, LSind, perfStats):
    strLong='Long portfolio: '
    strShort='Short portfolio: '
    for x in zip(FactorAbbrs,LSind):
        if x[1]==1:
            strLong=strLong+'High '+x[0]+' '
            strShort=strShort+'Low '+x[0]+' '
        else:
            strLong=strLong+'Low '+x[0]+' '
            strShort=strShort+'High '+x[0]+' '
    fig=plt.figure(figsize=(12,7))
    gs = GridSpec(8, 7, figure=fig)
    ax1 = fig.add_subplot(gs[0:5, :])
    ax2 = fig.add_subplot(gs[-2, 1:7])

    portfolioValues[0].plot(x='PriceDate',y='PortfolioValue',label=strLong,color='blue',ax=ax1)
    portfolioValues[1].plot(x='PriceDate',y='PortfolioValue',label=strShort,color='red',ax=ax1)
    bmValues.plot(x='PriceDate',y='PortfolioValue',label='ASX200 accumulation index',color='black',ax=ax1)
    ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=12,bymonthday=-1))
    ax1.xaxis.set_minor_locator(mdates.MonthLocator())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
    priceDates=list(portfolioValues[0].index.values)
    ax1.set_xlim([min(priceDates), max(priceDates)])
    for label in ax1.get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    ax1.grid(True)
    ax1.set(xlabel='Date',ylabel='Total return index')
    ax1.legend(bbox_to_anchor=(0,1), loc='lower left',shadow=True,fancybox=True)
    # add performance stats
    rows=['Daily mean return (%)','t-statistic','p-value (1-sided)',\
          'Alpha, annualised', 'Information Ratio']
    columns=['Long','Short','Long minus short']
    cell_text=[]
    for row in perfStats:
        cell_text.append(['%8.4f' % x for x in row])
    ax2.table(cellText=cell_text, rowLabels=rows, colLabels=columns,loc='bottom',cellLoc='center')
    ax2.axis('off')
    ax2.axis('tight')
    plt.subplots_adjust(bottom=0.2,hspace=0.2)
    plt.show()
    return fig
