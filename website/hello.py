#-*- coding:utf-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
import client
import json
app = Flask(__name__)

import sys
reload(sys)
sys.setdefaultencoding("utf8")


message = { 'login' : "Successfully login",
            'logout' : "Successfully logout",
            'signup' : "Successfully signup",
            'logfail' : "Wrong id or password",
            'modify' : "Successfully modify the profile",
            'modifyfail' : "Fail to modify the profile",
            'pwdfail' : "Repeat password has to match with the password"}

@app.route('/')
def index():
    current_user = session.get('userid','')
    fromWhere = request.args.get("from","")

    return render_template('index.html',
                            message = message.get(fromWhere, ""),
                            user = current_user)

@app.route('/user/<userid>')
def userinfo(userid="0"):
    current_user = session.get('userid','')
    fromWhere = request.args.get("from","")
    result = client.query_profile(userid)
    print result
    if result == "0\n\0":
        return "Not Found"
    result = unicode(result, "utf-8")
    data = result[:-2].split(" ")
    #print data
    return render_template('userinfo.html',
                            user = current_user,
                            message = message.get(fromWhere, ""),
                            id=userid, 
                            name=data[0],
                            email=data[1],
                            phone=data[2])

@app.route('/login')
def login():
    current_user = session.get('userid','')
    fromWhere = request.args.get("from","")
    if current_user:
        return render_template("warning.html",
                            message = "You have logged in.",
                            user = current_user
            )
    return render_template('login.html',
                            message = message.get(fromWhere, ""),
                            user = current_user)

@app.route('/signup')
def signup():
    current_user = session.get('userid','')
    fromWhere = request.args.get("from","")
    if current_user:
        return render_template("warning.html",
                            message = "You have logged in.",
                            user = current_user)
    return render_template('signup.html',
                            message = message.get(fromWhere, ""),
                            user = current_user)

@app.route('/action/login', methods=['POST', 'GET'])
def action_login():
    if request.method == 'POST':
        para = ("userid", "password")
        
        for item in para:
            if not request.form.has_key(item):
                print item
                return ""
        
        result = client.login(request.form['userid'],request.form['password'])
        print(result, len(result))
        if result == "1\n\0":
            session['userid'] = request.form['userid']
            return redirect('/?from=login')
        else:
            return redirect('/login?from=logfail')
    return "invalid login"

@app.route('/action/signup', methods=['POST', 'GET'])
def action_signup():
    if request.method == 'POST':
        para = ("name", "password", "password2", "email", "phone")
        
        for item in para:
            if not request.form.has_key(item):
                print item
                return ""
        if (request.form['password'] != request.form['password2']):
            return redirect('/signup?from=pwdfail')
        result = client.register(
                request.form['name'],
                request.form['password'],
                request.form['email'],
                request.form['phone']
                )
        if result == "-1\n\0":
            return redirect('/')
        else:
            session['userid'] = result[:-2]
            return redirect('/?from=signup')
    return "invalid signup"

@app.route('/action/modify_profile', methods=['POST', 'GET'])
def action_modify_profile():
    if request.method == 'POST':
        para = ("userid", "name", "password", "password2", "email", "phone")
        
        for item in para:
            if not request.form.has_key(item):
                print item
                return ""
        userid = request.form['userid']
        if (request.form['password'] != request.form['password2']):
            return redirect('/user/'+userid+'?from=pwdfail')
        if request.form['password']:
            result = client.modify_profile(
                request.form['userid'],
                request.form['name'],
                request.form['password'],
                request.form['email'],
                request.form['phone']
                )
        else:
            result = client.modify_profile2(
                request.form['userid'],
                request.form['name'],
                request.form['email'],
                request.form['phone']
                )
        if result == "1\n\0":
            return redirect('/user/'+userid+'?from=modify')
        else:
            return redirect('/user/'+userid+'?from=modifyfail')
    return "invalid login"

@app.route('/action/logout')
def action_logout():
    if (not session.has_key('userid')):
        return render_template("warning.html",
                            message = "You have not logged in yet.",
                            user = current_user)
    userid = session['userid']
    session.pop('userid', None)
    return redirect('/?from=logout')

def json_register(data):
    para = ("name", "password", "email", "phone")
    for item in para:
        if not data.has_key(item):
            return ""
    result = client.register(data["name"],
            data["password"],
            data["email"],
            data["phone"])
    json_obj={}
    if result == "0\n\0":
        json_obj["success"] = False
    else:
        json_obj["success"] = True
        json_obj["id"] = result[:-2]
    return json.dumps(json_obj)

def json_login(data):
    para = ("id", "password")
    for item in para:
        if not data.has_key(item):
            return ""
    result = client.login(data["id"],
            data["password"],)
    json_obj={}
    if result == "0\n\0":
        json_obj["success"] = False
    else:
        json_obj["success"] = True
    return json.dumps(json_obj)

def json_query_profile(data):
    para = ("id",)
    #print data,data.has_key("id")
    for item in para:
        if not data.has_key(item):
            print item
            return ""
    #print "here"
    result = client.query_profile(data["id"])
    json_obj={}
    if result == "0\n\0":
        json_obj["success"] = False
    else:
        json_obj["success"] = True
        info = result[:-2].split(' ')
        json_obj["name"]  = info[0]
        json_obj["email"] = info[1]
        json_obj["phone"] = info[2]
    return json.dumps(json_obj)

def json_modify_profile(data):
    para = ("id", "name", "password", "email", "phone")
    for item in para:
        if not data.has_key(item):
            return ""
    result = client.modify_profile(data["id"],
            data["name"],
            data["password"],
            data["email"],
            data["phone"])
    json_obj={}
    if result == "0\n\0":
        json_obj["success"] = False
    else:
        json_obj["success"] = True
    return json.dumps(json_obj)

def json_modify_privilege(data):
    para = ("id1", "id2", "privilege")
    for item in para:
        if not data.has_key(item):
            return ""
    result = client.modify_privilege(data["id1"],
            data["id2"],
            data["privilege"])
    json_obj={}
    if result == "0\n\0":
        json_obj["success"] = False
    else:
        json_obj["success"] = True
    return json.dumps(json_obj)

@app.route('/action/post', methods=['POST', 'GET'])
def action_post():
    if request.method == 'POST':
        raw_text = request.form.get('input','')
        try:
            data = json.loads(raw_text)
        except ValueError:
            return ""
        #return str(data)
        if (not (isinstance(data, dict) and data.has_key("type"))):
            return ""
        func = {"register":json_register,
                "login":json_login,
                "query_profile":json_query_profile,
                "modify_profile":json_modify_profile,
                "modify_privilege":json_modify_privilege
                }
        #print data["type"],func.has_key(data["type"])
        if func.has_key(data["type"]):
            return func[data["type"]](data)
        else:
            return ""
    return ""

app.secret_key = 'A0Zr98j/3asdfHH!&&mN]LWX/,?RT'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
