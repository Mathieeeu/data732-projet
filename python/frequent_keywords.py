'''
Barchart of the most frequent keywords in the dataset
'''

import plotly.graph_objects as go
import json

# Load data
file_name = "topaz-data732--france--www.fdesouche.com--20190101--20211231.json"
# Structure du json : data-all -> <year> -> <month> -> <day> -> [<article_id> -> kws : 'nb']

f = open("data/" + file_name, "r", encoding="utf-8")
data = json.loads(f.read())
f.close()

# Count keywords frequency
keywords = {}
for year in data["data-all"]:
    for month in data["data-all"][year]:
        for day in data["data-all"][year][month]:
            for article in data["data-all"][year][month][day]:
                for kw in article['kws']:
                    if kw in keywords:
                        keywords[kw] += article['kws'][kw]
                    else:
                        keywords[kw] = article['kws'][kw]

# Sort keywords by frequency (and make a subdict with the n most frequent)
n = 20
keywords = dict(sorted(keywords.items(), key=lambda item: item[1], reverse=True))
top_keywords = {k: keywords[k] for k in list(keywords)[:n]}
# print(top_keywords)

# Plot with red-white-blue gradient and values on top of bars and 1px black border around bars
# when hovering over a bar, the value is displayed in a box "The word '<kw>' appears <n> times"

fig = go.Figure(data=[
    go.Bar(
        x=list(top_keywords.keys()), 
        y=list(top_keywords.values()),
        marker=dict(color=list(top_keywords.values()), colorscale='RdBu'),
        text=list(top_keywords.values()),
        textposition='outside',
        marker_line_width=1,
        marker_line_color='black',
        hovertemplate="The word '<b>%{x}</b>' appears %{y} times<extra></extra>"
)])
fig.update_layout(title_text="Most frequent keywords in the dataset",
                  xaxis_title="Keywords",
                  yaxis_title="Frequency",
)
fig.show()
