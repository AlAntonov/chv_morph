import sys
import string
import os
import numpy as np

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
  
def chv_conjugate_site(verb):
 chosen_inv_verb, trn_verb = chv_deconjugate(verb, 'andreev.chv', 'andreev.ru', 'conj_table.txt', verbal=True)
 return chv_conjugate(chosen_inv_verb, 'conj_table.txt', 'pronoun_table.txt', trn_verb)

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
  # print (conj_table.keys())
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

def chv_deconjugate_site(verb):
 return chv_deconjugate(verb, 'andreev.chv', 'andreev.ru', 'conj_table.txt', verbal=True)
  
def chv_deconjugate(verb, verb_filename, trn_verb_filename, conj_filename, verbal=True):
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
      if is_verb(trn_verb_candidate):
        if trn_verb != '':
          trn_verb = trn_verb + '; '
        trn_verb = trn_verb + trn_verb_candidate
        chosen_inv_verb = inf_verb
        chosen_form = forms[form_index]
  if trn_verb == '':
    trn_verb = 'нет в словаре'
  if verbal:
    if len(inf_verbs) == 0:
      print('глагол не найден')
    else:
      print('%s: глагол %s в форме %s\n%s' % (verb, chosen_inv_verb, chosen_form[2:], trn_verb))  
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

def chv_search_form(verb, verb_filename, trn_verb_filename, conj_filename, form_list, verbal=True):
  verb = check_encoding(verb, False)
  verb = verb.lower()
  conj_table = chv_read_conj_table(conj_filename, True)
  verbs_list = chv_read_verbs_list(verb_filename)
  trn_verbs_list = chv_read_verbs_list(trn_verb_filename)
  trn_verb = ''
  inf_verbs, forms = chv_apply_derules(verb, conj_table)
  chosen_inv_verb = ''
  chosen_form = ''
  form_index = -1
  form_found = False
  for inf_verb in inf_verbs:
    # print(inf_verb)
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
  return form_found, chosen_form, verb
  
def chv_search(search_filename, verb_filename, trn_verb_filename, conj_filename, config_filename, index_filename=None, create_index=False):
  found_sents = 0
  total_sents = 0
  verbs_list = chv_read_verbs_list(verb_filename)
  translator = str.maketrans('', '', string.punctuation)
  form_found = False
  word_form_found = False
  new_line = ''
  index_table = {}
  verb_index_table = {}
  form_list = chv_get_form_from_config(config_filename)
  print(form_list)
  if create_index or index_filename is None:
    with open(search_filename, encoding="utf-8") as search_file:
      for line in search_file:
        total_sents += 1
        form_found = False
        new_line = line[:-1].replace('-',' ')
        words = new_line.translate(translator).split(' ')
        for word in words:
          word_form_found, chosen_form, verb = chv_search_form(word, verb_filename, trn_verb_filename, conj_filename, form_list, True)
          if word_form_found:
            form_found = True
          if create_index and chosen_form != '':
            chosen_form = chosen_form[2:]
            if chosen_form in index_table.keys():
              index_table[chosen_form] += ' ' + str(total_sents)
            else:
              index_table[chosen_form] = str(total_sents)
            chosen_form_num = chosen_form + str(total_sents)
            if chosen_form_num in verb_index_table.keys():
              verb_index_table[chosen_form_num] +=  ' ' + verb
            else:
              verb_index_table[chosen_form_num] =  verb
        if form_found:
          found_sents += 1
          print('%d из %d:%s' % (found_sents, total_sents, line))
    if create_index:
      np.save(index_filename, index_table)
      verb_index_filename = 'verb_' + index_filename
      np.save(verb_index_filename, verb_index_table)
  else:
    index_table = np.load(index_filename, allow_pickle='TRUE').item()
    verb_index_filename = 'verb_' + index_filename
    verb_index_table = np.load(verb_index_filename, allow_pickle='TRUE').item()
    sent_numbers = set()
    for form in form_list:
      if form in index_table.keys():
        sent_numbers = sent_numbers.union(map(int, index_table[form].split(' ')))
    sent_numbers = sorted(sent_numbers)
    print(len(sent_numbers))
    with open(search_filename, encoding="utf-8") as search_file:
      for line in search_file:
        total_sents += 1
        if total_sents in sent_numbers:
          for form in form_list:
            form_num = form + str(total_sents)
            if form_num in verb_index_table.keys():
              verb_list = verb_index_table[form_num].split(' ')
              for verb in verb_list:
                chv_deconjugate(verb, verb_filename, trn_verb_filename, conj_filename, verbal=True)
          print('%d:%s' % (total_sents, line))
          
    

if __name__ == '__main__':
  # verb = sys.argv[1]
  # form = sys.argv[1]
  
  conj_filename = 'conj_table.txt'
  verb_filename = 'andreev.chv_verb' # 'verbs.txt'
  trn_verb_filename = 'andreev.ru_verb'
  search_filename = 'волкимал.chv2'
  prnn_filename = 'pronoun_table.txt'
  config_filename = 'config.txt'
  index_filename = 'index.npy'
  create_index = False
  
  # chv_conjugate(verb, conj_filename, prnn_filename, '')
  # chv_conjugate_site(verb)
  # chv_deconjugate(verb, verb_filename, trn_verb_filename, conj_filename, verbal=True)
  chv_search(search_filename, verb_filename, trn_verb_filename, conj_filename, config_filename, index_filename, create_index)