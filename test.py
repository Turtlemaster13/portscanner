#the file I test stuff in
import nmap
import sys

args = sys.argv

host = args[1]
protocol = args[2]
np = nmap.PortScanner()
#print(np.scan("localhost", "1-443"))
np.scan(host, "1-65535")
for key in np[host]['tcp'].keys():
    #print(key)
    #print ('port : %s\tstate : %s' % (key, np[host][protocol][key]['state']))
    print("port :",key, "\tstate :", np[host][protocol][key]['state'])
