from requests import get
from json import loads, dump
from datetime import datetime


def get_games_list(country):
    r = get(
        f'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country={country}')
    return loads(r.text)["data"]["Catalog"]["searchStore"]["elements"]


def active_promotions_list(games):
    active_games = []
    for game in games:
        if game["promotions"] != None:
            if game["promotions"]["promotionalOffers"] != []:
                game["status"] = "active"
                active_games.append(game)
    return active_games


def upcoming_promotions_list(games):
    upcoming_games = []
    for game in games:
        if game["promotions"] != None:
            if game["promotions"]["promotionalOffers"] == []:
                game["status"] = "upcoming"
                upcoming_games.append(game)
    return upcoming_games


def ended_promotion_list(games):
    ended_games = []
    for game in games:
        if game["promotions"] == None:
            game["status"] = "ended"
            ended_games.append(game)
    return ended_games


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


def get_min_game_info(game):
    new_info = {}
    new_info["title"] = get_title(game)
    new_info["price"] = get_price(game)
    new_info["company_seller"] = get_company_seller(game)
    new_info["thumbnail"] = get_thumbnail(game)
    new_info["status"] = game['status']
    return new_info


def build_min_games_list(country):
    games = get_games_list(country)
    active_games = active_promotions_list(games)
    upcoming_games = upcoming_promotions_list(games)
    ended_games = ended_promotion_list(games)
    filedata = {}
    filedata['allGames'] = []
    filedata['activeGames'] = []
    filedata['upcomingGames'] = []
    filedata['endedGames'] = []
    for game in games:
        new_info = get_min_game_info(game)
        filedata['allGames'].append(new_info)
    for game in active_games:
        new_info = get_min_game_info(game)
        filedata['activeGames'].append(new_info)
    for game in upcoming_games:
        new_info = get_min_game_info(game)
        filedata['upcomingGames'].append(new_info)
    for game in ended_games:
        new_info = get_min_game_info(game)
        filedata['endedGames'].append(new_info)
    with open('games.min.json', 'w') as file:
        dump(filedata, file, indent=4)
    return 'OK'


def main():
    build_min_games_list('RU')


if __name__ == "__main__":
    main()
