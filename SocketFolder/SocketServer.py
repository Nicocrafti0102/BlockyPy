import socket
import threading
from tkinter import *
import random
import time

host = 'localhost'
port = int

clients = []
QuitLoop = True

NoPwdVerification = True

def handle_client(client_socket):
    while QuitLoop != True:
        try:
            # Recevoir les données du client
            msg = client_socket.recv(1024).decode()

            print(f"Message reçu: {msg}")
            # Réenvoyer le message à tous les clients
            broadcast(msg, client_socket)
        except:
            # Supprimer le client si la connexion est interrompue
            clients.remove(client_socket)
            break
    

def SetQuitLoopToFalse():
    server_socket.close()
    QuitLoop=False
    exit()



def broadcast(msg, sender_socket):
    # Envoyer le message à tous les clients, y compris l'expéditeur
    for client in clients:
        try:
            client.sendall(msg.encode())
        except:
            clients.remove(client)


def PwdVerification():
    global PortButton
    if PwdEntry.get() == (SelectedStrFromList + "1") or NoPwdVerification:
        PwdEntry.destroy()
        PwdConfirmBtn.destroy()
        PwdLabel.destroy()
        PortLabel.pack(expand=True)
        PortEntry.pack(expand=True)
        PortButton.pack(expand=True)


def ConnectSocket():
    server_socket.bind((host, int(PortEntry.get())))
    server_socket.listen(5)
    print(f"Serveur en écoute sur {host}:{PortEntry.get()}")
    PortButton.destroy()
    PortEntry.destroy()
    PortLabel.destroy()
    ACLbl.pack(expand=True)
    PlayersACLbl.pack(expand=True)
    StopButtonAC.pack(expand=True)
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion établie avec {addr}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket))
        client_thread.start()


def start_server_thread():
    if Port_IsValid:
        server_thread = threading.Thread(target=ConnectSocket)
        server_thread.start()


# Créer une socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


################################################# Port validation ##############################################
def invalid_port():
    global PortButton
    if 'PortButton' in globals() and PortButton.winfo_exists():
        PortButton.destroy()
    PortButton = Button(root, text='Valider', bg='grey', fg='white')
    PortButton.config(state=DISABLED)
    PortButton.pack(expand=True)


def validate_port(port=CHAR):
    global Port_IsValid
    global PortButton

    if port == "":
        Port_IsValid = False
        invalid_port()
        return True

    # Vérifie si le port est num
    if not port.isdigit():
        return False

    # Vérifie si ne dépasse pas 5 chiffres
    if len(port) > 5:
        return False

    port_int = int(port)

    #limites du port 
    if port_int < 0 or port_int > 65535:
        Port_IsValid = False
        invalid_port()
        return True

    # Active le bouton de connexion uniquement si le port est valide
    Port_IsValid = True
    if 'PortButton' in globals() and PortButton.winfo_exists():
        PortButton.destroy()
    PortButton = Button(root, text='Valider', bg='green', fg='white',command=start_server_thread)
    PortButton.config(state=NORMAL)
    PortButton.pack(expand=True)
    
    return True  # Tout est valide

################################################# Port validation ##############################################

################################################# TKINTER #################################################

ListOfRandomStr = [ ########### LE MOT DE PASSE SE FAIT AVEC LA CHAINE DE CARACTERE SUIVI DE 
    "8kop", "ty8a", "op89", "re22", "iok3", "sw8d", "io3r",
    "plm2", "zoe7", "mnq8", "wsa4", "yhb9", "fgr3", "bvn7",
    "xks1", "lpo5", "nmj2", "qaz3", "wsx4", "edc5", "rfv6",
    "tgb7", "yhn8", "ujm9", "ikl0", "okm2", "jui3", "zxc4"
]
SelectedStrFromList = ListOfRandomStr[random.randint(0, 27)]
# Window
root = Tk()
root.title(f"SocketServer - {SelectedStrFromList}")
root.maxsize(500, 200)
root.minsize(500, 200)
# Widget
PwdLabel = Label(root, text="Mot de passe (et oui):")
PwdEntry = Entry(root, show="u")
PwdConfirmBtn = Button(root, text='Valider', fg="white", bg="green", command=PwdVerification)
# After PWD
PortEntry = Entry(root, validate='key', validatecommand=(root.register(validate_port), '%P'))
PortLabel = Label(root, text="Port:")
PortButton = Button(root, text='Valider', bg='grey', fg='white')
PortButton.config(state=DISABLED)
#When connected
#AC = AfterConnected
ACLbl = Label(root,text=('Le serveur est ouvert sur le port ', PortEntry.get()), fg="green")
PlayersACLbl = Label(root,text="Nombre de joueurs: ")
StopButtonAC = Button(root, text='Arrêter', bg="red", fg='white', command=SetQuitLoopToFalse)

# Pack
PwdLabel.pack(expand=True)
PwdEntry.pack(expand=True)
PwdConfirmBtn.pack(expand=True)

root.mainloop()
