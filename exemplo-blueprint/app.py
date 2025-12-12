from flask import Flask
from app.admin import admin
from app.public import public

app = Flask(__name__)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(public)

if __name__ == '__main__':
    app.run(debug=True)