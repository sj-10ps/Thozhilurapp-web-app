from flask import *
from public import public
from admin import admin
from overseer import overseer
from mate import mate
from api import api
from payment import payment



app=Flask(__name__)

app.secret_key="pjt"

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(overseer)
app.register_blueprint(mate)
app.register_blueprint(api)
app.register_blueprint(payment)

app.run(debug=True, host="0.0.0.0",port=5005)