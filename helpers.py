import requests
from urllib.parse import urlencode
import settings

def get_summoner_puuid(summoner_name = None, summoner_tag = None, region = settings.DEFAULT_REGION):
    """
    Account-v1 API portal
    info abt summoner by their name and tag
    :return: summoner information as a dictionary (puuid) or None if issues
    """
    if not summoner_name:
        summoner_name = input("Summoner Name: ")
    if not summoner_tag:
        summoner_tag = input("Summoner tag without #: ")

    params = {
        'api_key' : settings.API_KEY
    }
    api_url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tag}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Issue getting summoner data from API: {e}")
        return None


def get_summoner_info(puuid, region = settings.DEFAULT_REGION_CODE):
    """
    SUMMONER-v4 API portal
    info abt summoner by their puuid
    :return: summoner information as a dictionary or None if issues
    """

    params = {
        'api_key' : settings.API_KEY
    }
    api_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Issue getting summoner data from API: {e}")
        return None

def get_match_ids_by_puuid(puuid, matches_count, region = settings.DEFAULT_REGION):
    '''
    Retrieves list of matches recently played by summoner
    :param puuid: str - retrieved before
    :param matches_count: int number of match ids to retrieve
    :param region: default
    :return: none or list of match ids
    '''
    params = {
        'api_key' : settings.API_KEY,
        'count' : matches_count,
        'type' : 'ranked'
    }
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Issue getting summoner match data from api: {e}')
        return None

def match_json(puuid, match_id, region=settings.DEFAULT_REGION):
    params = {
        'api_key': settings.API_KEY,
    }
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"

    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        match_data = response.json()
        return match_data
    except requests.exceptions.RequestException as e:
        print(f'Issue getting match data from match id from API: {e}')
        return None

def extract_useful_info_from_json(puuid, match_data):
    if puuid in match_data['metadata']['participants']:
        player_index = match_data['metadata']['participants'].index(puuid)
    else:
        return None
    game_duration = match_data['info']["gameDuration"]
    player_info = match_data['info']['participants'][player_index]
    return player_info['win'], game_duration // 60, player_info['championName']

def get_tier_and_division(puuid, region = settings.DEFAULT_REGION_CODE):
    params = {
        'api_key': settings.API_KEY
    }
    api_url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    try:
        response = requests.get(api_url, params=urlencode(params))
        response.raise_for_status()
        tier_div = response.json()
        return tier_div[0]['tier'], tier_div[0]['rank']
    except requests.exceptions.RequestException as e:
        print(f'Issue getting tier and division: {e}')
        return None

