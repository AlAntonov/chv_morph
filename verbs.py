import sys
import string
import os
import numpy as np
from config import Config

def chv_apply_10_rule(word, affix, conj_word):
  # у десяти глаголов на –р (йӗр, кӗр, кӳр, пар, пер, пыр, хур, шӑр, яр конечный звук выпадает
  if word in ['йӗр', 'кӗр', 'кӳр', 'пар', 'пер', 'пыр', 'тӑр', 'хур', 'шӑр', 'яр']:
    return word[:-1] + affix
  return conj_word
  
def chv_apply_rln_rule(word, affix, form, conj_word):
  # у десяти глаголов на –р (йӗр, кӗр, кӳр, пар, пер, пыр, хур, шӑр, яр конечный звук выпадает
  if word in ['йӗр', 'кӗр', 'кӳр', 'пар', 'пер', 'пыр', 'тӑр', 'хур', 'шӑр', 'яр']:
    if form[4] == '3': 
      return word[:-1] + 'ч' + affix[1:]
    else:
      return word[:-1] + 'т' + affix[1:]
  # c основами на р, л, н –р меняется на –т, а в 3 лице – на –ч.
  if word[-1] in ['р', 'л', 'н']:
    if form[4] == '3': 
      return word + 'ч' + affix[1:]
    else:
      return word + 'т' + affix[1:]
  return conj_word

def chv_apply_last_vokal_rule(word, affix, conj_word):
  # у глаголов оканчивающюхся на 'а', 'я', 'е' последняя буква корня сливается с первой окончания
  if word[-1] in ['а', 'е']:
    return word[:-1] + affix
  if word[-1] in ['я']:
    return word[:-1] + 'я' + affix[1:]
  return conj_word

def chv_apply_last_y_rule(word, affix, conj_word):
  # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
  if word[-1] in ['у']:
    conj_word = word[:-1] + 'ӑв' + affix
  return conj_word
  
def chv_apply_verb_rules(word, conj_table, form):
  affix = conj_table[form]
  conj_word = word + affix
  # для положительной формы настояще-будущего времени
  if form[6] == 'p' and form[8:10] == 'nb':
    conj_word = chv_apply_last_vokal_rule(word, affix, conj_word)
    # у глаголов оканчивающюхся на 'й' эта буква заменяется на 'я'
    if word[-1] in ['й']:
      conj_word = word[:-1] + 'я' + affix[1:]
    conj_word = chv_apply_last_y_rule(word, affix, conj_word)
  # для отрицательной формы настояще-будущего времени
  if form[6] == 'n' and form[8:10] == 'nb':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для положительной формы прошедшего очевидного времени
  if form[6] == 'p' and form[8:10] == 'po':
    conj_word = chv_apply_rln_rule(word, affix, form, conj_word)
  # для отрицательной формы прошедшего очевидного времени
  if form[6] == 'n' and form[8:10] == 'po':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для положительной формы будущего времени
  if form[6] == 'p' and form[8:10] == 'bb':
    # у глаголов оканчивающюхся на 'а' эта буква выпадает
    if word[-1] in ['а']:
      conj_word = word[:-1] + affix
    # у глаголов оканчивающюхся на 'е'  эта буква выпадает
    if word[-1] in ['е']:
      conj_word = word[:-1] + affix
    # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
    if word[-1] in ['я']:
      if affix[0] in 'ӑ':
        conj_word = word[:-1] + 'ь' + affix
      if affix[0] in 'ӗ':
        conj_word = word[:-1] + affix
    # у глаголов оканчивающюхся на 'и' добавляется 'й'
    if word[-1] in ['и']:
      conj_word = word + 'й' + affix
    conj_word = chv_apply_last_y_rule(word, affix, conj_word)
  # для отрицательной формы будущего времени
  if form[6] == 'n' and form[8:10] == 'bb':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для прошедшего неочевидного времени
  if form[8:10] == 'ps':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для давнопрошедшего времени
  if form[8:10] == 'pd':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для повелительного наклонения, 2 лица мн. числа
  if form[8:10] == 'im' and (form[2:5] == 'm_2' or form[4:5] == '1'):
  # у глаголов оканчивающюхся на 'а' эта буква выпадает
    if word[-1] in ['а']:
      conj_word = word[:-1] + affix
    # у глаголов оканчивающюхся на 'е'  эта буква выпадает
    if word[-1] in ['е']:
      conj_word = word[:-1] + affix
    # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ'
    if word[-1] in ['я']:
      if affix[0] in 'ӑ':
        conj_word = word[:-1] + 'ь' + affix
    # у глаголов оканчивающюхся на 'и' добавляется 'й'
    if word[-1] in ['и']:
      conj_word = word + 'й' + affix
    conj_word = chv_apply_last_y_rule(word, affix, conj_word)
  # для повелительного наклонения, 3 лица мн. числа
  if form[8:10] == 'im' and form[2:5] == 'm_3':
  # у глаголов не оканчивающюхся на 'т', 'х', 'ҫ' две чч
    if word[-1] not in ['т', 'х', 'ҫ']:
      conj_word = word + 'ч' + affix
  # для инфинитива
  if form[8:10] == 'in':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для причастия настоящего времени
  if form[8:10] == 'pn':
    conj_word = chv_apply_last_vokal_rule(word, affix, conj_word)
    conj_word = chv_apply_last_y_rule(word, affix, conj_word)
  # для причастия будущего времени
  if form[8:10] == 'pb':
    conj_word = chv_apply_last_vokal_rule(word, affix, conj_word)
    conj_word = chv_apply_last_y_rule(word, affix, conj_word)
  # для причастия долженстования
  if form[8:10] == 'pm':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для отрицательной формы условно-временного деепричастия
  if form[6] == 'n' and form[8:10] == 'du':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  if form[6] == 'n' and form[8:10] == 'dv':
    conj_word = chv_apply_10_rule(word, affix, conj_word)
  # для положительной формы условно-временного деепричастия
  if form[6] == 'p' and form[8:10] == 'dv':
    # у глаголов оканчивающюхся на 'c' она выпадает
    if word[-1] == 'с':
      conj_word = word[:-1] + affix
  return conj_word

def chv_apply_noun_last_vokal_rule(word, affix, conj_word):
  # у существительных оканчивающюхся на 'а', в 3-м лице вместо 'ӗ' ставится 'и'
  if word[-1] in ['а']:
    return word[:-1] + 'и'
  return conj_word
  
def chv_apply_noun_rules(word, conj_table, form):
  affix = conj_table[form]
  conj_word = word + affix
  #для 3-го лица
  if form[4] == '3':
    conj_word = chv_apply_noun_last_vokal_rule(word, affix, conj_word)
  return conj_word
  
def chv_apply_adj_rules(word, conj_table, form):
  affix = conj_table[form]
  conj_word = word + affix
  return conj_word
  
def chv_apply_rules(word, conj_table, form, pos):
  if pos == "noun":
    return chv_apply_noun_rules(word, conj_table, form)
  elif pos == "adj":    
    return chv_apply_adj_rules(word, conj_table, form)
  else:
    return chv_apply_verb_rules(word, conj_table, form)

def get_hs(word):
  hard = ['а', 'ӑ', 'о', 'у', 'ы', 'ю', 'я']
  soft = ['е', 'ӗ', 'ӳ', 'и']
  for a in reversed(word):
    if a in hard:
      return 'h'
    if a in soft:
      return 's'
  return 'n'

def chv_apply_10_derule(word, i, inf_verbs):
  # у десяти глаголов на –р (йӗр, кӗр, кӳр, пар, пер, пыр, хур, шӑр, яр конечный звук выпадает
  if word[:i] in ['йӗ', 'кӗ', 'кӳ', 'па', 'пе', 'пы', 'тӑ', 'ху', 'шӑ', 'я']:
    inf_verbs.append(word[:i] + 'р')

def chv_apply_last_vokal_derule(word, i, inf_verbs):
  # у глаголов оканчивающюхся на 'а', 'я', 'е' последняя буква корня сливается с первой окончания
  if word[i:i+1] in ['а', 'я', 'е']:
    inf_verbs.append(word[:i+1])

def chv_apply_verb_derules(word, conj_table):
  inf_verbs = []
  forms = [] # 'форма не найдена'
  form = 'форма не найдена'
  trn_verb = 'нет в словаре'
  inf_verbs.append(word)
  forms.append("h_e_2_p_im")
  for i in range(-7,0):
    if word[i:] in conj_table:
      # if word[:i][-1] not in ['а', 'я', 'й']:
      inf_verbs.append(word[:i])
      form = conj_table[word[i:]]
      # для положительной формы настояще-будущего времени
      if form[6] == 'p' and form[8:10] == 'nb':
        chv_apply_last_vokal_derule(word, i, inf_verbs)
        # у глаголов оканчивающюхся на 'й' эта буква заменяется на 'я'
        if word[i-1:i+1] in ['ая', 'уя']:
          inf_verbs.append(word[:i] + 'й')
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if word[i-2:i] in ['ӑв']:
          inf_verbs.append(word[:i-2] + 'у')
      # для отрицательной формы настояще-будущего времени
      if form[6] == 'n' and form[8:10] == 'nb':
        chv_apply_10_derule(word, i, inf_verbs)
      # для прошедшего очевидного времени
      if form[8:10] == 'po':
        chv_apply_10_derule(word, i, inf_verbs)
      # для положительной формы будущего времени
      if form[6] == 'p' and form[8:10] == 'bb':
        # у глаголов оканчивающюхся на 'а' эта буква выпадает
        if word[i:i+1] in ['ӑ']:
          inf_verbs.append(word[:i] + 'а')
        if word[i:i+1] in ['ӗ'] or word[i:] in ['ӗ']:
          inf_verbs.append(word[:i] + 'а')
        # у глаголов оканчивающюхся на 'е'  эта буква выпадает
        if word[i:i+1] in ['ӗ'] or word[i:] in ['ӗ']:
          inf_verbs.append(word[:i] + 'е')
        # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
        if word[i-1:i+1] in ['ьӑ']:
          inf_verbs.append(word[:i-1] + 'я')
        if word[i:i+1] in ['ӗ'] or word[i:] in ['ӗ']:
          inf_verbs.append(word[:i] + 'я')
        # у глаголов оканчивающюхся на 'и' добавляется 'й'
        if word[i-1:i+1] in ['йӗ'] or word[i-1:] in ['йӗ']:
          inf_verbs.append(word[:i-1])
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if word[i-2:i] in ['ӑв']:
          inf_verbs.append(word[:i-2] + 'у')
      # для отрицательной формы будущего времени
      if form[6] == 'n' and form[8:10] == 'bb':
        chv_apply_10_derule(word, i, inf_verbs)
      # для прошедшего неочевидного времени
      if form[8:10] == 'ps':
        chv_apply_10_derule(word, i, inf_verbs)
      # для давнопрошедшего времени
      if form[8:10] == 'pd':
        chv_apply_10_derule(word, i, inf_verbs)
      # для повелительного наклонения, 2 лица мн. числа
      if form[8:10] == 'im' and (form[2:5] == 'm_2'):
        # у глаголов оканчивающюхся на 'а' эта буква выпадает
        if word[i:i+1] in ['ӑ']:
          inf_verbs.append(word[:i] + 'а')
        # у глаголов оканчивающюхся на 'е'  эта буква выпадает
        if word[i:i+1] in ['ӗ'] or word[i:] in ['ӗ']:
          inf_verbs.append(word[:i] + 'е')
        # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
        if word[i-1:i+1] in ['ьӑ']:
          inf_verbs.append(word[:i-1] + 'я')
        # у глаголов оканчивающюхся на 'и' добавляется 'й'
        if word[i-1:i+1] in ['йӗ'] or word[i-1:] in ['йӗ']:
          inf_verbs.append(word[:i-1])
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if word[i-2:i] in ['ӑв']:
          inf_verbs.append(word[:i-2] + 'у')
      # для повелительного наклонения, 1 лица
      if form[8:10] == 'im' and (form[4:5] == '1'):
        # у глаголов оканчивающюхся на 'а' эта буква выпадает
        if word[i:i+1] in ['а']:
          inf_verbs.append(word[:i] + 'а')
        # у глаголов оканчивающюхся на 'е'  эта буква выпадает
        if word[i:i+1] in ['е'] or word[i:] in ['е']:
          inf_verbs.append(word[:i] + 'е')
        # у глаголов оканчивающюхся на 'я' эта буква заменяется на 'ь' перед 'ӑ' и выпадает перед 'ӗ'
        if word[i-1:i+1] in ['ьа']:
          inf_verbs.append(word[:i-1] + 'а')
        # у глаголов оканчивающюхся на 'и' добавляется 'й'
        if word[i-1:i+1] in ['йе'] or word[i-1:] in ['йе']:
          inf_verbs.append(word[:i-1])
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if word[i-2:i] in ['ӑв']:
          inf_verbs.append(word[:i-2] + 'у')
      # для повелительного наклонения, 3 лица мн. числа
      if form[8:10] == 'im' and form[2:5] == 'm_3':
        # у глаголов не оканчивающюхся на 'т', 'х', 'ҫ' две чч
        if word[i-1:i+1] in ['чч']:
          inf_verbs.append(word[:i-1])
      # для инфинитива
      if form[8:10] == 'in':
        chv_apply_10_derule(word, i, inf_verbs)
      # для причастия настоящего времени
      if form[8:10] == 'pn':
        chv_apply_last_vokal_derule(word, i, inf_verbs)
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if word[i-2:i] in ['ӑв']:
          inf_verbs.append(word[:i-2] + 'у')
      # для причастия будущего времени
      if form[8:10] == 'pb':
        chv_apply_last_vokal_derule(word, i, inf_verbs)
        # у глаголов оканчивающюхся на 'у' эта буква заменяется на 'ӑв'
        if word[i-2:i] in ['ӑв']:
          inf_verbs.append(word[:i-2] + 'у')
      # для причастия долженстования
      if form[8:10] == 'pm':
        chv_apply_10_derule(word, i, inf_verbs)
      # для отрицательной формы условно-временного деепричастия
      if form[6] == 'n' and form[8:10] == 'du':
        chv_apply_10_derule(word, i, inf_verbs)
      if form[6] == 'n' and form[8:10] == 'dv':
        chv_apply_10_derule(word, i, inf_verbs)
      # для положительной формы условно-временного деепричастия
      if form[6] == 'p' and form[8:10] == 'dv':
        # у глаголов оканчивающюхся на 'c' она выпадает
        if word[i:i+1] in ['с']:
          inf_verbs.append(word[:i] + 'с')
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
  
def chv_apply_noun_last_vokal_derule(word, i, inf_verbs):
  # у существительных оканчивающюхся на 'а', в 3-м лице вместо 'ӗ' ставится 'и'
  if word[i:] in ['и', 'ин', 'ине', 'инче', 'инчен', 'ипе', 'исӗр', 'ишӗн']:
    inf_verbs.append(word[:i] + 'а')
    return True
  return False
  
def chv_apply_noun_derules(noun, conj_table):
  im_nouns = []
  forms = [] # 'форма не найдена'
  form = 'форма не найдена'
  trn_noun = 'нет в словаре'
  #if "e_0_im" in form_list:
  im_nouns.append(noun)
  forms.append("h_e_0_im")
  for i in range(-7,0):
    if noun[i:] in conj_table:      
      skip = False
      form = conj_table[noun[i:]]
      # для 3-го лица
      if form[4] == '3':
        skip = chv_apply_noun_last_vokal_derule(noun, i, im_nouns)
      # для прилагательных -ллӑ/-ллӗ от существительных
      if form[6:8] == 'pr':
        # у существительных оканчивающюхся на гласную 'л' удваивается
        if noun[i-1:i] in ['л']:
          im_nouns.append(noun[:i-1])
      #if form[2:] in form_list:
      if not skip:
        im_nouns.append(noun[:i])
      for j in range(len(forms),len(im_nouns)):
        forms.append(form)
  return im_nouns, forms
  
def chv_apply_adj_derules(word, conj_table):
  im_word = []
  forms = [] # 'форма не найдена'
  form = 'форма не найдена'
  trn_noun = 'нет в словаре'
  im_word.append(word)
  forms.append("h_im")
  for i in range(-7,0):
    if word[i:] in conj_table:
      form = conj_table[word[i:]]
      # для наречий -ӑн/-ӗн/-н от прилагательных
      if form[2:4] == 'na':
        # у прилагательных последние согласные удваиваются
        if len(word) > 4 and word[i-1] == word[i-2]:
          im_word.append(word[:i-1])
          if form[0] == "h":
            im_word.append(word[:i-1] + 'ӑ')
          if form[0] == "s":
            im_word.append(word[:i-1] + 'ӗ')
      # для наречий -ӑн/-ӗн не действует простое правило добавления суффикса
      if form[2:4] != 'na' or (form[2:4] == 'na' and word[i:] == 'н'):
        im_word.append(word[:i])
      for j in range(len(forms),len(im_word)):
        forms.append(form)
  return im_word, forms
  
def chv_apply_derules(word, conj_table, pos):
  if pos == "noun":
    return chv_apply_noun_derules(word, conj_table)
  elif pos == "adj":
    return chv_apply_adj_derules(word, conj_table)
  else:
    return chv_apply_verb_derules(word, conj_table)

def chv_get_wordforms_from_lemma(config, form_list, config_wordform_list, config_is_lemma, vocab_table): # from 'chv_conjugate'  
  wordform_list = []
  if config_is_lemma:
    for lemma in config_wordform_list:
      lemma = fix_encoding_lower(lemma)
      hs = get_hs(lemma)
      for pos in config.pos_list:
        for form in config.conj_normal_table[pos].keys():
          if form[0] != hs:
            continue
          if form[2:] not in form_list:
            continue
          wordform = chv_apply_rules(lemma, config.conj_normal_table[pos], form, pos)
          wordform_list.append(fix_encoding_lower(wordform, False))
  else:
    for wordform in config_wordform_list:
      fixed_wordform = fix_encoding_lower(wordform, False)
      if '*' in fixed_wordform:
        wordform_vocab_list = []
        if fixed_wordform[-1] == '*':
          wordform_vocab_list = [d for d in vocab_table.keys() if d.startswith(fixed_wordform[:-1])]
        if fixed_wordform[0] == '*':
          wordform_vocab_list = [d for d in vocab_table.keys() if d.endswith(fixed_wordform[1:])]
        for wordform_vocab in wordform_vocab_list:
          wordform_list.append(fix_encoding_lower(wordform_vocab, False))
      else:
        wordform_list.append(fixed_wordform)
      
  return list(set(wordform_list))
  
def fix_encoding_lower(word, reverse = True):
  word = word.lower().strip()
  if reverse:
    return word.replace('ӗ','ĕ').replace('ӑ','ă').replace('ҫ','ç').replace('ӳ','ÿ')
  else:
    return word.replace('ĕ','ӗ').replace('ă','ӑ').replace('ç','ҫ').replace('ÿ','ӳ')

def chv_search_form(word, pos, config, form_list, verbal=False):
  conj_table = config.conj_table[pos]
  words_list = config.src_list[pos]
  trn_words_list = config.trn_list[pos]
  pos_verbal = config.pos_verbal[pos]
  inf_words, forms = chv_apply_derules(word, conj_table, pos)
  trn_word = ''
  chosen_inf_word = ''
  chosen_form = ''
  form_index = -1
  form_found = False
  for inf_word in inf_words:
    form_index = form_index + 1
    for index in [i for i, x in enumerate(words_list) if x == fix_encoding_lower(inf_word)]:      
      trn_word_candidate = trn_words_list[index]
      if trn_word != '':
        trn_word = trn_word + '; '
      trn_word = trn_word + trn_word_candidate
      chosen_inf_word = inf_word
      chosen_form = forms[form_index]
  if trn_word == '':
    trn_word = 'нет в словаре'
  if chosen_form[2:] in form_list:
    if verbal:
      print('%s: %s %s в форме %s\n%s' % (word, pos_verbal, chosen_inf_word, chosen_form[2:], trn_word))
    form_found = True
  return form_found, (chosen_form[2:], chosen_inf_word)
  
def chv_search_wordform(wordform_list, config, total_sents, vocab_table, counter, counter_list):
  for wordform in wordform_list:
    if wordform in vocab_table.keys():
      for wf in vocab_table[wordform]:
        if int(wf[0]) == total_sents:
          wf1 = int(wf[1])
          if counter:
            counter_list.append(wf1)
          else:
            if (config.has_second_word < 1) or (wf1 in counter_list[total_sents]):
              print('%s: словоформа' % wordform)
  
def chv_search_form_in_list(form_list, config, total_sents, word_index_table, pos, line, counter, counter_list):
  translator = str.maketrans('', '', string.punctuation)
  for form in form_list:
    form_num = form + str(total_sents)
    if form_num in word_index_table.keys():
      word_list = word_index_table[form_num]
      for word in word_list:
        word_index = line.replace('-',' ').translate(translator).split(' ').index(word)
        if counter:
          counter_list.append(word_index)
        else:
          if (config.has_second_word < 1) or (word_index in counter_list[total_sents]):
            chv_search_form(word, pos, config, form_list, verbal=True)
  
def chv_search(config, show_first_sents=10):
  index_table = np.load(config.index_filename, allow_pickle='TRUE').item()
  word_index_table = np.load(config.word_index_filename, allow_pickle='TRUE').item()
  vocab_table = np.load(config.vocab_filename, allow_pickle='TRUE').item()
  sent_numbers = set()
  sent_numbers2 = set()
  word_sent_numbers = set()
  word_sent_numbers2 = set()
  translator = str.maketrans('', '', string.punctuation)
  all_form_list = sum(config.form_list.values(), [])
  all_form2_list = sum(config.form2_list.values(), [])
  wordform_list = chv_get_wordforms_from_lemma(config, all_form_list, config.wordform_list, config.is_lemma, vocab_table)
  wordform2_list = chv_get_wordforms_from_lemma(config, all_form2_list, config.wordform2_list, config.is_lemma2, vocab_table)
    
  if len(all_form_list) > 0 and len(wordform_list) == 0:
    print("первый список форм")
    for pos in config.pos_list:
      if len(config.form_list[pos]) > 0: print(config.form_list[pos])
  if len(all_form2_list) > 0 and len(wordform2_list) == 0:
    print("второй список форм")
    for pos in config.pos_list:
      if len(config.form2_list[pos]) > 0: print(config.form2_list[pos])
  for form in all_form_list:
    if form in index_table.keys():
      sent_numbers = sent_numbers.union(map(int, [row[0] for row in index_table[form]]))
  if len(wordform_list) > 0:
    print("первый список форм")
    print(wordform_list)
    for wordform in wordform_list:
      if wordform in vocab_table.keys():
        word_sent_numbers = word_sent_numbers.union(map(int, [row[0] for row in vocab_table[wordform]]))
    if len(all_form_list) > 0 and len(wordform_list) == 0:
      sent_numbers = sent_numbers.intersection(word_sent_numbers)
    else:
      sent_numbers = word_sent_numbers
  if config.has_second_word >= 1:
    for form2 in all_form2_list:
      if form2 in index_table.keys():
        sent_numbers2 = sent_numbers2.union(map(int, [row[0] for row in index_table[form2]]))
    if len(wordform2_list) > 0:
      print("второй список форм")
      print(wordform2_list)
      for wordform2 in wordform2_list:
        if wordform2 in vocab_table.keys():
          word_sent_numbers2 = word_sent_numbers2.union(map(int, [row[0] for row in vocab_table[wordform2]]))
      if len(all_form2_list) > 0 and len(wordform2_list) == 0:
        sent_numbers2 = sent_numbers2.intersection(word_sent_numbers2)
      else:
        sent_numbers2 = word_sent_numbers2    
    print("расстояние: %d" % config.has_second_word)
    sent_numbers = sent_numbers.intersection(sent_numbers2)
  sent_numbers = sorted(sent_numbers)
  
  with open(config.search_filename, encoding="utf-8") as search_file:
    total_sents = 0
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
          if len(all_form_list) > 0 and len(wordform_list) == 0:
            for pos in config.pos_list:
              chv_search_form_in_list(config.form_list[pos], config, total_sents, word_index_table, pos, line, True, counter1_list)
          if len(wordform_list) > 0:
            chv_search_wordform(wordform_list, config, total_sents, vocab_table, True, counter1_list)
          if len(all_form2_list) > 0 and len(wordform2_list) == 0:
            for pos in config.pos_list:
              chv_search_form_in_list(config.form2_list[pos], config, total_sents, word_index_table, pos, line, True, counter2_list)
          if len(wordform2_list) > 0:
            chv_search_wordform(wordform2_list, config, total_sents, vocab_table, True, counter2_list)
          #if (total_sents == 2):
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
      line_norm = fix_encoding_lower(line, False)
      if total_sents in dist_sent_numbers:
        if len(all_form_list) > 0 and len(wordform_list) == 0:
          for pos in config.pos_list:
            chv_search_form_in_list(config.form_list[pos], config, total_sents, word_index_table, pos, line_norm, False, dist_pair1)
        if len(wordform_list) > 0:
          chv_search_wordform(wordform_list, config, total_sents, vocab_table, False, dist_pair1)
        if config.has_second_word >= 1:
          if len(all_form2_list) > 0 and len(wordform2_list) == 0:
            for pos in config.pos_list:
              chv_search_form_in_list(config.form2_list[pos], config, total_sents, word_index_table, pos, line_norm, False, dist_pair2)
          if len(wordform2_list) > 0:
            chv_search_wordform(wordform2_list, config, total_sents, vocab_table, False, dist_pair2)
        print('%d:%s' % (total_sents, line))
  
def chv_create_search_index(config):
  found_sents = 0
  total_sents = 0
  translator = str.maketrans('', '', string.punctuation)
  vocab = {}
  cash_dict = {}
  index_dict = {}
  word_index_dict = {}
  with open(config.search_filename, encoding="utf-8") as search_file:
    for line in search_file:
      total_sents += 1
      form_found = False
      pos_form_found = {}
      chosen_pos_form_inf = {}
      line = fix_encoding_lower(line, False)
      words = line.replace('-',' ').translate(translator).split(' ')
      word_ind = 0
      for word in words:
        debug = word == "хыттӑн"
        if word not in cash_dict.keys():
          for pos in config.pos_list:
            pos_form_found[pos], chosen_pos_form_inf[pos] = chv_search_form(word, pos, config, config.form_list[pos])
          form_found = bool(sum(pos_form_found.values()))
          vocab[word] = [[str(total_sents), str(word_ind)]]
          cash_dict[word] = list(set((chosen_pos_form_inf.values())))
          if debug: print(cash_dict[word])
        else:
          form_found = True
          tmp = vocab[word]
          tmp.append([str(total_sents), str(word_ind)])
          vocab[word] = tmp        
        for chosen_form_inf in cash_dict[word]:
          chosen_form = chosen_form_inf[0]
          if chosen_form != '':
            if chosen_form in index_dict.keys():
              tmp = index_dict[chosen_form]
              tmp.append([str(total_sents), str(word_ind)])
              index_dict[chosen_form] = tmp
            else:
              index_dict[chosen_form] = [[str(total_sents), str(word_ind)]]
            chosen_form_num = chosen_form + str(total_sents)
            if chosen_form_num in word_index_dict.keys():
              tmp = word_index_dict[chosen_form_num]
              tmp.append(word)
              word_index_dict[chosen_form_num] = tmp
            else:
              word_index_dict[chosen_form_num] = [word]
        word_ind += 1
      if form_found:
        found_sents += 1
        print('%d из %d:%s' % (found_sents, total_sents, line))
    np.save(config.index_filename, index_dict)
    np.save(config.word_index_filename, word_index_dict)
    np.save(config.cash_filename, cash_dict)
    np.save(config.vocab_filename, vocab)

if __name__ == '__main__':
  show_first_sents = int(sys.argv[1])
  has_second_word = int(sys.argv[2])
  is_index = False
  config = Config(has_second_word, is_index)
  
  if is_index:
    chv_create_search_index(config)
  else:
    chv_search(config, show_first_sents)
    
  #добавить -лӑ/-лӗ/ -ллӑ/-ллӗ [Done]
  #Добавить все возможные варианты - кил [Done]
  #Добавить наречие -ӑн/-ӗн/-н типа сиввӗн
  #Лемма с гласной в конце хула или хул?