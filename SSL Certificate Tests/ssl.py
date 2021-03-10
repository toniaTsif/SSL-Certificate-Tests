import socket
import ssl
from datetime import datetime
 
hostname=input("Please provide a url.\n")
ctx = ssl.create_default_context()
with ctx.wrap_socket(socket.socket(), server_hostname= hostname) as s:
    #Establishing connection
	s.connect((hostname,443))
    #Getting the information about this certificate
	cert= s.getpeercert()

#DATE
date1=cert['notBefore']
date2=cert['notAfter']

#Converting strings to datetime objects
before=datetime.strptime(date1,'%b %d %X %Y GMT')
after=datetime.strptime(date2,'%b %d %X %Y GMT')

#Getting input from user about the date
choice=input("Do you want to check with current date or one that you will provide? (current/mine)\n")
if(choice=="current"):
    #Getting current date from datetime library
    cur=datetime.today()
    #Converting the date to the wanted format
    cur1=cur.strftime('%b %d %X %Y GMT')
    date=datetime.strptime(str(cur1),'%b %d %X %Y GMT')
elif(choice=="mine"):
    usersdate=input("Please provide a date.\n")
    #Converting the date to the wanted format
    date=datetime.strptime(str(usersdate),'%b %d %X %Y GMT')

answer= before.date() < date.date() < after.date()
if(answer):
    print("Current date is between date of issue and expiration date of the certificate!")
else:
    print("Current date is NOT between date of issue and expiration date of the certificate.")
 

#ISSUER
#Saving to a file the list of trusted CAs that the user provides
file=open("caList.txt","a")
more="yes"
while(more=="yes"):
    ca=input("Please provide a trusted CA.\n")
    file.write("%s\n" %ca)
    more=input("Do you want to give more CAs? (yes/no)\n")
    
file.close()

#Getting information about the issuer
issuer=cert['issuer']
length=len(issuer)
i=issuer[length-1][0][1]

#Iterating through the file to check if the issuer is in the file
with open("caList.txt","r") as file1:
    for line in file1:
        stripped_line=line.strip()
        if(stripped_line==i):
            check=1
        else:
            check=0

file1.close()

if(check):
    print("%s is among the list of trusted CAs!\n" %i)
else:
    print("Certificate issuer is not in the list.\n")

    
#SUBJECT
server=input("Which server do you want?\n")
try:
    #Checking if the server which the user provided is the same as the hostname of the certificate
    ssl.match_hostname(cert, server)
    print("It is indeed server %s!\n" %server)
except:
    print("It is NOT %s server.\n" %server)    


#VERSION
version=cert['version']
ver=input("Which version do you want?\n")
#Checking if the version the user provided is the same version of the certificate
if(ver==str(version)):
    print("Version is indeed %s!\n" %version)
else:
    print("Version is NOT %s!\n" %ver)