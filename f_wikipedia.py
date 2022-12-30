import requests
import wikipedia as w
import bs4
import pandas as pd


def get_calendar():
    url = "https://en.wikipedia.org/wiki/2023_Formula_One_World_Championship"
    r = requests.get(url)
    dfs = pd.read_html(r.text)
    
    ## calendar is 2nd table on page (bottom row is for source)
    races = dfs[1].head(-1)
    return races

def convert_coordinates(x):
    return tuple(float(y) for y in x.split(" / ")[-1].split("; "))

def get_infobox(url):
    # load page and get infobox section
    r = requests.get(url)
    site = bs4.BeautifulSoup(r.text)
    infobox = site.find('table', {'class': 'infobox'})

    # convert each row of infobox into key:value item in a dictionary
    items_html = infobox.find_all("tr")
    items_dict = {}
    for x in items_html:
        try:
            key = x.find("th").text
            value = x.find("td").text
            items_dict[key] = value
        except AttributeError:
            pass

    # look for any geo objects if there is no explicit coordinates in the infobox
    # else, use 0,0
    if "Coordinates" in items_dict.keys():
        items_dict["Coordinates"] = convert_coordinates(items_dict["Coordinates"])
    else:
        try:
            items_dict["Coordinates"] = convert_coordinates(infobox.find("span", {"class": "geo"}).text)
        except AttributeError:
            items_dict["Coordinates"] = (0,0)
    
    return items_dict


#TODO: convert to async
def circuit_to_coordinates(name):
    name = name.split(",")[0]
    
    # Las Vegas Circuit page has no coordinates
    if name == "Las Vegas Street Circuit":
        search = ["Las Vegas Strip"]
    else:
        search = w.search(name)
    track = w.page(search[0], auto_suggest=False)
    info = get_infobox(track.url)

    return info["Coordinates"]