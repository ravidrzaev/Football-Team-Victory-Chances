# class TeamData


class TeamData:
    def __init__(self, name, pos, win, draw, loss, points, goals_dif, last_win, last_draw, last_loss, games, league):
        self.name = name
        self.pos = pos
        self.win = win
        self.draw = draw
        self.loss = loss
        self.points = points
        self.point_avr = points / games
        self.goals_dif = goals_dif
        self.last_win = last_win
        self.last_draw = last_draw
        self.last_loss = last_loss
        self.games = games
        self.league = league

    def get_team_data(self):
        team_data = {'name': self.name, 'pos': self.pos, 'games': self.games, 'win': self.win, 'draw': self.draw,
                     'loss': self.loss, 'points': self.points, 'point_avr': self.point_avr, 'goals_dif': self.goals_dif,
                     'last_win': self.last_win, 'last_draw': self.last_draw, "last_loss": self.last_loss,
                     'league': self.league}
        return team_data

    def get_tuple_data(self):
        return self.name, self.pos, self.games, self.win, self.draw, self.loss, self.points, self.point_avr, self.goals_dif, self.last_win, self.last_draw, self.last_loss, \
               self.league['name'], self.league['level'], self.league['num_clubs'], self.league['number_of_games']
