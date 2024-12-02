'''
Dashboard
'''
import json
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc


data = ["topaz-data732--france--www.fdesouche.com--20190101--20211231.json"]

#Create the dash app
app = dash.Dash()

#Layout setup
app.layout = html.Div(children=[
    html.H1(children = "Dashboard test"),
    dcc.Dropdown(id="dataset",
                 options = [{'label': file}
                            for file in data],
                 value = data[0]),
    dcc.Graph(id = "graphs")
])

#Callback function
@app.callback(
    Output(component_id = "graphs", component_property="figure"),
    Input(component_id = "dataset", component_property = "value")
)

def update_graphs(selected_dataset):
    #Load dataset
    f = open(selected_dataset, "r", encoding="utf-8")
    data = json.loads(f.read())
    f.close()
    
    #Generate graphs
    frequent_keywords = 
    fig = 
    
    return fig