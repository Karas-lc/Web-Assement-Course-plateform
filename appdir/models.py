from appdir import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(64))
    passwords = db.Column(db.String(128))
    email = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    key = db.Column(db.String(64))
    TeacherID = db.Column(db.String(64))
    StudentID = db.Column(db.String(64))
    introduction = db.Column(db.String(400))
    semester = db.Column(db.String(64))
