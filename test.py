#the file I test stuff in
import nmap
np = nmap.PortScanner()
print(np.scan("localhost", "22-443"))