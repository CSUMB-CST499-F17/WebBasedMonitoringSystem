#project/models.py
#database model, encrypts password using bcrypt
from app import db
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):

	__tablename__= 'users'	
	
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	_password = db.Column(db.Binary(60), nullable=False)
	auth = db.Column(db.Boolean, default=False)

	def __init__(self,username,pt_password):
		self.username = username
		self.password = pt_password
		self.auth = False

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def set_password(self, pt_password):
		self._password = bcrypt.generate_password_hash(pt_password)

	@hybrid_method
    	def is_correct_password(self, pt_password):
        	return bcrypt.check_password_hash(self.password, pt_password)

	def is_authenticated(self):
		return True
	
	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self._id)	
