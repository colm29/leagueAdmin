from leagueAdmin import db


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(80))


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default=str(db.func.year()), nullable=False)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Comp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    section = db.relationship(Section)
    cup = db.Column(db.Boolean, default=0, nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    day = db.relationship(Day)


class Surface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    surface_id = db.Column(db.Integer, db.ForeignKey('surface.id'), nullable=False)
    surface = db.relationship(Surface)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    home = db.relationship(Home)
    comp_id = db.Column(db.Integer, db.ForeignKey('comp.id'))
    comp = db.relationship(Comp)
    user_id = db.Column(db.Integer, db.ForeignKey('appuser.id'))
    appuser = db.relationship(AppUser)


class Referee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)


class NewsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    createdOn = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    createdBy = db.Column(db.Integer, db.ForeignKey('appuser.id'), nullable=False)
    user1 = db.relationship(AppUser, foreign_keys='NewsItem.createdBy')
    updatedOn = db.Column(db.DateTime)
    updatedBy = db.Column(db.Integer, db.ForeignKey('appuser.id'))
    user2 = db.relationship(AppUser,  foreign_keys='NewsItem.updatedBy')


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('comp.id'), nullable=False)
    comp = db.relationship(Comp)
    homeTeam = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team1 = db.relationship(Team, foreign_keys='Match.homeTeam')
    awayTeam = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team2 = db.relationship(Team, foreign_keys='Match.awayTeam')
    homeScore = db.Column(db.Integer)
    awayScore = db.Column(db.Integer)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    home = db.relationship(Home)
    referee_id = db.Column(db.Integer, db.ForeignKey('referee.id'), nullable=False)
    referee = db.relationship(Referee)
    createdOn = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    createdBy = db.Column(db.Integer, db.ForeignKey('appuser.id'), nullable=False)
    user1 = db.relationship(AppUser, foreign_keys='Match.createdBy')
    updatedOn = db.Column(db.DateTime)
    updatedBy = db.Column(db.Integer, db.ForeignKey('appuser.id'))
    user2 = db.relationship(AppUser, foreign_keys='Match.updatedBy')