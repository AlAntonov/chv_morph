import os

class Config:
  def __init__(self, has_second_word, is_index):
    pos_list = ['noun', 'adj', 'verb']
    self.pos_list = pos_list
    
    rule_list = {}
    rule_list['noun'] = []
    rule_list['noun'].append(['h', 's'])
    rule_list['noun'].append(['e', 'm'])
    rule_list['noun'].append(['0','1', '2', '3'])
    rule_list['noun'].append(['im', 'ro', 'da', 'me', 'is', 'tv', 'li', 'pc', 'pr', 'hi', 'na'])
    rule_list['noun'].append(['vi', 'vj', 'mm', ''])
    rule_list['adj'] = []
    rule_list['adj'].append(['h', 's', 'y'])
    rule_list['adj'].append(['im', 'na', 'sr', 'vi', 'vj'])
    rule_list['adj'].append(['vi', 'vj', ''])
    rule_list['adj'].append(['im', 'ro', 'da', 'me', 'is', 'tv', 'li', 'pc', 'pr', 'hi', ''])
    rule_list['verb'] = []
    rule_list['verb'].append(['h', 's', 'y'])
    rule_list['verb'].append(['e', 'm'])
    rule_list['verb'].append(['1', '2', '3'])
    rule_list['verb'].append(['p', 'n'])
    rule_list['verb'].append(['nb', 'po', 'bb', 'ps', 'pd', 'im', 'in', 'pn', 'pb', 'pm', 'de', 'dx', 'du', 'dv'])
    rule_list['verb'].append(['vi', 'vj', 'pu', ''])
    rule_list['verb'].append(['im', 'ro', 'da', 'me', 'is', 'tv', 'li', 'pc', ''])
    
    conj_filename = {}
    src_filename = {}
    trn_filename = {}
    config_filename = {}
    config2_filename = {}
    for pos in pos_list:
      conj_filename[pos] = 'conj_%s_table.txt' % pos
      src_filename[pos] = 'andreev.chv_%s' % pos
      trn_filename[pos] = 'andreev.ru_%s' % pos
      config_filename[pos] = 'config.txt'
      #if is_index:
      #  config_filename[pos] = 'config_%s_base.txt' % pos
      config2_filename[pos] = None
      if has_second_word >= 1:
        config2_filename[pos] = 'config2.txt'
    conj_join_filename = 'conj_join.txt'
    
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

    def chv_read_conj_table(conj_filename, conj_join_filename, pos, reverse = False):
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
      
    def chv_add_conj_join(conj_table, reverse = False):      
      def add_to_join_tail(join_list, splitted_first, splitted_second, index, sum, first, second, join_str_list):
        for js in join_list[index]:
          new_first = ''
          if index >= (len(splitted_first) - 1):
            new_first = first
          elif splitted_first[index+1] == '*':
            new_first = first + '_' + js
          elif splitted_first[index+1] == '-':
            new_first = first
          else:
            new_first = first + '_' + splitted_first[index+1]
          new_second = ''
          if index >= (len(splitted_second) - 1):
            new_second = second
          elif splitted_second[index+1] == '*':
            new_second = second + '_' + js
          elif splitted_second[index+1] == '-':
            new_second = second
          else:
            new_second = second + '_' + splitted_second[index+1]
          if index < (len(join_list) - 1):
            add_to_join_tail(join_list, splitted_first, splitted_second, index + 1, sum + '_' + js, new_first, new_second, join_str_list)
          else:
            join_str_list.append([sum + '_' + js, new_first, new_second])
        return join_str_list
        
      location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
      with open(os.path.join(location, conj_join_filename), encoding="utf-8") as conj_join_file:
        for line in conj_join_file:
          join_list = []
          join_list_first = []
          join_list_second = []
          splitted_line = line.strip().split(':')
          assert len(splitted_line) == 3
          splitted_sum = splitted_line[0].split('_')
          splitted_first = splitted_line[1].split('_')
          splitted_second = splitted_line[2].split('_')
          for i in range(1,len(splitted_sum)):
            if splitted_sum[i] == '*':
              join_list.append([v for v in rule_list[splitted_sum[0]][i-1] if v != ''])
            else:
              join_list.append([splitted_sum[i]])
          join_str_list = []
          add_to_join_tail(join_list, splitted_first, splitted_second, 0, splitted_sum[0], splitted_first[0], splitted_second[0], join_str_list)
          for join_str in join_str_list:
            s_sum = join_str[0].split('_')
            s_first = join_str[1].split('_')
            s_second = join_str[2].split('_')
            conj_table[s_sum[0]][join_str[0].replace("%s_" % s_sum[0],"")] = conj_table[s_first[0]][join_str[1].replace("%s_" % s_first[0],"")] + conj_table[s_second[0]][join_str[2].replace("%s_" % s_second[0],"")]
      
      inv_dict = {}
      for pos in pos_list:
        inv_dict[pos] = {v: k for k, v in conj_table[pos].items()}
      
      return conj_table, inv_dict
    
    def add_to_tail(pos_form_list, i, form, form_list):
      for pos_form_i in pos_form_list[i]:
        if i < len(pos_form_list) - 1:
          add_to_tail(pos_form_list, i+1, form + "_" + pos_form_i.strip(), form_list)
        else:
          app_form = form + "_" + pos_form_i.strip()
          form_list.append(app_form.strip('_'))
            
    def chv_get_form_from_verb_config(config_filename):
      form_list = []
      pos = 'verb'
      chislo_list = rule_list[pos][1]
      lico_list = rule_list[pos][2]
      negative_list = rule_list[pos][3]
      verb_form_list = [rule_list[pos][4]]
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
            verb_form_list = []
            for i in range(len(splitted_line[1].split(','))):
              verb_form_list.append(splitted_line[1].split(',')[i].split('|'))
      for chislo in chislo_list:
        for lico in lico_list:
          for negative in negative_list:
            form = chislo.strip() + '_' + lico.strip() + '_' + negative.strip()
            add_to_tail(verb_form_list, 0, form, form_list)          
      return form_list

    def chv_get_form_from_noun_config(config_filename):
      form_list = []
      pos = 'noun'
      chislo_list = rule_list[pos][1]
      lico_list = rule_list[pos][2]
      noun_form_list = [rule_list[pos][3]]
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
          if splitted_line[0] == 'Форма':
            noun_form_list = []
            for i in range(len(splitted_line[1].split(','))):
              noun_form_list.append(splitted_line[1].split(',')[i].split('|'))
      for chislo in chislo_list:
        for lico in lico_list:
          form = '_' + chislo.strip() + '_' + lico.strip()
          add_to_tail(noun_form_list, 0, form, form_list)
      return form_list
      
    def chv_get_form_from_adj_config(config_filename):            
      form_list = []
      pos = 'adj'
      adj_form_list = [rule_list[pos][1]]
      with open(config_filename, encoding="utf-8") as config_file:
        for line in config_file:
          splitted_line = line.replace('\n','').split(':')
          if splitted_line[0] == 'Часть_речи':
            if 'aj' not in splitted_line[1].split(','):
              return form_list
          if splitted_line[0] == 'Форма':
            adj_form_list = []
            for i in range(len(splitted_line[1].split(','))):
              adj_form_list.append(splitted_line[1].split(',')[i].split('|'))
      add_to_tail(adj_form_list, 0, "", form_list)
      return form_list
      
    def chv_get_form_from_config(config_filename, pos):
      assert pos in pos_list
      
      if pos == 'noun':
        return chv_get_form_from_noun_config(config_filename)
      elif pos == 'adj':
        return chv_get_form_from_adj_config(config_filename)
      else:
        return chv_get_form_from_verb_config(config_filename)
    
    def chv_get_form_from_rule_list(rule_list, pos):
      form_list = []
      add_to_tail(rule_list[pos][1:], 0, "", form_list)
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
    
    self.form_list = {}
    self.conj_table = {}
    self.conj_normal_table = {}
    self.src_list = {}
    self.trn_list = {}
    self.form2_list = {}
    for pos in pos_list:
      if is_index:
        self.form_list[pos] = chv_get_form_from_rule_list(rule_list, pos)
      else:
        self.form_list[pos] = chv_get_form_from_config(config_filename[pos], pos)
      self.conj_table[pos] = chv_read_conj_table(conj_filename[pos], conj_join_filename, pos, True)
      self.conj_normal_table[pos] = chv_read_conj_table(conj_filename[pos], conj_join_filename, pos, False)
      self.src_list[pos] = chv_read_words_list(src_filename[pos])
      self.trn_list[pos] = chv_read_words_list(trn_filename[pos])
      self.form2_list[pos] = []
      if has_second_word >= 1:
        self.form2_list[pos] = chv_get_form_from_config(config2_filename[pos], pos)
    self.conj_normal_table, self.conj_table = chv_add_conj_join(self.conj_normal_table)
    self.wordform_list, self.is_lemma = chv_get_wordform_from_config(config_filename["verb"])
    self.wordform2_list = []
    self.is_lemma2 = False
    if has_second_word >= 1:
      self.wordform2_list, self.is_lemma2 = chv_get_wordform_from_config(config2_filename["verb"])
    
    self.pos_verbal = {}
    self.pos_verbal["noun"] = "существительное"
    self.pos_verbal["adj"] = "прилагательное"
    self.pos_verbal["verb"] = "глагол"