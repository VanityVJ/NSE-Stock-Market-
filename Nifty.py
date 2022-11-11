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


with open('C:\\Users\\VJN\\Desktop\\Sunny\\Nifty-files\\bb\\sample.txt', 'r') as file:
    datafile = file.read()
    print(datafile)

Nfilenamecsv = "C:\\Users\\VJN\\Desktop\\Sunny\\Nifty-files\\bb\\Nifty-2022-11-04-"+datafile+".csv"
print(Nfilenamecsv)
optionchain = pd.read_csv(
    "C:\\Users\\VJN\\Desktop\\Sunny\\Nifty-files\\bb\\Nifty-2022-11-04-"+datafile+".csv")

# output the dataframe
print(optionchain)


def callMain():
    '''optionchain = dataframe(rawop)'''
    print(optionchain)
    print(optionchain['CALL OI'])
    # If we want to total CALL OI
    TotalCallOI = optionchain['CALL OI'].sum()
    TotalPutOI = optionchain['PUT OI'].sum()
    print(
        f'Total Call OI: {TotalCallOI}, Total Put OI: {TotalPutOI}, OI Difference : {TotalPutOI-TotalCallOI}')


# for Totaling the Call IO and Put IO
TotalCallOI = optionchain['CALL OI'].sum()
TotalPutOI = optionchain['PUT OI'].sum()
totalIO = []
totalG = {'Total Call OI': TotalCallOI, 'Total Put OI': TotalPutOI,
          'OI Difference': TotalPutOI+TotalCallOI}
totalIO.append(totalG)
totalchain = pd.DataFrame(totalIO)

# for Totaling the Call IO and Put IO
NTotalCallOI = optionchain['CALL CHNG OI'].sum()
NTotalPutOI = optionchain['PUT CHNG OI'].sum()
NtotalIO = []
NtotalG = {'Total Call Cng OI': NTotalCallOI, 'Total Cng Put OI': NTotalPutOI,
           'OI Difference': NTotalPutOI+NTotalCallOI}
NtotalIO.append(NtotalG)
Ntotalchain = pd.DataFrame(NtotalIO)


def bniftyGraph():
    for template in ["plotly_dark", ]:
        fig1 = px.bar(optionchain, y='STRIKE PRICE',
                      x=['CALL CHNG OI', 'CALL OI'], text_auto='.2s', orientation='h', template=template, title="Nifty CALL CHANGE IO Trend: '%s' theme" % template,)
        fig1.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig1.update_layout(yaxis_range=[17500, 19000])

        fig1.write_html('N-CALLIO-CHNGIO.html')

    fig = px.bar(totalchain, x=['Total Call OI', 'Total Put OI'], y='OI Difference',
                 title='Total CALL+PUT')
    fig.update_traces(textposition="auto")
    fig.update_layout({
        'plot_bgcolor': 'rgba(90,90,90,0.8)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    })
    fig.write_html('NTOTAL.html')

    for template in ["plotly_dark", ]:
        fig2 = px.bar(optionchain, y='STRIKE PRICE',
                      x=['PUT CHNG OI', 'PUT OI'], text_auto='.2s', orientation='h', template=template, title="Nifty PUT CHANGE IO Trend: '%s' theme" % template,)
        fig2.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig2.update_layout(yaxis_range=[17000, 18500])

        fig2.write_html('N-PUTIO-PUTCHNGIO.html')


bniftyGraph()

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


def dashboardGraph():
    for template in ["plotly_dark", ]:
        fig3 = px.bar(optionchain, y='STRIKE PRICE',
                      x=['Var-Call', 'Var-Put'], text_auto='.2s', orientation='h', template=template, title="Nifty Consolidated PUT and CALL: '%s' theme" % template,)
        fig3.update_traces(textfont_size=10, textangle=0,
                           textposition="outside", cliponaxis=False)
        fig3.update_layout(yaxis_range=[17000, 19000])

        fig3.write_html('N-DIFF-CALL-V-PUT.html')

    for template in ["plotly_dark", ]:
        fig4 = px.bar(ctotalchain, y='cOI Difference',
                      x=['CTotal Call OI', 'cTotal Put OI'], text_auto='.2s', orientation='h', template=template, title="Sum of Consolidated PUT and CALL: ' % s' theme" % template,)
        fig4.update_traces(textfont_size=20, textangle=0,
                           textposition="outside", cliponaxis=False)

        fig4.write_html('cNTOTAL.html')


dashboardGraph()

print("Data Downloaded and Plot created Succesfully")
