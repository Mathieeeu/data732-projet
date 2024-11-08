'''
Barchart of number of articles per month
'''

import plotly.graph_objects as go
import json
import calendar
from datetime import datetime

file_name = "topaz-data732--france--www.fdesouche.com--20190101--20211231.json"

f = open("data/"+file_name, 'r', encoding='utf-8')
df = json.loads(f.read())
f.close()

articles_per_month = []

data_months = df["data-all"]
for year, months in data_months.items():
    for month, cat in months.items():
        name_month = calendar.month_name[int(month)]
        articles_count = sum(len(cat[c]) for c in cat)
        articles_per_month.append([f"{year}-{name_month}",articles_count])
 
sorted_data = sorted(articles_per_month, key=lambda x: datetime.strptime((x[0]), "%Y-%B"))        
        
months = [sorted_data[i][0] for i in range(len(sorted_data))]
counts = [sorted_data[j][1] for j in range (len(sorted_data))]

fig = go.Figure(data=[
    go.Bar(x=months,
           y=counts,
           marker=dict(
                color=counts, 
                colorscale="Greens",
                colorbar=dict(title="Number of Articles")  # Afficher une barre de couleur à droite
            ),
            hovertemplate="<b>Date:</b> %{x}<br>" + "<b>Number of articles:</b> %{y}<extra></extra>"
    )
])

fig.update_layout(
    title="Articles per month",
    xaxis_title="Month",
    yaxis_title="Number of articles",
    xaxis_tickangle=-45,
    template="plotly_white"
)

fig.show()
