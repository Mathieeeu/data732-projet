'''
Barchart of the most frequent keywords in the dataset
'''

import plotly.graph_objects as go
import json

# Load data
file_name = "topaz-data732--france--www.fdesouche.com--20190101--20211231.json"
# json struct : data-all -> <year> -> <month> -> <day> -> [<article_id> -> kws : 'nb']

f = open("data/" + file_name, "r", encoding="utf-8")
data = json.loads(f.read())
f.close()

# Count keywords frequency
keywords = {}
keywords_total = {}
for year in data["data-all"]:
    keywords_per_years = {}
    for month in data["data-all"][year]:
        for day in data["data-all"][year][month]:
            for article in data["data-all"][year][month][day]:
                for kw in article['kws']:
                    if kw in keywords_total:
                        keywords_total[kw] += article['kws'][kw]
                    else:
                        keywords_total[kw] = article['kws'][kw]
                    if kw in keywords_per_years:
                        keywords_per_years[kw] += article['kws'][kw]
                    else:
                        keywords_per_years[kw] = article['kws'][kw]
                        
    keywords[year] = keywords_per_years
   
keywords["All"] = keywords_total
keywords = dict(sorted(keywords.items()))

# Sort keywords by frequency (and make a subdict with the n most frequent)
n = 20
top_keywords = {}
for key in keywords.keys() :
    keywords[key] = dict(sorted(keywords[key].items(), key=lambda item: item[1], reverse=True))
    top_keywords[key] = {k: keywords[key][k] for k in list(keywords[key])[:n]}


# Plot
fig = go.Figure()

for key in keywords.keys():
    fig.add_trace(
        go.Bar(
            x=list(top_keywords[key].keys()), 
            y=list(top_keywords[key].values()),
            marker=dict(color=list(top_keywords[key].values()), colorscale='RdBu'),
            text=list(top_keywords[key].values()),
            textposition='outside',
            marker_line_width=1,
            marker_line_color='black',
            hovertemplate="The word '<b>%{x}</b>' appears %{y} times<extra></extra>",
            visible=(key == "All")
    ))
    


fig.update_layout(title_text="Most frequent keywords in the dataset",
                  xaxis_title="Keywords",
                  yaxis_title="Frequency",
                  updatemenus=[
                      dict(
                          buttons=[
                            dict(
                                label=year,
                                method="update",
                                args=[{"visible": [i == j for i in range(len(keywords.keys()))]},
                                    {"title": f"Most frequent keywords in {year}"} if j!=len(keywords.keys())-1 else {"title": f"Most frequent keywords in the dataset"}]
                                )
                            for j, year in enumerate(keywords.keys())
                        ],
                        direction="down",
                        showactive=True,
                        x=1,  # Shift the menu to the right of the graph
                        xanchor="left",  # Align the menu to the left side of the dropdown
                        y=1,  # Position the menu at the top of the figure
                        yanchor="top",
                        active=len(keywords.keys())-1
                    ),
                ]
)

fig.show()