from flask_migrate import Migrate
from flask_session import Session
from flask_mail import Mail
from flask_wtf import CSRFProtect
from apifairy import APIFairy
from flask_sqlalchemy import SQLAlchemy

session = Session()
mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
apifairy = APIFairy()