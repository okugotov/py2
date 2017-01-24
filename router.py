import telnetlib
import time
import snmp_helper
import yaml

TELNET_PORT = 23
TELNET_TIMEOUT = 6
SNMP_PORT = 161
CONFIG_FILE = "router_list.yaml"

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

    def SNMP_GetOID(self, OID):
        
        self.snmp_output = snmp_helper.snmp_extract(snmp_helper.snmp_get_oid((self.ip_addr, self.community, SNMP_PORT), oid = OID, display_errors=True))

    def SNMP_Print(self):

        print self.snmp_output

def main():
    
    with open(CONFIG_FILE) as f:
        config = yaml.load(f)

    router_list = []

    for element in config:
        router_name = element.keys()[0]
        router_ipaddr = element[router_name]['ip_addr']
        router_username = element[router_name]['username']
        router_password = element[router_name]['password']
        router_community = element[router_name]['community']

        #print "%s %s %s %s %s" % (router_name,router_ipaddr,router_username,router_password,router_community)

        router_list.append(NetDevice(router_name,router_ipaddr,router_username,router_password,router_community))



    """
    router1.Connect()


    router1.Execute('term length 0')
    router1.Execute('show ip int brief')
    router1.Print()

    router1.Execute('show version')
    router1.Print()

    router1.Close()
    """

    for element in router_list:
        print "requesting data from router: %s" % element.name
        element.SNMP_GetOID('.1.3.6.1.2.1.1.1.0')
        element.SNMP_Print()
        element.SNMP_GetOID('.1.3.6.1.2.1.1.5.0')
        element.SNMP_Print()
        print

if __name__ == "__main__":
    main()
