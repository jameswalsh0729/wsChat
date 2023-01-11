import globe
import myparser

from itertools import islice

cookies = 0

def liveupdate(maindata):
    #copy base code from webs file
    global cookies
    while(True):
        dataraw = maindata.request.recv(1024)

        opcode = dataraw[0] & 15 #grab last 4 bits

        #if someone quits we remove them from the list and update everyuser
        if(opcode == 8): #8 means to close
            globe.cookieclients.remove(maindata)
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


        #modify data here
        print("FULL DATA!",fulldata)

        type = myparser.findbufferend(fulldata,b"type\":\"",b"\"}")

        catcost = 20 + ((globe.cats * 15) * 1.1);
        dogcost = 100 + ((globe.dogs * 90) * 1.05);

        if type == b"1":#add base cookies
            globe.cookieclicks += 1+(globe.cats*1)+(globe.dogs*5)
        elif type == b"2":
            if(globe.cookieclicks >= catcost):
                globe.cats += 1
                globe.cookieclicks -= catcost
        elif type == b"3":
            if (globe.cookieclicks >= dogcost) :
                globe.dogs += 1
                globe.cookieclicks -= dogcost

        retdata = "{\"cookies\":\"" + str(globe.cookieclicks) + "\""

        retdata += ",\"cats\":\"" + str(globe.cats) + "\""

        retdata += ",\"dogs\":\"" + str(globe.dogs) + "\"}"



        retlen = len(retdata)
        if(retlen >= 126):
            reply.append(126)
            reply.append((retlen & 0B1111111100000000) >> 8) #append upper 4 bytes
            reply.append(retlen & 0B11111111) #append lower 4 bytes
        else:
            reply.append(retlen)


        retdata = retdata.encode('utf-8')
        reply.extend(retdata)


        print("REPLY!",reply)
        for x in globe.cookieclients:
            x.request.sendall(bytes(reply))





