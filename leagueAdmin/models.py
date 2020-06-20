from leagueAdmin import db


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    picture = db.Column(db.String(80))
    # created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    # created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    # user1 = db.relationship(AppUser, foreign_keys='app_user.created_by', nullable=False)
    # updated_on = db.Column(db.DateTime)
    # updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    # user2 = db.relationship(AppUser, foreign_keys='app_user.updated_by')


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default=str(db.func.year()), nullable=False)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class Surface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    surface_id = db.Column(db.Integer, db.ForeignKey('surface.id'), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    surface = db.relationship(Surface)
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class Comp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    cup = db.Column(db.Boolean, default=0, nullable=False)
    day_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    section = db.relationship(Section)
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)
    teams = db.relationship('Team', secondary='comp_reg')


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80))
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    home = db.relationship(Home)
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)
    comp = db.relationship(Comp, secondary='comp_reg')


class CompReg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('comp.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    active = db.Column(db.Boolean, default=True, nullable=False)

    comp = db.relationship(Comp, backref='comp_reg', lazy=True)
    team = db.relationship(Team, backref='comp_reg', lazy=True)
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class Referee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class NewsItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    message = db.Column(db.String(500), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class FixtureRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    comp_id = db.Column(db.Integer, db.ForeignKey('comp.id'), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    season = db.relationship(Season)
    comp = db.relationship(Comp)
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fixture_round_id = db.Column(db.Integer, db.ForeignKey('fixture_round.id'), nullable=False)
    datetime_override = db.Column(db.DateTime)
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'), nullable=False)
    referee_id = db.Column(db.Integer, db.ForeignKey('referee.id'), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    updated_on = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, db.ForeignKey('app_user.id'))

    fixture_round = db.relationship(FixtureRound)
    team1 = db.relationship(Team, foreign_keys='Match.home_team')
    team2 = db.relationship(Team, foreign_keys='Match.away_team')
    home = db.relationship(Home)
    referee = db.relationship(Referee)
    user1 = db.relationship(AppUser, foreign_keys=created_by)
    user2 = db.relationship(AppUser, foreign_keys=updated_by)
