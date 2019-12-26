import unit_laliga
import pymysql

conn = pymysql.connect("localhost", "ravid", "tommy1513", "win_chance_predicte")
cur = conn.cursor()

values = list()|


def get_league_data():
    for index in range(len(unit_laliga.table_data)):
        values.append(unit_laliga.send_team_data(index))


"""insert all data in table"""


def insert_to_data_base():
    get_league_data()
    command = f"insert into la_liga (TeamName, Pos, numofgames, win, draw, loss, points, point_avr, goals_dif, last_win, last_draw, last_loss, league_name, league_level, num_clubs, number_of_games_in_the_league) values "
    for value in values:
        command += f"{value}, "

    command = command[:-2]
    cur.execute(command)
    conn.commit()


"""update the table data"""


def update_data_table():
    get_league_data()
    i = 1
    for value in values:
        command = f"update win_chance_predicte.la_liga set TeamName= '{value[0]}', Pos= {value[1]}, numofgames= {value[2]}, win= {value[3]}, draw= {value[4]}, loss= {value[5]}, points= {value[6]}, point_avr= {value[7]}, goals_dif= {value[8]}, last_win= {value[9]}, last_draw= {value[10]}, last_loss= {value[11]}, league_name= '{value[12]}', league_level= {value[13]}, num_clubs= {value[14]}, number_of_games_in_the_league= {value[15]} where Pos = {i}"
        i += 1
        cur.execute(command)


# insert_to_data_base()
update_data_table()

conn.commit()
