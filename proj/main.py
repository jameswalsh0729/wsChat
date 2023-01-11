import socketserver

import globe
import myparser
import auth

import replies
import webs
import websocket2


class server(socketserver.BaseRequestHandler):
    def handle(self):
        dataraw = self.request.recv(2048)
        print(dataraw);


        #check what sort of data we've received
        datatype = ''
        if (dataraw.find(b'POST') == 0) :
            datatype = 'Post'
        elif (dataraw.find(b'GET') == 0) :
            datatype = 'Get'

        #### GET FUNCTIONS ####
        if datatype == 'Get':
            data = dataraw.decode("utf-8") #since it's a get request we know it's just headers
            split1  = data.split("\r") #divide up
            split2  = split1[0].split(" ")
            path    = split2[1]
            print(path)
            if(path == "/"):#send them the homepage
                replies.sendmsg("200 OK", "Base", self)

            elif(path == "/auth"):#check if they're logged in first
                    if (auth.checkvalid(data,self) == True) :  # if its a real token
                        replies.sendmsg("200 OK", "Base2", self)
                        return
                    else:
                        replies.sendmsg('403 Forbidden', "Not allowed, wrong token. User must log in to view page",self)

            elif (path == '/websocket'):
                print("Web!")
                if (auth.checkvalid(data, self) == True) :  # if its a real token
                    print("Pass!")
                    webs.hands(data, self)
                      # add the client to the list
                    #sloppy
                    token3 = myparser.findbufferend(data, "Cookie:", "\r\n")
                    token3 += ';'  # add ; at the end to normalize the cookie format in case of misorder
                    token = myparser.findbufferend(token3, "token=", ";")
                    #
                    username = auth.GetUsername(token)
                    globe.clients.append([self,username]) #add self to list of connected users along with user name

                    webs.readsock(self,username)  # keep socket open
                else :
                    replies.sendmsg('403 Forbidden', "Not allowed, wrong token. User must log in to view page", self)
            elif (path == '/functions.js') :
                replies.sendmsg("Base3", "Base3", self)

            elif (path == '/login_style.css') :
                replies.sendmsg("Base4","Base4",self)

            elif (path == '/chatpage_style.css') :
                replies.sendmsg("Base4.5","Base4.5",self)
                
            elif (path[0:17] == '/profilepictures/'):
                with open(path[1:], "rb") as file:
                    data = file.read()

                response = "HTTP/1.1 200 OK\r\nContent-Type: image/" + path[-3:] + "\r\nX-Content-Type-Options: nosniff\r\nContent-Length: " + str(len(data)) + "\r\n\r\n"
                self.request.sendall(response.encode() + data)

                ###############################
                # cookie clicker will be below!!
            elif (path == "/cookie"):  # check if they're logged in first
                if (auth.checkvalid(data, self) == True) :  # if its a real token
                    replies.sendmsg("200 OK", "Base2.5", self)
                    return
                else :
                    replies.sendmsg('403 Forbidden', "Not allowed, wrong token. User must log in to view page", self)
            elif (path == '/websocket2') :
                if (auth.checkvalid(data, self) == True) :
                    webs.hands(data, self)
                    globe.cookieclients.append(self)
                    websocket2.liveupdate(self)




            elif (path == '/functions.js') :
                replies.sendmsg("Base3", "Base3", self)
            elif (path == '/functionscookie.js') :
                replies.sendmsg("Base5", "Base5", self)

            else :  # we check for image requests in here
                path2 = path.split('/')
                if (path2[1] == 'image') :  # if first part is an image
                    replies.sendmsg("image", path, self)

        ### POST FUNCTIONS #####
        elif datatype == 'Post':
            pathindex = dataraw.find(b'/')  # find first / for the path
            postpath = myparser.findtill(dataraw, "/", 32)  # custom function to find / after pathindex up until 32

            if (postpath == 'create-account') :
                length = int(myparser.findbufferend(dataraw,b'Content-Length: ', b'\r\n').decode('utf-8'))
                boundary = b'--' + myparser.findbufferend(dataraw, b'boundary=', b'\r\n')
                if (dataraw.endswith(boundary+b'--\r\n')): #all data exists in current buffer, dont have to read more
                    username = myparser.findbufferend(dataraw, b'name="Username"\r\n\r\n', b'\r\n-').decode('utf-8')
                    password = myparser.findbufferend(dataraw, b'name="Password"\r\n\r\n', b'\r\n-').decode('utf-8')

                    if auth.create_account(username, password, self) == 1: #create acc with default pfp
                        auth.addPFP(username,"profilepictures/defaultPFP.png")
                else: #user uploaded pfp or user/pass exceeded current buffer, have to read more data
                    myparser.buildPFP(dataraw,length,boundary,self)

            if (postpath == 'login') :
                username = myparser.findbufferend(dataraw, b'name="Username"\r\n\r\n', b'\r\n-')
                if(username== -1):
                    dataraw = self.request.recv(2048)
                username = myparser.findbufferend(dataraw, b'name="Username"\r\n\r\n', b'\r\n-').decode('utf-8')
                password = myparser.findbufferend(dataraw, b'name="Password"\r\n\r\n', b'\r\n-').decode('utf-8')
                auth.login(username, password, self)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    token2 = 0


    server = socketserver.ThreadingTCPServer((host,port), server)
    server.serve_forever()