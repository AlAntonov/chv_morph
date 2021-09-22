import sys
import string
import os
import numpy as np
from config import Config

def chv_apply_10_rule(verb, affix, conj_verb):
  # у десяти глаголов на –р (йӗр, кӗр, кӳр, пар, пер, пыр, хур, шӑр, яр конечный звук выпадает
  if verb in ['йӗр', 'кӗр', 'кӳр', 'пар', 'пер', 'пыр', 'тӑр', 'хур', 'шӑр', 'яр']:
    return verb[:-1] + affix
  return conj_verb
  
def chv_apply_rln_rule(verb, affix, form, conj_verb):
  # у десяти глаголов на –р (йӗр, кӗр, кӳр, пар, пер, пыр, хур, шӑр, яр конечный звук выпадает
  if verb in ['йӗр', 'кӗр', 'кӳр', 'пар', 'пер', 'пыр', 'тӑр', 'хур', 'шӑр', 'яр']:
    if form[4] == '3': 
      return verb[:-1] + 'ч' + affix[1:]
    else:
      return verb[:-1] + 'т' + affix[1:]
  # c основами на р, л, н –р меняется на –т, а в 3 лице – на –ч.
  if verb[-1] in ['р', 'л', 'н']:
    if form[4] == '3': 
      return verb + 'ч' + affix[1:]
    else:
      return verb + 'т' + affix[1:]
  return conj_verb

def chv_apply_last_vokal_rule(verb, affix, conj_verb):
  # у глаголов оканчивающюхся на 'а', 'я', 'е' последняя буква корня сливается с первой окончания
  if verb[-1] in ['а', 'е']:
    return verb[:-1] + affix
  if verb[-1] in ['я']:
    return verb[:-1] + 'я' + affix[1:]
  return conj_verb

def chv_apply_last_y_rule(verb, affix, conj_verb):
  # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
  if verb[-1] in ['у']:
    conj_verb = verb[:-1] + 'ӑв' + affix
  return conj_verb
  
def chv_apply_rules(verb, conj_table, form):
  affix = conj_table[form]
  conj_verb = verb + affix
  # для положительной формы настояще-будущего времени
  if form[6] == 'p' and form[8:10] == 'nb':
    conj_verb = chv_apply_last_vokal_rule(verb, affix, conj_verb)
    # у глаголов оканчивающюхся на 'й' эта буква заменяется на 'я'
    if verb[-1] in ['й']:
      conj_verb = verb[:-1] + 'я' + affix[1:]
    conj_verb = chv_apply_last_y_rule(verb, affix, conj_verb)
  # для отрицательной формы настояще-будущего времени
  if form[6] == 'n' and form[8:10] == 'nb':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для положительной формы прошедшего очевидного времени
  if form[6] == 'p' and form[8:10] == 'po':
    conj_verb = chv_apply_rln_rule(verb, affix, form, conj_verb)
  # для отрицательной формы прошедшего очевидного времени
  if form[6] == 'n' and form[8:10] == 'po':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для положительной формы будущего времени
  if form[6] == 'p' and form[8:10] == 'bb':
    # у глаголов оканчивающюхся на 'а' эта буква выпадает
    if verb[-1] in ['а']:
      conj_verb = verb[:-1] + affix
    # у глаголов оканчивающюхся на 'е'  эта буква выпадает
    if verb[-1] in ['е']:
      conj_verb = verb[:-1] + affix
    # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
    if verb[-1] in ['я']:
      if affix[0] in 'ӑ':
        conj_verb = verb[:-1] + 'ь' + affix
      if affix[0] in 'ӗ':
        conj_verb = verb[:-1] + affix
    # у глаголов оканчивающюхся на 'и' добавляется 'й'
    if verb[-1] in ['и']:
      conj_verb = verb + 'й' + affix
    conj_verb = chv_apply_last_y_rule(verb, affix, conj_verb)
  # для отрицательной формы будущего времени
  if form[6] == 'n' and form[8:10] == 'bb':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для прошедшего неочевидного времени
  if form[8:10] == 'ps':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для давнопрошедшего времени
  if form[8:10] == 'pd':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для повелительного наклонения, 2 лица мн. числа
  if form[8:10] == 'im' and (form[2:5] == 'm_2' or form[4:5] == '1'):
  # у глаголов оканчивающюхся на 'а' эта буква выпадает
    if verb[-1] in ['а']:
      conj_verb = verb[:-1] + affix
    # у глаголов оканчивающюхся на 'е'  эта буква выпадает
    if verb[-1] in ['е']:
      conj_verb = verb[:-1] + affix
    # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ'
    if verb[-1] in ['я']:
      if affix[0] in 'ӑ':
        conj_verb = verb[:-1] + 'ь' + affix
    # у глаголов оканчивающюхся на 'и' добавляется 'й'
    if verb[-1] in ['и']:
      conj_verb = verb + 'й' + affix
    conj_verb = chv_apply_last_y_rule(verb, affix, conj_verb)
  # для повелительного наклонения, 3 лица мн. числа
  if form[8:10] == 'im' and form[2:5] == 'm_3':
  # у глаголов не оканчивающюхся на 'т', 'х', 'ҫ' две чч
    if verb[-1] not in ['т', 'х', 'ҫ']:
      conj_verb = verb + 'ч' + affix
  # для инфинитива
  if form[8:10] == 'in':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для причастия настоящего времени
  if form[8:10] == 'pn':
    conj_verb = chv_apply_last_vokal_rule(verb, affix, conj_verb)
    conj_verb = chv_apply_last_y_rule(verb, affix, conj_verb)
  # для причастия будущего времени
  if form[8:10] == 'pb':
    conj_verb = chv_apply_last_vokal_rule(verb, affix, conj_verb)
    conj_verb = chv_apply_last_y_rule(verb, affix, conj_verb)
  # для причастия долженстования
  if form[8:10] == 'pm':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для отрицательной формы условно-временного деепричастия
  if form[6] == 'n' and form[8:10] == 'du':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  if form[6] == 'n' and form[8:10] == 'dv':
    conj_verb = chv_apply_10_rule(verb, affix, conj_verb)
  # для положительной формы условно-временного деепричастия
  if form[6] == 'p' and form[8:10] == 'dv':
    # у глаголов оканчивающюхся на 'c' она выпадает
    if verb[-1] == 'с':
      conj_verb = verb[:-1] + affix
  return conj_verb

def get_hs(verb):
  hard = ['а', 'ӑ', 'о', 'у', 'ы', 'ю', 'я']
  soft = ['е', 'ӗ', 'ӳ', 'и']
  for a in reversed(verb):
    if a in hard:
      return 'h'
    if a in soft:
      return 's'
  return 'n'

def chv_apply_10_derule(verb, i, inf_verbs):
  # у десяти глаголов на –р (йӗр, кӗр, кӳр, пар, пер, пыр, хур, шӑр, яр конечный звук выпадает
  if verb[:i] in ['йӗ', 'кӗ', 'кӳ', 'па', 'пе', 'пы', 'тӑ', 'ху', 'шӑ', 'я']:
    inf_verbs.append(verb[:i] + 'р')

def chv_apply_last_vokal_derule(verb, i, inf_verbs):
  # у глаголов оканчивающюхся на 'а', 'я', 'е' последняя буква корня сливается с первой окончания
  if verb[i:i+1] in ['а', 'я', 'е']:
    inf_verbs.append(verb[:i+1])

def chv_apply_derules(verb, conj_table):
  inf_verbs = []
  forms = [] # 'форма не найдена'
  form = 'форма не найдена'
  trn_verb = 'нет в словаре'
  inf_verbs.append(verb)
  forms.append("h_e_1_p_im")
  for i in range(-7,0):
    if verb[i:] in conj_table:
      # if verb[:i][-1] not in ['а', 'я', 'й']:
      inf_verbs.append(verb[:i])
      form = conj_table[verb[i:]]
      # для положительной формы настояще-будущего времени
      if form[6] == 'p' and form[8:10] == 'nb':
        chv_apply_last_vokal_derule(verb, i, inf_verbs)
        # у глаголов оканчивающюхся на 'й' эта буква заменяется на 'я'
        if verb[i-1:i+1] in ['ая', 'уя']:
          inf_verbs.append(verb[:i] + 'й')
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if verb[i-2:i] in ['ӑв']:
          inf_verbs.append(verb[:i-2] + 'у')
      # для отрицательной формы настояще-будущего времени
      if form[6] == 'n' and form[8:10] == 'nb':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для прошедшего очевидного времени
      if form[8:10] == 'po':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для положительной формы будущего времени
      if form[6] == 'p' and form[8:10] == 'bb':
        # у глаголов оканчивающюхся на 'а' эта буква выпадает
        if verb[i:i+1] in ['ӑ']:
          inf_verbs.append(verb[:i] + 'а')
        if verb[i:i+1] in ['ӗ'] or verb[i:] in ['ӗ']:
          inf_verbs.append(verb[:i] + 'а')
        # у глаголов оканчивающюхся на 'е'  эта буква выпадает
        if verb[i:i+1] in ['ӗ'] or verb[i:] in ['ӗ']:
          inf_verbs.append(verb[:i] + 'е')
        # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
        if verb[i-1:i+1] in ['ьӑ']:
          inf_verbs.append(verb[:i-1] + 'я')
        if verb[i:i+1] in ['ӗ'] or verb[i:] in ['ӗ']:
          inf_verbs.append(verb[:i] + 'я')
        # у глаголов оканчивающюхся на 'и' добавляется 'й'
        if verb[i-1:i+1] in ['йӗ'] or verb[i-1:] in ['йӗ']:
          inf_verbs.append(verb[:i-1])
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if verb[i-2:i] in ['ӑв']:
          inf_verbs.append(verb[:i-2] + 'у')
      # для отрицательной формы будущего времени
      if form[6] == 'n' and form[8:10] == 'bb':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для прошедшего неочевидного времени
      if form[8:10] == 'ps':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для давнопрошедшего времени
      if form[8:10] == 'pd':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для повелительного наклонения, 2 лица мн. числа
      if form[8:10] == 'im' and (form[2:5] == 'm_2'):
        # у глаголов оканчивающюхся на 'а' эта буква выпадает
        if verb[i:i+1] in ['ӑ']:
          inf_verbs.append(verb[:i] + 'а')
        # у глаголов оканчивающюхся на 'е'  эта буква выпадает
        if verb[i:i+1] in ['ӗ'] or verb[i:] in ['ӗ']:
          inf_verbs.append(verb[:i] + 'е')
        # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
        if verb[i-1:i+1] in ['ьӑ']:
          inf_verbs.append(verb[:i-1] + 'я')
        # у глаголов оканчивающюхся на 'и' добавляется 'й'
        if verb[i-1:i+1] in ['йӗ'] or verb[i-1:] in ['йӗ']:
          inf_verbs.append(verb[:i-1])
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if verb[i-2:i] in ['ӑв']:
          inf_verbs.append(verb[:i-2] + 'у')
      # для повелительного наклонения, 1 лица
      if form[8:10] == 'im' and (form[4:5] == '1'):
        # у глаголов оканчивающюхся на 'а' эта буква выпадает
        if verb[i:i+1] in ['а']:
          inf_verbs.append(verb[:i] + 'а')
        # у глаголов оканчивающюхся на 'е'  эта буква выпадает
        if verb[i:i+1] in ['е'] or verb[i:] in ['е']:
          inf_verbs.append(verb[:i] + 'е')
        # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
        if verb[i-1:i+1] in ['ьа']:
          inf_verbs.append(verb[:i-1] + 'а')
        # у глаголов оканчивающюхся на 'и' добавляется 'й'
        if verb[i-1:i+1] in ['йе'] or verb[i-1:] in ['йе']:
          inf_verbs.append(verb[:i-1])
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if verb[i-2:i] in ['ӑв']:
          inf_verbs.append(verb[:i-2] + 'у')
      # для повелительного наклонения, 3 лица мн. числа
      if form[8:10] == 'im' and form[2:5] == 'm_3':
        # у глаголов не оканчивающюхся на 'т', 'х', 'ҫ' две чч
        if verb[i-1:i+1] in ['чч']:
          inf_verbs.append(verb[:i-1])
      # для инфинитива
      if form[8:10] == 'in':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для причастия настоящего времени
      if form[8:10] == 'pn':
        chv_apply_last_vokal_derule(verb, i, inf_verbs)
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if verb[i-2:i] in ['ӑв']:
          inf_verbs.append(verb[:i-2] + 'у')
      # для причастия будущего времени
      if form[8:10] == 'pb':
        chv_apply_last_vokal_derule(verb, i, inf_verbs)
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if verb[i-2:i] in ['ӑв']:
          inf_verbs.append(verb[:i-2] + 'у')
      # для причастия долженстования
      if form[8:10] == 'pm':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для отрицательной формы условно-временного деепричастия
      if form[6] == 'n' and form[8:10] == 'du':
        chv_apply_10_derule(verb, i, inf_verbs)
      if form[6] == 'n' and form[8:10] == 'dv':
        chv_apply_10_derule(verb, i, inf_verbs)
      # для положительной формы условно-временного деепричастия
      if form[6] == 'p' and form[8:10] == 'dv':
        # у глаголов оканчивающюхся на 'c' она выпадает
        if verb[i:i+1] in ['с']:
          inf_verbs.append(verb[:i] + 'с')
      for j in range(len(forms)-1,len(inf_verbs)):
        modal_candidate = inf_verbs[j]
        # инфинитив оканчивающий на 'й', исключая короткие слова, является кандидатом быть формой 'могу'
        if len(modal_candidate) > 3 and modal_candidate[-1] == 'й':
          inf_verbs.append(modal_candidate[:-1])
          inf_verbs.append(modal_candidate[:-2])
        # инфинитив оканчивающий на 'тар', 'тер', 'ттар', 'ттер', является кандидатом быть понудительной формы
        if modal_candidate[-4:] in ['ттар', 'ттер']:
          inf_verbs.append(modal_candidate[:-4])
        if modal_candidate[-3:] in ['тар', 'тер']:
          inf_verbs.append(modal_candidate[:-3])
      for j in range(len(forms),len(inf_verbs)):
        forms.append(form)
  return inf_verbs, forms
  
def chv_apply_noun_derules(noun, noun_table, form_list = []):
  im_nouns = []
  forms = [] # 'форма не найдена'
  form = 'форма не найдена'
  trn_noun = 'нет в словаре'
  if "e_0_im" in form_list:
    im_nouns.append(noun)
    forms.append("h_e_0_im")
  for i in range(-7,0):
    if noun[i:] in noun_table:
      form = noun_table[noun[i:]]
      if form[2:] in form_list:
        im_nouns.append(noun[:i])
        for j in range(len(forms),len(im_nouns)):
          forms.append(form)
  return im_nouns, forms
  
def fix_encoding_lower(verb, reverse = True):
  verb = verb.lower()
  if reverse:
    return verb.replace('ӗ','ĕ').replace('ӑ','ă').replace('ҫ','ç').replace('ӳ','ÿ')
  else:
    return verb.replace('ĕ','ӗ').replace('ă','ӑ').replace('ç','ҫ').replace('ÿ','ӳ')

def chv_search_form(verb, pos, config, form_verb_list, verbal=False):
  debug = verb == "хӑмпӑ"
  if pos == "verb":
    conj_table = config.conj_verb_table
    words_list = config.verbs_list
    trn_words_list = config.trn_verbs_list
    pos_verbal = "глагол"
    inf_words, forms = chv_apply_derules(verb, conj_table)
  else:
    conj_table = config.conj_noun_table
    words_list = config.nouns_list
    trn_words_list = config.trn_nouns_list
    pos_verbal = "существительное"
    inf_words, forms = chv_apply_noun_derules(verb, conj_table, form_verb_list)
  trn_verb = ''
  chosen_inv_verb = ''
  chosen_form = ''
  form_index = -1
  form_found = False
  for inf_verb in inf_words:
    form_index = form_index + 1
    for index in [i for i, x in enumerate(words_list) if x == fix_encoding_lower(inf_verb)]:
      trn_verb_candidate = trn_words_list[index]
      if trn_verb != '':
        trn_verb = trn_verb + '; '
      trn_verb = trn_verb + trn_verb_candidate
      chosen_inv_verb = inf_verb
      chosen_form = forms[form_index]
  if trn_verb == '':
    trn_verb = 'нет в словаре'
  if chosen_form[2:] in form_verb_list:
    if verbal:
      print('%s: %s %s в форме %s\n%s' % (verb, pos_verbal, chosen_inv_verb, chosen_form[2:], trn_verb))
    form_found = True
  return form_found, chosen_form[2:]
  
def chv_search_form_in_list(form_list, config, total_sents, verb_index_table, pos, line, counter, counter_list):
  translator = str.maketrans('', '', string.punctuation)
  for form in form_list:
    form_num = form + str(total_sents)
    if form_num in verb_index_table.keys():
      verb_list = verb_index_table[form_num]
      for verb in verb_list:
        verb_index = line[:-1].replace('-',' ').translate(translator).split(' ').index(verb)
        if not counter:
          if (config.has_second_word < 1) or (verb_index in counter_list[total_sents]):
            chv_search_form(verb, pos, config, form_list, verbal=True)
        else:
          counter_list.append(verb_index)
  
def chv_search(config, show_first_sents=10):
  index_table = np.load(config.index_filename, allow_pickle='TRUE').item()
  verb_index_table = np.load(config.verb_index_filename, allow_pickle='TRUE').item()  
  sent_numbers = set()
  sent_numbers2 = set()
  
  print("первый список форм")
  if len(config.form_verb_list) > 0: print(config.form_verb_list)
  if len(config.form_noun_list) > 0: print(config.form_noun_list)
  if config.has_second_word >= 1:
    print("второй список форм")
    if len(config.form2_verb_list) > 0: print(config.form2_verb_list)
    if len(config.form2_noun_list) > 0: print(config.form2_noun_list)
    print("расстояние: %d" % config.has_second_word)
  total_sents = 0
  for form in config.form_verb_list + config.form2_verb_list:
    if form in index_table.keys():
      sent_numbers = sent_numbers.union(map(int, index_table[form]))
  if config.has_second_word >= 1:
    for form2 in config.form2_verb_list + config.form2_noun_list:
      if form2 in index_table.keys():
        sent_numbers2 = sent_numbers2.union(map(int, index_table[form2]))
    sent_numbers = sent_numbers.intersection(sent_numbers2)
  sent_numbers = sorted(sent_numbers)
  with open(config.search_filename, encoding="utf-8") as search_file:
    dist_sent_numbers = set()
    dist_pair1 = {}
    dist_pair2 = {}
    if config.has_second_word >= 1:
      for line in search_file:
        total_sents += 1
        line = fix_encoding_lower(line, False)
        if total_sents in sent_numbers:
          counter1_list = []
          counter2_list = []
          chv_search_form_in_list(config.form_verb_list, config, total_sents, verb_index_table, "verb", line, True, counter1_list)
          chv_search_form_in_list(config.form_noun_list, config, total_sents, verb_index_table, "noun", line, True, counter1_list)
          chv_search_form_in_list(config.form2_verb_list, config, total_sents, verb_index_table, "verb", line, True, counter2_list)
          chv_search_form_in_list(config.form2_noun_list, config, total_sents, verb_index_table, "noun", line, True, counter2_list)
          #print(counter1_list)
          #print(counter2_list)
          #print("\n")
          
          for cnt1 in counter1_list:
            for cnt2 in counter2_list:
              if (cnt2 > cnt1) and (cnt2 <= (cnt1 + config.has_second_word)):              
                dist_sent_numbers.add(total_sents)
                if total_sents in dist_pair1.keys():
                  tmp = dist_pair1[total_sents]
                  tmp.append(cnt1)
                  dist_pair1[total_sents] = tmp
                else:
                  dist_pair1[total_sents] = [cnt1]
                if total_sents in dist_pair2.keys():
                  tmp = dist_pair2[total_sents]
                  tmp.append(cnt2)
                  dist_pair2[total_sents] = tmp
                else:
                  dist_pair2[total_sents] = [cnt2]
    else:
      dist_sent_numbers = sent_numbers
    
    dist_sent_numbers = sorted(dist_sent_numbers)    
    print("найдено предложений: %d" % len(dist_sent_numbers))
    if (show_first_sents > 0):  
      dist_sent_numbers = dist_sent_numbers[:show_first_sents]
      print("показаны первые: %d"  % len(dist_sent_numbers))
    print("\n")
  
  with open(config.search_filename, encoding="utf-8") as search_file:  
    total_sents = 0    
    for line in search_file:
      total_sents += 1
      line = fix_encoding_lower(line, False)
      if total_sents in dist_sent_numbers:
        chv_search_form_in_list(config.form_verb_list, config, total_sents, verb_index_table, "verb", line, False, dist_pair1)
        chv_search_form_in_list(config.form_noun_list, config, total_sents, verb_index_table, "noun", line, False, dist_pair1)
        chv_search_form_in_list(config.form2_verb_list, config, total_sents, verb_index_table, "verb", line, False, dist_pair2)
        chv_search_form_in_list(config.form2_noun_list, config, total_sents, verb_index_table, "noun", line, False, dist_pair2)
        print('%d:%s' % (total_sents, line))
  
def chv_create_search_index(config):
  found_sents = 0
  total_sents = 0
  translator = str.maketrans('', '', string.punctuation)  
  cash_dict = {}
  index_dict = {}
  verb_index_dict = {}
  with open(config.search_filename, encoding="utf-8") as search_file:
    for line in search_file:
      total_sents += 1
      form_found = False
      word_form_found = False
      noun_form_found = False
      line = fix_encoding_lower(line, False)
      words = line[:-1].replace('-',' ').translate(translator).split(' ')
      for word in words:
        if word not in cash_dict.keys():
          word_form_found, chosen_verb_form = chv_search_form(word, "verb", config, config.form_verb_list)
          noun_form_found, chosen_noun_form = chv_search_form(word, "noun", config, config.form_noun_list)
        else:
          word_form_found = True
          chosen_verb_form = cash_dict[word]
        if word_form_found or noun_form_found:
          form_found = True
        if chosen_verb_form != '':
          chosen_form = chosen_verb_form
          if word not in cash_dict.keys():
            cash_dict[word] = chosen_form
          if chosen_form in index_dict.keys():
            tmp = index_dict[chosen_form]
            tmp.append(str(total_sents))
            index_dict[chosen_form] = tmp
          else:
            index_dict[chosen_form] = [str(total_sents)]
          chosen_form_num = chosen_form + str(total_sents)
          if chosen_form_num in verb_index_dict.keys():
            tmp = verb_index_dict[chosen_form_num]
            tmp.append(word)
            verb_index_dict[chosen_form_num] = tmp
          else:
            verb_index_dict[chosen_form_num] = [word]
        if chosen_noun_form != '':
          chosen_form = chosen_noun_form
          if word not in cash_dict.keys():
            cash_dict[word] = chosen_form
          if chosen_form in index_dict.keys():
            tmp = index_dict[chosen_form]
            tmp.append(str(total_sents))
            index_dict[chosen_form] = tmp
          else:
            index_dict[chosen_form] = [str(total_sents)]
          chosen_form_num = chosen_form + str(total_sents)
          if chosen_form_num in verb_index_dict.keys():
            tmp = verb_index_dict[chosen_form_num]
            tmp.append(word)
            verb_index_dict[chosen_form_num] = tmp
          else:
            verb_index_dict[chosen_form_num] = [word]
      if form_found:
        found_sents += 1
        print('%d из %d:%s' % (found_sents, total_sents, line))
    np.save(config.index_filename, index_dict)
    np.save(config.verb_index_filename, verb_index_dict)  

if __name__ == '__main__':
  show_first_sents = int(sys.argv[1])
  has_second_word = int(sys.argv[2])
  is_index = False
  config = Config(has_second_word, is_index)
  
  if is_index:
    chv_create_search_index(config)
  else:
    chv_search(config, show_first_sents)