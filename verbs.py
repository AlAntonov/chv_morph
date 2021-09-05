import sys
import string
import os
import numpy as np
import time
from multiprocessing import Process, Manager

class FullVerb:
   def __init__(self, form, verb):
      self.form = form
      self.verb = verb

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

def chv_conjugate(verb, conj_filename, prnn_filename, trn_verb):
  verb = check_encoding(verb, False)
  verb = verb.lower()
  conj_table = chv_read_conj_table(conj_filename)
  prnn_filename = chv_read_conj_table(prnn_filename, True)
  hs = get_hs(verb)
  conj_verb_list = []
  prev_form_title = ''
  for form in conj_table.keys():
    if form[0] != hs:
      continue	
    text_form = prnn_filename[form[2:5]]
    form_title = prnn_filename[form[6:10]]
    conj_verb = chv_apply_rules(verb, conj_table, form)
    print(text_form + " " + conj_verb)
    if form_title != prev_form_title:
      conj_verb_list.append(FullVerb("title",check_encoding(form_title, False)))
    prev_form_title = form_title
    conj_verb_list.append(FullVerb(check_encoding(text_form, False),check_encoding(conj_verb, False)))
  return check_encoding(verb, False), trn_verb, conj_verb_list

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

def is_verb(trn_verb):
  return trn_verb[-2:] == 'ть' or  trn_verb[-4:] == 'ться' or trn_verb[-2:] == 'ти'
  
def check_encoding(verb, reverse = True):
  if reverse:
    return verb.replace('ӗ','ĕ').replace('ӑ','ă').replace('ҫ','ç').replace('ӳ','ÿ')
  else:
    return verb.replace('ĕ','ӗ').replace('ă','ӑ').replace('ç','ҫ').replace('ÿ','ӳ') 
  
def chv_read_verbs_list(verb_filename):
  verbs_list = []
  location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  with open(os.path.join(location, verb_filename), encoding="utf-8") as verb_file:
    for line in verb_file:
      verbs_list.append(line[:-1])
  return verbs_list

def chv_read_conj_table(conj_filename, reverse = False):
  conj_table = {}
  location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
  with open(os.path.join(location, conj_filename), encoding="utf-8") as conj_file:
    for line in conj_file:
      splitted_line = line[:-1].split(':')
      if reverse:
        conj_table[splitted_line[1]] = splitted_line[0]
      else:
        conj_table[splitted_line[0]] = splitted_line[1]
  return conj_table  
  
def chv_deconjugate(verb, verb_filename, trn_verb_filename, conj_filename, pos, verbal=True):
  verb = check_encoding(verb, False)
  verb = verb.lower()
  conj_table = chv_read_conj_table(conj_filename, True)
  verbs_list = chv_read_verbs_list(verb_filename)
  trn_verbs_list = chv_read_verbs_list(trn_verb_filename)
  trn_verb = ''
  inf_verbs, forms = chv_apply_derules(verb, conj_table)
  #if verbal:
    #print(inf_verbs)
    #print(forms)
  chosen_inv_verb = ''
  chosen_form = ''
  form_index = -1
  for inf_verb in inf_verbs:
    # print(inf_verb)
    form_index = form_index + 1
    for index in [i for i, x in enumerate(verbs_list) if x == check_encoding(inf_verb)]:
      trn_verb_candidate = trn_verbs_list[index]
      # if is_verb(trn_verb_candidate): только для глаголов
      if trn_verb != '':
        trn_verb = trn_verb + '; '
      trn_verb = trn_verb + trn_verb_candidate
      chosen_inv_verb = inf_verb
      chosen_form = forms[form_index]
  if trn_verb == '':
    trn_verb = 'нет в словаре'
  if verbal:
    if len(inf_verbs) == 0:
      print(pos + ' не найден')
    else:
      print('%s: %s %s в форме %s\n%s' % (verb, pos, chosen_inv_verb, chosen_form[2:], trn_verb))  
  # return '%s: глагол %s в форме %s\n%s' % (verb, chosen_inv_verb, chosen_form[2:], trn_verb)
  return chosen_inv_verb, trn_verb
  # return trn_verb != 'нет в словаре'
  
def chv_get_form_from_config(config_filename):
  form_list = []
  chislo_list = ['e', 'm']
  lico_list = ['1', '2', '3']
  negative_list = ['p', 'n']
  verb_form_list = ['nb', 'po', 'bb', 'ps', 'pd', 'im', 'in', 'pn', 'pb', 'pm', 'de', 'du', 'dv']
  with open(config_filename, encoding="utf-8") as config_file:
    for line in config_file:
      splitted_line = line.replace('\n','').split(':')
      if splitted_line[0] == 'Часть_речи':
        if 'v' not in splitted_line[1].split(','):
          return form_list
      if splitted_line[0] == 'Число':
        chislo_list = splitted_line[1].split(',')
      if splitted_line[0] == 'Лицо':
        lico_list = splitted_line[1].split(',')
      if splitted_line[0] == 'Отрицание':
        negative_list = splitted_line[1].split(',')
      if splitted_line[0] == 'Форма':
        verb_form_list = splitted_line[1].split(',')
  for chislo in chislo_list:
    for lico in lico_list:
      for negative in negative_list:
        for verb_form in verb_form_list:
          form_list.append(chislo + '_' + lico + '_' + negative + '_' + verb_form)
  return form_list

def chv_get_form_from_noun_config(config_filename):
  form_list = []
  chislo_list = ['e', 'm']
  lico_list = ['0','1', '2', '3']
  padezh_list = ['im', 'ro', 'da', 'me', 'is', 'tv', 'pc']
  with open(config_filename, encoding="utf-8") as config_file:
    for line in config_file:
      splitted_line = line.replace('\n','').split(':')
      if splitted_line[0] == 'Часть_речи':
        if 'n' not in splitted_line[1].split(','):
          return form_list
      if splitted_line[0] == 'Число':
        chislo_list = splitted_line[1].split(',')
      if splitted_line[0] == 'Лицо':
        lico_list = splitted_line[1].split(',')
      if splitted_line[0] == 'Падеж':
        padezh_list = splitted_line[1].split(',')
  for chislo in chislo_list:
    for lico in lico_list:
      for padezh in padezh_list:
        form_list.append(chislo + '_' + lico + '_' + padezh)
  return form_list

def chv_search_form(verb, verbs_list, trn_verbs_list, conj_table, form_list, verbal=True):
  verb = check_encoding(verb, False)
  verb = verb.lower()
  trn_verb = ''
  inf_verbs, forms = chv_apply_derules(verb, conj_table)
  chosen_inv_verb = ''
  chosen_form = ''
  form_index = -1
  form_found = False
  for inf_verb in inf_verbs:
    form_index = form_index + 1
    for index in [i for i, x in enumerate(verbs_list) if x == check_encoding(inf_verb)]:
      trn_verb_candidate = trn_verbs_list[index]
      if is_verb(trn_verb_candidate):
        if trn_verb != '':
          trn_verb = trn_verb + '; '
        trn_verb = trn_verb + trn_verb_candidate
        chosen_inv_verb = inf_verb
        chosen_form = forms[form_index]
  if trn_verb == '':
    trn_verb = 'нет в словаре'
  if chosen_form[2:] in form_list:
    if verbal:
      print('%s: глагол %s в форме %s\n%s' % (verb, chosen_inv_verb, chosen_form[2:], trn_verb))
    form_found = True
  return form_found, chosen_form[2:]

def chv_search_noun_form(noun, nouns_list, trn_nouns_list, noun_table, form_list, verbal=True):
  noun = check_encoding(noun, False)
  noun = noun.lower()
  trn_noun = ''
  im_nouns, forms = chv_apply_noun_derules(noun, noun_table, form_list)
  chosen_im_noun = ''
  chosen_form = ''
  form_index = -1
  form_found = False
  for im_noun in im_nouns:
    form_index = form_index + 1
    for index in [i for i, x in enumerate(nouns_list) if x == check_encoding(im_noun)]:
      trn_noun_candidate = trn_nouns_list[index]
      #if is_verb(trn_verb_candidate):
      if trn_noun != '':
        trn_noun = trn_noun + '; '
      trn_noun = trn_noun + trn_noun_candidate
      chosen_im_noun = im_noun
      chosen_form = forms[form_index]
  if trn_noun == '':
    trn_noun = 'нет в словаре'
  if chosen_form[2:] in form_list:
    if verbal:
      print('%s: существительное %s в форме %s\n%s' % (noun, chosen_im_noun, chosen_form[2:], trn_noun))
    form_found = True
  return form_found, chosen_form[2:]
  
def chv_search(search_filename, verb_filename, trn_verb_filename, noun_filename, trn_noun_filename, conj_verb_filename, conj_noun_filename, config_filename, index_filename, show_first_sents=10, config2_filename=None):
  index_table = np.load(index_filename, allow_pickle='TRUE').item()
  verb_index_filename = 'verb_' + index_filename
  verb_index_table = np.load(verb_index_filename, allow_pickle='TRUE').item()
  sent_numbers = set()
  sent_numbers2 = set()
  sent_numbers3 = set()
  sent_numbers4 = set()
  form_verb_list = chv_get_form_from_config(config_filename)
  form_noun_list = chv_get_form_from_noun_config(config_filename)
  conj_verb_table = chv_read_conj_table(conj_verb_filename, True)
  conj_noun_table = chv_read_conj_table(conj_noun_filename, True)
  verbs_list = chv_read_verbs_list(verb_filename)
  trn_verbs_list = chv_read_verbs_list(trn_verb_filename)
  nouns_list = chv_read_verbs_list(noun_filename)
  trn_nouns_list = chv_read_verbs_list(trn_noun_filename)
  form2_verb_list = []
  form2_noun_list = []
  print("первый список форм")
  if len(form_verb_list)>0: print(form_verb_list)
  if len(form_noun_list)>0: print(form_noun_list)
  if config2_filename is not None:
    form2_verb_list = chv_get_form_from_config(config2_filename)
    form2_noun_list = chv_get_form_from_noun_config(config2_filename)
    print("второй список форм")
    if len(form2_verb_list)>0: print(form2_verb_list)
    if len(form2_noun_list)>0: print(form2_noun_list)
  conj_verb_table = chv_read_conj_table(conj_verb_filename, True)
  conj_noun_table = chv_read_conj_table(conj_noun_filename, True)
  total_sents = 0
  for form in form_verb_list:
    if form in index_table.keys():
      sent_numbers = sent_numbers.union(map(int, index_table[form]))
  for form2 in form2_verb_list:
    if form2 in index_table.keys():
      sent_numbers2 = sent_numbers2.union(map(int, index_table[form2]))
  for form in form_noun_list:
    if form in index_table.keys():
      sent_numbers = sent_numbers.union(map(int, index_table[form]))
  for form2 in form2_noun_list:
    if form2 in index_table.keys():
      sent_numbers2 = sent_numbers2.union(map(int, index_table[form2]))
  if config2_filename is not None:
    sent_numbers = sent_numbers.intersection(sent_numbers2)
  sent_numbers = sorted(sent_numbers)
  print("найдено предложений")
  print(len(sent_numbers))
  if (show_first_sents > 0):
    print("показаны первые")    
    sent_numbers = sent_numbers[:show_first_sents]
    print(len(sent_numbers))
  with open(search_filename, encoding="utf-8") as search_file:
    for line in search_file:
      total_sents += 1
      if total_sents in sent_numbers:
        for form in form_verb_list:
          form_num = form + str(total_sents)
          if form_num in verb_index_table.keys():
            verb_list = verb_index_table[form_num]
            for verb in verb_list:
              chv_search_form(verb, verbs_list, trn_verbs_list, conj_verb_table, form_verb_list, verbal=True)
        for form in form_noun_list:
          form_num = form + str(total_sents)
          if form_num in verb_index_table.keys():
            verb_list = verb_index_table[form_num]
            for verb in verb_list:
              chv_search_noun_form(verb, nouns_list, trn_nouns_list, conj_noun_table, form_noun_list, verbal=True)
        for form2 in form2_verb_list:
          form_num = form2 + str(total_sents)
          if form_num in verb_index_table.keys():
            verb_list = verb_index_table[form_num]
            for verb in verb_list:
              chv_search_form(verb, verbs_list, trn_verbs_list, conj_verb_table, form2_verb_list, verbal=True)
        for form2 in form2_noun_list:
          form_num = form2 + str(total_sents)
          if form_num in verb_index_table.keys():
            verb_list = verb_index_table[form_num]
            for verb in verb_list:
              chv_search_noun_form(verb, nouns_list, trn_nouns_list, conj_noun_table, form2_noun_list, verbal=True)
        print('%d:%s' % (total_sents, line))
  
def chv_create_search_index(s_list, verb_filename, trn_verb_filename, noun_filename, trn_noun_filename, conj_verb_filename, conj_noun_filename, config_filename, index_dict, verb_index_dict, index_filename=None):
  found_sents = 0
  total_sents = 0
  translator = str.maketrans('', '', string.punctuation)
  form_found = False
  word_form_found = False
  new_line = ''
  form_verb_list = chv_get_form_from_config(config_filename)
  form_noun_list = chv_get_form_from_noun_config(config_filename)
  conj_verb_table = chv_read_conj_table(conj_verb_filename, True)
  conj_noun_table = chv_read_conj_table(conj_noun_filename, True)
  verbs_list = chv_read_verbs_list(verb_filename)
  trn_verbs_list = chv_read_verbs_list(trn_verb_filename)
  nouns_list = chv_read_verbs_list(noun_filename)
  trn_nouns_list = chv_read_verbs_list(trn_noun_filename)
  cash_dict = {}
  for line in s_list:
      total_sents += 1
      form_found = False
      word_form_found = False
      noun_form_found = False
      new_line = line[:-1].replace('-',' ')
      words = new_line.translate(translator).split(' ')
      for word in words:
        word = check_encoding(word, False)
        word = word.lower()
        debug = word == "тухсан"
        if word not in cash_dict.keys():
          word_form_found, chosen_verb_form = chv_search_form(word, verbs_list, trn_verbs_list, conj_verb_table, form_verb_list, False)
          noun_form_found, chosen_noun_form = chv_search_noun_form(word, nouns_list, trn_nouns_list, conj_noun_table, form_noun_list, False)
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
            verb_index_dict[chosen_form_num] =  [word]
      if form_found:
        found_sents += 1
        print('%d из %d:%s' % (found_sents, total_sents, line))

if __name__ == '__main__':
  start_time = time.time()
  show_first_sents = int(sys.argv[1])
  has_second_word = int(sys.argv[2])
  
  conj_noun_filename = 'conj_noun_table.txt'
  conj_verb_filename = 'conj_table.txt'
  noun_filename = 'andreev.chv_noun'
  trn_noun_filename = 'andreev.ru_noun'
  verb_filename = 'andreev.chv_verb'
  trn_verb_filename = 'andreev.ru_verb'
  search_filename = 'chv.100K.monocorpus.txt'
  prnn_filename = 'pronoun_table.txt'
  config_filename = 'config.txt'
  config2_filename = 'config2.txt'
  if has_second_word != 1: config2_filename = None
  index_filename = 'index.npy'
    
  with open(search_filename, encoding="utf-8") as search_file:
    lines = search_file.read().splitlines()
  n = len(lines) # 300
  search_list = (lines[i:i+n] for i in range(0, len(lines), n))  
  index_table_list = []
  verb_index_table_list = []
  procs = []
  '''
  manager = Manager()
  mp_index_dict = manager.dict()
  mp_verb_index_dict = manager.dict()
  for index, s_list in enumerate(search_list):
    index_table_list.append({})
    verb_index_table_list.append({})
    proc = Process(target=chv_create_search_index, args=(s_list, verb_filename, trn_verb_filename, noun_filename, trn_noun_filename, conj_verb_filename, conj_noun_filename, config_filename, mp_index_dict, mp_verb_index_dict, index, n, index_filename,))
    procs.append(proc)
    proc.start()
  for proc in procs:
    proc.join()
  
  index_dict = mp_index_dict.copy()
  verb_index_dict = mp_verb_index_dict.copy()
  '''
  '''
  index_dict = {}
  verb_index_dict = {}
  chv_create_search_index(search_list, verb_filename, trn_verb_filename, noun_filename, trn_noun_filename, conj_verb_filename, conj_noun_filename, config_filename, index_dict, verb_index_dict, index_filename)
  np.save(index_filename, index_dict)
  verb_index_filename = 'verb_' + index_filename
  np.save(verb_index_filename, verb_index_dict)  
  '''  
  chv_search(search_filename, verb_filename, trn_verb_filename, noun_filename, trn_noun_filename, conj_verb_filename, conj_noun_filename, config_filename, index_filename, show_first_sents, config2_filename)
  
  print("--- %s seconds ---" % (time.time() - start_time))  