from config import db

class Person(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    vk_id = db.Column(db.Integer, unique=True, nullable=False)

    distribution = db.Column(db.Boolean, default=True)

    Name = db.Column(db.String(80), default='-')
    Surname = db.Column(db.String(80), default='-')
    Middlename = db.Column(db.String(80), default='-')
    Gender = db.Column(db.String(80), default='-')
    Data_of_Birth = db.Column(db.String(80), default='-')
    Place_of_Birth = db.Column(db.String(80), default='-')
    Place_of_residence = db.Column(db.String(80), default='-')
    Nation = db.Column(db.String(80), default='-')
    Sexual_Orientation = db.Column(db.String(80), default='-')
    Img = db.Column(db.Text, default='https://w7.pngwing.com/pngs/178/595/png-transparent-user-profile-computer-icons-login-user-avatars-thumbnail.png')

    Count = db.Column(db.Integer, default=0)


    def __repr__(self):
        return '<User ' + str(self.vk_id) + '>'
