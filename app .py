from flask import Flask, request, render_template
from model import *
import pymysql as pms
app = Flask(__name__)
@app.route("/")
def main():
    return render_template("log.html")
@app.route("/check", methods=['Post'])
def check():
    username = request.form['username']
    password = request.form['password']
    conn=pms.connect(host="localhost",port=3306,user="root",password="password",db="dbms")
    cur=conn.cursor() 
    cur.execute("select * from namess")
    for i in cur.fetchall():
        if i[0]==username and i[1]==password:
            return render_template("the_success_page.html")
    return render_template("log.html",data="INVALID USER CREDENTIALS!!PLEASE TRY AGAIN")
@app.route("/recommend", methods=['Post'])
def recommend():
    input_series = request.form['series']
    rec = reccs(input_series)
    return render_template("the_success_page.html",data=rec)
if __name__=='__main__':
    app.run(host='localhost',port=5000)