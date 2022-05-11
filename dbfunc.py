import sqlite3

class MydbClass:
    def __init__(self,path):
        self.db = sqlite3.connect(path)
        self.c = self.db.cursor()

    def __del__(self):
        self.db.close()

    def validusername(self,username):
        result = self.c.execute("""SELECT username FROM user_info WHERE username = ?""",(username,)).fetchone()
        if result == None:
            return True
        return False

    def insertuserinfo(self,username,password,name,filetype):
        id = self.c.execute("""SELECT id FROM user_info ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0])+1

        self.c.execute("""INSERT INTO user_info (id,username,password,icon,name) VALUES (?,?,?,?,?)""",(id,username,password,str(id)+'.'+filetype,name))

        self.db.commit()
        return str(id)+'.'+filetype

    def validlogin(self,username,password):
        info = self.c.execute("""SELECT username,name FROM user_info WHERE username == ? and password == ?""",(username,password)).fetchone()
        if info == None:
            return False
        else:
            return info

    def validaddfriend(self,username):
        info = self.c.execute("""SELECT username,name,icon FROM user_info WHERE id == ?""",(username,)).fetchone()

        if info == None:
            return False
        else:
            return info

    def validaddfriendCheckRepeat(self,username,myusername):
        check = self.c.execute("""SELECT id FROM actionlist WHERE receiver_id == ? and status == ? and sender_id == ?""", (username,0,myusername)).fetchall()
        if check == []:
            check = self.c.execute("""SELECT id FROM actionlist WHERE sender_id == ? and status == ? and receiver_id == ?""",(username,0,myusername)).fetchall()
            if check == []:
                return True
            else:
                return check
        else:
            return check

    def validaddfriendCheckIsFd(self,username,ownuser):
        check = self.c.execute("""SELECT relation,leader FROM relationship WHERE type == ?""",("friend",)).fetchall()
        if check != []:
            for i in check:
                if i[0] == username and i[1] == ownuser:
                    return True
                if i[0] == ownuser and i[1] == username:
                    return True

        return False

    def addfriendsendreq(self,sender_id,receiver_id,comment):
        id = self.c.execute("""SELECT id FROM actionlist ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        self.c.execute("""INSERT INTO actionlist (id,sender_id,receiver_id,status,comment) VALUES (?,?,?,?,?)""",(id,sender_id,receiver_id,0,comment))
        self.db.commit()
        return "success"

    def getnews(self,username):

        info = self.c.execute("""SELECT  u.username,name,icon,status,a.comment FROM actionlist AS a INNER JOIN user_info AS u ON a.sender_id == u.id  WHERE receiver_id == ? ORDER BY status""",(username,)).fetchall()

        if info == []:
            return None
        else:
            return info

    def getUnreadMessage(self,ownuser):
        counter = 0
        relationship = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(ownuser,)).fetchone()
        if relationship != None:
            relationship = relationship[0].split(',')
            relationship = [i for cnt, i in enumerate(relationship) if cnt != len(relationship) - 1]

            for i in relationship:
                curcount = self.c.execute("""SELECT id,status FROM messages WHERE relationship_id == ?""",(i,)).fetchall()
                if curcount != []:
                    for j in curcount:
                        tmp = j[1].split(',')
                        tmp = [i for cnt, i in enumerate(tmp) if cnt != len(tmp) - 1]
                        if ownuser not in tmp:
                            counter += 1
        return counter

    def getNameByUsername(self,username):
        name = self.c.execute("""SELECT name FROM user_info WHERE username == ?""",(username,)).fetchone()
        return name[0]

    def geticonByUsername(self,username):
        icon = self.c.execute("""SELECT icon FROM user_info WHERE username == ?""", (username,)).fetchone()
        return icon[0]

    def getidByUsername(self,username):
        id = self.c.execute("""SELECT id FROM user_info WHERE username == ?""",(username,)).fetchone()
        return id[0]

    def getrelationidBySenderAndReceiver(self,ownuser,username):
        id = self.c.execute("""SELECT id FROM relationship WHERE leader == ? and relation == ?""",(username,ownuser)).fetchone()
        return id[0]

    def geticonById(self,username):
        icon = self.c.execute("""SELECT icon FROM user_info WHERE id == ?""",(username,)).fetchone()
        return icon[0]

    def insertrelationship(self,ownuser,username):
        id = self.c.execute("""SELECT id FROM relationship ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1


        self.c.execute("""INSERT INTO relationship (id,relation,leader,counter,name,type) VALUES (?,?,?,?,?,?)""",(id,ownuser,username,1,"","friend"))

        ownuserRELA = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(ownuser,)).fetchone()
        userRELA = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(username,)).fetchone()

        if ownuserRELA == None:
            self.c.execute("""INSERT INTO userhvRelationship (relationship_id,user_id) VALUES (?,?)""",(str(id)+",",ownuser))
        else:
            self.c.execute("""UPDATE userhvRelationship SET relationship_id = ? WHERE user_id == ?""",(ownuserRELA[0]+str(id)+",",ownuser))

        if userRELA == None:
            self.c.execute("""INSERT INTO userhvRelationship (relationship_id,user_id) VALUES (?,?)""",(str(id) + ",", username))
        else:
            self.c.execute("""UPDATE userhvRelationship SET relationship_id = ? WHERE user_id == ?""",(userRELA[0] + str(id) + ",", username))

        self.c.execute("""UPDATE actionlist SET status = 1 WHERE sender_id == ? and receiver_id == ?""",(username,ownuser))
        self.db.commit()
        return

    def insertGrouprelationship(self,ownuser,relationship,usernamelst,groupName):
        id = self.c.execute("""SELECT id FROM relationship ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1


        self.c.execute("""INSERT INTO relationship (id,relation,leader,counter,name,type) VALUES (?,?,?,?,?,?)""",(id,relationship,ownuser,len(usernamelst)+1,f"{groupName}({len(usernamelst)+1})","group"))

        ownuserRELA = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(ownuser,)).fetchone()


        if ownuserRELA == None:
            self.c.execute("""INSERT INTO userhvRelationship (relationship_id,user_id) VALUES (?,?)""",(str(id)+",",ownuser))
        else:
            self.c.execute("""UPDATE userhvRelationship SET relationship_id = ? WHERE user_id == ?""",(ownuserRELA[0]+str(id)+",",ownuser))

        for i in usernamelst:
            userRELA = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(i,)).fetchone()
            if userRELA == None:
                self.c.execute("""INSERT INTO userhvRelationship (relationship_id,user_id) VALUES (?,?)""",(str(id) + ",", i))
            else:
                self.c.execute("""UPDATE userhvRelationship SET relationship_id = ? WHERE user_id == ?""",(userRELA[0] + str(id) + ",", i))

        self.db.commit()
        return

    def insertmessage(self,ownuser,username,content,sender_id,type):
        relationship_id = self.getrelationidBySenderAndReceiver(ownuser,username)

        id = self.c.execute("""SELECT id FROM messages ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        self.c.execute("""INSERT INTO messages (id,content,sender_id,relationship_id,status,type) VALUES (?,?,?,?,?,?)""",(id,content,sender_id,relationship_id,ownuser+",",type))
        self.db.commit()
        return

    def getfriendlist(self,ownuser):
        infolst = []
        relationship_id = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(ownuser,)).fetchone()

        if relationship_id != None:
            relationship_id = relationship_id[0].split(',')
            relationship_id = [i for cnt,i in enumerate(relationship_id) if cnt != len(relationship_id)-1]

            for i in relationship_id:
                info = self.c.execute("""SELECT u.username,u.name,icon FROM relationship as r inner join user_info as u ON r.leader == u.id WHERE r.id == ? and u.id != ? and r.type == ?""",(i, ownuser,"friend")).fetchone()
                if info == None:
                    info = self.c.execute("""SELECT u.username,u.name,icon FROM relationship as r inner join user_info as u ON r.relation == u.id WHERE r.id == ? and r.type == ?""",(i,"friend")).fetchone()

                if info != None:
                    tempdic = {"username":info[0],
                               "name":info[1],
                               "icon":info[2]}
                    infolst.append(tempdic)
        return infolst

    def getchatfriends(self,ownuser):
        infolst = []
        relationship = self.c.execute("""SELECT relationship_id FROM userhvRelationship WHERE user_id == ?""",(ownuser,)).fetchone()
        #print(relationship)
        if relationship != None:
            relationship = relationship[0].split(',')
            relationship = [i for cnt, i in enumerate(relationship) if cnt != len(relationship) - 1]
            #print(relationship)
            for i in relationship:
                info = self.c.execute("""SELECT u.username,u.name,icon,r.type FROM relationship as r inner join user_info as u ON r.leader == u.id WHERE r.id == ? and u.id != ? and r.type == ?""",(i,ownuser,"friend")).fetchone()
                if info == None:
                    info = self.c.execute("""SELECT u.username,u.name,icon,r.type FROM relationship as r inner join user_info as u ON r.relation == u.id WHERE r.id == ? and r.type == ?""",(i,"friend")).fetchone()

                #print(i,info)
                if info != None:
                    tempdic = {"username": info[0],
                               "name": info[1],
                               "icon": info[2],
                               "message":"",
                               "message_id":"",
                               "relationship_id":i,
                               "type":info[3]}
                else:
                    info = self.c.execute("""SELECT name,type FROM relationship WHERE id == ?""",(i,)).fetchone()
                    tempdic = {"username":"",
                               "name":info[0],
                               "icon":"group.png",
                               "message":"",
                               "message_id":"",
                               "relationship_id":i,
                               "type":info[1]}

                message = self.c.execute("""SELECT id,content FROM messages WHERE relationship_id == ? ORDER BY id DESC""",(i,)).fetchone()
                if message != None:
                    tempdic["message"] = message[1]
                    tempdic["message_id"] = int(message[0])
                else:
                    tempdic["message_id"] = -1
                infolst.append(tempdic)
        return infolst

    def getmessages(self,ownuser,username):
        relationship_id = self.c.execute("""SELECT id FROM relationship WHERE relation == ? and leader == ?""",(ownuser,username)).fetchone()
        if relationship_id == None:
            #print(ownuser,username)
            relationship_id = self.c.execute("""SELECT id FROM relationship WHERE relation == ? and leader == ?""",(username,ownuser)).fetchone()
            relationship_id = relationship_id[0]
        else:
            relationship_id = relationship_id[0]

        info = self.c.execute("""SELECT id,content,type,sender_id FROM messages WHERE relationship_id == ? ORDER BY id ASC""",(relationship_id,)).fetchall()

        return info

    def getGroupmessages(self,ownuser,relationship_id):
        info = self.c.execute("""SELECT id,content,type,sender_id FROM messages WHERE relationship_id == ? ORDER BY id ASC""",(relationship_id,)).fetchall()
        return info

    def sendmessage(self,relationship_id,message,type,ownuser):
        id = self.c.execute("""SELECT id FROM messages ORDER BY id DESC""").fetchone()
        if id == None:
            id = 0
        else:
            id = int(id[0]) + 1

        self.c.execute("""INSERT INTO messages (id,content,sender_id,relationship_id,status,type) VALUES (?,?,?,?,?,?)""",(id,message,ownuser,relationship_id,ownuser+",",type))
        self.db.commit()
        return

    def getnewmessageTimer(self,relationship_id,maxmessage_id,ownuser):
        message = self.c.execute("""SELECT id,content,type,sender_id FROM messages WHERE relationship_id == ? and id > ? ORDER BY id ASC""",(relationship_id,maxmessage_id)).fetchall()
        if message != []:
            return message
        else:
            return []

    def geteachunread(self,relationship_id,ownuser):
        count = self.c.execute("""SELECT id,status FROM messages WHERE relationship_id == ?""",(relationship_id,)).fetchall()
        counter = 0
        if count != None:
            for j in count:
                tmp = j[1].split(',')
                tmp = [i for cnt, i in enumerate(tmp) if cnt != len(tmp) - 1]
                if ownuser not in tmp:
                    counter += 1
        return counter

    def getnewestmessage(self,relationship_id,ownuser):
        newestmessage = self.c.execute("""SELECT content FROM messages WHERE relationship_id == ? ORDER BY id DESC""",(relationship_id,)).fetchone()

        if newestmessage == None:
            return ""
        return newestmessage[0]

    def setRead(self,relationship_id,ownuser):
        status = self.c.execute("""SELECT status FROM messages WHERE relationship_id == ?""",(relationship_id,)).fetchall()
        if status != None:
            for j in status:
                tmpstatus = j[0].split(',')
                tmpstatus = [i for cnt,i in enumerate(tmpstatus) if cnt != len(tmpstatus)-1]
                #print(tmpstatus,ownuser in tmpstatus)
                if ownuser in tmpstatus:
                    continue
                try:
                    self.c.execute("""UPDATE messages SET status = ? WHERE relationship_id == ?""",(j[0]+ownuser+",",relationship_id))
                except:
                    pass
                self.db.commit()
        return

    def getGroupMember(self,relationship_id):
        Group = {"leader":{},
                 "member":[]}

        info = self.c.execute("""SELECT leader,relation FROM relationship WHERE id == ?""",(relationship_id,)).fetchone()

        leader = info[0]
        member = info[1].split(',')
        member = [i for cnt, i in enumerate(member) if cnt != len(member) -1]

        leader = self.c.execute("""SELECT name,icon FROM user_info WHERE id == ?""",(leader,)).fetchone()
        Group["leader"] = {"name":leader[0],
                           "icon":leader[1]}

        for i in member:
            tmp = self.c.execute("""SELECT name,icon FROM user_info WHERE id == ?""",(i,)).fetchone()
            tmpmember = {"name":tmp[0],
                         "icon":tmp[1]}

            Group["member"].append(tmpmember)

        return Group

if __name__ == "__main__":
    path = "Chat.db"
    db = MydbClass(path)
    del db