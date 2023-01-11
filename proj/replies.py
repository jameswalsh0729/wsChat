def sendmsg(code, msg, conenction):
    if msg == "Base": # if msg is base we send homepage
        reply = "HTTP/1.1 "
        reply += code
        reply += "\r\n"
        reply += "Content-Type:text/html\r\n"
        reply += "\r\n\r\n"

        #open html file and read it
        file = open("html/index.html")
        line = file.read().replace("\n", " ")
        file.close()

        #append html file to the reply
        reply += line
        reply += "\r\n"
        conenction.request.sendall(bytes(reply, 'utf-8'))

    elif(msg == "Base2"):

        reply = "HTTP/1.1 "
        reply += code
        reply += "\r\n"
        reply += "Content-Type:text/html\r\n"
        reply += "\r\n\r\n"

        # open html file and read it
        file = open("html/chatpage.html")
        line = file.read().replace("\n", " ")
        file.close()

        # append html file to the reply
        reply += line
        reply += "\r\n"
        conenction.request.sendall(bytes(reply, 'utf-8'))
    elif (msg == "Base2.5") :

        reply = "HTTP/1.1 "
        reply += code
        reply += "\r\n"
        reply += "Content-Type:text/html\r\n"
        reply += "\r\n\r\n"

        # open html file and read it
        file = open("html/cookie.html")
        line = file.read().replace("\n", " ")
        file.close()

        # append html file to the reply
        reply += line
        reply += "\r\n"
        conenction.request.sendall(bytes(reply, 'utf-8'))
    elif (code == "403 Forbidden") :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"

        reply2 += "Content-Type:text/plain\r\n"
        reply2 += "X-Content-Type-Options:nosniff\r\n"
        reply2 += "Content-Length:"
        reply2 += str(len(msg))
        reply2 += "\r\n"
        reply2 += "\r\n"
        reply2 += msg
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif (code == "200 OK" or code == "404 Not Found") :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"

        reply2 += "Content-Type:text/plain\r\n"
        reply2 += "X-Content-Type-Options:nosniff\r\n"
        reply2 += "Content-Length:"
        reply2 += str(len(msg))
        reply2 += "\r\n"



        reply2 += "\r\n"
        reply2 += msg
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif (code == "301 Moved Permanently") :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"
        reply2 += "Location: "
        reply2 += msg
        reply2 += "\r\n"
        reply2 += "\r\n"
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif msg == "Base3" :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"
        reply2 += "Content-Type:text/javascript\r\n"
        reply2 += "\r\n"
        file = open("./html/functions.js")
        line = file.read()#.replace("\n", " ")
        file.close()
        reply2 += line
        reply2 += "\r\n"
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif msg == "Base4" :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"
        reply2 += "Content-Type:text/css\r\n"
        reply2 += "\r\n"
        file = open("./html/login_style.css")
        line = file.read()#.replace("\n", " ")
        file.close()
        reply2 += line
        reply2 += "\r\n"
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif msg == "Base4.5" :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"
        reply2 += "Content-Type:text/css\r\n"
        reply2 += "\r\n"
        file = open("./html/chatpage_style.css")
        line = file.read()#.replace("\n", " ")
        file.close()
        reply2 += line
        reply2 += "\r\n"
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif msg == "Base5" :
        reply2 = "HTTP/1.1 "
        reply2 += code
        reply2 += "\r\n"
        reply2 += "Content-Type:text/javascript\r\n"
        reply2 += "\r\n"
        file = open("./html/functionscookie.js")
        line = file.read()#.replace("\n", " ")
        file.close()
        reply2 += line
        reply2 += "\r\n"
        conenction.request.sendall(bytes(reply2, 'utf-8'))
    elif code == "image" :
        file = open("."+msg, "rb")

        data = file.read()
        length1 = len(data)
        reply = "HTTP/1.1 "
        reply += code
        reply += "\r\n"
        reply += "Content-Type:image/jpeg\r\n"
        reply += "X-Content-Type-Options: nosniff\r\n"
        reply += "Content-Length: "
        reply += str(length1)
        reply += "\r\n"
        reply += "\r\n"
        reply = reply.encode('utf-8')
        reply += data

        conenction.request.sendall(reply)

