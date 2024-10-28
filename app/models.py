from app import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.Text(), nullable=False)

    def __init__(self, username, hash):
        self.username = username
        self.hash = hash


class Users_information(db.Model):
    __tablename__ = 'users_information'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    realname = db.Column(db.Text(), nullable=True)
    nickname = db.Column(db.Text(), nullable=True)
    is_club_member = db.Column(db.Text(), nullable=True)
    contact = db.Column(db.Text(), nullable=True)

    def __init__(self, user_id, realname=None, nickname=None, is_club_member=None, contact=None):
        self.user_id = user_id
        self.realname = realname
        self.nickname = nickname
        self.is_club_member = is_club_member
        self.contact = contact

    def to_dict(self, include_user_id=True):
        data = {
            "realname": self.realname,
            "nickname": self.nickname,
            "is_club_member": self.is_club_member,
            "contact": self.contact
        }
        if include_user_id:
            data["user_id"] = self.user_id
            
        return data


class Users_role(db.Model):
    __tablename__ = 'users_role'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role = db.Column(db.Text(), nullable=False, default='reader')
    is_hidden = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, user_id, role='reader', is_hidden=1):
        self.user_id = user_id
        self.role = role
        self.is_hidden = is_hidden
        

class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_read = db.Column(db.Boolean, default=False)
    
    def __init__(self, sender_id, recipient_id, title, content):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.title = title
        self.content = content