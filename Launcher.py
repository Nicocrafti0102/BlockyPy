import pygame
from pyvidplayer import Video
from Main import launch_game
import time
import os
import sys
import re

from tkinter import *

# Chemin vers la vidéo
video_file = "Menu/dragon_intro.mp4"

# Fonction pour jouer la vidéo d'introduction
def intro():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("BlockyPy")
    pygame.display.set_icon(pygame.image.load('icon.ico'))

    vid = Video(video_file)
    vid.set_size(screen.get_size())

    frame_count = 0
    fps = 300
    vid.seek(0)
    pygame.display.update()

    while True:
        vid.draw(screen, (0, 0), True)
        pygame.display.update()

        frame_count += 1
        time.sleep(1/fps)
        if pygame.event.peek(pygame.MOUSEBUTTONDOWN) or frame_count >= 340:
            vid.set_size((0, 0))
            vid.close()
            pygame.quit()
            return

# Interface utilisateur avec Tkinter
def clear_canvas():
    for widget in canvas.winfo_children():
        widget.destroy()

def create_page1():
    clear_canvas()
    global PlayBtn
    global ShopBtn
    global SettingsBtn
    global QuitBtn

    logoLabel = Label(canvas, border=0, image=logo, bg='black')
    logoLabel.place(relx=0.5, rely=0.16, anchor="center") 
    
    PlayBtn = Button(canvas, border=0, width=690, height=70, image=bck_btn_play, bg="black", activebackground="black", command=create_page2)
    PlayBtn.place(relx=0.5, rely=0.4, anchor="center") 
    
    ShopBtn = Button(canvas, border=0, width=690, height=70, image=bck_btn_Shop, bg="black", activebackground="black", command=create_page4)
    ShopBtn.place(relx=0.5, rely=0.5, anchor="center") 
    
    SettingsBtn = Button(canvas, border=0, width=690, height=70, image=bck_btn_opt, bg="black", activebackground="black", command=create_page3)
    SettingsBtn.place(relx=0.5, rely=0.6, anchor="center") 
    
    QuitBtn = Button(canvas, border=0, width=690, height=70, image=bck_btn_quit, bg="black", activebackground="black", command=sys.exit)
    QuitBtn.place(relx=0.5, rely=0.7, anchor="center") 

    MadeByLbl = Label(root, text='Made by Thomas M. & Nicolas P. ドラゴンスクリプト',  bg='black', fg="yellow", font=("Arial black", 13, "bold"))
    MadeByLbl.place(relx=0.928, rely=0.99, anchor="center") 

    MadeByLbl = Label(root, text='©Copyright to Dragon Script Studio || ドラゴンスクリプト',  bg='black', fg="yellow", font=("Arial black", 13, "bold"))
    MadeByLbl.place(relx=0.073, rely=0.99, anchor="center") 
    

def create_page2():
    clear_canvas()
    global ConnectBtn
    global CancelBtn


    logoLabel = Label(canvas, border=0, image=logo, bg='black')
    logoLabel.place(relx=0.5, rely=0.16, anchor="center")
    
    NameLabel = Label(canvas, text="Entrez un pseudo", bg="black", fg='white', font=("Arial black", 20, "bold"))
    NameLabel.place(relx=0.5, rely=0.4, anchor="center")
    
    global NameEntry
    NameEntry = Entry(canvas, width=50,validate='key',validatecommand=(root.register(validate_name), '%P'), font=("Arial black", 20, "bold"))
    NameEntry.place(relx=0.5, rely=0.5, anchor="center")
    
    global PortLabel
    PortLabel = Label(canvas, text="Entrez le port", bg="black", fg='white', font=("Arial black", 20, "bold"))
    PortLabel.place(relx=0.5, rely=0.6, anchor="center")
    
    global PortEntry
    PortEntry = Entry(canvas, width=50,validate='key', validatecommand=(root.register(validate_port), '%P'), font=("Arial black", 20, "bold"))
    PortEntry.place(relx=0.5, rely=0.7, anchor="center")
    
    ConnectBtn = Button(canvas, border=0, width=670, height=75, image=bck_btn_rejR, bg="black",activebackground="black",command=quit_launcher)
    ConnectBtn.place(relx=0.5, rely=0.82, anchor="center")
    ConnectBtn.config(state=DISABLED)

    CancelBtn = Button(canvas, text="Retour",image=bck_btn_ret,bg='black', activebackground="black",border=0, command=create_page1)
    CancelBtn.place(relx=0.5, rely=0.9, anchor="center")

    MadeByLbl = Label(root, text='Made by Thomas M. & Nicolas P. ドラゴンスクリプト',  bg='black', fg="yellow", font=("Arial black", 13, "bold"))
    MadeByLbl.place(relx=0.928, rely=0.99, anchor="center") 

    MadeByLbl = Label(root, text='©Copyright to Dragon Script Studio || ドラゴンスクリプト',  bg='black', fg="yellow", font=("Arial black", 13, "bold"))
    MadeByLbl.place(relx=0.073, rely=0.99, anchor="center") 
    
def create_page3():
    clear_canvas()
    global BackBtn

    logoLabel = Label(canvas, border=0, image=logo, bg='black')
    logoLabel.place(relx=0.5, rely=0.16, anchor="center") 

    SettingsTitle = Label(canvas, text="Voici les contrôles", font=("Arial black", 30, "bold"), bg="black", fg="white")
    SettingsTitle.place(relx=0.5, rely=0.4, anchor='center')
    
    SettingsLbl = Label(canvas, text="Avancer: Z\nReculer: S\nDroite: D\nGauche: Q", font=("Arial black", 20, "bold"), bg="black", fg="white")
    SettingsLbl.place(relx=0.5, rely=0.5, anchor='center')
    
    BackBtn = Button(canvas, text="Retour",image=bck_btn_ret,bg='black', activebackground="black",border=0, command=create_page1)
    BackBtn.place(relx=0.5, rely=0.6, anchor="center")

    MadeByLbl = Label(root, text='Made by Thomas M. & Nicolas P. ドラゴンスクリプト',  bg='black', fg="yellow", font=("Arial black", 13, "bold"))
    MadeByLbl.place(relx=0.928, rely=0.99, anchor="center") 

    MadeByLbl = Label(root, text='©Copyright to Dragon Script Studio || ドラゴンスクリプト',  bg='black', fg="yellow", font=("Arial black", 13, "bold"))
    MadeByLbl.place(relx=0.073, rely=0.99, anchor="center") 

def create_page4():
    clear_canvas()
    logoLabel = Label(canvas, border=0, image=logo, bg='black')
    logoLabel.place(relx=0.5, rely=0.16, anchor="center")

    dispLabel = Label(canvas, text="Bientot disponible !", bg="black", fg='grey', font=("Arial black", 50, "bold"))
    dispLabel.place(relx=0.5, rely=0.5, anchor="center")

    BackBtn = Button(canvas, text="Retour",image=bck_btn_ret,bg='black', activebackground="black",border=0, command=create_page1)
    BackBtn.place(relx=0.5, rely=0.8, anchor="center")

def no_rej():
    ConnectBtn = Button(canvas, border=0, width=670, height=75, image=bck_btn_rejR, bg="black",activebackground="black")
    ConnectBtn.place(relx=0.5, rely=0.82, anchor="center")
    ConnectBtn.config(state=DISABLED)

def invalid_port():
    global Port_error
    # Si Port_error existe déjà, détruire l'ancienne étiquette
    if 'Port_error' in globals():
        Port_error.destroy()
    # Créer un nouveau message d'erreur
    Port_error = Label(canvas, text="Invalide ! || Veuillez entrer un port entre 0 et 65535", bg="black", fg='red', font=("Arial black", 20, "bold"))
    Port_error.place(relx=0.5, rely=0.63, anchor="center")
    
    ConnectBtn = Button(canvas, border=0, width=670, height=75, image=bck_btn_rejR, bg="black",activebackground="black")
    ConnectBtn.place(relx=0.5, rely=0.82, anchor="center")
    ConnectBtn.config(state=DISABLED)

def GetName():
    if Name_IsValid == True:    
        return NameEntry.get()

def GetPort():
    if Port_IsValid == True:
        return PortEntry.get()


def validate_name(name):
    # Vérifie si le nom est vide
    global Name_IsValid
    if name == "":
        no_rej()
        Name_IsValid = False
        return True  # Nom vide n'est pas valide
    else:
        Name_IsValid = True
        try:
            if Port_IsValid:
                ConnectBtn = Button(canvas, border=0, width=670, height=75, image=bck_btn_rej, bg="black", activebackground="black",command=quit_launcher)
                ConnectBtn.place(relx=0.5, rely=0.82, anchor="center")
                ConnectBtn.config(state=NORMAL)
        except:
            pass
    

    # Vérifie la longueur du nom
    if len(name) > 15:
        return False  # Trop de caractères

    # Interdit les caractères spéciaux spécifiés, y compris l'apostrophe
    forbidden_characters = r'¤*£%§!:;\/.,?<>"\'{[(-|`_\^@]}=+~# $'
    
    # Vérifie si le nom contient des caractères interdits
    if re.search(f"[{re.escape(forbidden_characters)}]", name):
        return False  # Contient des caractères spéciaux interdits

    return True  # Nom valide

def validate_port(port=CHAR):
    global Port_IsValid
    # Si l'entrée est vide, on gère cela
    if port == "":
        no_rej()
        Port_IsValid = False
        if 'Port_error' in globals() and Port_error.winfo_exists():
            Port_error.destroy()
        return True

    # Vérifie si le port est numérique
    if not port.isdigit():
        no_rej()
        Port_IsValid = False
        return False

    # Vérifie si la longueur dépasse 5 chiffres
    if len(port) > 5:
        return False

    port_int = int(port)

    # Vérifie les limites du port
    if port_int < 0 or port_int > 65535:
        no_rej()
        Port_IsValid = False
        invalid_port()  # Affiche l'erreur pour valeur hors limites
        return True

    # Si tout est valide, on détruit Port_error s'il existe
    if 'Port_error' in globals() and Port_error.winfo_exists():
        Port_error.destroy()

    # Active le bouton de connexion uniquement si le port est valide
    validate_name(NameEntry.get())
    if Name_IsValid:
        ConnectBtn = Button(canvas, border=0, width=670, height=75, image=bck_btn_rej, bg="black", activebackground="black", command=quit_launcher)
        ConnectBtn.place(relx=0.5, rely=0.82, anchor="center")
        ConnectBtn.config(state=NORMAL)
    Port_IsValid = True
        

    return True  # Tout est valide

def quit_launcher():
    time.sleep(0.07)
    launch_game()
    exit()

    

# Initialisation de Tkinter
root = Tk()
root.attributes('-fullscreen', True)
root.title("BlockyPY")
root.config(bg='black')
root.iconbitmap('icon.ico')
# Canevas pour le changement de pages
canvas = Canvas(root, bg='black', highlightthickness=0, border=0)
canvas.pack(expand=True, fill=BOTH)

#### IMAGE ########################################################

current_dir = os.path.dirname(os.path.abspath(__file__))

logo = PhotoImage(file=os.path.join(current_dir,"Menu/minecraft_title.png"))

bck_btn_play = PhotoImage(file=os.path.join(current_dir, "Menu/button_jouer.png"))
bck_btn_Shop = PhotoImage(file=os.path.join(current_dir, "Menu/button_magasin.png"))
bck_btn_quit = PhotoImage(file=os.path.join(current_dir, "Menu/button_quitter.png"))
bck_btn_opt = PhotoImage(file=os.path.join(current_dir, "Menu/button_options.png"))
bck_btn_rej = PhotoImage(file=os.path.join(current_dir, "Menu/button_se-connecter.png"))
bck_btn_ret = PhotoImage(file=os.path.join(current_dir, "Menu/button_retour.png"))
bck_btn_rejR = PhotoImage(file=os.path.join(current_dir, "Menu/button_se-connecterR.png"))

# Lancer l'introduction
intro()

# Lancer l'interface utilisateur
create_page1()
root.mainloop()

if __name__ == "__main__":
    Port_IsValid = False
    Name_IsValid = False
