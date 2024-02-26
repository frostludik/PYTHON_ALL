"""
elections_scraper.py (projekt 3): 
třetí projekt do Engeto Online Python Akademie

author: Ludek Mraz
email: ludek.mraz@centrum.cz
discord: Luděk M.#5570
"""

# This program scaps election results from site VOLBY.CZ
# Tested on district "Okres Brno-venkov"
# https://www.volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=11&xnumnuts=6203


import requests
from bs4 import BeautifulSoup as bs
import sys
import csv


def verify_arguments():
    """
    This function verifies given arguments:
    1st must be URL heading to https://www.volby.cz..
    2nd must be filename including .csv extension
    """
    if len(sys.argv) != 3:
        print("You must state 2 arguments: URL and CSV file name. Exiting program!")
        sys.exit()
    if not sys.argv[1].startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("1st argument is incorrect. Must be URL. Exiting program!")
        sys.exit()
    if not sys.argv[2].endswith(".csv"):
        print("2nd argument is incorrect. Missing file extension! Exiting program!")
        sys.exit()
    else:
        print(f"Scraping data from: {sys.argv[1]}")
        
        
def get_town_details(child, list):
    """
    This function takes a td tag representing a town in the HTML table and a list,
    and extracts the town name and code from the tag and appends them to the list.
    """
    list.append(child.find("a").string)
    list.append(child.parent.find_all()[2].string)
    return list


def get_town_soup(base_url, child):
    """
    Function takes a base URL and a td tag representing a town, and constructs the full
    URL for the town's page, fetches the HTML for the page, and returns a BeautifulSoup
    object representing the page.
    """
    town_url = requests.get(base_url + child.find("a").attrs["href"])
    return bs(town_url.text, "html.parser")


def get_totals(town_results, list):
    """
    This function takes a BeautifulSoup object representing a town's page and a list,
    and extracts the total number of registered voters,total number of envelopes sent, 
    and total number of valid votes from the page, and appends them to the list.
    """
    list.append(town_results.find("td", {"class": "cislo", "headers": "sa2"}).string)
    list.append(town_results.find("td", {"class": "cislo", "headers": "sa3"}).string)
    list.append(town_results.find("td", {"class": "cislo", "headers": "sa6"}).string)
    return list


def get_votes(parties, list):
    """
    This function takes a list of tr tags representing the rows in the HTML table
    containing data for each political party,and a list, and extracts the number of
    votes received by each party and appends them to the list.
    If the vote count is not present or is not a valid integer, it appends None to
    the list instead
    """
    for line in parties:
        if not line.find("th"):
            votes = line.find_all("td", {"class": "cislo"})
            if len(votes) >= 2 and votes[1].string.strip():
                list.append(int(votes[1].string.replace("\xa0", "").replace(",", "")))
            else:
                list.append(None)
    return list


def main():
    """
    This function runs the main programs. Calls functions and states global variables.
    """
    verify_arguments()
    output_file = sys.argv[2]
    district_url = sys.argv[1].replace('"', '')
    
    file = open(output_file, mode="w", encoding="UTF-16", newline='')
    writer = csv.writer(file, delimiter=";")
    
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    web = requests.get(district_url)
    soup = bs(web.text, "html.parser")
    all_towns = soup.find_all("td", {'class': 'cislo'})
    
    header = False

    for child in all_towns:
        town_data = []
        town_data = get_town_details(child, town_data)
        town_soup = get_town_soup(base_url, child)
        town_results = town_soup.find(id="ps311_t1")
        town_data = get_totals(town_results, town_data)
        parties = town_soup.find(id="inner").find_all("tr")
        town_data = get_votes(parties, town_data)

        if not header:
            column_names = ["code", "location", "registered", "envelopes", "valid"]
            for line in parties:
                if not line.find("th"):
                    column_names.append(line.find_all("td")[1].string)
            writer.writerow(column_names)
            header = True

        writer.writerow(town_data)

    file.close()
    print("Finished! Data successfuly saved in csv")

#call main function
main()
