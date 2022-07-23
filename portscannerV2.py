
from unittest import skip
import nmap
import sys
import json
from datetime import datetime


args = sys.argv# get the arguments
runscan = True


try:# if there is a first argument
    host = args[1]# then set the host to the argument
except:#else
    host = "127.0.0.1"#set it to local host
try:#if there is a second and third argument
    port_range_start = args[2]#set the starting and ending ports to scan
    port_range_end = args[3]
except:
    port_range_start = 1#else scan all the ports
    port_range_end = 65535
protocol = "tcp"#set the protocal to tcp

Datetime = datetime.now()# get the datetime

with open("data.json", "r") as file:
    data = json.load(file)
    time_gap_hours = (datetime.timestamp(Datetime) - int(data['timestamp']) ) // 3600
    print(time_gap_hours)
    if time_gap_hours <= 2:
        choice = input("you have a scan from within the last 2 hours, would you like to use that? y/n ")
        if choice == "y":
            for p in data:
                if str(p) != "time" and str(p) != "timestamp":
                    print("port : " ,p, "\t state : ", data[p]["state"], "\t name : ", data[p]["name"])
            file.close()
            sys.exit(0)

print(f'staring scan of ports {port_range_start} through {port_range_end} on {host}')


np = nmap.PortScanner()#create the port scanner object
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
json_object = json.dumps(data, indent=4)##convert the dictionary of open ports to a json object
try:
    with open("data.json", "w") as file:#open the file
        file.write(json_object)#write to the file
except:
    print("error writing to file")
finally:#make sure the file closes
    print("done")