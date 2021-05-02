from socket import *
from pathlib import *
from random import *
import subprocess
from threading import *
from tkinter import *
import os
import codecs


"""
================================================================================
Fonctions pour fichier de configuration:
"""

ad_desti=('255.255.255.255',68)
lmask = 0
lserv = 1
lbox = 2
lbroad = 3
lplage = 4
ldyn = 5
lbail = 6
lasso = 7
lblac = 8
list_offer = []
opt1 = [1, 4, lmask]
opt3 = [3, 4, lbox]
opt6 = [6, 4, lbox]
opt28 = [28, 4, lbroad]
opt51 = [51, 4, lbail]
opt54 = [54, 4, lserv]
liste_ip=[]


with open('config.txt', 'r') as l:
        txt = l.readlines()


def extr_fic(fic, ligne):
    cpt = 0
    for c in fic[ligne]:
        if c == '[':
            start = cpt + 1
            if ligne == ldyn:
                return fic[ligne][start]
        elif c == ']':
            stop = cpt
        cpt += 1
    if ligne == lbail or ligne == lasso or ligne == lblac:
        return fic[ligne][start:stop]
    return list(map(int, fic[ligne][start:stop].split('.')))


def set_opt(n):
    add = extr_fic(txt, n[2])
    tmp = [n[0], n[1], add[0], add[1], add[2], add[3]]
    return tmp


def set_bail(n):
    add = extr_fic(txt, n[2])
    tmp = ''
    for i in range(9-len(add)):
        tmp += '0'
    tmp += hex(int(add))[2:]
    rtn = [n[0], n[1], int('0x' + tmp[0:2], 16), int('0x' + tmp[3:5], 16), int('0x' + tmp[5:7], 16), int('0x' + tmp[7:], 16)]
    return rtn


def plage_addr(text, line):
    start1=[]
    end1=[]
    cpt=0
    for t in text[line]:
        if t=='(':
            start1.append(cpt)
        else :
            if t==")":
                end1.append(cpt)
        cpt+=1
    final_list=[]
    for i in range (len(start1)):
        start=[]
        end=[]
        cpt1=0
        for j in text[line][start1[i]:end1[i]]:
            if j=='[':
                start.append(cpt1+start1[i])
            else :
                if j==']':
                    end.append(cpt1+start1[i])
            cpt1+=1
        list_adr=[]
        for d in range(len(start)):
            list_adr.append(list(map(int, text[line][start[d]+1:end[d]].split('.'))))
        for r in range(len(list_adr)-1):
            list1=list_adr[r]
            list2=list_adr[r+1]
            for i in range (int(list1[0]),int(list2[0]+1)):
                for j in range (list1[1],list2[1]+1):
                    for k in range (list1[2],list2[2]+1):
                        for l in range (list1[3],list2[3]+1):
                            list3=[i,j,k,l]
                            if list3 not in final_list:
                                final_list.append(list3)
    return final_list

list_addr=plage_addr(txt, lplage)
limit=int((len(list_addr)*3)/4)


def associa_ip(mac):
    tmp = extr_fic(txt, lasso).split(';')
    for add in tmp:
        test = add[1:18].split(':')
        L = []
        for i in test:
            L += [int(i, 16)]
        if bytes([L[0], L[1], L[2], L[3], L[4], L[5]]) == mac:
            return add[21:-1].split('.')
    return 0


def blacklist(mac):
    tmp = extr_fic(txt, lblac).split(';')
    for add in tmp:
        test = add.split(':')
        L = []
        for i in test:
            L += [int(i, 16)]
        if bytes([L[0], L[1], L[2], L[3], L[4], L[5]]) == mac:
            return 1
    return 0


"""
================================================================================
Fonctions pour efféctuer les pings:
"""

def ping(ip):
    command = ['ping', '-c' , '1', ip]
    if(subprocess.call(command, stdout=subprocess.DEVNULL) == 0):
            liste_ip.append(ip)
    return


def thread_ip():
    global liste_ip
    liste_ip=[]
    tab=[]
    for i in range (len(list_addr)):
        s=str(list_addr[i][0]) + '.' + str(list_addr[i][1]) + '.' + str(list_addr[i][2]) + '.' + str(list_addr[i][3])
        tab.append(Thread(target=ping,args=(s,)))
    return tab


def thread_ip2():
    global liste_ip
    tab=[]
    for i in liste_ip:
        tab.append(Thread(target=ping,args=(i,)))
    liste_ip=[]
    return tab


"""
================================================================================
Fonctions autre:
"""

def get_random_addr():
    r=randint(0,len(list_addr))
    while (list_addr[r] in liste_ip):
        r=randint(0,len(list_addr))
    temp=list_addr[r]
    return temp


def extract_ip_req(r):
    i = 243
    while i < len(r)-1:
        if r[i] == 50 and r[i+1] == 4:
            return ([r[i+2], r[i+3], r[i+4], r[i+5]])
        i += 1


def transf_into_mac(mac):
    mac=codecs.encode(mac, 'hex').decode()
    return mac[0:2]+":"+mac[2:4]+":"+mac[4:6]+":"+mac[6:8]+":"+mac[8:10]+":"+mac[10:12]


def ajout_journal(s):
    with open('journal.txt', 'a') as j:
        j.write(s + "\n")


def verif_bail():
    tab=[]
    t = Timer(60, verif_bail)
    t.start()
    tab_thread=thread_ip2()
    for ta in tab_thread:
        ta.start()
    for ta in tab_thread:
        ta.join()
"""
================================================================================
Fonctions pour structurer les messages:
"""

def get_offer(discover, addr=False):
    CH1 = bytes([0x02, 0x01, 0x06, 0x00])
    ID = bytes([discover[4], discover[5], discover[6], discover[7]])
    CH2 = bytes(8)
    if not addr:
        addr=get_random_addr()
    IP = bytes(addr)
    SERV = bytes(extr_fic(txt, lserv))
    CH3 = bytes(4)
    MAC = bytes([discover[28], discover[29], discover[30], discover[31], discover[32], discover[33]])
    CH4 = bytes([0x8D, 0x59, 0x00, 0x00])
    CH5 = bytes(198)
    CH6 = bytes([0x63, 0x82, 0x53, 0x63, 53 , 1 , 2])
    Opt54 = bytes(set_opt(opt54))
    Opt51 = bytes(set_bail(opt51))
    Opt1 = bytes(set_opt(opt1))
    Opt3 = bytes(set_opt(opt3))
    Opt6 = bytes(set_opt(opt6))
    Opt28 = bytes(set_opt(opt28))
    Opt255 = bytes([255 , 255 , 0xC0, 0xA8, 0x01, 0x01])
    return [addr, CH1 + ID + CH2 + IP + SERV + CH3 + MAC + CH4 + CH5 + CH6 + Opt54 + Opt51 + Opt1 + Opt3 + Opt6 + Opt28 + Opt255]


def get_nack(r):
    CH1 = bytes([0x02, 0x01, 0x06, 0x00])
    ID = bytes([r[4], r[5], r[6], r[7]])
    CH2 = bytes(20)
    MAC = bytes([r[28], r[29], r[30], r[31], r[32], r[33]])
    CH3 = bytes(202)
    CH4 = bytes([0x63, 0x82, 0x53, 0x63, 53 , 1 , 6])
    Opt = bytes(set_opt(opt54))
    Opt255 = bytes([255 , 255 , 0xC0, 0xA8, 0x01, 0x01])
    return CH1 + ID + CH2 + MAC + CH3 + CH4 + Opt + Opt255


def get_ack(r, address):
    CH1 = bytes([0x02, 0x01, 0x06, 0x00])
    ID = bytes([r[4], r[5], r[6], r[7]])
    CH2 = bytes(8)
    IP = bytes([address[0],address[1],address[2],address[3]])
    SERV = bytes(extr_fic(txt, lserv))
    CH3 = bytes(4)
    MAC = bytes([r[28], r[29], r[30], r[31], r[32], r[33]])
    CH4 = bytes([0x8D, 0x59])
    CH5 = bytes(200)
    CH6 = bytes([0x63, 0x82, 0x53, 0x63, 53 , 1 , 5])
    Opt54 = bytes(set_opt(opt54))
    Opt51 = bytes(set_bail(opt51))
    Opt1 = bytes(set_opt(opt1))
    Opt3 = bytes(set_opt(opt3))
    Opt6 = bytes(set_opt(opt6))
    Opt28 = bytes(set_opt(opt28))
    Opt255 = bytes([255 , 255 , 0xC0, 0xA8, 0x01, 0x01])
    return CH1 + ID + CH2 + IP + SERV + CH3 + MAC + CH4 + CH5 + CH6 + Opt54 + Opt51 + Opt1 + Opt3 + Opt6 + Opt28 + Opt255


"""
================================================================================
Fonctions pour fichier historique:
"""

def search_fic_line(mac, ip, id):
    with open('historique.txt', 'r') as l:
        lines = l.readlines()
    for line in lines:
        if line.split('-')[0] == str(mac) and line.split('-')[1] == str(ip) and line.split('-')[2][:-1] == str(id):
            return 1
    return 0


def search_fic_macip(mac, ip):
    with open('historique.txt', 'r') as l:
        lines = l.readlines()
    for line in lines:
        if line.split('-')[0] == str(mac) and line.split('-')[1] == str(ip):
            return 1
    return 0


def search_fic_mac(mac):
    with open('historique.txt', 'r') as l:
        lines = l.readlines()
    for line in lines:
        if line.split('-')[0] == str(mac):
            return line.split('-')[1]
    return 0


def fic_offer(mac, ip, id):
    with open('historique.txt', 'r') as l:
        lines = l.readlines()
    cpt = 0
    while cpt < len(lines):
        if lines[cpt].split('-')[0] == str(mac):
            lines[cpt] = str(mac)+'-'+str(ip)+'-'+str(id)+'\n'
            break
        cpt += 1
    if cpt == len(lines):
        with open('historique.txt', 'a') as l:
            l.write(str(mac)+'-'+str(ip)+'-'+str(id)+'\n')
    else:
        with open('historique.txt', 'w+') as l:
            for line in lines:
                l.write(line)

"""
================================================================================
Fonctions pour la fenêtre de commandes:
"""


'''Classe qui permet d'afficher la fenêtre de commandes'''
class MyCommand(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.command = StringVar()

        label = Label( self, text="Entrez la commande :")
        label.pack()

        command = Entry(self, textvariable=self.command )
        command.focus_set()
        command.pack()

        button = Button( self, text="Entrer", command=self.managecommand, fg="red")
        button.pack()

        label = Label( self, text="\nTapez ipocc pour voir les adresses ip attribuées.\nTapez iplib pour voir les adresses ip libres.\nType quit to stop the server.")
        label.pack()

        self.geometry( "500x300" )
        self.title( "Fenêtre de commandes" )

    def managecommand(self):
        if (self.command.get()== "ipocc"):
            print( "Adresses ip attribuées : " + str(liste_ip))
        else :
            if (self.command.get()== "iplib"):
                l=[]
                for i in list_addr :
                    s=str(i[0])+"."+str(i[1])+"."+str(i[2])+"."+str(i[3])
                    if (s not in liste_ip):
                        l.append(s)
                print( "Adresses ip libres : " + str(l))
            else :
                if (self.command.get()== "quit"):
                    os._exit(0)
                else :
                    print( "Erreur, retapez.")


def create_win():
    command_win=MyCommand()
    command_win.mainloop()

"""
=====================================================================================
Fonction Principale:
"""

def handle_client(cs):
    r = cs.recv(4096)
    aff=transf_into_mac(r[28:34])
    if r[242] == 1:
        """Prévention contre l'attaque du DHCP Starvation"""
        if len(liste_ip)<=limit:
            ajout_journal("Réception d'un DHCP DISCOVER de " + aff)
            ajout_journal(str(r)+ "\n")
            """ test blacklist"""
            if not blacklist(r[28:34]):
                """ test si dans la liste a associer"""
                if associa_ip(r[28:34]):
                    get = get_offer(r, list(map(int,associa_ip(r[28:34]))))
                    fic_offer(r[28:34], get[0], r[4:8])
                else:
                    """ test ip fixe """
                    if extr_fic(txt, ldyn) == '0':
                        if search_fic_mac(r[28:34]):
                            get = get_offer(r, list(map(int,search_fic_mac(r[28:34])[1:-1].split(','))))
                        else:
                            get = get_offer(r)
                            fic_offer(r[28:34], get[0], r[4:8])
                    else:
                        get = get_offer(r)
                        fic_offer(r[28:34], get[0], r[4:8])
                cs.sendto(get[1], ad_desti)
                aff1=str(get[0][0])+'.'+str(get[0][1])+'.' + str(get[0][2])+'.'+ str(get[0][3])
                ajout_journal("Envoi d'un DHCP OFFER à " + aff + " pour l'adresse ip : " + aff1 + ".")
                ajout_journal(str(get[1])+ "\n")
            else:
                ajout_journal("L'adresse mac " + aff + " est dans la blacklist.")
        else :
            ajout_journal("Impossible de répondre à DHCP OFFER de " + aff + ". Limite d'attribution d'adresses ip atteinte.")
    elif r[242] == 3:
        ajout_journal("Réception d'un DHCP REQUEST de " + aff)
        ajout_journal(str(r)+ "\n")
        req_ip = extract_ip_req(r)
        req_ip2=""
        if req_ip != None :
            req_ip2=str(req_ip[0])+'.'+str(req_ip[1])+'.' + str(req_ip[2])+'.'+ str(req_ip[3])
        """ test blacklist"""
        if blacklist(r[28:34]):
            ans = get_nack(r)
            ajout_journal("L'adresse mac " + aff + " est dans la blacklist. Envoi d'un DHCP NAK.")
            """ teste si dans la liste associée"""
        elif associa_ip(r[28:34]):
            if req_ip == list(map(int,associa_ip(r[28:34]))):
                ans = get_ack(r, req_ip)
                if req_ip2 not in liste_ip:
                    liste_ip.append(req_ip2)
                ajout_journal("Envoi d'un DHCP ACK à " + aff + " pour l'adresse ip : " + req_ip2 + ".")
            else:
                ans = get_nack(r)
                ajout_journal("Envoi d'un DHCP NAK à " + aff + " pour l'adresse ip : " + req_ip2 + ".")
        else:
            """ test ip dynamic """
            if extr_fic(txt, ldyn) == '1':
                if search_fic_line(r[28:34], req_ip, r[4:8]):
                    ans = get_ack(r, req_ip)
                    if req_ip2 not in liste_ip:
                        liste_ip.append(req_ip2)
                    ajout_journal("Envoi d'un DHCP ACK à " + aff + " pour l'adresse ip : " + req_ip2 + ".")
                else:
                    if req_ip == None:
                        ans = get_ack(r, r[12:16])
                        ajout_journal("Envoi d'un DHCP ACK à " + aff + " pour l'adresse ip : " + str(r[12:16]) + ".")
                    else:
                        ans = get_nack(r)
                        ajout_journal("Envoi d'un DHCP NAK à " + aff + ".")
            else:
                if search_fic_macip(r[28:34], req_ip):
                    ans = get_ack(r, req_ip)
                    if req_ip2 not in liste_ip:
                        liste_ip.append(req_ip2)
                    ajout_journal("Envoi d'un DHCP ACK à " + aff + " pour l'adresse ip : " + req_ip2 + ".")
                else:
                    if req_ip == None:
                        ans = get_ack(r, r[12:16])
                        ajout_journal("Envoi d'un DHCP ACK à " + aff + " pour l'adresse ip : " + str(r[12:16]) + ".")
                    else:
                        ans = get_nack(r)
                        ajout_journal("Envoi d'un DHCP NAK à " + aff + ".")
        cs.sendto(ans, ad_desti)
        ajout_journal(str(ans)+ "\n")
    elif r[242] == 4:
        ajout_journal("Réception d'un DHCP DECLINE de " + aff)
        ajout_journal(str(r) + "\n")
        req_ip = extract_ip_req(r)
        req_ip2=str(req_ip[0])+'.'+str(req_ip[1])+'.' + str(req_ip[2])+'.'+ str(req_ip[3])
        if req_ip2 not in liste_ip :
            liste_ip.append(req_ip2)

"""
=====================================================================================
Initialisation du serveur:
"""

serverPort = 67
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST,1)

serverSocket.bind(('',serverPort))

with open ("journal.txt", "w") as f:
    f.write("")
tab_thread=thread_ip()
for t in tab_thread:
    t.start()
for t in tab_thread:
    t.join()

Thread(target=create_win).start()

verif_bail()

print('Server ready')

while True :
    handle_client(serverSocket)
