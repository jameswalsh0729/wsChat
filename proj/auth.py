import hashlib
import secrets

import pymongo
import replies
import bcrypt

import myparser

myclient = pymongo.MongoClient("mongo")
#myclient = pymongo.MongoClient(port=27017)

def create_account(username,password,connection): #returns -1 on failure of acc creation, 1 on success
    mydb = myclient["mydatabase"]
    usercol = mydb['users']


    for x in usercol.find():
        if x['username'] == username:
            #error username already used
            replies.sendmsg('403 Forbidden', "Not allowed, username is taken.", connection)
            return -1
    #if user name wasnt found continue

    #password requirements
    if len(password) < 8:
        #error
        replies.sendmsg("404 Not Found", "Creation unsuccessful, password too short", connection)
        return -1
    elif not any(x.isupper() for x in password):
        #error
        replies.sendmsg("404 Not Found", "Creation unsuccessful, password has no uppercase", connection)
        return -1
    elif not any(x.islower() for x in password):
        #error
        replies.sendmsg("404 Not Found", "Creation unsuccessful, password has no lowercase", connection)
        return -1
    elif not any(x.isdigit() for x in password):
        #error
        replies.sendmsg("404 Not Found", "Creation unsuccessful, password has no numbers", connection)
        return -1
    elif password.isalnum():
        #error
        replies.sendmsg("404 Not Found", "Creation unsuccessful, password has no special characters", connection)
        return -1
    elif len(password) > 32:
        #error
        replies.sendmsg("404 Not Found", "Creation unsuccessful, password too long", connection)
        return -1

    salt = bcrypt.gensalt().decode('utf-8')
    password = (password+salt).encode('utf-8')
    newpass = hashlib.sha256(password).hexdigest()

    insertuser = {'username' : username, 'password' : newpass, 'salt' : salt}
    usercol.insert_one(insertuser)

    #refresh page
    replies.sendmsg("301 Moved Permanently", "/", connection)
    return 1


def login(username,password,connection):


    mydb = myclient["mydatabase"]
    usercol = mydb['users']


    user = ''
    for x in usercol.find():
        if x['username'] == username:
            user = x

    salt = x['salt']
    newpass = (password + salt).encode('utf-8')
    newpass = hashlib.sha256(newpass).hexdigest()
    hash = x['password']


    if(newpass == hash):
        #create auth cookie
        token = (secrets.token_urlsafe()).encode('utf-8')
        print("token1", token)

        tokenscol = mydb['tokens']
        hashedtoken = hashlib.sha256(token).hexdigest()
        print("first hash", hashedtoken)
        inserthash = {"hash" : hashedtoken, "username" : username}
        tokenscol.insert_one(inserthash)

        reply2 = "HTTP/1.1 "
        reply2 += "200 OK"
        reply2 += "\r\n"

        reply2 += "Content-Type:text/plain\r\n"
        reply2 += "X-Content-Type-Options:nosniff\r\n"
        reply2 += "Content-Length:"
        reply2 += str(len("Login successful"))
        reply2 += "\r\n"

        #add auth cookie here
        reply2 += "Set-Cookie: token="
        reply2 += token.decode('utf-8')
        reply2 += "; Max-Age: 3600"
        reply2 += "; HttpOnly\r\n"

        reply2 += "\r\n"
        reply2 += "Login successful"
        connection.request.sendall(bytes(reply2, 'utf-8'))


    else:
        replies.sendmsg("404 Not Found", "Login Unsuccessful, Username-password combo not found.", connection, 0, 0)


def check_token(token, connection):


    mydb = myclient["mydatabase"]
    tokencol = mydb['tokens']

    token2 = token.encode('utf-8')
    print("token2", token2)
    hashedtoken = hashlib.sha256(token2).hexdigest()
    print("token check:",hashedtoken)

    for x in tokencol.find():
        if x['hash'] == hashedtoken:
            #found one
            replies.sendmsg("200 OK", "Authorized user:"+x['username'], connection, 0,0)
            return

    replies.sendmsg('403 Forbidden', "Not allowed, wrong token. User must log in to view page", connection, 0, None)


def Check_Login(token, connection):


    mydb = myclient["mydatabase"]
    tokencol = mydb['tokens']

    token2 = token.encode('utf-8')
    print("token2", token2)
    hashedtoken = hashlib.sha256(token2).hexdigest()
    print("token check:",hashedtoken)

    for x in tokencol.find():
        if x['hash'] == hashedtoken:
            #found one
            return True

    return False

def GetUsername(token):


    mydb = myclient["mydatabase"]
    tokencol = mydb['tokens']

    token2 = token.encode('utf-8')
    print("token2", token2)
    hashedtoken = hashlib.sha256(token2).hexdigest()
    print("token check:",hashedtoken)

    for x in tokencol.find():
        if x['hash'] == hashedtoken:
            #found one
            return x['username']

    return

def checkvalid(data,self):
    if "token=" in data :
        token3 = myparser.findbufferend(data, "Cookie:", "\r\n")
        token3 += ';'  # add ; at the end to normalize the cookie format in case of misorder
        token = myparser.findbufferend(token3, "token=", ";")
        if Check_Login(token, self) == True:
            print("True!")
            return True
        else:
            print("False :(")
            return False

def addPFP(username,path):
    mydb = myclient["mydatabase"]
    users = mydb['users']
    users.find_one_and_update({"username": username},
                                 {"$set": {"PFP": path}})
