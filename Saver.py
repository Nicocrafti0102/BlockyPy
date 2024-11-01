def read_data():
    with open("data/saved_data.txt", 'r') as fichier:
        contenu = fichier.read()  # Lire le contenu du fichier

        # Vérifier si le contenu est vide
        if contenu.strip():  # strip() enlève les espaces vides
            return contenu
        
    

def save_data(name_id,coins):
    Fsave = open("data/saved_data.txt","w")
    Fsave.write(name_id)
    Fsave.write("\n")
    Fsave.write(str(coins))