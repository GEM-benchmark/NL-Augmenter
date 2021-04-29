#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, shutil
from shutil import copyfile
import sys
import glob
import subprocess
from subprocess import Popen, PIPE
from datasets import load_dataset
import timeit
import datetime
import codecs
import re
import secrets
secure_random = secrets.SystemRandom()

#Datasets:
###############
# summarization: mlsum_de, mlsum_es, (wiki_lingua_es_en, wiki_lingua_ru_en, wiki_lingua_tr_en, wiki_lingua_vi_en,) xsum
# struct2text: common_gen, cs_restaurants, (dart,) e2e_nlg, totto, web_nlg_en, web_nlg_ru
# simplification: wiki_auto_asset_turk
# dialog: schema_guided_dialog

#Perturbations:
###############
# RamdomSample
# ScrambleInputStructure

# To create full json that contains special test set
JSON = 'yes'
# To create json file that only contains the IDs of selected inputs (keep to 'no' for now, not finished)
IDs = 'no'

start = timeit.default_timer()

def write_log(message, log_file):
    log_file.write(message+'\n')
    print(message)
    
log_file = codecs.open('log.txt', 'a', 'utf-8')

#Random selection
#################
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'common_gen', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'common_gen', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'cs_restaurants', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'cs_restaurants', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'e2e_nlg', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'e2e_nlg', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'mlsum_de', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'mlsum_de', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'mlsum_es', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'mlsum_es', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'schema_guided_dialog', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'schema_guided_dialog', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'totto', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'totto', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'web_nlg_en', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'web_nlg_en', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'web_nlg_ru', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'web_nlg_ru', 'train', 'RandomSample', '500', JSON, IDs])
#subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'wiki_auto_asset_turk', 'validation', 'RandomSample', '500', JSON, IDs])
#subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'wiki_auto_asset_turk', 'train', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'xsum', 'validation', 'RandomSample', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'xsum', 'train', 'RandomSample', '500', JSON, IDs])

#Change input order
#################
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'common_gen', 'test', 'ScrambleInputStructure', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'cs_restaurants', 'test', 'ScrambleInputStructure', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'e2e_nlg', 'test', 'ScrambleInputStructure', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'schema_guided_dialog', 'test', 'ScrambleInputStructure', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'totto', 'test', 'ScrambleInputStructure', '500', JSON, IDs])
subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'web_nlg_en', 'test', 'ScrambleInputStructure', '500', JSON, IDs])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'web_nlg_ru', 'test', 'ScrambleInputStructure', '500', JSON, IDs])

#Postprocess Varun & Laura's datasets
#DONE path1 = os.path.join('varun', 'test_xsum_ButterFingersPerturbation_p=0.02.json')
#DONE path2 = os.path.join('varun', 'test_xsum_ButterFingersPerturbation_p=0.05.json')
#DONE path3 = os.path.join('varun', 'test_xsum_WithoutPunctuation.json')
#DONE path4 = os.path.join('varun', 'test_schema_guided_dialog_ButterFingersPerturbation_p=0.02.json')
#DONE path5 = os.path.join('varun', 'test_schema_guided_dialog_ButterFingersPerturbation_p=0.05.json')
#DONE path6 = os.path.join('varun', 'test_schema_guided_dialog_WithoutPunctuation.json')
#path7 = os.path.join('laura', 'de_test_covid19.json')
#path8 = os.path.join('laura', 'es_test_covid19.json')
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'xsum', 'test', 'ButterFingersPerturbation_p=0.02_', '500', JSON, IDs, path1])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'xsum', 'test', 'ButterFingersPerturbation_p=0.05_', '500', JSON, IDs, path2])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'xsum', 'test', 'WithoutPunctuation', '500', JSON, IDs, path3])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'schema_guided_dialog', 'test', 'ButterFingersPerturbation_p=0.02_', '500', JSON, IDs, path4])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'schema_guided_dialog', 'test', 'ButterFingersPerturbation_p=0.05_', '500', JSON, IDs, path5])
#DONE subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'schema_guided_dialog', 'test', 'WithoutPunctuation', '500', JSON, IDs, path6])
#subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'mlsum_de', 'test', 'Covid19_', '500', JSON, IDs, path7])
#subprocess.call(['python', 'GEM_SpecialTest_convert.py', 'mlsum_es', 'test', 'Covid19_', '500', JSON, IDs, path8])

#dataset = load_dataset('gem', 'wiki_auto_asset_turk')

stop = timeit.default_timer()
timeConversion = str(datetime.timedelta(seconds=round((stop - start), 2)))
write_log('\n--------------------\nDONE', log_file)
write_log(str(timeConversion), log_file)
write_log('--------------------\n', log_file)

log_file.close()