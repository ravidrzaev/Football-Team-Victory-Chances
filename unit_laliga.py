from bs4 import BeautifulSoup as bs
import urllib.request
from selenium import webdriver
import TeamData

table_data = []
last_games = []
league = {}


def league_data(league_name):
    """init the league data"""
    global league
    if league_name == "La Liga":
        league = {'name': 'La Liga', 'level': 1, 'num_clubs': 20, 'number_of_games': 38}
    elif league_name == "Premier League":
        league = {'name': 'Premier League', 'level': 1, 'num_clubs': 20, 'number_of_games': 38}
    elif league_name == "Serie A":
        league = {'name': 'Serie A ', 'level': 1, 'num_clubs': 20, 'number_of_games': 38}


def load_data_from_website(url):
    """get url and load league table data from url(website) to table_data list"""
    page = urllib.request.urlopen(url)
    soup = bs(page, 'html.parser')

    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    driver.implicitly_wait(100)
    driver.close()

    for game in soup.find_all('span'):
        if "standing-table" in str(game):
            last_games.append(str(game))

    for item in soup.find_all('tr'):
        if item.get_text().split()[0].isdigit():
            table_data.append(item.get_text().split())

    for row_data in table_data:
        if row_data[1].isalpha() and row_data[2].isalpha():
            row_data[1] += ' ' + row_data[2]
            row_data.pop(2)
        row_data[0], row_data[1] = row_data[1], row_data[0]  # now the team name in index 0

        for i in range(len(row_data)):
            if row_data[i].isdigit() or ('-' in row_data[i]):
                row_data[i] = int(row_data[i])

    for i in range(len(table_data)):
        init_last_games(i * 6, i * 6 + 6, table_data[i])


def init_last_games(first, last, team_list_data):
    """init to list data last games"""
    for i in range(3):
        team_list_data.append(0)
    for i in range(first, last):
        if 'win' in last_games[i]:
            team_list_data[-3] += 1
        elif 'draw' in last_games[i]:
            team_list_data[-2] += 1
        elif 'loss' in last_games[i]:
            team_list_data[-1] += 1


def select_teams(home_team, away_team):
    """get names of selected teams and call to get_win_chances with selected teams data"""
    for team_data in table_data:
        if home_team == team_data[0]:
            home_team = team_data
        elif away_team == team_data[0]:
            away_team = team_data
    get_win_chances(home_team, away_team)


def send_team_data(index):
    team = table_data[index]
    team = TeamData.TeamData(team[0], team[1], team[3], team[4], team[5],
                             team[9],
                             team[8], team[10],
                             team[11], team[12], team[2], league)
    return team.get_tuple_data()


def pos_effect(team):
    overall = (team['league']['num_clubs'] - team['pos'] + 1) / (team['league']['num_clubs'])
    overall *= (team['league']['number_of_games'] - team['games']) / team['league']['number_of_games']
    overall *= team['league']['level']
    return overall


def point_avr_effect(team):
    overall = (team['point_avr'] / 3) * (team['games'] / team['league']['number_of_games'])
    return overall


def goals_dif_effect(home_team, away_team):
    if (home_team['goals_dif'] / home_team['games']) > (away_team['goals_dif'] / away_team['games']):
        effect = [
            1 + 0.5 * (home_team['goals_dif'] / home_team['games'] - away_team['goals_dif'] / away_team['games']), 1]
    else:
        effect = [1,
                  1 + 0.5 * (away_team['goals_dif'] / away_team['games'] - home_team['goals_dif'] / home_team['games'])]
    return effect


def last_games_effect(team):
    last = (team['last_win'] * 2 + team['last_draw'] + team['last_loss'] * 0) / (
            (team['last_win'] + team['last_draw'] + team['last_loss']) * 2)
    return last


def predicting_chances(home_team, away_team):
    """get teams data and calculate win chances of these teams
       return home_team chances, draw chances, away_team chances"""
    home_team_overall = away_team_overall = 0
    home_team_overall += 7 * pos_effect(home_team)
    away_team_overall += 7 * pos_effect(away_team)
    home_team_overall += 10 * point_avr_effect(home_team)
    away_team_overall += 10 * point_avr_effect(away_team)
    goals_dif_eff = goals_dif_effect(home_team, away_team)
    home_team_overall += 10 * goals_dif_eff[0]
    away_team_overall += 10 * goals_dif_eff[1]
    home_team_overall += 15 * last_games_effect(home_team)
    away_team_overall += 15 * last_games_effect(away_team)
    home_team_overall *= 1.2

    if home_team_overall > away_team_overall:
        draw_chance = 30 + ((away_team_overall / home_team_overall) * 7)
    else:
        draw_chance = 30 + ((home_team_overall / away_team_overall) * 7)

    home_team_chance_to_win = (home_team_overall / (home_team_overall + away_team_overall)) * (100 - draw_chance)
    away_team_chance_to_win = (away_team_overall / (home_team_overall + away_team_overall)) * (100 - draw_chance)

    return home_team_chance_to_win, draw_chance, away_team_chance_to_win


def get_win_chances(home_team, away_team):
    """load team data of each team and call to predicting_chances function,
    print the chances result"""
    home_team_data = TeamData.TeamData(home_team[0], home_team[1], home_team[3], home_team[4], home_team[5],
                                       home_team[9],
                                       home_team[8], home_team[10],
                                       home_team[11], home_team[12], home_team[2], league)
    away_team_data = TeamData.TeamData(away_team[0], away_team[1], away_team[3], away_team[4],
                                       away_team[5],
                                       away_team[9],
                                       away_team[8], away_team[10],
                                       away_team[11], away_team[12], away_team[2], league)
    home_team_chances, draw, away_team_chances = predicting_chances(home_team_data.get_team_data(),
                                                                    away_team_data.get_team_data())
    print(
        f"""\nThe victory chances (result):\n{home_team[0]} (home team): {home_team_chances} %  draw:{draw} %  {away_team[0]} (away teeam): {away_team_chances} %""")

#
# if __name__ == '__main__':
#     load_data_from_website("https://www.skysports.com/la-liga-table")
