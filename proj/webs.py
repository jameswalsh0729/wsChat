import hashlib
import globe
import base64

import myparser
import replies
import pymongo


from itertools import islice


myclient = pymongo.MongoClient("mongo")

def hands(data,connection):

    key = myparser.findbufferend(data,"Sec-WebSocket-Key: ","\r\n")

    reply = "HTTP/1.1 "
    reply += '101 Switching Protocols\r\n'
    reply += "Upgrade: websocket\r\n"
    reply += "Connection: Upgrade\r\n"
    #append that static value to the end of our key
    key2 = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    newvalue = hashlib.sha1((key+key2).encode('utf-8')).digest()
    newvalue = base64.b64encode(newvalue)


    newvalue = newvalue.decode('utf-8')

    reply += "Sec-WebSocket-Accept: " + newvalue + "\r\n"

    reply += "\r\n"

    connection.request.sendall(bytes(reply, 'utf-8'))

    return

def catchup(data,connection):
    reply = bytearray([129])
    data = data.replace("}",",\"type\":\"1\"}")

    retdata = data
    retlen = len(retdata)

    if (retlen >= 126) :
        reply.append(126)
        reply.append((retlen & 0B1111111100000000) >> 8)

        # append upper 4 bytes
        reply.append(retlen & 0B11111111)  # append lower 4 bytes
    else :
        reply.append(retlen)

    retdata = retdata.encode('utf-8')
    reply.extend(retdata)
    connection.request.sendall(bytes(reply))


def readsock(maindata,username):
    #this will loop and keep open so we can continually read data from the websocket!

    #first access mongo database and grab all the messages
    print(maindata)
    print(username)
    mydb = myclient["mydatabase"]
    mycol = mydb["chatters"]

    for x in mycol.find(): #for every chat msg we find, send it to current socket
        catchup(x['value'],maindata)


    #update everyone that a user has joined!
    for x in globe.clients:
        updateuser(x[0]) #x[0] is connection x[1] is username



    open = 1
    while(open == 1):
        dataraw = maindata.request.recv(1024)

        opcode = dataraw[0] & 15 #grab last 4 bits

        #if someone quits we remove them from the list and update everyuser
        if(opcode == 8): #8 means to close
            open = 0
            for x in globe.clients:
                if x[0] == maindata:
                    globe.clients.remove(x)

            for x in globe.clients:
                updateuser(x[0])
            break

        mask = dataraw[1] & 0b10000000 #grab mask
        payload1 = dataraw[1] & 0b01111111
        length = 0
        add = 0 #depending on the length we may need to skip over bytes for the data
        if(payload1 == 126): #if greater there is more length (16 bits)
            data = dataraw[2] << 8 #shift over a byte so we can add the next 8 bits
            data += dataraw[3]
            length = data


            add = 2
        elif(payload1 == 127): #if this then its 64 bits
            #not needed as it's not part of the homework
            length = 0
            add = 8
        else:
            length = payload1


        if(mask == 128): #look at 4 bytes
            #bytes 10-13 are the masking bytes
            maskkey0 = dataraw[2+add]
            maskkey1 = dataraw[3+add]
            maskkey2 = dataraw[4+add]
            maskkey3 = dataraw[5+add]
        else: #ignore 4 bytes
            length = 0

        index = 0
        fulldata = bytearray()
        for item in islice(dataraw,6+add,None):
            index = index % 4
            data = 0

            if(index == 0):
                data = item ^ maskkey0
            elif(index == 1):
                data = item ^ maskkey1
            elif(index == 2):
                data = item ^ maskkey2
            elif(index == 3):
                data = item ^ maskkey3
            fulldata.append(data)
            index += 1



        reply = bytearray([129])
        retdata = myparser.removeHTML(fulldata.decode('utf-8')) #remove html


        #here is where I check if they want to send a private messege
        user = myparser.findbufferend(retdata,"/w "," ")



        #add username here
        retdata = retdata.replace("}",(",\"username\":\""+username+"\"}"))
        #add pfp here
        pfp = mydb["users"].find_one({"username" : username })["PFP"]
        retdata = retdata.replace("}",(",\"pfp\":\""+pfp+"\"}"))

        retdata2 = retdata
        retdata = retdata.replace("}", ",\"type\":\"1\"}") #add type 1 to show that it will be used for chat msg and not usernames
        retlen = len(retdata)



        if(retlen >= 126):
            reply.append(126)
            reply.append((retlen & 0B1111111100000000) >> 8) #append upper 4 bytes
            reply.append(retlen & 0B11111111) #append lower 4 bytes


        else:
            reply.append(retlen)


        retdata = retdata.encode('utf-8')
        reply.extend(retdata)




        mydict = {"value": retdata2}

        #only adds messege to database if there isn't a requested user
        if user == -1:
            mycol.insert_one(mydict) #send our msg to the database

        #if we didnt find 'user' then print all
        #else print just to the two users
        print("RETDATA:")
        print(retdata)
        print("\n\n\nREPLY")
        print(reply)
        if user == -1:
            for x in globe.clients:
                x[0].request.sendall(bytes(reply))
        else:
            #checks to see if user exists, if it does it sends
            for x in globe.clients:
                if x[1] == user:
                    print(reply)
                    x[0].request.sendall(bytes(reply))
                    maindata.request.sendall(bytes(reply))





def updateuser(connection):
    data = "{\"type\":\"2\",\"data\":\""

    for x in globe.clients:
        data += x[1]+" - "
    data += "\"}"



    reply = bytearray([129])
    retdata = data
    retlen = len(retdata)

    if (retlen >= 126) :
        reply.append(126)
        reply.append((retlen & 0B1111111100000000) >> 8)

        # append upper 4 bytes
        reply.append(retlen & 0B11111111)  # append lower 4 bytes
    else :
        reply.append(retlen)

    retdata = retdata.encode('utf-8')
    reply.extend(retdata)
    connection.request.sendall(bytes(reply))

