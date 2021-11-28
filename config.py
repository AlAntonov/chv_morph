import os

class Config:
  def __init__(self, has_second_word, is_index):
    pos_list = ['noun', 'adj', 'verb']
    self.pos_list = pos_list
    
    conj_filename = {}
    src_filename = {}
    trn_filename = {}
    for pos in pos_list:
      conj_filename[pos] = 'conj_%s_table.txt' % pos
      src_filename[pos] = 'andreev.chv_%s' % pos
      trn_filename[pos] = 'andreev.ru_%s' % pos
    config_filename = 'config.txt'
    if is_index:
      config_filename = 'config_all_base.txt'
    config2_filename = None
    if has_second_word >= 1:
      config2_filename = 'config2.txt'
    
    self.search_filename = 'chv.monocorpus.txt'
    self.index_filename = 'index.npy'
    self.word_index_filename = 'word_index.npy'
    self.cash_filename = 'cash_index.npy'
    self.vocab_filename = 'vocab_index.npy'
    self.has_second_word = has_second_word
  
    def chv_read_words_list(word_filename):
      words_list = []
      location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
      with open(os.path.join(location, word_filename), encoding="utf-8") as word_file:
        for line in word_file:
          words_list.append(line[:-1])
      return words_list

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
      
    def chv_get_form_from_verb_config(config_filename):
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
      padezh_list = ['im', 'ro', 'da', 'me', 'is', 'tv', 'li', 'pc', 'pr']
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
      
    def chv_get_form_from_adj_config(config_filename):
      form_list = []
      adj_form_list = ['im', 'na']
      with open(config_filename, encoding="utf-8") as config_file:
        for line in config_file:
          splitted_line = line.replace('\n','').split(':')
          if splitted_line[0] == 'Часть_речи':
            if 'aj' not in splitted_line[1].split(','):
              return form_list
          if splitted_line[0] == 'Форма':
            adj_form_list = splitted_line[1].split(',')
      for adj_form in adj_form_list:
        form_list.append(adj_form.strip())
      return form_list
      
    def chv_get_form_from_config(config_filename, pos):
      assert pos in pos_list
      
      if pos == "noun":
        return chv_get_form_from_noun_config(config_filename)
      elif pos == "adj":
        return chv_get_form_from_adj_config(config_filename)
      else:
        return chv_get_form_from_verb_config(config_filename)
    
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
    
    self.form_list = {}
    self.conj_table = {}
    self.conj_normal_table = {}
    self.src_list = {}
    self.trn_list = {}
    self.form2_list = {}
    for pos in pos_list:
      self.form_list[pos] = chv_get_form_from_config(config_filename, pos)
      self.conj_table[pos] = chv_read_conj_table(conj_filename[pos], True)
      self.conj_normal_table[pos] = chv_read_conj_table(conj_filename[pos], False)
      self.src_list[pos] = chv_read_words_list(src_filename[pos])
      self.trn_list[pos] = chv_read_words_list(trn_filename[pos])
      self.form2_list[pos] = []
      if has_second_word >= 1:
        self.form2_list[pos] = chv_get_form_from_config(config2_filename, pos)    
    self.wordform_list, self.is_lemma = chv_get_wordform_from_config(config_filename)
    self.wordform2_list = []
    self.is_lemma2 = False
    if has_second_word >= 1:
      self.wordform2_list, self.is_lemma2 = chv_get_wordform_from_config(config2_filename)
    
    self.pos_verbal = {}
    self.pos_verbal["noun"] = "существительное"
    self.pos_verbal["adj"] = "прилагательное"
    self.pos_verbal["verb"] = "глагол"