#coding=utf-8
import re
import codecs
import sys
import secrets
import json
secure_random = secrets.SystemRandom()
from datasets import load_dataset

# Parameters
############################################
# summarization: mlsum_de, mlsum_es, wiki_lingua_es_en, wiki_lingua_ru_en, wiki_lingua_tr_en, wiki_lingua_vi_en, xsum
# struct2text: common_gen, cs_restaurants, dart, e2e_nlg, totto, web_nlg_en, web_nlg_ru
# simplification: wiki_auto_asset_turk
# dialog: schema_guided_dialog
dataset_name = sys.argv[1]
subSet = sys.argv[2]
perturbation = sys.argv[3]
num_samples = int(sys.argv[4])
create_new_test_set_file = sys.argv[5]
create_list_of_ids = sys.argv[6]
path = ''
if len(sys.argv) > 7:
    path = sys.argv[7]
# dataset_name = 'web_nlg_en'
# subSet = 'validation'
# num_samples = 500
# create_new_test_set_file = 'yes'
# create_list_of_ids = 'no'

# Input dataset samples
############################################
# See at bottom of file

def write_log(message, log_file):
    log_file.write(message+'\n')
    print(message)

log_file = codecs.open('log.txt', 'a', 'utf-8')
#log_file = codecs.open('log.txt', 'a', 'cp1252')

write_log('\n##########################################################\nProcessing '+dataset_name+' '+subSet+' '+perturbation+' '+str(num_samples)+'...\n##########################################################', log_file)

dataset = {}
if path:
    dataset = json.load(open(path))
else:
    dataset = load_dataset('gem', dataset_name)

#print(dataset['validation'][0])
#print(dataset[subSet][1])
#print(dataset['validation'][0]['input'])
#print(dataset['test'][0])

def fillDicoCount(dico, key):
    if not key in dico:
        dico[key] = 1
    else:
        dico[key] += 1
    return(dico)

def getMaxValueDico(dico):
        max_value = 0
        for obj in dico:
            if dico.get(obj) > max_value:
                max_value = dico.get(obj)
        return(max_value)
        
def scrambleInputsTotto(highlighted_cells, table):
    """ returns a list with the same elements as the input list, but with a different order; for Totto, returns the updated highlighted_cells field too."""
    # Create list with original row numbers
    table_rows_numbers = []
    x = 0
    for row in table:
        table_rows_numbers.append(x)
        x += 1
    # print('Original row numbers: ', table_rows_numbers)
    # Create list with shuffled row numbers
    shuffled_table_rows_numbers = secure_random.sample(table_rows_numbers, len(table_rows_numbers))
    # print('Shuffled row numbers: ', shuffled_table_rows_numbers)
    # Create dictionary with mapping between origina and shuffled row numbers
    dico_mapping = {}
    for y, z in list(zip(table_rows_numbers, shuffled_table_rows_numbers)):
        dico_mapping[y] = z
    # print('Dico mapping: ', dico_mapping)
    # print('Original cells: ', highlighted_cells)
    # Reorder the rows according to the new shuffled order
    new_list_rows = []
    for new_row_number in shuffled_table_rows_numbers:
        new_list_rows.append(table[new_row_number])
    # Update the highlighted cells field according to the new row order
    new_list_highlighted_cells = []
    for cell in highlighted_cells:
        new_list_cell_coord = []
        new_list_cell_coord.append(dico_mapping.get(cell[0]))
        new_list_cell_coord.append(cell[1])
        new_list_highlighted_cells.append(new_list_cell_coord)
    # print('Shuffled cells: ', new_list_highlighted_cells)
    return(new_list_highlighted_cells, new_list_rows)
        
def scrambleInputs(list_structures):
    """ returns a list with the same elements as the input list, but with a different order"""
    num_samples = len(list_structures)
    scrambled_random_selection = secure_random.sample(list_structures, num_samples)
    return(scrambled_random_selection)

def FillDicoOut(dico_main, input_object, list_selection, dataset_name, perturbation, subSet):
    """writes the contents of the full json structure that can be used as input for the GEM tasks"""
    dico_input_structure = {}
    # CommonGen #####################################################
    if dataset_name == 'common_gen':
        dico_input_structure['concept_set_id'] = input_object.concept_set_id
        if perturbation == 'ScrambleInputStructure':
            scrambled_input_structure = scrambleInputs(input_object.input_structure)
            dico_input_structure['concepts'] = scrambled_input_structure
            #dico_input_structure['concepts-orig'] = str(input_object.input_structure)
        else:
            dico_input_structure['concepts'] = input_object.input_structure
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
    # CS Restaurants #####################################################
    elif dataset_name == 'cs_restaurants':
        if perturbation == 'ScrambleInputStructure':
            scrambled_input_structure = scrambleInputs(input_object.property_list)
            dico_input_structure['dialog_act'] = input_object.dialogue_act_main+'('+str(','.join(scrambled_input_structure))+')'
            #dico_input_structure['dialog_act-orig'] = str(input_object.input_structure)
        else:    
            dico_input_structure['dialog_act'] = str(input_object.input_structure)
        dico_input_structure['dialog_act_delexicalized'] = input_object.input_structure_delex
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
        dico_input_structure['target_delexicalized'] = input_object.target_delex
    # E2E #####################################################
    elif dataset_name == 'e2e_nlg':
        dico_input_structure['gem_id'] = input_object.gem_id
        if perturbation == 'ScrambleInputStructure':
            scrambled_input_structure = scrambleInputs(input_object.property_list)
            dico_input_structure['meaning_representation'] = str(', '.join(scrambled_input_structure))
            #dico_input_structure['meaning_representation-orig'] = str(input_object.input_structure)
        else:    
            dico_input_structure['meaning_representation'] = str(input_object.input_structure)
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
    # MLSum #####################################################
    elif (dataset_name == 'mlsum_de' or dataset_name == 'mlsum_es'):
        dico_input_structure['date'] = input_object.date
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
        dico_input_structure['text'] = input_object.input_text
        dico_input_structure['title'] = input_object.title
        dico_input_structure['topic'] = input_object.topic
        dico_input_structure['url'] = input_object.url
    # Schema-guided Dialog #####################################################
    elif dataset_name == 'schema_guided_dialog':
        if perturbation == 'ScrambleInputStructure':
            scrambled_input_structure = scrambleInputs(input_object.input_structure)
            dico_input_structure['dialog_acts'] = scrambled_input_structure
            #dico_input_structure['dialog_acts-orig'] = str(input_object.input_structure)
        else:    
            dico_input_structure['dialog_acts'] = input_object.input_structure
        dico_input_structure['dialog_id'] = input_object.dialog_id
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['prompt'] = input_object.prompt
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
        dico_input_structure['turn_id'] = input_object.turn_id
    # Totto #####################################################
    elif dataset_name == 'totto':
        dico_input_structure['example_id'] = input_object.example_id
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['overlap_subset'] = input_object.overlap_subset
        dico_input_structure['references'] = input_object.references
        dico_input_structure['sentence_annotations'] = input_object.sentence_annotations
        if perturbation == 'ScrambleInputStructure':
            dico_input_structure['highlighted_cells'], dico_input_structure['table'] = scrambleInputsTotto(input_object.input_structure, input_object.table)
            #dico_input_structure['highlighted_cells_orig'] = input_object.input_structure
            #dico_input_structure['table_orig'] = input_object.table
        else:
            dico_input_structure['highlighted_cells'] = input_object.input_structure
            dico_input_structure['table'] = input_object.table
        dico_input_structure['table_page_title'] = input_object.table_page_title
        dico_input_structure['table_section_text'] = input_object.table_section_text
        dico_input_structure['table_section_title'] = input_object.table_section_title
        dico_input_structure['table_webpage_url'] = input_object.table_webpage_url
        dico_input_structure['target'] = input_object.target
        dico_input_structure['totto_id'] = input_object.totto_id
    # WebNLG #####################################################
    elif (dataset_name == 'web_nlg_en' or dataset_name == 'web_nlg_ru'):
        if input_object.gem_id in list_selection:
            dico_input_structure['category'] = input_object.category
            dico_input_structure['gem_id'] = input_object.gem_id
            if perturbation == 'ScrambleInputStructure':
                scrambled_input_structure = scrambleInputs(input_object.input_structure)
                dico_input_structure['input'] = scrambled_input_structure
                #dico_input_structure['input-orig'] = str(input_object.input_structure)
            else:
                dico_input_structure['input'] = input_object.input_structure
            dico_input_structure['references'] = input_object.references
            dico_input_structure['target'] = input_object.target
            dico_input_structure['webnlg_id'] = input_object.webnlg_id
    # Wiki Auto #####################################################
    elif dataset_name == 'wiki_auto_asset_turk':
        dico_input_structure['source'] = input_object.input_text
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
        dico_input_structure['source_id'] = input_object.source_id
        dico_input_structure['target_id'] = input_object.target_id
    # XSum #####################################################
    elif dataset_name == 'xsum':
        dico_input_structure['document'] = input_object.input_text
        dico_input_structure['gem_id'] = input_object.gem_id
        dico_input_structure['references'] = input_object.references
        dico_input_structure['target'] = input_object.target
        dico_input_structure['xsum_id'] = input_object.xsum_id

    # For WebNLG, only write structures selected in this function; for other datasets, selection is done before.
    if (dataset_name == 'web_nlg_en' or dataset_name == 'web_nlg_ru'):
        if input_object.gem_id in list_selection:
            dico_main[subSet].append(dico_input_structure)
    else:
        dico_main[subSet].append(dico_input_structure)

class TripleWebNLG:
    def __init__ (self, line_triple):
        """breaks down each WebNLG input triple into subject, property, object"""
        self.subj = line_triple.split(' | ')[0]
        self.prop = line_triple.split(' | ')[1]
        self.obj = line_triple.split(' | ')[2]
        
class DataEntryCommonGen:
    def __init__ (self, gem_id, concepts, concept_set_id, references, target):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.concept_set_id = concept_set_id
        self.input_structure = concepts
        self.references = references
        self.target = target
        self.input_size = len(concepts)

class DataEntryCsRestaurants:
    def __init__ (self, gem_id, dialog_act, dialog_act_delexicalized, references, target, target_delexicalized):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.input_structure = dialog_act
        self.input_structure_delex = dialog_act_delexicalized
        self.dialogue_act_main = dialog_act.split('(')[0]
        self.property_list = dialog_act.split('(')[1].split(')')[0].split(',')
        self.references = references
        self.target = target
        self.target_delex = target_delexicalized
        self.input_size = len(self.property_list)

class DataEntryE2E:
    def __init__ (self, gem_id, meaning_representation, references, target):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.input_structure = meaning_representation
        self.property_list = meaning_representation.split(', ')
        self.references = references
        self.target = target
        self.input_size = len(self.property_list)

class DataEntryMLSum:
    def __init__ (self, gem_id, date, references, target, text, title, topic, url):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.input_text = text
        self.references = references
        self.target = target
        self.date = date
        self.title = title
        self.topic = topic
        self.url = url
        self.input_size = len(' '.split(text))

class DataEntrySGDialog:
    def __init__ (self, gem_id, dialog_acts, dialog_id, prompt, references, target, turn_id):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.input_structure = dialog_acts
        self.dialog_id = dialog_id
        self.prompt = prompt
        self.references = references
        self.target = target
        self.turn_id = turn_id
        self.input_size = len(dialog_acts)
        
class DataEntryTotto:
    def __init__ (self, gem_id, example_id, highlighted_cells, overlap_subset, references, sentence_annotations, table, table_page_title, table_section_text, table_section_title, table_webpage_url, target, totto_id):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.example_id = example_id
        self.input_structure = highlighted_cells
        self.overlap_subset = overlap_subset
        self.references = references
        self.sentence_annotations = sentence_annotations
        self.table = table
        self.table_page_title = table_page_title
        self.table_section_text = table_section_text
        self.table_section_title = table_section_title
        self.table_webpage_url = table_webpage_url
        self.target = target
        self.totto_id = totto_id
        self.input_size = len(highlighted_cells)

class DataEntryWebNLG:
    def __init__ (self, gem_id, category, triples, references, target, webnlg_id):
        """to store all input data and access all parts when building the output file; also calculates metrics for representing input complexity. """
        self.gem_id = gem_id
        self.category = category
        self.references = references
        self.target = target
        self.webnlg_id = webnlg_id
        self.input_structure = triples
        self.triple_object_list = []
        dico_subj = {}
        dico_obj = {}
        dico_prop = {}
        max_chain = []
        for instance_triple in triples:
            triple = TripleWebNLG(instance_triple)
            self.triple_object_list.append(triple)
            fillDicoCount(dico_subj, triple.subj)
            fillDicoCount(dico_obj, triple.obj)
            fillDicoCount(dico_prop, triple.prop)
        # check for max num of shared subj, max num of shared obj, num of chain entities that appear both as subject and object
        # on test set: up to 7 same subjects per triple set
        self.max_subj_same = getMaxValueDico(dico_subj)
        # on test set: up to 3 same objects per triple set
        self.max_obj_same = getMaxValueDico(dico_obj)
        # on test set: up to 2 same properties per triple set
        self.max_prop_same = getMaxValueDico(dico_prop)
        entity_subj_obj = []
        for subj in dico_subj:
            if subj in dico_obj:
                entity_subj_obj.append(subj)
        # on test set: 0, 1 or 2 entities found both as subject and object
        self.subj_obj_same = len(entity_subj_obj)
        # if self.max_prop_same > 2:
            # print(gem_id, self.max_prop_same)
            # print('  ', triples)
        # 1 to 7 triples
        self.input_size = len(triples)

class DataEntryWikiAuto:
    def __init__ (self, gem_id, source, references, target, source_id, target_id):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.input_text = source
        self.references = references
        self.target = target
        self.source_id = source_id
        self.target_id = target_id
        self.input_size = len(' '.split(source))

class DataEntryXSum:
    def __init__ (self, gem_id, document, references, target, xsum_id):
        """to store all input data and access all parts when building the output file. """
        self.gem_id = gem_id
        self.input_text = document
        self.references = references
        self.target = target
        self.xsum_id = xsum_id
        self.input_size = len(' '.split(document))

# Restructure input data if needed
############################################
write_log('Reading input data and selecting subset...', log_file)
x = 0
write_log('  '+str(len(dataset[subSet]))+' inputs found.', log_file)

# dico where the key is a category and the value is a list which will contain all DataEntryWebNLG objects of that category
dico_input_objects_per_category = {}

# dico where the key is a category and the value is a dico in which the key is the input size and the value a list which will contain all DataEntryWebNLG objects of that category
#dico_input_objects_per_category_per_size = {}
        
if (dataset_name == 'web_nlg_en' or dataset_name == 'web_nlg_ru'):
    for instance in dataset[subSet]:
        while x < len (dataset[subSet]):
            input_object = DataEntryWebNLG(dataset[subSet][x]['gem_id'], dataset[subSet][x]['category'], dataset[subSet][x]['input'], dataset[subSet][x]['references'], dataset[subSet][x]['target'], dataset[subSet][x]['webnlg_id'])
            # if the current category is not found in the dico, create a key with the category label in the dico
            if not input_object.category in dico_input_objects_per_category:
                dico_input_objects_per_category[input_object.category] = []
            dico_input_objects_per_category[input_object.category].append(input_object)
            
            # if the current category is not found in the dico, create a key with the category label in the dico
            # if not input_object.category in dico_input_objects_per_category_per_size:
                # dico_input_objects_per_category_per_size[input_object.category] = {}
            # if the current input size is not found in the dico, create a key with the input size number label in the embedded dico
            # if not input_object.input_size in dico_input_objects_per_category_per_size[input_object.category]:
                # dico_input_objects_per_category_per_size[input_object.category][input_object.input_size] = []
            # dico_input_objects_per_category_per_size[input_object.category][input_object.input_size].append(input_object)
            x += 1

# Build list with IDs of desired inputs
############################################

# list which contains all DataEntry objects found in the data
list_input_objects = []

num_category = 0
num_input_ctrl = 0
line = ''
# get a proportional number of samples per category: num of inputs per category * desired number of samples / total number of inputs
coeff = num_samples/len(dataset[subSet])
write_log('  Proportion kept: '+str(coeff), log_file)

list_selected_inputs_random = []
list_selected_inputs_complexity = []

if (dataset_name == 'web_nlg_en' or dataset_name == 'web_nlg_ru'):
    # To sample randomly from all triple set sizes at the same time
    for category in sorted(dico_input_objects_per_category):
        num_input_category = len(dico_input_objects_per_category[category])
        num_samples_category = round(num_input_category*coeff)
        write_log('Category #'+str(num_category)+' '+category+' (total: '+str(num_input_category)+' / selected: '+str(num_samples_category)+')', log_file)
        random_selection = secure_random.sample(dico_input_objects_per_category[category], num_samples_category)
        for selected_element in random_selection:
            num_input_ctrl += 1
            list_selected_inputs_random.append(selected_element.gem_id)
            #print(' ', selected_element.gem_id)
        num_category += 1

    # To sample according to the size of the triple set
    # for category in sorted(dico_input_objects_per_category_per_size):
        # print('Category #', num_category, category)
        # for input_size in sorted(dico_input_objects_per_category_per_size[category]):
            # print('Size #', input_size)
            # if len(dico_input_objects_per_category_per_size[category][input_size]) > num_samples:
                # random_selection = secure_random.sample(dico_input_objects_per_category_per_size[category][input_size], num_samples)
            # else:
                # random_selection = dico_input_objects_per_category_per_size[category][input_size]
            # for selected_element in random_selection:
                # print(' ', selected_element.gem_id)
        # num_category += 1

else:
    random_selection = secure_random.sample(list(dataset[subSet]), num_samples)
    x = 0
    if dataset_name == 'common_gen':
        while x < len (random_selection):
            input_object = DataEntryCommonGen(random_selection[x]['gem_id'], random_selection[x]['concepts'], random_selection[x]['concept_set_id'], random_selection[x]['references'], random_selection[x]['target'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif dataset_name == 'cs_restaurants':
        while x < len (random_selection):
            input_object = DataEntryCsRestaurants(random_selection[x]['gem_id'], random_selection[x]['dialog_act'], random_selection[x]['dialog_act_delexicalized'], random_selection[x]['references'], random_selection[x]['target'], random_selection[x]['target_delexicalized'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif dataset_name == 'e2e_nlg':
        while x < len (random_selection):
            input_object = DataEntryE2E(random_selection[x]['gem_id'], random_selection[x]['meaning_representation'], random_selection[x]['references'], random_selection[x]['target'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif (dataset_name == 'mlsum_de' or dataset_name == 'mlsum_es'):
        while x < len (random_selection):
            input_object = DataEntryMLSum(random_selection[x]['gem_id'], random_selection[x]['date'], random_selection[x]['references'], random_selection[x]['target'], random_selection[x]['text'], random_selection[x]['title'], random_selection[x]['topic'], random_selection[x]['url'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif dataset_name == 'schema_guided_dialog':
        while x < len (random_selection):
            input_object = DataEntrySGDialog(random_selection[x]['gem_id'], random_selection[x]['dialog_acts'], random_selection[x]['dialog_id'], random_selection[x]['prompt'], random_selection[x]['references'], random_selection[x]['target'], random_selection[x]['turn_id'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif dataset_name == 'totto':
        while x < len (random_selection):
            input_object = DataEntryTotto(random_selection[x]['gem_id'], random_selection[x]['example_id'], random_selection[x]['highlighted_cells'], random_selection[x]['overlap_subset'], random_selection[x]['references'], random_selection[x]['sentence_annotations'],random_selection[x]['table'], random_selection[x]['table_page_title'], random_selection[x]['table_section_text'], random_selection[x]['table_section_title'], random_selection[x]['table_webpage_url'], random_selection[x]['target'], random_selection[x]['totto_id'])
            #list_selected_inputs_random.append(input_object.gem_id)    
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif dataset_name == 'wiki_auto_asset_turk':
        while x < len (random_selection):
            input_object = DataEntryWikiAuto(random_selection[x]['gem_id'], random_selection[x]['source'], random_selection[x]['references'], random_selection[x]['target'], random_selection[x]['source_id'], random_selection[x]['target_id'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
            
    elif dataset_name == 'xsum':
        while x < len (random_selection):
            input_object = DataEntryXSum(random_selection[x]['gem_id'], random_selection[x]['document'], random_selection[x]['references'], random_selection[x]['target'], random_selection[x]['xsum_id'])
            list_input_objects.append(input_object)       
            num_input_ctrl += 1       
            x += 1
    
line = line + 'Total number of selected inputs: ' + str(num_input_ctrl)
write_log('-----------------------', log_file)
write_log(line, log_file)
write_log('-----------------------', log_file)

# Build output json file
############################################
write_log('Buidling output file(s)...', log_file)
if create_new_test_set_file == 'yes':
    fileName_out = subSet+'_'+dataset_name+'_'+perturbation+str(num_samples)+'.json'
    fo = codecs.open(fileName_out, 'w', 'utf-8')
    dico_main = {}
    dico_main[subSet] = []
    #fo.write("{\n    '"+subSet+"': [\n")
    count = 0
    if dico_input_objects_per_category:
        for category in sorted(dico_input_objects_per_category):
            for input_object in dico_input_objects_per_category[category]:
                # calls function that writes output file the function returns the updated counter if something was written; we need to keep track for the last comma (see function)
                #count = int(writeOutFileStructure(input_object, list_selected_inputs_random, fo, count, dataset_name, perturbation, subSet))
                #print(list_selected_inputs_random)
                FillDicoOut(dico_main, input_object, list_selected_inputs_random, dataset_name, perturbation, subSet)
                
    elif list_input_objects:
        for input_object in list_input_objects:
            # calls function that writes output file the function returns the updated counter if something was written; we need to keep track for the last comma (see function)
            #count = int(writeOutFileStructure(input_object, list_selected_inputs_random, fo, count, dataset_name, perturbation, subSet))
            FillDicoOut(dico_main, input_object, list_selected_inputs_random, dataset_name, perturbation, subSet)
            
    #fo.write("    ]\n}")
    fo.write(json.dumps(dico_main))
    fo.close()
    write_log('Created special input file!', log_file)
    write_log('-----------------------', log_file)

# Build output ID file
############################################
if create_list_of_ids == 'yes':
    fileName_out = subSet+'_'+dataset_name+'_'+perturbation+str(num_samples)+'_IDs.json'
    fo = codecs.open(fileName_out, 'w', 'utf-8')
    dico_main = {}
    dico_main[subSet] = []
    #fo.write("{\n    '"+subSet+"': [\n")
    if list_selected_inputs_random:
        #writeOutFileID(list_selected_inputs_random, fo)
        for ID in sorted(list_selected_inputs_random):
            dico_main[subSet].append(ID)
    #fo.write("    ]\n}")
    fo.write(json.dumps(dico_main))
    fo.close()
    write_log('Created ID file!', log_file)
    write_log('-----------------------', log_file)

log_file.close()  


# Input dataset samples
############################################
# See at bottom of file
#CommonGen
# {'concept_set_id': 0,
# 'concepts': ['field', 'look', 'stand'],
# 'gem_id': 'common_gen-validation-0',
# 'references': ['The player stood in the field looking at the batter.',
               # 'The coach stands along the field, looking at the goalkeeper.',
               # 'I stood and looked across the field, peacefully.',
               # 'Someone stands, looking around the empty field.'],
# 'target': 'The player stood in the field looking at the batter.'}
 
#CSRestaurants
# {'dialog_act': '?request(area)',
# 'dialog_act_delexicalized': '?request(area)',
# 'gem_id': 'cs_restaurants-validation-0',
# 'references': ['Jakou lokalitu hledáte ?'],
# 'target': 'Jakou lokalitu hledáte ?',
# 'target_delexicalized': 'Jakou lokalitu hledáte ?'}
 
# Dart
# {'dart_id': 0,
# 'gem_id': 'dart-validation-0',
# 'references': ['A school from Mars Hill, North Carolina, joined in 1973.'],
# 'subtree_was_extended': True,
# 'target': 'A school from Mars Hill, North Carolina, joined in 1973.',
# 'target_sources': ['WikiSQL_decl_sents'],
# 'tripleset': [['Mars Hill College', 'JOINED', '1973'], ['Mars Hill College', 'LOCATION', 'Mars Hill, North Carolina']]}

#E2E
# {'gem_id': 'e2e_nlg-validation-0',
# 'meaning_representation': 'name[Alimentum], area[city centre], familyFriendly[no]',
# 'references': ['There is a place in the city centre, Alimentum, that is not family-friendly.'],
# 'target': 'There is a place in the city centre, Alimentum, that is not family-friendly.'}

#MLSum
# {'date': '00/04/2019',
# 'gem_id': 'mlsum_de-validation-0',
# 'references': ['In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ihrer Wohnung gefunden worden. Nun stehen zwei Bekannte unter Verdacht.'],
# 'target': 'In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ihrer Wohnung gefunden worden. Nun stehen zwei Bekannte unter Verdacht.',
# 'text': 'Kerzen und Blumen stehen vor dem Eingang eines Hauses, in dem eine 18-jährige Frau tot aufgefunden wurde. In einer Kleinstadt auf der Insel Usedom war eine junge Frau tot in ...',
# 'title': 'Tod von 18-Jähriger auf Usedom: Zwei Festnahmen',
# 'topic': 'panorama',
# 'url': 'https://www.sueddeutsche.de/panorama/usedom-frau-tot-festnahme-verdaechtige-1.4412256'}

# Schema-guided Dialog
# {'dialog_acts': [{'act': 2, 'slot': 'song_name', 'values': ['Carnivore']}, {'act': 2, 'slot': 'playback_device', 'values': ['TV']}],
# 'dialog_id': '10_00054',
# 'gem_id': 'schema_guided_dialog-validation-0',
# 'prompt': 'Yes, I would.',
# 'references': ['Please confirm the song Carnivore on tv.'],
# 'target': 'Please confirm the song Carnivore on tv.',
# 'turn_id': 15}

# Totto
# {'example_id': '7391450717765563190',
# 'gem_id': 'totto-validation-0',
# 'highlighted_cells': [[3, 0], [3, 2], [3, 3]],
# 'overlap_subset': 'True',
# 'references': ['Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                # 'Daniel Henry Chamberlain was the 76th Governor of South Carolina, beginning in 1874.',
                # 'Daniel Henry Chamberlain was the 76th Governor of South Carolina who took office in 1874.'],
# 'sentence_annotations': [{'final_sentence': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                           # 'original_sentence': 'Daniel Henry Chamberlain (June 23, 1835 – April 13, 1907) was an American planter, lawyer, author and the 76th Governor of South Carolina '
                                                # 'from 1874 until 1877.',
                           # 'sentence_after_ambiguity': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
                           # 'sentence_after_deletion': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.'},
                          # ...
                          # ],
# 'table': [[{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '#'},
            # {'column_span': 2, 'is_header': True, 'row_span': 1, 'value': 'Governor'},
            # {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Took Office'},
            # {'column_span': 1, 'is_header': True, 'row_span': 1, 'value': 'Left Office'}],
           # [{'column_span': 1, 'is_header': True, 'row_span': 1, 'value': '74'},
            # {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': '-'},
            # {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'Robert Kingston Scott'},
            # {'column_span': 1, 'is_header': False, 'row_span': 1, 'value': 'July 6, 1868'}],
           # ...
          # ],
# 'table_page_title': 'List of Governors of South Carolina',
# 'table_section_text': 'Parties Democratic Republican',
# 'table_section_title': 'Governors under the Constitution of 1868',
# 'table_webpage_url': 'http://en.wikipedia.org/wiki/List_of_Governors_of_South_Carolina',
# 'target': 'Daniel Henry Chamberlain was the 76th Governor of South Carolina from 1874.',
# 'totto_id': 0}
 
#WebNLG
# {'category': 'Airport',
# 'gem_id': 'web_nlg_en-validation-0',
# 'input': ['Aarhus | leader | Jacob_Bundsgaard'],
# 'references': ['The leader of Aarhus is Jacob Bundsgaard.'],
# 'target': 'The leader of Aarhus is Jacob Bundsgaard.',
# 'webnlg_id': 'dev/Airport/1/Id1'}

# Wiki Auto Asset Turk
# {'gem_id': 'wiki_auto_asset_turk-validation-0',
# 'references': ['The Gandalf Awards honor excellent writing in in fantasy literature.'],
# 'source': 'The Gandalf Awards, honoring achievement in fantasy literature, were conferred by the World Science Fiction Society annually from 1974 to 1981.',
# 'source_id': '350_691837-1-0-0',
# 'target': 'The Gandalf Awards honor excellent writing in in fantasy literature.',
# 'target_id': '350_691837-0-0-0'}

# Wiki Lingua
# {'gem_id': 'wiki_lingua_ru_en-val-0',
# 'references': ['Get immediate medical care if you notice signs of a complication. Undergo diagnostic tests to check for gallstones and complications. Ask your doctor about your treatment '
                # 'options.'],
# 'source': 'И хотя, скорее всего, вам не о чем волноваться, следует незамедлительно обратиться к врачу, если вы подозреваете, что у вас возникло осложнение желчекаменной болезни. Это ...',
# 'target': 'Get immediate medical care if you notice signs of a complication. Undergo diagnostic tests to check for gallstones and complications. Ask your doctor about your treatment '
          # 'options.'}
          
# XSum
# {'document': 'Burberry reported pre-tax profits of £166m for the year to March. A year ago it made a loss of £16.1m, hit by charges at its Spanish operations.\n'
             # 'In the past year it has opened 21 new stores and closed nine. It plans to open 20-30 stores this year worldwide.\n'
             # 'The group has also focused on promoting the Burberry brand online...',
# 'gem_id': 'xsum-validation-0',
# 'references': ['Luxury fashion designer Burberry has returned to profit after opening new stores and spending more on online marketing'],
# 'target': 'Luxury fashion designer Burberry has returned to profit after opening new stores and spending more on online marketing',
# 'xsum_id': '10162122'}

    