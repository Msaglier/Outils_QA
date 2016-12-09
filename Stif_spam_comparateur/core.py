##  -*- coding: utf-8 -*-
ENCODING="iso-8859-1"

import os
import csv
import datetime




#Nom du dossier où je recupere les CSV.
source_dir = 'C:/Users/msaglier\Desktop\CanalTP\SPAM\AT/'
#Dossier + nom du fichier où les résultats sont indiqués.
result_file = 'C:/Users/msaglier\Desktop\CanalTP\SPAM\AT/result.txt'






def weekly_messages_to_be_send(date, day=1):
    """
    Regarde les fichiers csv de AT et regarde combien concernent iOS et combien Android, pour les comparer ensuite à ceux envoyés.
    :param date : Je veux le nombre d'envois iOS et Android contenus dans les fichiers csv contenant cette date.
    :return:
    """

    list_result = scandir(source_dir, date, day)
    dict_final_result=total_result_by_day_and_device(list_result)
    #print("Apres result by day = {0}".format(dict_final_result))
    write_result(dict_final_result)



def adding_day(date, day):
    """
    Permets de connaitre quelle date nous serons dans x days de la date consultée.
    :param date: La date de reference.
    :param day: Dans combien de days
    :return: Quelle date il sera dans date + day
    """

    first_day=datetime.datetime.strptime(date,"%Y%m%d")
    next_day_to_check = first_day + datetime.timedelta(day)
    return next_day_to_check.strftime("%Y%m%d")




def total_result_by_day_and_device(list_result):
    """
    Aggrege les informations récupérées en nombre d'envois par mobile & date, plutot que par fichier csv.
    :param list_result: les date + mobile + nb d'envoi de chaque csv.
    :return: un dictionnaire au format {date:{mobile:nb_envois}}
    """

    dico = {}
    dico = dico
    for i in list_result:
        #Est ce que j'ai deja la date dans mon dico?
        if i.date in dico:
            #est ce que j'ai deja le smartphone dans mon dico?
            if i.device in dico[i.date]:
                #Je l'ai, j'additionne donc les valeurs.
                dico[i.date][i.device] = int(dico[i.date][i.device]) + int(i.nb_sent)
            else:
                #Je ne l'ai pas, je créé donc le smartphone dans mon dico[date]
                dico2 = {i.device:i.nb_sent}
                dico[i.date].update(dico2)
        else:
            #je créé la date dans mon dico avec le smartphone et le nombre d'envois correspondant.
            dico[i.date] ={i.device:i.nb_sent}
    return dico


class MessagesSentFromAT(object):
    def __init__(self, date, device, nb_sent):
        self.date = date
        self.device = device
        self.nb_sent = nb_sent

    def __eq__(self, other):
        return self.date == other.date and self.device == other.device and self.nb_sent == other.nb_sent






def write_result(dict_final_result):
    """
    Enregistre les données récupérées dans un fichier txt.
    :param dict_final_result:  le dictionnaire contenant les informations {date:{mobile:nb_envois}}
    :return:
    """

    with open(result_file, "w") as out_file:
        for i in dict_final_result:
            for platform in ("iOS", "Android"):
                to_join = (i,platform,str(dict_final_result[i][platform]))
                out_file.write((";".join(to_join)) + "\n")






def scandir(source_dir, date, day):
    """
    regarde s'il y a des fichiers .csv dans le dossier source.
    on ne regarde pas les dossiers à l'interieur du dossier principal.
    :param: source_dir : le dossier que l'on scan pour trouver les csv.
    :param date : la date du file que l'on souhaite consulter.
    :param day : le nombre de days à partir de la date que l'on souhaite consulter.(Date comprise).
    :return:
    """

    list_result = []
    for file in os.listdir(source_dir):
        #print("je regarde si csv")
        if file.lower().endswith(".csv"):
            #print("j'ai un csv")
            for i in range(day):
            #je regarde si ce fichier corresponds à une date que je cherche
                new_date = adding_day(date,i)         #J'ajoute i à la date, en partant de 0, pour faire le tour de la serie de days.
                if new_date in file:
                    list_result.extend(separate_ios_android(source_dir + file,new_date))
                    #print(list_result)
                    break    #j'ai la date, pas besoin de poursuivre.
            #print("j'ai fini la boucle de day")
        #else:
            #print("pss de fichier csv")
            #else:
             #   print("Aucun fichier .csv ne corresponds à cette date.")    #TODO : informer qu'il n'y a pas de fichier pour cette date.
        #else:
         #   print("Aucun fichier.csv disponible") #TODO: informer qu'il n'y a pas de fichier csv.
    return list_result


def separate_ios_android(file, new_date):
    """
    on distingue pour chaque fichier csv les envois iOS et les envois Android. Cette information se trouve dans la seconde colonne.
    :param file : le dossier + nom du fichier que l'on decortique.
    :parem new_date: la nouvelle date
    :return:
    """
    with open(file) as smartphone_file:
        list_result = []
        nb_ios = 0
        nb_android = 0


        reader_smartphone = csv.reader(smartphone_file,delimiter=";",quoting=csv.QUOTE_NONE)
        #TODO:Doit respecter la casse "Android" et "IOS".
        for row in reader_smartphone:
            if "Android" in row[1]:
                nb_android += 1
            elif "IOS" in row[1]:
                nb_ios += 1
        list_result.append(MessagesSentFromAT(str(new_date), "iOS", str(nb_ios)))
        list_result.append(MessagesSentFromAT(str(new_date),"Android", str(nb_android)))

    return list_result


def input_for_comparator():
    #todo: check de format, configuration des fichiers d'envois.
    print("Bienvenu dans Spam Comparator.\n")
    date = input("A partir de quand souhaitez-vous extraire les envois CSV d'Alert Trafic?(format AAAAMMJJ)\n")
    day = input("Combien de jours voulez vous consulter?(Minimum : 1)\n")
    weekly_messages_to_be_send(date,int(day))
    print("Merci, votre fichier result.txt a été généré dans {0}".format(result_file))



if __name__ == '__main__':
    input_for_comparator()

