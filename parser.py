from requests import get
from json import loads, dump
from datetime import datetime


def get_games_list(country):
    r = get(
        f'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country={country}')
    games = loads(r.text)["data"]["Catalog"]["searchStore"]["elements"]
    with open('games list.json', 'w') as file:
        dump(games, file)
    return games


def active_promotions_list(games):
    active_games = []
    for game in games:
        if game["promotions"] != None:
            if game["promotions"]["promotionalOffers"] != []:
                active_games.append(game)
    return active_games


def upcoming_promotions_list(games):
    upcoming_games = []
    for game in games:
        if game["promotions"] != None:
            if game["promotions"]["promotionalOffers"] == []:
                upcoming_games.append(game)
    return upcoming_games


def get_title(game):
    if game['title'] != None:
        return game['title']
    else:
        return None


def get_company_seller(game):
    if game['seller'] != None:
        if game['seller']['name'] != None:
            return game['seller']['name']
        else:
            return None

    else:
        return None


def get_price(game):
    if game["price"] != None:
        if game["price"]['totalPrice'] != None:
            if game["price"]['totalPrice']['fmtPrice'] != None:
                if game["price"]['totalPrice']['fmtPrice']['originalPrice'] != None:
                    return game["price"]['totalPrice']['fmtPrice']['originalPrice']
                else:
                    return None
            else:
                return None
        else:
            return None
    else:
        return None


# game['keyImages'][4]['url']
# return "ThumbnailNotFound (THIS IS NOT URL, I AM SERIOUSLY)"

def get_thumbnail(game):
    if game['keyImages'] != None:
        for image in game['keyImages']:
            if image['type'] != None:
                if image['type'] == 'Thumbnail':
                    return image['url']
                else:
                    continue
            else:
                continue
    else:
        return None


def main():
    games = get_games_list('RU')
    active_games = active_promotions_list(games)
    upcoming_games = upcoming_promotions_list(games)
    for game in games:
        print(f'''\nName: {get_title(game)},
Company Seller: {get_company_seller(game)}
Price: {get_price(game)}
Thumbnail: {get_thumbnail(game)}
----------------------------------------\n''')


if __name__ == "__main__":
    main()
