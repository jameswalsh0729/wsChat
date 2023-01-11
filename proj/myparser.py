import auth
import globe

def findtill(data, start, end) :  # iterate through the string to find char
    index = data.find(start.encode('ascii'))
    index = index + len(start)
    ret = ""
    while (data[index] != end) :  # loop through until we find end char must be in ascii
        # print(chr(data[index]))
        ret += chr(data[index])
        index += 1
    return ret


def findbufferend(data, start, end) :  # i just used splice for this one, much easier

    if data.find(start) == -1:
        return -1
    index = data.find(start)
    index = index + len(start)
    ret = bytearray()
    first = data.find(start) + len(start)  # get the location of the end of 'start'
    data = data[first :]
    second = data.find(end)  # get location of the beginning of the 'end'
    data = data[:second]

    return data


def removeHTML(data) :
    ret = data.replace('&', "&amp;")  # remove all html characters
    ret = ret.replace('<', "&lt;")
    ret = ret.replace('>', "&gt;")
    return ret

def build(data,boundary,index):
    if data.endswith(boundary + b'--\r\n'):
        return data[index:data.find(b'\r\n' + boundary + b'--\r\n')]
    else:
        return data[index:]

def uploadPFP(PFP,username,imageType):
    print(username)
    username = username.replace('"', "") #clean up our file name and get it ready for our system
    username = username.replace('/', "")
    username = username.replace('~', "")
    filename = "profilepictures/" + username + "." + imageType

    with open(filename, "wb") as file:
        file.write(PFP)
    auth.addPFP(username,filename)

def buildPFP(data,length,boundary,self):
    username = findbufferend(data, b'name="Username"\r\n\r\n', b'\r\n-')
    if(username == -1):
        data = self.request.recv(2048)
    username = findbufferend(data, b'name="Username"\r\n\r\n', b'\r\n-').decode('utf-8')
    password = findbufferend(data, b'name="Password"\r\n\r\n', b'\r\n-').decode('utf-8')
    if auth.create_account(username,password,self) == 1: #valid signup build PFP
        imageType = findbufferend(data,b'Content-Type: image/', b'\r\n\r\n')
        if imageType!= -1:
            startOfImage = b'Content-Type: image/' + imageType + b'\r\n\r\n'
            index = data.find(startOfImage) + len(startOfImage)
            PFP = build(data,boundary,index)
            remaining = length - len(data)
            while remaining>0:
                data = self.request.recv(2048)
                PFP += build(data,boundary,0)
                remaining = remaining - len(data)
            uploadPFP(PFP,username,imageType.decode('utf-8'))
        else:
            auth.addPFP(username,"profilepictures/defaultPFP.png")