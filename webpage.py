from flask import Flask, request, redirect, url_for, render_template
from ocr import ocr
from Admin_db import ad

app = Flask(__name__)

@app.route('/')
def default():
    return redirect(url_for("home"))

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method == "POST":
        role = request.form["role"]
        if role == "Admin":
            return redirect(url_for("verify"))
        else: 
            return redirect(url_for("user"))
    else:
        return render_template("home.html")

@app.route('/user', methods=['POST','GET'])
def user():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("bill",usr = user))
    else: 
        return render_template("user.html")    

@app.route('/verify', methods=['POST','GET'])
def verify():
    if request.method == "POST":
        key = request.form["key"]
        if key == "secret":
            return redirect(url_for("admin"))
        else:
            return render_template("verify.html") 
    else:
        return render_template("verify.html") 

@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == "POST":
        user = request.form["nm"]
        previous = request.form['prev']
        path = request.form["path"]
        ad(user,previous,path)
        return redirect(url_for("home"))
    else:
        return render_template("admin.html")        

@app.route("/<usr>",methods=['POST','GET'])
def bill(usr):
    [a,b,c,d] = ocr(usr)    
    return render_template("bill.html", pre = "Previous reading : " + str(a) , curr = "Current Reading : "+ str(b), Units = "Units consumed : "+ str(c), bill= "Bill : "+ str(d))

if __name__ == "__main__" :
    app.run(debug = True)
