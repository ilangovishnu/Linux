
import sys
import os

class FireWall:

    def __init__(self):
        self.state = "Disabled"
        # Note: Force reset will reset all your default rules
        #Ufw().execute_command('ufw --force reset')
        Ufw().execute_command('ufw disable')

    def check_state(self):
        print('Current state: {0}'.format(self.state))
        return self.state

    def change_state(self, new_state):
        old_state = self.state

        if self.state == "Disabled" :
            self.state = "Enabled"
            Ufw().execute_command('ufw enable')

        new_state = self.state

        print('Changing state from: {old_state} to {new_state}'.format(old_state=old_state, new_state=new_state))

    def white_list_ip(self, ip):
        f = Ufw()
        f.add_rule(ip.ip)
        print('whitelisted ip: {0}'.format(ip.ip))

    def revert_ip(self, ip):
        f = Ufw()
        f.delete_rule(ip.ip)
        print ('Deleted ip: {0}'.format(ip.ip))



class IPAddress:

    def __init__(self, ip):
        print("IP: {0}".format(ip))

        self.ip = ip

    def change_ip(self):
        print('Given IP: {0}'.format(self.ip))
        #self.ip = new_ip
        print('Set IP: {0}'.format(self.ip))


class Ufw:

    def __init__(self):
        pass

    # add rule
    def add_rule(self,ip): 
        cmd = 'ufw allow from {ip} to any'.format(ip=ip)
        print(cmd)
        self.execute_command(cmd)

    #delete rule

    def delete_rule(self,ip):
        print("Deleting ip from rule....")
        cmd = 'ufw delete allow from {ip} to any'.format(ip=ip)
        print(cmd)
        self.execute_command(cmd)

    def execute_command(self,cmd):
        import commands
        print(commands.getoutput(cmd))

    def list_rules(self):
        self.execute_command('ufw status')



# Get an argument from user, Validate the ip
first_argument = sys.argv[1]
second_argument = sys.argv[2]

# Allow only if root user
if not os.getuid() == 0:
    	print ("You must be root user to change firewall settings")
	sys.exit(2)

else:

    if first_argument == "--ip":
        print("Setting UP IP")
        ip = IPAddress(second_argument)

        firewall = FireWall()
        if (firewall.check_state() == "Disabled"):
            ip.change_ip()
        firewall.white_list_ip(ip)
        firewall.change_state("Enabled")

    #elif first_argument == "--change-ip":
    #    ip = IPAddress(second_argument)
        #ip.change_ip('192.168.56.22')
    elif first_argument == "--delete" :
        print("Deleting IP")
        ip = IPAddress(second_argument)

        firewall = FireWall()
        if (firewall.check_state() == "Disabled"):
            ip.change_ip()
        firewall.revert_ip(ip)
        firewall.change_state("Enabled")

    else:
        print("Unknown argument")
        exit(0)






# Pass the ip as arguments in command line
# python fw.py --ip 192.168.1.202
# python fw.py --delete 192.168.1.202

