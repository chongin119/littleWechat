from flask import Flask, url_for, request, session, redirect, render_template, session, flash, jsonify
from datetime import timedelta
from dbfunc import MydbClass
from werkzeug.utils import secure_filename
import os
import time

chat = Flask(__name__)
chat.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
chat.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
chat.config['SECRET_KEY'] = "hellohellohello"
chat.config['UPLOAD_FOLDER'] = 'static/userIcon/'
chat.config['PATH'] = "Chat.db"


@chat.before_request
def check():
    if request.method == "POST":
        pass
    elif not request.path.startswith('/static'):
        if session.get('username') == None:
            if request.path == '/login' or request.path == '/' or request.path == '/register':
                pass
            else:
                return redirect(url_for('login'))
        else:
            if request.path == '/login' or request.path == '/' or request.path == '/register':
                return redirect(url_for('usermainpage'))
            else:
                pass

@chat.route('/')
def index():
    return redirect(url_for('login'))

@chat.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        db = MydbClass(chat.config['PATH'])
        info = db.validlogin(username,password)
        del db
        if info:
            session['username'] = username
            return redirect(url_for('usermainpage'))
        else:
            flash('帐号不存在')
            return redirect(url_for('login'))

    return render_template('login.html')

@chat.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        personalpic = request.files['personalpic']

        filetype = personalpic.filename[personalpic.filename.rfind('.') + 1:]

        db = MydbClass(chat.config['PATH'])
        filename = db.insertuserinfo(username, password, name, filetype)
        del db

        personalpic.save(os.path.join(chat.config['UPLOAD_FOLDER'], secure_filename(filename)))



        return redirect(url_for('login'))

    return render_template('register.html')

@chat.route('/usermainpage',methods=["GET","POST"])
def usermainpage():
    db = MydbClass(chat.config['PATH'])
    username = session['username']
    name = db.getNameByUsername(username)
    icon = db.geticonByUsername(username)
    del db
    return render_template('usermain.html',username = username,picsrc = icon,name = name)


#These are API routes
@chat.route('/logout',methods=["POST"])
def logout():
    if session['username'] != None:
        del session['username']
    return redirect(url_for('login'))

@chat.route('/valid',methods=["POST"])
def valid():

    db = MydbClass(chat.config['PATH'])

    username = request.form.get('username')
    if db.validusername(username):
        del db
        return "true"
    del db
    return "false"

@chat.route('/addfriendvalid',methods=["POST"])
def addfriendvalid():
    respdict = {"status": "false", "info": ""}

    db = MydbClass(chat.config["PATH"])

    try:
        username = db.getidByUsername(request.form.get('username'))
        myusername = db.getidByUsername(session["username"])
    except:
        return respdict
    #print(username,myusername)
    if username == myusername:
        respdict["status"] = "own"
        return jsonify(respdict)

    checkRepeat = db.validaddfriendCheckRepeat(username,myusername)
    #print(checkRepeat)
    if checkRepeat != True:
        respdict["status"] = "hvRepeat"
        return jsonify(respdict)

    checkIsFd = db.validaddfriendCheckIsFd(username,myusername)
    if checkIsFd == True:
        respdict["status"] = "isFd"
        return jsonify(respdict)

    info = db.validaddfriend(username)
    del db
    if info:
        respdict["info"] = info
        respdict["status"] = "true"
    return jsonify(respdict)

@chat.route('/addfriendsendreq',methods=["POST"])
def addfriendsendreq():

    db = MydbClass(chat.config["PATH"])

    sender_id = db.getidByUsername(session["username"])
    receiver_id = db.getidByUsername(request.form.get('receiver_id'))
    comment = request.form.get('comment')

    db.addfriendsendreq(sender_id,receiver_id,comment)
    del db
    return "true"

@chat.route('/getnews',methods=["POST"])
def getnews():

    db = MydbClass(chat.config["PATH"])

    info = db.getnews(db.getidByUsername(session["username"]))

    respdic = {"status":"false","counter":"","info":[]}
    #print(info)
    if info != None:
        if request.form.get('message') != "needCounter":
            for i in info:
                newdic = {"username": i[0],
                          "name": i[1],
                          "icon": i[2],
                          "status":i[3],
                          "comment":i[4]}
                respdic["info"].append(newdic)

        respdic["counter"] = len([i for i in info if i[3] == "0"])
        respdic["status"] = "true"

        del db
    return jsonify(respdic)

@chat.route('/getUnreadMessage',methods=["POST"])
def getUnreadMessage():
    db = MydbClass(chat.config["PATH"])

    ownuser = db.getidByUsername(session["username"])
    counter = db.getUnreadMessage(ownuser)
    respdic = {"counter":counter}
    del db
    return jsonify(respdic)

@chat.route('/confirmFriendReq',methods=["POST"])
def confirmFriendReq():

    db = MydbClass(chat.config["PATH"])

    ownuser = db.getidByUsername(session["username"])
    username = db.getidByUsername(request.form.get('username'))

    db.insertrelationship(ownuser,username)

    #confirm后要发送一条范例信息
    message = "我通过了你的好友验证请求，现在我们可以开始聊天了"
    type = "text"
    db.insertmessage(ownuser,username,message,ownuser,type)
    del db
    return "success"

@chat.route('/getfriendlist',methods=["POST"])
def getfriendlist():
    db = MydbClass(chat.config["PATH"])

    ownuser = db.getidByUsername(session["username"])

    friends = db.getfriendlist(ownuser)
    #print(friends)
    friends.sort(key=lambda x:x['username'])
    #print(friends)
    del db
    return jsonify(friends)

@chat.route('/getchatfriends',methods=["POST"])
def getchatfriends():
    db = MydbClass(chat.config["PATH"])

    ownuser = db.getidByUsername(session["username"])

    chatfriendsInfo = db.getchatfriends(ownuser)
    chatfriendsInfo.sort(key=lambda x:x["message_id"],reverse=True)
    #print(chatfriendsInfo)
    del db
    return jsonify(chatfriendsInfo)

@chat.route('/getmessage',methods=["POST"])
def getmessage():
    db = MydbClass(chat.config["PATH"])
    messagelist = []
    #print(request.form.get('username'))
    if request.form.get('username') == None:
        del db
        return jsonify(messagelist)
    ownuser = db.getidByUsername(session["username"])
    username = db.getidByUsername(request.form.get('username'))

    messages = db.getmessages(ownuser,username)

    for i in messages:
        if i[3] == ownuser:
            judge = "true"
        else:
            judge = "false"

        curmessage = {"message_id":i[0],
                      "content":i[1],
                      "type":i[2],
                      "sender_icon":db.geticonById(i[3]),
                      "isOwn":judge}

        messagelist.append(curmessage)
    del db
    return jsonify(messagelist)

@chat.route('/getGroupmessage',methods=["POST"])
def getGroupmessage():
    db = MydbClass(chat.config["PATH"])
    messagelist = []
    # print(request.form.get('username'))
    if request.form.get('relationship_id') == None:
        del db
        return jsonify(messagelist)

    ownuser = db.getidByUsername(session["username"])
    relationship_id = request.form.get('relationship_id')
    #print(relationship_id)
    messages = db.getGroupmessages(ownuser, relationship_id)

    for i in messages:
        if i[3] == ownuser:
            judge = "true"
        else:
            judge = "false"

        curmessage = {"message_id": i[0],
                      "content": i[1],
                      "type": i[2],
                      "sender_icon": db.geticonById(i[3]),
                      "isOwn": judge}

        messagelist.append(curmessage)
    #print(messagelist)
    del db
    #print(messagelist)
    return jsonify(messagelist)

@chat.route('/sendmessage',methods=["POST"])
def sendmessage():

    db = MydbClass(chat.config["PATH"])

    relationship_id = request.form.get('relationship_id')
    message = request.form.get('message')
    type = request.form.get('type')

    ownuser = db.getidByUsername(session["username"])

    db.sendmessage(relationship_id,message,type,ownuser)

    del db
    return "success"

@chat.route('/checknewmessage',methods=["POST"])
def checkmessage():
    db = MydbClass(chat.config["PATH"])
    newmessagelst = []

    relationship_id = request.form.get('relationship_id')
    maxmessage_id = request.form.get('maxmessage_id')

    ownuser = db.getidByUsername(session["username"])

    newmessage = db.getnewmessageTimer(relationship_id,maxmessage_id,ownuser)
    for i in newmessage:
        if i[3] == ownuser:
            judge = "true"
        else:
            judge = "false"

        curmessage = {"message_id":i[0],
                      "content":i[1],
                      "type":i[2],
                      "sender_icon":db.geticonById(i[3]),
                      "isOwn":judge}

        newmessagelst.append(curmessage)
    #print(newmessagelst,ownuser,maxmessage_id)
    del db
    return jsonify(newmessagelst)

@chat.route('/geteachunread',methods=["POST"])
def geteachunread():
    db = MydbClass(chat.config["PATH"])

    relations = request.json
    ownuser = db.getidByUsername(session["username"])
    #print(relations)

    countlst = []

    for i in relations:
        count = db.geteachunread(i,ownuser)
        newestmessage = db.getnewestmessage(i,ownuser)
        curdict = {"count":count,
                   "relationship_id":i,
                   "newestmessage":newestmessage}
        countlst.append(curdict)

    del db
    return jsonify(countlst)

@chat.route('/setRead',methods=["POST"])
def setRead():

    db = MydbClass(chat.config["PATH"])
    relationship_id = request.form.get('relationship_id')
    ownuser = db.getidByUsername(session["username"])

    db.setRead(relationship_id,ownuser)
    del db
    return "success"

@chat.route('/createGroup',methods=["POST"])
def createGroup():
    db = MydbClass(chat.config["PATH"])

    ownuser = db.getidByUsername(session["username"])
    username = request.json
    relationship = ""
    usernamelst = []
    groupName = ""

    for cnt,i in enumerate(username):
        if cnt == len(username) - 1:
            groupName = i["GroupName"]
        else:
            usernamelst.append(db.getidByUsername(i))
            relationship += db.getidByUsername(i) + ","
    #print(relationship)
    db.insertGrouprelationship(ownuser,relationship,usernamelst,groupName)

    del db
    return "success"

@chat.route('/savefile',methods=["POST"])
def savefile():
    db = MydbClass(chat.config["PATH"])
    file = request.files['avator']
    filename = ""
    if file:
        timestr = time.strftime("%Y%m%d-%H%M%S")

        ownuser = db.getidByUsername(session["username"])

        filename = secure_filename(file.filename)
        position = filename.rfind('.')
        if position != -1:
            filetype = filename[position:]
        else:
            filetype = "."+filename
        #print(filetype)
        filename = "FILE_" + timestr + "_" + ownuser + filetype
        file.save(os.path.join(os.getcwd()+'/static/filemessage',filename))

    #relationship_id = request.files['relationship_id']
    #print(file)
    del db
    return filename

@chat.route('/sendfile',methods=["POST"])
def sendfile():
    db = MydbClass(chat.config["PATH"])
    ownuser = db.getidByUsername(session["username"])
    relationship_id = request.form.get("relationship_id")
    locate = request.form.get('locate')

    db.sendmessage(relationship_id,locate,"file",ownuser)
    del db
    return "success"

@chat.route('/getGroupMember',methods=["POST"])
def getGroupMember():
    db = MydbClass(chat.config["PATH"])
    relationship_id = request.form.get('relationship_id')
    group = db.getGroupMember(relationship_id)
    del db
    return jsonify(group)

if __name__ == '__main__':
    chat.run(debug=True,port=8000)