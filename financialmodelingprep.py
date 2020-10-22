# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 21:50:38 2020

@author: home
"""


import requests
import pandas as pd

companies = []
demo = 'ef4e4c3aaa98681b369a8341ebcd2d55'
marketcap = str(1000000000)
url = (f'https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={marketcap}&betaMoreThan=1&volumeMoreThan=10000&sector=Technology&exchange=NASDAQ&dividendMoreThan=0&limit=1000&apikey={demo}')

#get companies based on criteria defined about
screener = requests.get(url).json()
print(screener)

#add selected companies to a list
for item in screener:
 companies.append(item['symbol'])
print(companies)

value_ratios ={}
#get the financial ratios
count = 0
for company in companies:
    try:
        if count <30:
            count = count + 1
            fin_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
            value_ratios[company] = {}
            value_ratios[company]['ROE'] = fin_ratios[0]['returnOnEquity']
            value_ratios[company]['ROA'] = fin_ratios[0]['returnOnAssets']
            value_ratios[company]['Debt_Ratio'] = fin_ratios[0]['debtRatio']
            value_ratios[company]['Interest_Coverage'] = fin_ratios[0]['interestCoverage']
            value_ratios[company]['Payout_Ratio'] = fin_ratios[0]['payoutRatio']
            value_ratios[company]['Dividend_Payout_Ratio'] = fin_ratios[0]['dividendPayoutRatio']
            value_ratios[company]['PB'] = fin_ratios[0]['priceToBookRatio']
            value_ratios[company]['PS'] = fin_ratios[0]['priceToSalesRatio']
            value_ratios[company]['PE'] = fin_ratios[0]['priceEarningsRatio']
            value_ratios[company]['Dividend_Yield'] = fin_ratios[0]['dividendYield']
            value_ratios[company]['Gross_Profit_Margin'] = fin_ratios[0]['grossProfitMargin']
            #more financials on growth:https://financialmodelingprep.com/api/v3/financial-growth/AAPL?apikey=demo
            growth_ratios = requests.get(f'https://financialmodelingprep.com/api/v3/financial-growth/{company}?apikey={demo}').json()
            value_ratios[company]['Revenue_Growth'] = growth_ratios[0]['revenueGrowth']
            value_ratios[company]['NetIncome_Growth'] = growth_ratios[0]['netIncomeGrowth']
            value_ratios[company]['EPS_Growth'] = growth_ratios[0]['epsgrowth']
            value_ratios[company]['RD_Growth'] = growth_ratios[0]['rdexpenseGrowth']
    except:
        pass
print(value_ratios)


'''
Value Ratio Dictionary outcome:
{'AAPL': {'ROE': 0.6106445053487756, 'ROA': 0.16323009842961633,
          'Debt_Ratio': 0.7326921031797611, 'Interest_Coverage': 18.382829977628635,
          'Payout_Ratio': 0.25551976255972203, 'Dividend_Payout_Ratio': 0.25551976255972203,
          'PB': 12.709658271815046, 'PS': 4.420393881402446, 'PE': 20.81351450883162, 
          'Dividend_Yield': 0.012276627402416805, 'Gross_Profit_Margin': 0.3781776810903472,
          'Revenue_Growth': -0.020410775805267418, 'NetIncome_Growth': -0.07181132519191681,
          'EPS_Growth': -0.003330557868442893, 'RD_Growth': 0.1391542568137117},
 'MSFT': {'ROE': 0.3834652594547054, 'ROA': 0.13693658482111698, 
 'Debt_Ratio': 0.6428970253632798, 'Interest_Coverage': 5.881980640357408, 
 'Payout_Ratio':0.35196228338430174, 'Dividend_Payout_Ratio': 0.3519622833843017, 
 'PB': 10.52384979966774, 'PS': 8.557532401484389, 'PE': 27.444076197757386, 
 'Dividend_Yield': 0.012824708722134454, 'Gross_Profit_Marg
'''

#Creating a Pandas DataFrame containing Financial Ratios
DF = pd.DataFrame.from_dict(value_ratios,orient='index')
print(DF.head(4))

#Creating our Ranking Investment Model
#criteria ranking
ROE = 1.2
ROA = 1.1
Debt_Ratio = -1.1
Interest_Coverage = 1.05
Dividend_Payout_Ratio = 1.01
PB = -1.10
PS = -1.05
Revenue_Growth = 1.25
Net_Income_Growth = 1.10

#mean to enable comparison across ratios
ratios_mean = []
for item in DF.columns:
 ratios_mean.append(DF[item].mean())#divide each value in dataframe by mean to normalize values
DF = DF / ratios_mean

#add a new column into our Pandas DataFrame containing the ranking factor
DF['ranking'] = DF['NetIncome_Growth']*Net_Income_Growth + DF['Revenue_Growth']*Revenue_Growth  + DF['ROE']*ROE + DF['ROA']*ROA + DF['Debt_Ratio'] * Debt_Ratio + DF['Interest_Coverage'] * Interest_Coverage + DF['Dividend_Payout_Ratio'] * Dividend_Payout_Ratio + DF['PB']*PB + DF['PS']*PS

#print the DataFrame including the ranking factor for each of the stocks in our 
#investment model
final = DF.sort_values(by=['ranking'],ascending=False)
print(DF.sort_values(by=['ranking'],ascending=False))
