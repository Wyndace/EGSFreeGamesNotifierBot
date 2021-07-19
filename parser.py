# -*- coding: utf-8 -*-
from requests import get
from json import loads, dump
from datetime import datetime


def get_games_list(country):
    try:
        r = get(
            f'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country={country}')
        return loads(r.text)["data"]["Catalog"]["searchStore"]["elements"]
    except Exception as ex:
        print(ex)
        return None


def active_promotions_list(games):
    try:
        active_games = []
        for game in games:
            if game["promotions"] != None:
                if game["promotions"]["promotionalOffers"] != []:
                    game["status"] = "active"
                    active_games.append(game)
        return active_games
    except Exception as ex:
        print(ex)
        return None


def upcoming_promotions_list(games):
    try:
        upcoming_games = []
        for game in games:
            if game["promotions"] != None:
                if game["promotions"]["promotionalOffers"] == []:
                    game["status"] = "upcoming"
                    upcoming_games.append(game)
        return upcoming_games
    except Exception as ex:
        print(ex)
        return None


def ended_promotion_list(games):
    try:
        ended_games = []
        for game in games:
            if game["promotions"] == None:
                game["status"] = "ended"
                ended_games.append(game)
        return ended_games
    except Exception as ex:
        print(ex)
        return None


def get_title(game):
    try:
        return game['title']
    except Exception as ex:
        print(ex)
        return None


def get_company_seller(game):
    try:
        return game['seller']['name']
    except Exception as ex:
        print(ex)
        return None


def get_price(game):
    try:
        return game["price"]['totalPrice']['fmtPrice']['originalPrice']
    except Exception as ex:
        print(ex)
        return None


def get_thumbnail(game):
    try:
        for image in game['keyImages']:
            if image['type'] != None:
                if image['type'] == 'Thumbnail':
                    return image['url']
                else:
                    continue
            else:
                continue
    except Exception as ex:
        print(ex)
        return None


def get_begin_time(game):
    try:
        time_str = None
        if game["promotions"]["promotionalOffers"] != []:
            time_str = game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["startDate"]
        elif game["promotions"]["promotionalOffers"] == []:
            time_str = game["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0]["startDate"]
        time = None
        if time_str != None:
            time = datetime.strptime(
                str(time_str), "%Y-%m-%dT%H:%M:%S.000Z").timestamp()
        return time
    except Exception as ex:
        print(ex)
        return None


def get_end_time(game):
    try:
        time_str = None
        if game["promotions"]["promotionalOffers"] != []:
            time_str = game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0]["endDate"]
        elif game["promotions"]["promotionalOffers"] == []:
            time_str = game["promotions"]["upcomingPromotionalOffers"][0]["promotionalOffers"][0]["endDate"]
        time = None
        if time_str != None:
            time = datetime.strptime(
                str(time_str), "%Y-%m-%dT%H:%M:%S.000Z").timestamp()
        return time
    except Exception as ex:
        print(ex)
        return None


def get_link(game):
    try:
        return f'https://www.epicgames.com/p/{game["catalogNs"]["mappings"][0]["pageSlug"]}'
    except Exception as ex:
        print(ex)
        return None


def get_min_game_info(game):
    try:
        new_info = {}
        new_info["title"] = get_title(game)
        new_info["company_seller"] = get_company_seller(game)
        new_info["price"] = get_price(game)
        new_info["link"] = get_link(game)
        new_info["thumbnail"] = get_thumbnail(game)
        new_info["beginTime"] = get_begin_time(game)
        new_info["endTime"] = get_end_time(game)
        new_info["status"] = game['status']
        return new_info
    except Exception as ex:
        print(ex)
        return None


def build_min_games_list(country):
    try:
        games = get_games_list(country)
        active_games = active_promotions_list(games)
        upcoming_games = upcoming_promotions_list(games)
        ended_games = ended_promotion_list(games)
        filedata = {}
        filedata['allGames'] = []
        filedata['activeGames'] = []
        filedata['upcomingGames'] = []
        filedata['activeUpcomingGames'] = []
        filedata['endedGames'] = []
        for game in games:
            new_info = get_min_game_info(game)
            filedata['allGames'].append(new_info)
        for game in active_games:
            new_info = get_min_game_info(game)
            filedata['activeGames'].append(new_info)
            filedata['activeUpcomingGames'].append(new_info)
        for game in upcoming_games:
            new_info = get_min_game_info(game)
            filedata['upcomingGames'].append(new_info)
            filedata['activeUpcomingGames'].append(new_info)
        for game in ended_games:
            new_info = get_min_game_info(game)
            filedata['endedGames'].append(new_info)
        with open('games.min.json', 'w') as file:
            dump(filedata, file, indent=4)
        return 'OK'
    except Exception as ex:
        print(ex)
        return None


def main():
    build_min_games_list('RU')


if __name__ == "__main__":
    main()
