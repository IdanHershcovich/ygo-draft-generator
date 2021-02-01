import requests
import json


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
    with open('ygo-sets.json', 'w', encoding='utf-8') as f:
        json.dump(sets, f, ensure_ascii=False, indent=4)



saveSets()