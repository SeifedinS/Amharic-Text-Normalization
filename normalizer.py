import sys 

# mukera 123
import codecs
import re
import  num_generator as ng
# print(ng.get_number_as_words(23))

data = codecs.open('2007.txt','r','utf-8').read()
acry_data = codecs.open('acrym','r','utf-8').read()
abr_data = codecs.open('abn','r','utf-8').read()
chars_list = codecs.open('ordinal','r','utf-8').read().splitlines()
mon_symb = codecs.open('money','r','utf-8').read().splitlines()
year_symb = codecs.open('year','r','utf-8').read().splitlines()
punct = codecs.open('punct','r','utf-8').read().splitlines()
dict_list =[]
acr_dic = {}
abr_dic = {}
for line in acry_data.splitlines():
	acr_dic[line.split()[0]] = ' '.join(line.split()[1:])
# print acr_dic
# for k,v in acr_dic.items():
# 	print k
# 	print v
for line in abr_data.splitlines():
	abr_dic[line.split()[0]] = ' '.join(line.split()[1:])

def abr_separate(word,dic):
	for k,v in dic.items():
		if k in word:
			return k

def num_separate(word):
	num_part = ''
	ind1 = re.search("\d", word)
	for i in range(ind1.start(),len(word)):
		if word[i].isdigit():
			num_part +=word[i]
		else:
			break
	return num_part

def tagger(data):
	tagged_sent = '"sentence_id","token_id","class","before","after" \n'
	data_line = data.splitlines()
	for i in range(len(data_line)):
		word_list = data_line[i].split()
		for j in range(len(word_list)):
			tagged_sent += str(i) + ','
			word = word_list[j]
			clas= ''
			tagged_sent += str(j) + ','
			if is_abr(word):
				clas = 'ABR'
			elif is_accr(word):
				clas= 'ACCRON'
			elif is_money(word):
				clas += 'MONEY'
			elif is_ordinal(word):
				clas = 'ORDINAL'
			elif is_year(word):
				clas = 'YEAR'
			elif is_time(word):
				clas = 'TIME'
			elif is_range(word):
				clas = 'RANGE'
			elif is_teleph(word):
				clas = 'PHONE'
			elif is_cardinal(word):
				clas = 'CARDINAL'
			elif is_date(word):
				clas = 'DATE'
			elif is_punct(word):
				clas = 'PUNCT'
			else:
				clas = 'PLAIN'
			tagged_sent +=  '\"' + clas + '\"'
			tagged_sent += ','+ '\"'  + word+ '\"'
			print(word)
			if clas == 'PLAIN':
				tagged_sent += ',' + '\"'+ word + '\"'+ '\n'
			elif clas == 'CARDINAL':
				num_part = num_separate(word)
				text_part = word.replace(num_part,'')
				word =word.strip()
				tagged_sent += ',' +'\"'+ str(ng.get_number_as_words(int(num_part))) + '\"'+text_part + '\n'
			elif clas == 'ORDINAL':
				num_part = num_separate(word)
				text_part = word.replace(num_part,'')
				new_word = ''
				if word[0].isdigit():
					if num_part.isdigit():
						new_word = str(ng.get_number_as_words(int(num_part))) + text_part
				else:
					new_word = text_part + str(ng.get_number_as_words(int(num_part)))

				tagged_sent +=',' +'\"'+ new_word + '\"'+ '\n'
			elif clas == 'ACCRON':
				new_word = ''
				acr_part = abr_separate(word,acr_dic)
				# print acr_part
				text_part = word.replace(acr_part,'')
				if text_part is None:
					tagged_sent += ',' +'\"' + acr_dic[acr_part]+ '\"'+ '\n'
				else:
					tagged_sent += ',' +'\"'+ text_part + acr_dic[acr_part]+ '\"' + '\n'
			elif clas == 'ABR':
				new_word = ''
				abr_part = abr_separate(word,abr_dic)
				# print abr_part
				if abr_part is None:
					text_part = ''
					tagged_sent += ',' +  '\"' + clas + '\"' + '\n'
				else:
					text_part = word.replace(abr_part,'')
					tagged_sent += ','  + '\"' + text_part + abr_dic[abr_part] + '\"'+ '\n'
			else:
				tagged_sent += ',' +  '\"' + word + '\"' +'\n'


	write_to_file(tagged_sent)

def is_abr(word):
	if '.' in word and not(has_number(word)):
		return True
	elif '/' in word and not(has_number(word)):
		return True
	else:
		return False

def is_accr(word):
	word = word.strip()
	stat = False
	for k,v in acr_dic.items():
		if k in word:
			stat = True
	if stat:
		return True
	else :
		return False

def is_cardinal(word):
	#Quantity
	#Number only # Decimal
	if word.isdigit() or (bool(re.search(r'\d',word))):
		return True
	else:
		return False

def is_ordinal(word):
	stat = False
	# Posiion
	# Contains [be,ke,le,tegna] as prefix or postfix
	for char in chars_list:
		if (char in word) and (has_number(word)) and (':' not in word):
			stat = True
			break
	if stat:
		return True
	else:
		return False

def is_money(word):
	# Contain $,ETB,birr,Pound,euro
	stat = False
	for mon in mon_symb:
		if mon in word:
			stat = True
	if stat:
		return True
	else:
		return False

def is_time(word):
	# return bool(time_re.match(word))
	# Contain :,use reg-exp
	symb = chars_list[:3]
	if ':' in word and has_number(word):
		for char in symb:
			if char in word:
				return True
	else:
		return False
	return False

def is_year(word):
	# Num and slash only or a.m use reg-exp
	if has_number(word):
		for yr in year_symb:
			if yr in word:
				return True
			else:
				return False
	else:
		return False

def is_date(word):
	# Num and slash only or a.m use reg-exp
	match = re.search(r'(\d+/\d+/\d+)',word)
	if match == None:
		return False
	else:
		return True

def is_range(word):
	# Use reg-expr
	if ('-' in word) and (has_number(word)):
		return True
	else:
		return False

def is_punct(word):
	for char in punct:
		if char in word:
			return True
	return False

def is_teleph(word):
	# 011, +251, 0 and 10 digits are the code of telephone number
	if (word[0] ==0) and ('251' in word) and (len(word)==10):
		return True
	else:
		return False


def has_number(word):
	return bool(re.search(r'\d',word))

def write_to_file(cont):
	file_ = 'tagged_data'
	fo = codecs.open(file_,'w','utf-8')
	fo.write(cont)
	print('Data written to %s ' % (file_))
	fo.close()


if __name__ == '__main__':
	new_cont = ''
	print('Total number of sentence %d ' % (len(data.splitlines())))
	for line in acry_data.splitlines():
		dict_list.append(line.split()[0])
	# test= '7' + chars_list[3]
	# print test
	# print is_ordinal(test)
	tagger(data)
