import telnetlib
import time


TELNET_PORT = 23
TELNET_TIMEOUT = 6

class NetDevice(object):
    def __init__(self, name, ip_addr, username, password, community='public'):
        self.name = name
        self.ip_addr = ip_addr
        self.password = password
        self.username = username
        self.community = community

    def Connect(self):

        try:
            self.conn_id = telnetlib.Telnet(self.ip_addr, TELNET_PORT, TELNET_TIMEOUT)
            self.conn_id.read_until("sername: ", TELNET_TIMEOUT)
            self.conn_id.write(self.username + '\n')
            self.conn_id.read_until("assword: ", TELNET_TIMEOUT)
            self.conn_id.write(self.password + '\n')
        except Exception:
            print "Can't initialize connection to router.name"

    def Execute(self, command):
    
        self.conn_id.write(command + '\n')
        time.sleep(1)
        self.command_output_raw =  self.conn_id.read_very_eager().split('\r\n')
        
        ''' remove first and last line from the output'''
        try:
            self.command_output_raw.pop(0)
            self.command_output_raw.pop(-1)
        except Exception:
            pass

        self.command_output = ''
        for line in self.command_output_raw:
            self.command_output += line
            self.command_output += '\r\n'

    def Print(self):

        print self.command_output

    def Close(self):
        self.conn_id.close()

def main():
    
    router = NetDevice('pynet-rtr1', '184.105.247.70', 'pyclass', '88newclass')

    print "Router: %s %s %s" % (router.ip_addr, router.username, router.community)

    router.Connect()


    router.Execute('term length 0')
    router.Execute('show ip int brief')
    router.Print()

    router.Execute('show version')
    router.Print()

    router.Close()
if __name__ == "__main__":
    main()
