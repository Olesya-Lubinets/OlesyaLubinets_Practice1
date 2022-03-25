import os
import string

from flask import Flask, send_from_directory, render_template, request,  redirect, url_for,flash
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient


app=Flask(__name__)

auth=HTTPBasicAuth()
client=MongoClient('localhost',27017)
db=client.wad

@auth.verify_password
def verify_password(username:string,password:string):
    if db.users.find_one({'username':username,'password':password}) is not None:
        return True
    else:
        return False

def create_user(username,password):
    db.users.insert_one(
        {
            'username': username,
            'password': password
        }
    )

@app.route('/',methods=["GET"])
def index():    return render_template("index.html")

@app.route('/auth',methods=["GET","POST"])
def auth():
    if request.method=="GET":
        return render_template("/auth.html")
    elif request.method == "POST":
        username=request.form.get("username")
        password=request.form.get('password')
        if verify_password(username, password)==True:
            return render_template("/cabinet.html",username=username,password=password)
        else:
            flash('the password is not correct')
            return redirect(url_for('auth'))


@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "GET":
       return render_template("/signup.html")
    elif request.method == "POST":
        username=request.form.get("username")
        password=request.form.get('password')
        if verify_password(username, password):
            flash('This user already exist')
            return redirect(url_for('auth'))
        else:
            create_user(username,password)
            return redirect(url_for('auth'))



@app.route('/uploadfile',methods=["POST","GET"])
def uploadfile():
    if request.method == "GET":
        return render_template("/uploadfile.html")
    elif request.method == "POST":
        file=request.files["image"]
        filename=file.filename
        #file.save(os.path.join('uploadfile',filename))
        return redirect(url_for('auth'))


if __name__ == '__main__':
    app.run()
