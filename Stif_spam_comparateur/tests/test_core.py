__author__ = 'msaglier'

from Stif_spam_comparateur.core import *


def test_total_result_by_day_and_device():
    dict_resultat =  [['20161101', 'iOS', '6'], ['20161101', 'Android', '7'], ['20161101', 'iOS', '1776'], ['20161101', 'Android', '4014'], ['20161101', 'iOS', '1774'], ['20161101', 'Android', '4013'], ['20161101', 'iOS', '760'], ['20161101', 'Android', '1838'], ['20161101', 'iOS', '760'], ['20161101', 'Android', '1838'], ['20161101', 'iOS', '28'], ['20161101', 'Android', '52'], ['20161101', 'iOS', '133'], ['20161101', 'Android', '223'], ['20161101', 'iOS', '575'], ['20161101', 'Android', '1337'], ['20161101', 'iOS', '224'], ['20161101', 'Android', '577'], ['20161101', 'iOS', '566'], ['20161101', 'Android', '1312'], ['20161101', 'iOS', '1222'], ['20161101', 'Android', '2644'], ['20161101', 'iOS', '1216'], ['20161101', 'Android', '2609'], ['20161101', 'iOS', '652'], ['20161101', 'Android', '1314'], ['20161101', 'iOS', '652'], ['20161101', 'Android', '1313']]
    assert total_result_by_day_and_device(dict_resultat) == {'20161101': {'iOS': 10344, 'Android': 23091}}



def test_separate_ios_android():
    file = source_dir + "/smartphone_20161101-021511.csv"
    assert separate_ios_android(file,20161101) == [['20161101', 'iOS', '6'], ['20161101', 'Android', '7']]


def test_scandir():
    assert scandir(source_dir,"20161101",1)== [['20161101', 'iOS', '6'], ['20161101', 'Android', '7'], ['20161101', 'iOS', '1776'], ['20161101', 'Android', '4014'], ['20161101', 'iOS', '1774'], ['20161101', 'Android', '4013'], ['20161101', 'iOS', '760'], ['20161101', 'Android', '1838'], ['20161101', 'iOS', '760'], ['20161101', 'Android', '1838'], ['20161101', 'iOS', '28'], ['20161101', 'Android', '52'], ['20161101', 'iOS', '133'], ['20161101', 'Android', '223'], ['20161101', 'iOS', '575'], ['20161101', 'Android', '1337'], ['20161101', 'iOS', '224'], ['20161101', 'Android', '577'], ['20161101', 'iOS', '566'], ['20161101', 'Android', '1312'], ['20161101', 'iOS', '1222'], ['20161101', 'Android', '2644'], ['20161101', 'iOS', '1216'], ['20161101', 'Android', '2609'], ['20161101', 'iOS', '652'], ['20161101', 'Android', '1314'], ['20161101', 'iOS', '652'], ['20161101', 'Android', '1313']]


def test_write_result():
    dict_resultat_final = {'20161101': {'iOS': 10344, 'Android': 23091}}
    #assert write_result(dict_resultat_final) == (
    #DOIT CONTENIR DANS LE FICHIER  : '20161101', 'iOS', '10344'),('20161101', 'Android', '23091'

def adding_day():
    assert adding_day("20161101",0) == "2016-11-01"
    assert adding_day("20161101",1) == "2016-11-02"


