'''
Barchart of number of articles per month
'''

import plotly.graph_objects as go
import calendar
from datetime import datetime

def articles_per_month(data):
    articles_per_month = []

    data_months = data["data-all"]
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
                    colorscale="plasma"
                    #colorbar=dict(title="Number of Articles")  # Afficher une barre de couleur à droite
                ),
                hovertemplate="<b>Date:</b> %{x}<br>" + "<b>Number of articles:</b> %{y}<extra></extra>"
        )
    ])

    fig.update_layout(
        title="Articles per month",
        xaxis_title="Month",
        yaxis_title="Number of articles",
        xaxis_tickangle=-45,
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor = 'rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=10, r=20, t=40, b=10)
    )
    
    return fig
