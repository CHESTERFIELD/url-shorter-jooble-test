from app import create_app
from flask_migrate import Migrate
from models import db

app = create_app()

migrate = Migrate(app, db)
print(app.config)


@app.route('/')
def hello_world():
    return 'Hello, World!'
