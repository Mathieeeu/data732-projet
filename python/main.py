from dashboard import generate_dashboard
import glob

# f = open("data/topaz-data732--france--www.fdesouche.com--20190101--20211231.json", "r", encoding="utf-8")
# data = json.loads(f.read())
# f.close()

# fig1, fig2 = mentionned_countries_map(data)
# fig1.show()
# fig2.show()


# Load data from all json files in the data folder
file_list = glob.glob("data/*.json")

    
html_files = [
    {'label': 'data/topaz-data732--france--fr.sputniknews.africa--20190101--20211231.json', 'value': 'graph_france_sputnik.html'},
    {'label': 'data/topaz-data732--france--french.presstv.ir--20190101--20211231.json', 'value': 'graph_france_presstv.html'}
]

    
if __name__ == "__main__":
    app = generate_dashboard(html_files)
    app.run_server(debug = True)
