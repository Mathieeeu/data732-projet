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

# Generate dashboard for each file
for file in file_list:
    excluded_countries = ["France", "Mali"] if "mali" in file else ["France"]
    #generate_dashboard(file, excluded_countries)
    
if __name__ == "__main__":
    app = generate_dashboard(file_list)
    app.run_server(debug = True)