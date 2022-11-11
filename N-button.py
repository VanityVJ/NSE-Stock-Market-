from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def main():
    return """<!DOCTYPE html>
                   <head>
                   
                      <script type="text/javascript" src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
                      <script>
                           $(document).ready(function(){

                                $('#btnSend').click(function(){

                                    $.ajax({
                                      type: 'POST',
                                      url: '/process',
                                      success: function(data){
                                        alert(data);
                                      }
                                    });
                                });

                           });
                      </script>
                   </head>
                   <body>
                    <input type="button" id="btnSend" value="Confirm Time">
                   </body>
                   </html>"""


@app.route('/process', methods=['POST'])
def view_do_something():

    if request.method == 'POST':
        import plotly.express as px
        import pandas as pd
        import matplotlib.pyplot as plt
        import plotly.express as px
        import plotly.graph_objects as go
        import plotly.io as pio
        from dash import dcc, html, Input, Output, Dash

        try:
            with open('C:\\Users\\VJN\Desktop\\Sunny-proj\\web-site-data\\time.txt', 'r') as file:
                datafile = file.readline()
                print(datafile)
                value1, value2 = datafile.split('-')
                print(type(value1))
                print(type(value2))

            Nfilenamecsv = "Nifty-2022-11-10-"+value1+"-"+value2+".csv"
            print(Nfilenamecsv)
            optionchain = pd.read_csv(
                "C:\\Users\\VJN\\Desktop\\Sunny-proj\\" + Nfilenamecsv)
        except:
            with open('C:\\Users\\VJN\Desktop\\Sunny-proj\\web-site-data\\time.txt', 'r') as file:
                datafile = file.readline()
                value1, value2 = datafile.split('-')
                value2 = int(value2)
                print(type(value2))
                value2 -= 5
                value2 = str(value2)
                print(value2)
                Nfilenamecsv = "Nifty-2022-11-10-"+value1+"-"+value2+".csv"
                print(Nfilenamecsv)
                optionchain = pd.read_csv(
                    "C:\\Users\\VJN\\Desktop\\Sunny-proj\\" + Nfilenamecsv)

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
                              x=['CALL OI', 'PUT OI'], text_auto='.2s', orientation='h', color_discrete_sequence=['crimson', 'green'], template=template, title="Nifty PUT & CALL OI Trend: ")
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
        optionchain['Var-Call'] = optionchain['CALL OI'] + \
            optionchain['CALL CHNG OI']
        optionchain['Var-Put'] = optionchain['PUT OI'] + \
            optionchain['PUT CHNG OI']

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

        print("Data Downloaded and Plot created Succesfully")

    else:
        return "NO OK"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
