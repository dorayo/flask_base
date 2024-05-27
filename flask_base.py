"""Welcome to Flask_base Project!

## Project Overview

This is a basic flask project with minimal features but elegant structure.
"""
from app import create_app, db
from app.models.user import User, UserLoginRecord 
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': User, 'login_record':UserLoginRecord}

