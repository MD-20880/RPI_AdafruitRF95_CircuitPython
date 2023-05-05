# ;==========================================
# ; Title:  SensorPi
# ; Author: Mingzhang Deng
# ; Date:   26 APR 2023
# ;==========================================

#This is a simple front end program
#The purpose of this program is to display the sensor data output


#This file could be further developed to be a front end control panel

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import utils
import datetime
from pprint import pprint


data = utils.loadSensorData("./logtest.txt")

def plotData(sensorID, parameter):
    dataframeDict = {parameter:[],
                    "TIME":[]}
    #Select Pressure
    for i in data["18"].keys():
        para = data["18"][i].get(parameter)
        if para is not None:
            dataframeDict[parameter].append(float(para))
            time = datetime.datetime.fromtimestamp(float(i))
            dataframeDict['TIME'].append(time)

    df = pd.DataFrame(data=dataframeDict)
    return df


#replace with Sensor Data






if __name__ == '__main__':
    # pprint(data)
    app = Dash(__name__)
    app.layout = html.Div([
        html.H2(children='Temperature', style={'textAlign':'center'}),
        dcc.Graph(figure=px.line(plotData("18","TEMPERATURE"),x='TIME', y='TEMPERATURE')),
        html.H2(children='PRESSURE', style={'textAlign':'center'}),
        dcc.Graph(figure=px.line(plotData("18","PRESSURE"),x='TIME', y='PRESSURE')),
        html.H2(children='PIR', style={'textAlign':'center'}),
        dcc.Graph(figure=px.line(plotData("18","PIR"),x='TIME', y='PIR'))
    ])

    
    app.run_server(debug=True)

    
