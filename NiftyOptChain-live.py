#! python3
# Libraries
import plotly.express as px
import requests
import json
import math
import pandas as pd
import time
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime


url_nf = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8',
           'accept-encoding': 'gzip, deflate, br'}

try:
    session = requests.Session()
    request = session.get(url_nf, headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url_nf, headers=headers, cookies=cookies).json()
    rawdata = pd.DataFrame(response)
    rawop = pd.DataFrame(rawdata['filtered']['data']).fillna(0)
except Exception as e:
    print("Data was no fetched from Server" + str(e))

try:
    def dataframe(rawop):
        data = []
        for i in range(0, len(rawop)):
            calloi = callcoi = cltp = putoi = putcoi = pltp = 0
            stp = rawop['strikePrice'][i]
            # For CALLS data
            if (rawop['CE'][i] == 0):
                calloi = callcoi = 0
            else:
                calloi = rawop['CE'][i]['openInterest']
                callcoi = rawop['CE'][i]['changeinOpenInterest']
                cltp = rawop['CE'][i]['lastPrice']

            # For PUT data
            if (rawop['PE'][i] == 0):
                putoi = putcoi = 0
            else:
                putoi = rawop['PE'][i]['openInterest']
                putcoi = rawop['PE'][i]['changeinOpenInterest']
                pltp = rawop['PE'][i]['lastPrice']

            # Data stored in to a arry
            opdata = {
                'CALL OI': calloi, "CALL CHNG OI": callcoi, 'CALL LTP': cltp, 'STRIKE PRICE': stp,
                'PUT OI': putoi, "PUT CHNG OI": putcoi, 'PUT LTP': pltp}
            data.append(opdata)
        optionchain = pd.DataFrame(data)
        return optionchain
except Exception as e:
    print("Data BankNifty  file was not Created" + str(e))

optionchain = dataframe(rawop)
# output the dataframe
print(optionchain)


def callMain():
    print(optionchain)
    # If we want to total CALL OI
    TotalCallOI = optionchain['CALL OI'].sum()
    TotalPutOI = optionchain['PUT OI'].sum()
    print(
        f'Total Call OI: {TotalCallOI}, Total Put OI: {TotalPutOI}, OI Difference : {TotalPutOI-TotalCallOI}')


# for Totaling the Call Chng IO and Put Chng IO
TotalCallCngOI = optionchain['CALL CHNG OI'].sum()
TotalPutCngOI = optionchain['PUT CHNG OI'].sum()
TotalSTP = optionchain['STRIKE PRICE'].sum()
totalIO = []
totalG = {'Total Call Cng OI': TotalCallCngOI, 'Total Put Cng OI': TotalPutCngOI,
          'OI Difference': TotalSTP+TotalPutCngOI}
totalIO.append(totalG)
totalCngIO = pd.DataFrame(totalIO)
print(totalIO)

# for Totaling the Call IO and Put IO
TotalCallOI = optionchain['CALL OI'].sum()
TotalPutOI = optionchain['PUT OI'].sum()
TotalSTP = optionchain['STRIKE PRICE'].sum()
totalIOH = []
totalH = {'Total Call OI': TotalCallOI, 'Total Put OI': TotalPutOI,
          'OI Difference': TotalSTP+TotalPutOI}
totalIOH.append(totalH)
totalIOH = pd.DataFrame(totalIOH)


def niftyGraph():
    for template in ["plotly_dark"]:
        colors = ['lightslategray', 'crimson']
        colors[1] = 'crimson'
        fig1 = px.bar(optionchain, y='STRIKE PRICE', x=['CALL CHNG OI', 'PUT CHNG OI'], text_auto='.2s', orientation='h', color_discrete_sequence=['crimson', 'green'],
                      template=template, title="Nifty CALL & PUT CHANGE-OI Trend: ")
        fig1.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig1.update_layout(barmode='group', yaxis_range=[17500, 18600])
        fig1.update_yaxes(showgrid=False,
                          ticks="outside",
                          tickson="boundaries",

                          tick0=0,
                          dtick=50,
                          )

        fig1.write_html('N-PUTvsCALL-CHNG-OI.html')

    for template in ["plotly_dark"]:
        fig2 = px.bar(totalCngIO, x='OI Difference', y=['Total Call Cng OI', 'Total Put Cng OI'],
                      text_auto='.2s', orientation='v', color_discrete_sequence=['crimson', 'green'],
                      template=template, title="Nifty CALL & PUT CHANGE-OI Total: ")
        fig2.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig2.update_layout(barmode='group')
        fig2.write_html('N-TOTAL-CNG-OI.html')

    for template in ["plotly_dark", ]:
        fig2 = px.bar(optionchain, y='STRIKE PRICE',
                      x=['PUT OI', 'CALL OI'], text_auto='.2s', orientation='h', color_discrete_sequence=['crimson', 'green'], template=template, title="Nifty PUT & CALL OI Trend: ")
        fig2.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig2.update_layout(barmode='group', yaxis_range=[17500, 18600])
        fig2.update_yaxes(showgrid=False,
                          ticks="outside",
                          tickson="boundaries",

                          tick0=0,
                          dtick=50,
                          )

        fig2.write_html('N-PUT-OI-vs-CALL-OI.html')

    for template in ["plotly_dark"]:
        fig3 = px.bar(totalIOH, x='OI Difference', y=['Total Call OI', 'Total Put OI'],
                      text_auto='.2s', orientation='v', color_discrete_sequence=['crimson', 'green'],
                      template=template, title="Nifty CALL & PUT OI Total:")
        fig3.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig3.update_layout(barmode='group')
        fig3.write_html('N-TOTAL-OI.html')


niftyGraph()

# total avetage graph of PUT and CALLL
optionchain['Var-Call'] = optionchain['CALL OI'] + optionchain['CALL CHNG OI']
optionchain['Var-Put'] = optionchain['PUT OI'] + optionchain['PUT CHNG OI']

cTotalCallOI = optionchain['Var-Call'].sum()
cTotalPutOI = optionchain['Var-Put'].sum()
ctotalIO = []
ctotalG = {'CTotal Call OI': cTotalCallOI, 'cTotal Put OI': cTotalPutOI,
           'cOI Difference': 150000000}
ctotalIO.append(ctotalG)
ctotalchain = pd.DataFrame(ctotalIO)


def variableGraph():
    for template in ["plotly_dark", ]:
        fig4 = px.bar(optionchain, y='STRIKE PRICE',
                      x=['Var-Call', 'Var-Put'], text_auto='.2s', orientation='h', color_discrete_sequence=['crimson', 'green'], template=template, title="Nifty Consolidated PUT and CALL: ")
        fig4.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig4.update_layout(barmode='group', yaxis_range=[17500, 18600])
        fig4.update_yaxes(showgrid=False,
                          ticks="outside",
                          tickson="boundaries",

                          tick0=0,
                          dtick=50,
                          )

        fig4.write_html('N-DIFF-CALL-V-PUT.html')


variableGraph()

# Extre grapfun
df = px.data.gapminder().query(
    "continent == 'Europe' and year == 2007 and pop > 2.e6")
for template in ["plotly_dark", ]:
    fig = px.bar(df, y='pop', x='country', text='pop', color_discrete_sequence=['crimson', 'green'],
                 template=template, title="Extra GK: '%s' theme" % template,)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.write_html('Extra.html')

print("Data Downloaded and Plot created Succesfully")

'''# Print data in 3 min interval
while True:
    niftyGraph()
    variableGraph()
    time.sleep(180)'''
