import os

class Config:
  def __init__(self, has_second_word, is_index):
    conj_noun_filename = 'conj_noun_table.txt'
    conj_verb_filename = 'conj_table.txt'
    noun_filename = 'andreev.chv_noun'
    trn_noun_filename = 'andreev.ru_noun'
    verb_filename = 'andreev.chv_verb'
    trn_verb_filename = 'andreev.ru_verb'
    config_filename = 'config.txt'
    if is_index:
      config_filename = 'config_all_base.txt'
    config2_filename = None
    if has_second_word >= 1:
      config2_filename = 'config2.txt'
    
    self.search_filename = 'chv.100K.monocorpus.txt'
    self.index_filename = 'index.npy'
    self.verb_index_filename = 'verb_index.npy'
    self.cash_filename = 'cash_index.npy'
    self.vocab_filename = 'vocab_index.npy'
    self.has_second_word = has_second_word
  
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
              form_list.append(chislo.strip() + '_' + lico.strip() + '_' + negative.strip() + '_' + verb_form.strip())
      return form_list

    def chv_get_form_from_noun_config(config_filename):
      form_list = []
      chislo_list = ['e', 'm']
      lico_list = ['0','1', '2', '3']
      padezh_list = ['im', 'ro', 'da', 'me', 'is', 'tv', 'li', 'pc']
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
            form_list.append(chislo.strip() + '_' + lico.strip() + '_' + padezh.strip())
      return form_list
    
    def chv_get_wordform_from_config(config_filename):
      wordform_list = []
      is_lemma = False
      with open(config_filename, encoding="utf-8") as config_file:
        for line in config_file:
          splitted_line = line.replace('\n','').split(':')
          if splitted_line[0] == 'Словоформа':
            wordform_list = splitted_line[1].split(',')
          if splitted_line[0] == 'Лемма':
            wordform_list = splitted_line[1].split(',')
            is_lemma = True
      return wordform_list, is_lemma
    

    self.form_verb_list = chv_get_form_from_config(config_filename)
    self.form_noun_list = chv_get_form_from_noun_config(config_filename)
    self.wordform_list, self.is_lemma = chv_get_wordform_from_config(config_filename)
    self.conj_verb_table = chv_read_conj_table(conj_verb_filename, True)
    self.conj_noun_table = chv_read_conj_table(conj_noun_filename, True)
    self.conj_verb_normal_table = chv_read_conj_table(conj_verb_filename, False)
    self.conj_noun_normal_table = chv_read_conj_table(conj_noun_filename, False)
    self.verbs_list = chv_read_verbs_list(verb_filename)
    self.trn_verbs_list = chv_read_verbs_list(trn_verb_filename)
    self.nouns_list = chv_read_verbs_list(noun_filename)
    self.trn_nouns_list = chv_read_verbs_list(trn_noun_filename)
    self.form2_verb_list = []
    self.form2_noun_list = []
    self.wordform2_list = []
    self.is_lemma2 = False
    if has_second_word >= 1:
      self.form2_verb_list = chv_get_form_from_config(config2_filename)
      self.form2_noun_list = chv_get_form_from_noun_config(config2_filename)
      self.wordform2_list, self.is_lemma2 = chv_get_wordform_from_config(config2_filename)