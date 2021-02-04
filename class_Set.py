# Get all cards in a given set
# Sort?
#get rarities of each card
import getSets
import requests


lob = getSets.readJSONFile('ygo-sets.json')[0]
class Set():
    def __init__(self, cardset_obj):
        self.cardset_obj = cardset_obj
        self.url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset='
        self.cardset_name = None
        self.endp = None



    def getSetName(self):
        param = 'set_name'
        cardset_name = self.cardset_obj[param]
        print(cardset_name)
        return cardset_name

    def setCardSetName(self):
        pass

    def getSetInfo(self):
        url_endp = self.url + self.getSetName()
        self.endp = url_endp
        try:
            r = requests.get(url_endp)
            # getSets.writeJSONFile(r.json(), 'lob.json')
            return r.json()
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            self.getSetInfo()
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print("incorrect URL")
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
    
    def getRarities(self, rarity: str):
        data = getSets.readJSONFile('lob.json')['data']
        cards_objs = []
        setname = self.getSetName()
        for card in data:
            for cardset in card['card_sets']:
                if cardset['set_name'] == setname and cardset['set_rarity'] == rarity:
                    cards_objs.append(card)
                    break
        return cards_objs
               
                    

                
        
    def getRaritiesFromAPI(self, rarity: str):
        url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset=' + self.getSetName()
        rarities_url = url + '&rarity='+ rarity
        try:
            r = requests.get(rarities_url)
            return r.json()
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            self.getRaritiesFromAPI(rarity)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            print("incorrect URL")
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)


lob_set = Set(lob)


# rares = lob_set.getRarities("Rare")

# print(rares)

# for card in rares:
#     print(card['name'])

# print(len(rares))
