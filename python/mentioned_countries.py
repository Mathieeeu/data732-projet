'''
- Barchart of all the countries mentioned in the dataset
- World map with the countries mentioned in the dataset colored according to the number of times they are mentioned
'''

import plotly.graph_objects as go

import json
import plotly.express as px


# Load data
file_name = "topaz-data732--france--www.fdesouche.com--20190101--20211231.json"
# json struct : data-all -> <year> -> <month> -> <day> -> [<article_id> -> content : 'text']

f = open("data/" + file_name, "r", encoding="utf-8")
data = json.loads(f.read())
f.close()

# Country list (in French, from json)
f = open("python/countries/countries.json", "r", encoding="utf-8")
countries = json.loads(f.read())
f.close()


# Count countries frequency
for year in data["data-all"]:
    for month in data["data-all"][year]:
        for day in data["data-all"][year][month]:
            for article in data["data-all"][year][month][day]:
                for country in countries:
                    countries[country] += article['content'].count(country) # Count the number of times the country is mentioned in the article

# Exclude countries from the count (e.g. France here)
excluded_countries = ["France"]             

# Sort countries by frequency (and make a subdict with all the countries mentioned at least once + a subdict with the n most mentioned)
n = 30
countries = dict(sorted(countries.items(), key=lambda item: item[1], reverse=True))
mentioned_countries = {k: countries[k] for k in countries if countries[k] > 0 and k not in excluded_countries}
most_mentioned_countries = {k: mentioned_countries[k] for k in list(mentioned_countries)[:n]}
# print(mentioned_countries)
# print(most_mentioned_countries)

# Plot
fig = go.Figure(data=[
    go.Bar(
        x=list(most_mentioned_countries.keys()), 
        y=list(most_mentioned_countries.values()),
        marker=dict(color=list(most_mentioned_countries.values()), colorscale='RdBu'),
        text=list(most_mentioned_countries.values()),
        textposition='outside',
        marker_line_width=1,
        marker_line_color='black',
        hovertemplate="'<b>%{x}</b>' is mentioned %{y} times<extra></extra>"
)])
fig.update_layout(title_text="Most mentioned countries in the dataset (excluding " + ", ".join(excluded_countries) + ")",
                  xaxis_title="Countries",
                  yaxis_title="Frequency",
)
fig.show()

# World map
import plotly.express as px

# Translate country names to English using countries_fr_to_en.json
f = open("python/countries/countries_fr_to_en.json", "r", encoding="utf-8")
countries_fr_to_en = json.loads(f.read())
f.close()
countries = {countries_fr_to_en[k]: countries[k] for k in countries if k in countries_fr_to_en}
# print(countries)

# Colors for the map
colors = [
    "#FFFFCC", # Light yellow
    "#FFFF66", # Yellow
    "#FFCC33", # Gold yellow
    "#FF9933", # Light orange
    "#FF6600", # Orange
    "#FF3300", # Dark orange
    "#FF0000", # Light red
    "#CC0000", # Bright red
    "#990000", # Red
    "#660000", # Dark red
    "#0000FF", # Blue
]

# Make a choropleth map with custom colors
fig = px.choropleth(
    locations=list(countries.keys()), 
    locationmode="country names", 
    color=list(countries.values()), 
    color_continuous_scale=colors
)
fig.add_trace(px.choropleth(
    locations=["France"], 
    locationmode="country names", 
    color=[0], 
    color_continuous_scale=["#FFFFFF"]
))
fig.update_layout(
    title_text="Countries mentioned in the dataset (excluding " + ", ".join(excluded_countries) + ")"
)
fig.show()