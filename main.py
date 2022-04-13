from flask import Flask, render_template, redirect, url_for, flash
# from flask_bootstrap import Bootstrap
# from flask_ckeditor import CKEditor
# from datetime import date
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
# from flask_gravatar import Gravatar
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fsahfhlsbanfherio1r7eyhro1738eyrh'

##CONNECT TO DB

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///meter.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLES
class Meters(db.Model):
    __tablename__ = 'meters'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    meters_data = relationship('MeterData', back_populates='meter_r')


class MeterData(db.Model):
    __tablename__ = 'meter_data'
    id = db.Column(db.Integer, primary_key=True)

    meter_id = db.Column(db.Integer, db.ForeignKey('meters.id'))
    meter_r = relationship('Meters', back_populates='meters_data')

    timestamp = db.Column(db.DateTime(timezone=True), nullable=False)
    value = db.Column(db.Integer, nullable=False)


db.create_all()



@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/meters/')
def show_all_meters():
    meters = Meters.query.all()
    return render_template('meters.html', all_meters=meters)


@app.route('/meter/<int:meter_id>')
def meter(meter_id):
    meter_info = Meters.query.get(meter_id)
    return render_template('meter.html', meter_information=meter_info)


if __name__ == "__main__":
    app.run(debug=True)
