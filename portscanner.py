import threading
import socket
import sys

def parseUrlForIP(host):
    host = host
    #the try except structures are their to build redundency in case the user does not put a full 
    try:#try to split the url at the // if we get an error the // is not there and we dont have to do that
        host = host.split("//")[1]
    except:
        pass    
    try:# try to split the url at the single / if it is not there we dont need to get rid of it
        host = host.split("/")[0]
    except:
        host = host[1]
    address = socket.gethostbyname_ex(host)
    ip = address[2]
    ip = ip[0]
    return(ip)


def portScanE(host, i): #Create a port scaner function
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#create a socket
    try:# try to connect to the port if you can then the port must be open, if you can not the port must be closed
        sock.connect((host, i)) # attempt the connection
        print(host, ":", i, ": open") #print the host and the open port
        listofopenports.append(i)# add the port to the list of open ports
    except:#if we cant connect to the port it is closed or it does not exsit
        pass
    sock.close()#close the socket, Idk why this is nessisary but python got mad without it

args = sys.argv #get the program arguments

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#create the socket AF_INET stands for Ipv4
if len(args) > 1:
    host = args[1]#set the Ip you want to look at
    if host.count(".") == 3:# basicly check if it is an ipv4 address by seeing how many dots are in the string kinda jank ik 
        pass#is it is already an ip address do nothing
    else:#if it is not an ip address parse it for the ip address
        host = parseUrlForIP(host)
else:
    print("this program requires one argument")
    exit(0)
listofports = []
for i in range(65535):
    listofports.append(i)#add the port to the list
listofopenports = []#create a list which will hold all open ports


print("Starting scan of:", host)

for i in listofports:#for every port create a thread
    thread = threading.Thread(target=portScanE, args=(host, i))#create a new thread that will run portScan() and give it one port to cheak
    thread.start()#start thread
