from frequent_keywords import frequent_keywords_hist
from mentioned_countries import mentionned_countries_map
import glob

def generate_dashboard(filename, excluded_countries = ["France"]):
    print(f"Generating dashboard ...", end=" ")
    fig = frequent_keywords_hist(filename)
    fig1, fig2 = mentionned_countries_map(filename, excluded_countries)
    fig.show()
    fig1.show()
    fig2.show()
    print("(done)")

# Load data from all json files in the data folder
file_list = glob.glob("data/*.json")

# Generate dashboard for each file
for file in file_list:
    excluded_countries = ["France", "Mali"] if "mali" in file else ["France"]
    generate_dashboard(file, excluded_countries)