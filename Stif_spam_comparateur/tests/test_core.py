__author__ = 'msaglier'

from Stif_spam_comparateur.core import *


"""
def test_total_result_by_day_and_device():
    dict_resultat =  [['20161101', 'iOS', '6'], ['20161101', 'Android', '7'], ['20161101', 'iOS', '1776'], ['20161101', 'Android', '4014'], ['20161101', 'iOS', '1774'], ['20161101', 'Android', '4013'], ['20161101', 'iOS', '760'], ['20161101', 'Android', '1838'], ['20161101', 'iOS', '760'], ['20161101', 'Android', '1838'], ['20161101', 'iOS', '28'], ['20161101', 'Android', '52'], ['20161101', 'iOS', '133'], ['20161101', 'Android', '223'], ['20161101', 'iOS', '575'], ['20161101', 'Android', '1337'], ['20161101', 'iOS', '224'], ['20161101', 'Android', '577'], ['20161101', 'iOS', '566'], ['20161101', 'Android', '1312'], ['20161101', 'iOS', '1222'], ['20161101', 'Android', '2644'], ['20161101', 'iOS', '1216'], ['20161101', 'Android', '2609'], ['20161101', 'iOS', '652'], ['20161101', 'Android', '1314'], ['20161101', 'iOS', '652'], ['20161101', 'Android', '1313']]
    assert total_result_by_day_and_device(dict_resultat) == {'20161101': {'iOS': 10344, 'Android': 23091}}




def test_separate_ios_android():
    file = source_dir + "/smartphone_20161101-021511.csv"
    assert separate_ios_android(file,20161101) == [['20161101', 'iOS', '6'], ['20161101', 'Android', '7']]



def test_write_result():
    dict_resultat_final = {'20161101': {'iOS': 10344, 'Android': 23091}}
    #assert write_result(dict_resultat_final) == (
    #DOIT CONTENIR DANS LE FICHIER  : '20161101', 'iOS', '10344'),('20161101', 'Android', '23091'
"""

def test_adding_day():
    assert adding_day("20161101",0) == "20161101"
    assert adding_day("20161101",1) == "20161102"


"""
def test_scandir2():
    wanted_result = [
        SentMessagesFromAT('20161101', 'Android', '7'),
        SentMessagesFromAT('20161101', 'iOS', '6'),
        SentMessagesFromAT('20161101', 'Android', '4014'),
        SentMessagesFromAT('20161101', 'iOS', '1776'),
        SentMessagesFromAT('20161101', 'Android', '4013'),
        SentMessagesFromAT('20161101', 'iOS', '1774'),
        SentMessagesFromAT('20161101', 'Android', '1838'),
        SentMessagesFromAT('20161101', 'iOS', '760'),
        SentMessagesFromAT('20161101', 'Android', '1838'),
        SentMessagesFromAT('20161101', 'iOS', '760'),
        SentMessagesFromAT('20161101', 'Android', '52'),
        SentMessagesFromAT('20161101', 'iOS', '28'),
        SentMessagesFromAT('20161101', 'Android', '223'),
        SentMessagesFromAT('20161101', 'iOS', '133'),
        SentMessagesFromAT('20161101', 'Android', '1337'),
        SentMessagesFromAT('20161101', 'iOS', '575'),
        SentMessagesFromAT('20161101', 'Android', '577'),
        SentMessagesFromAT('20161101', 'iOS', '224'),
        SentMessagesFromAT('20161101', 'Android', '1312'),
        SentMessagesFromAT('20161101', 'iOS', '566'),
        SentMessagesFromAT('20161101', 'Android', '2644'),
        SentMessagesFromAT('20161101', 'iOS', '1222'),
        SentMessagesFromAT('20161101', 'Android', '2609'),
        SentMessagesFromAT('20161101', 'iOS', '1216'),
        SentMessagesFromAT('20161101', 'iOS', '652'),
        SentMessagesFromAT('20161101', 'Android', '1314'),
        SentMessagesFromAT('20161101', 'iOS', '652'),
        SentMessagesFromAT('20161101', 'Android', '1313')
        ]

    result = [scandir(source_dir,"20161101",1)]
    for i in range (len(result)):
        assert result[i].date.__eq__(wanted_result[i].date)
        assert result[i].device.__eq__(wanted_result[i].device)
        assert result[i].nb_sent.__eq__(wanted_result[i].nb_sent)
"""

def test_scandir():
    wanted_result = (['20161101', 'iOS', '6'],
        ['20161101', 'Android', '7'],
        ['20161101', 'iOS', '1776'],
        ['20161101', 'Android', '4014'],
        ['20161101', 'iOS', '1774'],
        ['20161101', 'Android', '4013'],
        ['20161101', 'iOS', '760'],
        ['20161101', 'Android', '1838'],
        ['20161101', 'iOS', '760'],
        ['20161101', 'Android', '1838'],
        ['20161101', 'iOS', '28'],
        ['20161101', 'Android', '52'],
        ['20161101', 'iOS', '133'],
        ['20161101', 'Android', '223'],
        ['20161101', 'iOS', '575'],
        ['20161101', 'Android', '1337'],
        ['20161101', 'iOS', '224'],
        ['20161101', 'Android', '577'],
        ['20161101', 'iOS', '566'],
        ['20161101', 'Android', '1312'],
        ['20161101', 'iOS', '1222'],
        ['20161101', 'Android', '2644'],
        ['20161101', 'iOS', '1216'],
        ['20161101', 'Android', '2609'],
        ['20161101', 'iOS', '652'],
        ['20161101', 'Android', '1314'],
        ['20161101', 'iOS', '652'],
        ['20161101', 'Android', '1313'])
    result = scandir(source_dir,"20161101",1)
    for i in range (len(result)):
        assert result[i].date == wanted_result[i][0]
        assert result[i].device == wanted_result[i][1]
        assert result[i].nb_sent == wanted_result[i][2]




