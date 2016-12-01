##  -*- coding: utf-8 -*-
ENCODING="iso-8859-1"

import os
import csv
import datetime



#Nom du dossier où je recupere les CSV.
source_dir = 'C:/Users/msaglier\Desktop\CanalTP\SPAM\AT/'
result_file = 'C:/Users/msaglier\Desktop\CanalTP\SPAM\AT/result.txt'






def calculateur_jour(date,day):
    """
    Permets de connaitre quelle date nous serons dans x jours de la date consultée.
    :param date: La date de reference.
    :param day: Dans combien de jours
    :return: Quelle date il sera dans date + day
    """
    premier_jour = str(date)
    premier_jour = datetime.date(int(premier_jour[0:4]),int(premier_jour[4:6]),int(premier_jour[6:8]))
    jour_voulu = premier_jour + datetime.timedelta(day)
    return(jour_voulu)


def convertisseur_format_date_AAAAMMDD(date):
    """
    on recoit une date AAAA-MM-DD et on veut qu'elle devienne AAAAMMDD
    :param date: la date en format AAAA-MM-DD
    :return:la date en AAAAMMDD
    """
    return (str(date).replace("-",""))



def weekly_messages_to_be_send(date,day=0):
    """
    Regarde les fichiers csv de AT et regarde combien concernent iOS et combien Android, pour les comparer ensuite à ceux envoyés.
    :param date : Je veux le nombre d'envois iOS et Android contenus dans les fichiers csv contenant cette date.
    :return:
    """
    dict_resultat = []
    #dict_resultat_final = {}
    scandir(source_dir,date,day,dict_resultat)
    dict_resultat_final=total_resultat_by_day_and_device(dict_resultat) #,dict_resultat_final)
    write_result(dict_resultat_final)


def total_resultat_by_day_and_device(dict_resultat):    #,dict_resultat_final):
    dico = {}
    for i in dict_resultat:
        #Est ce que j'ai deja la date dans mon dico?
        if str(i[0]) in dico:
            #est ce que j'ai deja le smartphone dans mon dico?
            if str(i[1]) in dico[i[0]]:
                #Je l'ai, j'additionne donc les valeurs.
                print("ma valeur etait : " + str(dico[i[0]][i[1]]))
                dico[i[0]][i[1]] = int(dico[i[0]][i[1]]) + int(i[2])
            else:
                #Je ne l'ai pas, je créé donc le smartphone dans mon dico[date]
                print("mon dico date contenait : " + str(dico[i[0]]))
                dico2 = {i[1]:i[2]}
                dico[i[0]].update(dico2)
                print("mon dico date contient maintenant : " + str(dico[i[0]]))
        else:
            #je créé la date dans mon dico avec le smartphone et le nombre d'envois correspondant.
            dico[i[0]] ={i[1]:i[2]}
    #dict_resultat_final = dico
    return dico #dict_resultat_final






def write_result(dict_resultat_final):
    print("Je commence a inscrire le resultat")
    print(dict_resultat_final)
    out_file = open(result_file,"w")
    for i in dict_resultat_final:
        print(i)
        #print(dict_resultat_final[i])
        #print(dict_resultat_final[i]["Android"])
        #print(dict_resultat_final[i]["iOS"])
        out_file.write(str(i) + " ; iOS ; " +  str(dict_resultat_final[i]["iOS"]) + "\n")
        out_file.write(str(i) + " ; Android ; " +  str(dict_resultat_final[i]["Android"]) + "\n")
        #out_file.write((i[0] + " ; " + i[1] + " ; " + i[2] + "\n"))

    out_file.close()
    print("J'ai fini d'inscrire le resultat")



def scandir(source_dir,date,day,dict_resultat):
    """
    regarde s'il y a des fichiers .csv dans le dossier source.
    on ne regarde pas les dossiers à l'interieur du dossier principal.
    :param: source_dir : le dossier que l'on scan pour trouver les csv.
    :return:
    """

    for file in os.listdir(source_dir):
        file = file.lower()
        #est-ce un csv?
        if file.lower().endswith(".csv"):
            for i in range(day):
            #je regarde si ce fichier corresponds à une date que je cherche
                new_date = convertisseur_format_date_AAAAMMDD(calculateur_jour(date,i))
                #print("Je regarde la date " + str(new_date))
                #todo: veritable gestion de date.
                if str(new_date) in file:
                    separate_ios_android(source_dir + file,new_date,dict_resultat)
                    break    #j'ai la date, pas besoin de poursuivre.
                else:
                    #print("je cherche une autre date pour " + file)
                    pass

            #else:
             #   print("Aucun fichier .csv ne corresponds à cette date.")    #TODO : eviter la repetition
        #else:
         #   print("Aucun fichier.csv disponible")



def separate_ios_android(file,new_date,dict_resultat):
    """
    on distingue pour chaque fichier csv les envois iOS et les envois Android. Cette information se trouve dans la seconde colonne.
    :param file : le dossier + nom du fichier que l'on decortique.
    :return:
    """
    with open(file) as fichier_en_cours:
        nb_ios = 0
        nb_android = 0
        smartphone_file = open(file,"r")

        reader_smartphone = csv.reader(smartphone_file,delimiter=";",quoting=csv.QUOTE_NONE)
        #TODO:Doit respecter la casse "Android" et "IOS".
        for row in reader_smartphone:
            if "Android" in row[1]:
                nb_android += 1
            elif "IOS" in row[1]:
                nb_ios += 1
        print("{0} contient : {1} android et {2} ios".format(file,nb_android,nb_ios))
        dict_resultat.append([str(new_date), "iOS", str(nb_ios)])
        dict_resultat.append([str(new_date),"Android", str(nb_android)])




#weekly_messages_to_be_send()
weekly_messages_to_be_send("20161114",7)


