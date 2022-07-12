from flask import Flask, redirect, render_template, request, jsonify, abort, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc ,asc

from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, pprint
from datetime import datetime, timedelta
import  os
from os.path import isfile, join
from os import listdir
import json
from io import StringIO
from werkzeug.wrappers import Response
import itertools
import random
import string


app = Flask(__name__)
app.secret_key = 'development key'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="bartek1234",
    password="alamakota", # database passowrd hidden
    hostname="bartek1234.mysql.pythonanywhere-services.com",
    databasename="bartek1234$Messenger",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 # connection timeouts
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # no warning disruptions

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Student(db.Model):

    __tablename__ = "Student"
    id = db.Column(db.Integer, primary_key=True)
    Imie = db.Column(db.String(4096))
    Nazwisko = db.Column(db.String(4096))
    Indeks = db.Column(db.String(4096))
    Kierunek = db.Column(db.String(4096))
    Wydzial = db.Column(db.String(4096))
    Rok = db.Column(db.String(4096))



    def __init__(self, Imie, Nazwisko, Indeks, Kierunek, Wydzial, Rok):
        self.Imie = Imie
        self.Nazwisko = Nazwisko
        self.Indeks = Indeks
        self.Kierunek = Kierunek
        self.Wydzial = Wydzial
        self.Rok = Rok

class Pracownik(db.Model):

    __tablename__ = "Pracownik"
    id = db.Column(db.Integer, primary_key=True)
    Imie = db.Column(db.String(4096))
    Nazwisko = db.Column(db.String(4096))
    Tytul = db.Column(db.String(4096))
    Pokoj = db.Column(db.String(4096))
    Katedra = db.Column(db.String(4096))

    def __init__(self, id , Imie, Nazwisko, Tytul, Pokoj, Katedra):
        self.id = id
        self.Imie = Imie
        self.Nazwisko = Nazwisko
        self.Tytul = Tytul
        self.Pokoj = Pokoj
        self.Katedra = Katedra

class Wiadomosc(db.Model):

    __tablename__ = "Wiadomosc"
    id = db.Column(db.Integer, primary_key=True)
    Wiadomosc_id = db.Column(db.Integer)
    Status = db.Column(db.String(4096))   #typ zmiennej bool ?
    Tytul = db.Column(db.String(4096))
    Data = db.Column(db.String(4096))   #typ zmiennej data ?
    Osoba_1 = db.Column(db.Integer)
    Osoba_2 = db.Column(db.Integer)

    def __init__(self, id, Wiadomosc_id, Status, Tytul, Data, Osoba_1, Osoba_2):
        self.id = id
        self.Wiadomosc_id = Wiadomosc_id
        self.Status = Status
        self.Tytul = Tytul
        self.Data = Data
        self.Osoba_1 = Osoba_1
        self.Osoba_2 = Osoba_2

class Tresc(db.Model):

    __tablename__ = "Tresc"
    id = db.Column(db.Integer, primary_key=True)
    Tresc = db.Column(db.String(4096))
    Data = db.Column(db.String(4096))    #typ zmiennej data ?


    def __init__(self, id , Tresc, Data):
        self.id = id
        self.Tresc = Tresc
        self.Data = Data


class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id' ,'Imie', 'Nazwisko','Indeks','Kierunek','Wydzial','Rok')

class PracownikSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Imie', 'Nazwisko', 'Tytul', 'Pokoj', 'Katedra')

class WiadomoscSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Wiadomosc_id', 'Status', 'Tytul', 'Data', 'Osoba_1', 'Osoba_2')

class TrescSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Tresc', 'Data')

student_schema = StudentSchema()
studenci_schema = StudentSchema(many=True)

pracownik_schema = PracownikSchema()
pracownicy_schema = PracownikSchema(many=True)

wiadomosc_schema = WiadomoscSchema()
wiadomosci_schema = WiadomoscSchema(many=True)

tresc_schema = TrescSchema()
tresci_schema = TrescSchema(many=True)

@app.route('/student')
def get_student():
    all_users = Student.query.all()
    result = studenci_schema.dump(all_users)
    return jsonify(result)

@app.route("/studenci/<id>", methods=["GET"])
def get_Student(id):
    user = studenci_schema.query.get(id)
    result = student_schema.dump(user)
    return jsonify(result)

@app.route('/pracownik')
def get_pracownik():
    all_users = Pracownik.query.all()
    result = pracownicy_schema.dump(all_users)
    return jsonify(result)

@app.route("/pracownicy/<id>", methods=["GET"])
def get_Pracownik(id):
    user = pracownicy_schema.query.get(id)
    result = pracownik_schema.dump(user)
    return jsonify(result)

@app.route('/wiadomosc')
def get_wiadomosc():
    all_users = Wiadomosc.query.all()
    result = wiadomosci_schema.dump(all_users)
    return jsonify(result)

@app.route("/wiadomosci/<id>", methods=["GET"])
def get_Wiadomosc(id):
    user = wiadomosci_schema.query.get(id)
    result = wiadomosc_schema.dump(user)
    return jsonify(result)

@app.route('/tresc')
def get_tresc():
    all_users = Tresc.query.all()
    result = tresci_schema.dump(all_users)
    return jsonify(result)

@app.route("/tresci/<id>", methods=["GET"])
def get_Tresc(id):
    user = tresci_schema.query.get(id)
    result = tresc_schema.dump(user)
    return jsonify(result)

@app.route("/dstudent", methods=["POST"])
def add_student():
    A= request.json["Imie"]
    B= request.json["Nazwisko"]
    C= request.json["Indeks"]
    D= request.json["Kierunek"]
    E= request.json["Wydzial"]
    F= request.json["Rok"]
    new_user = Student(A,B,C,D,E,F)
    db.session.add(new_user)
    db.session.commit()  # PK increment
    user = Student.query.get(new_user.id)
    return student_schema.jsonify(user)

@app.route("/dpracownik", methods=["POST"])
def add_pracownik():
    I= request.json["id"]
    A= request.json["Imie"]
    B= request.json["Nazwisko"]
    C= request.json["Tytul"]
    D= request.json["Pokoj"]
    E= request.json["Katedra"]
    new_user = Pracownik(I,A,B,C,D,E)
    db.session.add(new_user)
    db.session.commit()  # PK increment
    user = Pracownik.query.get(new_user.id)
    return pracownik_schema.jsonify(user)

@app.route("/dwiadomosc", methods=["POST"])
def add_wiadomosc():
    I= request.json["id"]
    A= request.json["Wiadomosc_id"]
    B= request.json["Status"]
    C= request.json["Tytul"]
    D= request.json["Data"]
    E= request.json["Osoba_1"]
    F= request.json["Osoba_2"]
    new_user = Wiadomosc(I,A,B,C,D,E,F)
    db.session.add(new_user)
    db.session.commit()  # PK increment
    user = Wiadomosc.query.get(new_user.id)
    return wiadomosc_schema.jsonify(user)

@app.route("/dtresc", methods=["POST"])
def add_tresc():
    I= request.json["id"]
    A= request.json["Tresc"]
    B= request.json["Data"]
    new_user = Tresc(I,A,B)
    db.session.add(new_user)
    db.session.commit()  # PK increment
    user = Tresc.query.get(new_user.id)
    return tresc_schema.jsonify(user)

@app.route("/web/student", methods=["GET"])
def get_student_nasz():
    all_users = Student.query.order_by(Student.id).all()
    result = studenci_schema.dump(all_users)
    #return jsonify(result)
    return render_template('stronastudenci.html', title='Lista studentów', studenci=result)

@app.route("/web/pracownik", methods=["GET"])
def get_pracownik_nasz():
    all_users = Pracownik.query.order_by(Pracownik.id).all()
    result = pracownicy_schema.dump(all_users)
    #return jsonify(result)
    return render_template('stronapracownicy.html', title='Lista pracowników', pracownicy=result)

@app.route("/web/wiadomosc", methods=["GET"])
def get_wiadomosc_nasz():
    all_users = Wiadomosc.query.order_by(Wiadomosc.id).all()
    result = wiadomosci_schema.dump(all_users)
    #return jsonify(result)
    return render_template('stronawiadomosci.html', title='Lista wiadomosci', wiadomosci=result)

@app.route("/web/tresc", methods=["GET"])
def get_tresc_nasz():
    all_users = Tresc.query.order_by(Tresc.id).all()
    result = tresci_schema.dump(all_users)
    #return jsonify(result)
    return render_template('stronatresci.html', title='Tresc wiadomosci', tresci=result)# Tutaj pisz swój kod, młody padawanie ;-)
