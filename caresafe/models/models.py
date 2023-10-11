from caresafe import db, bcrypt
import datetime


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone_number = db.Column(db.String)
    address = db.Column(db.String)

    appointments = db.relationship('Appointment', back_populates='client')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Client {self.first_name} {self.last_name}>'


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    client = db.relationship('Client', back_populates='appointments')
    user = db.relationship('User', back_populates='appointments')  
    panics = db.relationship('Panic', back_populates='appointment')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def set_date(self, date: str):
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Appointment {self.id}>'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    checked_in = db.Column(db.Boolean, default=False)

    appointments = db.relationship('Appointment', back_populates='user')
    panics = db.relationship('Panic', back_populates='user')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<User {self.username}>'


class Panic(db.Model):
    __tablename__ = 'panics'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    appointment = db.relationship('Appointment', back_populates='panics')
    user = db.relationship('User', back_populates='panics')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f'<Panic {self.id} {self.user} {self.appointment}>'
    