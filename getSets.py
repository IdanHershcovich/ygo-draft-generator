import requests
import json
from datetime import datetime

# get all sets
# save sets to local file
# filter and sort sets in file
# read and write to local file


def getSetsJSON():
    """Grabs all the yugioh sets from the ygoprodeck API

    Raises:
        SystemExit: HTTP error

    Returns:
        JSON Object: 
        [{
            "set_name": "",
            "set_code": "",
            "num_of_cards": int,
            "tcg_date": ""
        },]
    """

    url = 'https://db.ygoprodeck.com/api/v7/cardsets.php'
    try:
        r = requests.get(url)
        return r.json()
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        getSets()
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Incorrect URL, please try another one")
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)


def saveSets():
    """Saves the yugioh sets returned from getSetsJSON() to a local .json file to avoid API calls """
    sets = getSetsJSON()
    writeJSONFile(sets, 'ygo-sets.json')


def filterSets():
    """Filters all the available sets to only exclude Speed Duel sets, promotional sets and Structure Decks"""
    sets = readJSONFile('ygo-sets.json')
    filtered = []
    for cardset in sets:
        if cardset['num_of_cards'] < 40 or "Speed Duel" in cardset['set_name'] or "Structure Deck" in cardset['set_name']:
            continue
        filtered.append(cardset)
    writeJSONFile(filtered, 'ygo-sets.json')


def readJSONFile(filename):
    """Reads the local JSON file containing the Card Sets

    Args:
        filename (string): the name and path of the JSON file to read

    Returns:
        [JSON]: JSON file data
    """
    with open(filename) as f:
        data = json.load(f)
    return data


def writeJSONFile(data, filename):
    """[Function to write to a specified JSON file]

    Args:
        data (JSON): The JSON data to write
        filename (string): the name and path of the JSON file to write to
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def sortSetsByDate():
    """Grabs the date attribute of the JSON Card Sets and sorts them by date. Oldest to Newest"""
    filename = 'ygo-sets.json'
    sets = readJSONFile(filename)
    sorted_sets = sorted(
        sets, key=lambda x: datetime.strptime(x['tcg_date'], "%Y-%m-%d"))
    writeJSONFile(sorted_sets, filename)

