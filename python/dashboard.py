'''
Dashboard
'''
import json
import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
from frequent_keywords import frequent_keywords_hist 
from mentioned_countries import mentionned_countries_map
from plotly.subplots import make_subplots

file_list = ["data/topaz-data732--france--www.fdesouche.com--20190101--20211231.json"]

#Create the dash app
app = dash.Dash()

#Layout setup
app.layout = html.Div(children=[
    html.H1(children = "Dashboard test"),
    dcc.Dropdown(id="dataset",
                 options = [{'label': file, 'value' : file}
                            for file in file_list],
                 value = file_list[0]),
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
    fig_frequent_keywords = frequent_keywords_hist(data)
    fig_country_hist, fig_country_map = mentionned_countries_map(data)
    
    # fig = make_subplots(rows=2, cols=2)
    # fig.add_trace(fig_frequent_keywords, row = 1, col = 1)
    # fig.add_trace(fig_country_hist, row = 1, col = 2)
    # fig.add_trace(fig_country_map, row = 2, col = 1)
    # Create a subplot
    
    fig = make_subplots(
        rows=2, cols=2,
        #subplot_titles=("Frequent Keywords", "Country Histogram", "Country Map"),
        specs=[
            [{"type": "xy"}, {"type": "xy"}],  # Row 1: cartesian plots
            [{"type": "geo"}, None]           # Row 2: map (geo) and empty cell
        ]
    )
    
    # Add traces from fig_frequent_keywords
    for trace in fig_frequent_keywords.data:
        fig.add_trace(trace, row=1, col=1)
    
    # Add traces from fig_country_hist
    for trace in fig_country_hist.data:
        fig.add_trace(trace, row=1, col=2)
    
    # Add traces from fig_country_map
    for trace in fig_country_map.data:
        fig.add_trace(trace, row=2, col=1)
    
    # Update layout for the subplot
    fig.update_layout(
        height=800,  # Adjust height to fit the content
        showlegend=False
    )
    
    return fig

#Run local server

if __name__ == "__main__":
    app.run_server(debug = True)