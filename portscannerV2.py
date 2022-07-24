import nmap
import sys
import json
from datetime import datetime


args = sys.argv# get the arguments
#runscan = True
protocol = "tcp"#set the protocal to tcp
scan_one_port = 0


match(len(args)):
    case 1:#if there is only one argument 
        host = "127.0.0.1"#set the host to local host
        port_range_start = 1#scan ports 1-65535
        port_range_end = 65535
    case 2:#if there is a second argument
        host = args[1]#set the second argument to host
        port_range_start = 1#scan ports 1-65535
        port_range_end = 65535
    case 3:#if there are 3 arguments
        host = args[1]#set the host to the second argument
        scan_one_port = args[2]#set the third argument to the one port you want to scan
    case 4:#if there are 4 arguments
        host = args[1]#set the host to the second argument
        port_range_start = args[2]#set the starting and ending ports to scan
        port_range_end = args[3]


Datetime = datetime.now()# get the datetime
with open("data.json", "r") as file:# open the json file
    f = json.load(file)#put the contents of the file into a dictionary object
    try:
        time_gap_hours = (datetime.timestamp(Datetime) - int(f['timestamp']) ) // 3600# grab the timestamp from the dictonary and the time it is now in date time
        print("time sence last scan: ", time_gap_hours)#print the time gap in hours sense the last run
    except:
        time_gap_hours = 100000
    if time_gap_hours <= 2:#if the time gap is less than or equal to 2
        choice = input("you have a scan from within the last 2 hours, would you like to use that? y/n: ") #ask the user if they want to use a preveious scan
        if choice == "y":#if the user says yes then just print the content of the file
            for p in f:
                if str(p) != "time" and str(p) != "timestamp":
                    print("port : " ,p, "\t state : ", f[p]["state"], "\t name : ", f[p]["name"])
            file.close()#close the file
            sys.exit(0)#exit the program
        file.close()#close the file



#data["time"] = datetime.strftime(Datetime,"%m/%j/%y %H:%M")#convert the date time to a more readable format
#data["timestamp"] = datetime.timestamp(Datetime)

np = nmap.PortScanner()#create the port scanner object

if scan_one_port == 0:
    print(f'staring scan of ports {port_range_start} through {port_range_end} on {host}')
    np.scan(host, str(port_range_start) + "-" + str(port_range_end))#scan the ports from range port_range_start to port_range_end

    closedports = 0#set closed ports to 0
    data = {}#intialize data dictionary

    data["time"] = datetime.strftime(Datetime,"%m/%j/%y %H:%M")#convert the date time to a more readable format
    data["timestamp"] = datetime.timestamp(Datetime)
    for i in range(int(port_range_start) -1, int(port_range_end)):#for every port in the computer
        try:#print that the port is open, if that fails the port is closed, otherise put it in a dictionary to be put in the file
            print("port :", i, "\tstate :", np[host][protocol][i]["state"], "\tname :", np[host][protocol][i]["name"])
            data[i] = {"state" : np[host][protocol][i]["state"], "name" : np[host][protocol][i]["name"]}
        except:
            closedports += 1#if the port is closed add 1 to closed ports
    print("closed ports :", closedports)#print how meny closed ports their are
    
else:
    np.scan(host, str(scan_one_port))
    data = {}#intialize data dictionary
    print("port :", scan_one_port, "\tstate :", np[host][protocol][int(scan_one_port)]["state"], "\tname :", np[host][protocol][int(scan_one_port)]["name"])
    data[scan_one_port] = {"state" : np[host][protocol][int(scan_one_port)]["state"], "name" : np[host][protocol][int(scan_one_port)]["name"]}

json_object = json.dumps(data, indent=4)##convert the dictionary of open ports to a json object
try:
    with open("data.json", "w") as file:#open the file
        file.write(json_object)#write to the file
except:
    print("error writing to file")
finally:#make sure the file closes
    print("done")