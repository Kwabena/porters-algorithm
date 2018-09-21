# Implementation of Porter's algorithm as presented in the final paper 
# reproduced at https://tartarus.org/martin/PorterStemmer/def.txt
# Author: Kwabena Antwi-Boasiako
# June 2017

# Step 1a
# SSES -> SS                         caresses  ->  caress
# IES  -> I                          ponies    ->  poni
#                                    ties      ->  ti
# SS   -> SS                         caress    ->  caress
# S    ->                            cats      ->  cat	
def step1a(string):
	if string[-4:] == 'sses':
		result = string[:-4] + 'ss'
	elif string[-3:] == 'ies':
		result = string[:-3] + 'i'
	elif string[-2:] == 'ss':
		result = string
	elif string[-1:] == 's':
		result = string[:-1]
	else:
		result = string

	return result

# Basic test for step1a()
def step1a_test():
	string_pairs = [('caresses', 'caress'), ('ponies', 'poni'), ('ties', 'ti'), 
					('caress', 'caress'), ('cats', 'cat')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step1a, inputs))
	if expected_outputs == outputs:
		print("step1a_test() passed")
	else:
		print("step1a_test() failed")

# Step 1b
# (m>0) EED -> EE                    feed      ->  feed
#                                    agreed    ->  agree
# (*v*) ED  ->                       plastered ->  plaster
#                                    bled      ->  bled
# (*v*) ING ->                       motoring  ->  motor
#                                    sing      ->  sing

# If the second or third of the rules in Step 1b is successful, the following
# is done:
# AT -> ATE                       conflat(ed)  ->  conflate
# BL -> BLE                       troubl(ed)   ->  trouble
# IZ -> IZE                       siz(ed)      ->  size
# (*d and not (*L or *S or *Z))
#    -> single letter
#                                 hopp(ing)    ->  hop
#                                 tann(ed)     ->  tan
#                                 fall(ing)    ->  fall
#                                 hiss(ing)    ->  hiss
#                                 fizz(ed)     ->  fizz
#      (m=1 and *o) -> E          fail(ing)    ->  fail
#                                 fil(ing)     ->  file

# The rule to map to a single letter causes the removal of one of the double
# letter pair. The -E is put back on -AT, -BL and -IZ, so that the suffixes
# -ATE, -BLE and -IZE can be recognised later. This E may be removed in step
# 4.
# Meanings of symbols:
# *S  - the stem ends with S (and similarly for the other letters).
# *v* - the stem contains a vowel.
# *d  - the stem ends with a double consonant (e.g. -TT, -SS).
# *o  - the stem ends cvc, where the second c is not W, X or Y (e.g.
       # -WIL, -HOP).
def step1b(string):
	rule2_or_rule3_successful = False
	if string[-3:] == 'eed': 
		if measure(string[:-3]) > 0:
			result = string[:-3] + 'ee'
		else:
			result = string
	elif string[-2:] == 'ed':
		if True in list(map(lambda i: vowel(string[:-2], i), range(len(string[:-2])))):
			result = string[:-2]
			rule2_or_rule3_successful = True
		else:
			result = string
	elif string[-3:] == 'ing':
		if True in list(map(lambda i: vowel(string[:-3], i), range(len(string[:-3])))):
			result = string[:-3]
			rule2_or_rule3_successful = True
		else:
			result = string
	else:
		result = string
		
	if rule2_or_rule3_successful:
		if result[-2:] == 'at':
			result = result[:-2] + 'ate'
		elif result[-2:] == 'bl':
			result = result[:-2] + 'ble'
		elif result[-2:] == 'iz':
			result = result[:-2] + 'ize'
		elif not vowel(result, len(result) - 1) and result[-1] == result[-2] and result[-1] not in 'lsz':
			result = result[:-1]
		elif measure(result) == 1 and not vowel(result, len(result) - 3) and \
		vowel(result, len(result) - 2) and not vowel(result, len(result) - 1) and result[-1] not in 'wxy':
			result += 'e'
		else:
			pass

	return result

# Basic test for step1b()
def step1b_test():
	string_pairs = \
	[('feed', 'feed'), ('agreed', 'agree'), ('plastered', 'plaster'), 
	('bled', 'bled'), ('motoring', 'motor'), ('sing', 'sing'), 
	('conflated', 'conflate'), ('troubled', 'trouble'), ('sized', 'size'), 
	('hopping', 'hop'), ('tanned', 'tan'), ('falling', 'fall'), ('hissing', 'hiss'), 
	('fizzed', 'fizz'), ('failing', 'fail'), ('filing', 'file')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step1b, inputs))
	if expected_outputs == outputs:
		print("step1b_test() passed")
	else:
		print("step1b_test() failed")
		print(expected_outputs)
		print(outputs)

# Step 1c
# (*v*) Y -> I                    happy        ->  happi
#                                 sky          ->  sky
# Step 1 deals with plurals and past participles. The subsequent steps are
# much more straightforward.
def step1c(string):
	if string[-1:] == 'y' and any(list(map(lambda i: vowel(string[:-1], i), range(len(string[:-1]))))):
		result = string[:-1] + 'i'
	else:
		result = string
		
	return result

# Basic test for step1c()
def step1c_test():
	string_pairs = [('happy', 'happi'), ('sky', 'sky'), ('ay', 'ai'), ('y', 'y'), ('', '')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step1c, inputs))
	if expected_outputs == outputs:
		print("step1c_test() passed")
	else:
		print("step1c_test() failed")
		print(expected_outputs)
		print(outputs)

# Step 2
# (m>0) ATIONAL ->  ATE           relational     ->  relate
# (m>0) TIONAL  ->  TION          conditional    ->  condition
#                                 rational       ->  rational
# (m>0) ENCI    ->  ENCE          valenci        ->  valence
# (m>0) ANCI    ->  ANCE          hesitanci      ->  hesitance
# (m>0) IZER    ->  IZE           digitizer      ->  digitize
# (m>0) ABLI    ->  ABLE          conformabli    ->  conformable
# (m>0) ALLI    ->  AL            radicalli      ->  radical
# (m>0) ENTLI   ->  ENT           differentli    ->  different
# (m>0) ELI     ->  E             vileli        - >  vile
# (m>0) OUSLI   ->  OUS           analogousli    ->  analogous
# (m>0) IZATION ->  IZE           vietnamization ->  vietnamize
# (m>0) ATION   ->  ATE           predication    ->  predicate
# (m>0) ATOR    ->  ATE           operator       ->  operate
# (m>0) ALISM   ->  AL            feudalism      ->  feudal
# (m>0) IVENESS ->  IVE           decisiveness   ->  decisive
# (m>0) FULNESS ->  FUL           hopefulness    ->  hopeful
# (m>0) OUSNESS ->  OUS           callousness    ->  callous
# (m>0) ALITI   ->  AL            formaliti      ->  formal
# (m>0) IVITI   ->  IVE           sensitiviti    ->  sensitive
# (m>0) BILITI  ->  BLE           sensibiliti    ->  sensible
def step2(string):
	if string[-7:] == 'ational':
		if measure(string[:-7]) > 0:
			result = string[:-7] + 'ate'
		else:
			result = string
	elif string[-6:] == 'tional' and measure(string[:-6]) > 0:
		result = string[:-6] + 'tion'
	elif string[-4:] == 'enci' and measure(string[:-4]) > 0:
		result = string[:-4] + 'ence'
	elif string[-4:] == 'anci' and measure(string[:-4]) > 0:
		result = string[:-4] + 'ance'
	elif string[-4:] == 'izer' and measure(string[:-4]) > 0:
		result = string[:-4] + 'ize'
	elif string[-4:] == 'abli' and measure(string[:-4]) > 0:
		result = string[:-4] + 'able'
	elif string[-4:] == 'alli' and measure(string[:-4]) > 0:
		result = string[:-4] + 'al'
	elif string[-5:] == 'entli' and measure(string[:-5]) > 0:
		result = string[:-5] + 'ent'
	elif string[-3:] == 'eli' and measure(string[:-3]) > 0:
		result = string[:-3] + 'e'
	elif string[-5:] == 'ousli' and measure(string[:-5]) > 0:
		result = string[:-5] + 'ous'
	elif string[-7:] == 'ization' and measure(string[:-7]) > 0:
		result = string[:-7] + 'ize'
	elif string[-5:] == 'ation' and measure(string[:-5]) > 0:
		result = string[:-5] + 'ate'
	elif string[-4:] == 'ator' and measure(string[:-4]) > 0:
		result = string[:-4] + 'ate'
	elif string[-5:] == 'alism' and measure(string[:-5]) > 0:
		result = string[:-5] + 'al'
	elif string[-7:] == 'iveness' and measure(string[:-7]) > 0:
		result = string[:-7] + 'ive'
	elif string[-7:] == 'fulness' and measure(string[:-7]) > 0:
		result = string[:-7] + 'ful'
	elif string[-7:] == 'ousness' and measure(string[:-7]) > 0:
		result = string[:-7] + 'ous'
	elif string[-5:] == 'aliti' and measure(string[:-5]) > 0:
		result = string[:-5] + 'al'
	elif string[-5:] == 'iviti' and measure(string[:-5]) > 0:
		result = string[:-5] + 'ive'
	elif string[-6:] == 'biliti' and measure(string[:-6]) > 0:
		result = string[:-6] + 'ble'
	else:
		result = string

	return result

# Basic test for step2()
def step2_test():
	string_pairs = [('relational', 'relate'), ('conditional', 'condition'), 
	('rational', 'rational'), ('valenci', 'valence'), ('hesitanci', 'hesitance'),
	('digitizer', 'digitize'), ('conformabli', 'conformable'), 
	('radicalli', 'radical'), ('differentli', 'different'), ('vileli', 'vile'),
	('analogousli', 'analogous'), ('vietnamization', 'vietnamize'), 
	('predication', 'predicate'), ('operator', 'operate'), ('feudalism', 'feudal'), 
	('decisiveness', 'decisive'), ('hopefulness', 'hopeful'), 
	('callousness', 'callous'), ('formaliti', 'formal'), 
	('sensitiviti', 'sensitive'), ('sensibiliti', 'sensible')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step2, inputs))
	if expected_outputs == outputs:
		print("step2_test() passed")
	else:
		print("step2_test() failed")
		print(expected_outputs)
		print(outputs)

# Step 3
# (m>0) ICATE ->  IC              triplicate     ->  triplic
# (m>0) ATIVE ->                  formative      ->  form
# (m>0) ALIZE ->  AL              formalize      ->  formal
# (m>0) ICITI ->  IC              electriciti    ->  electric
# (m>0) ICAL  ->  IC              electrical     ->  electric
# (m>0) FUL   ->                  hopeful        ->  hope
# (m>0) NESS  ->                  goodness       ->  good
def step3(string):
	if string[-5:] == 'icate' and measure(string[:-5]) > 0:
		result = string[:-5] + 'ic'
	elif string[-5:] == 'ative' and measure(string[:-5]) > 0:
		result = string[:-5]
	elif string[-5:] == 'alize' and measure(string[:-5]) > 0:
		result = string[:-5] + 'al'
	elif string[-5:] == 'iciti' and measure(string[:-5]) > 0:
		result = string[:-5] + 'ic'
	elif string[-4:] == 'ical' and measure(string[:-4]) > 0:
		result = string[:-4] + 'ic'
	elif string[-3:] == 'ful' and measure(string[:-3]) > 0:
		result = string[:-3]
	elif string[-4:] == 'ness' and measure(string[:-4]) > 0:
		result = string[:-4]
	else:
		result = string
	
	return result

# Basic test for step3()
def step3_test():
	string_pairs = [('triplicate', 'triplic'), ('formative', 'form'), 
	('formalize', 'formal'), ('electriciti', 'electric'), 
	('electrical', 'electric'), ('hopeful', 'hope'), ('goodness', 'good')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step3, inputs))
	if expected_outputs == outputs:
		print("step3_test() passed")
	else:
		print("step3_test() failed")
		print(expected_outputs)
		print(outputs)

# Step 4
# (m>1) AL    ->                  revival        ->  reviv
# (m>1) ANCE  ->                  allowance      ->  allow
# (m>1) ENCE  ->                  inference      ->  infer
# (m>1) ER    ->                  airliner       ->  airlin
# (m>1) IC    ->                  gyroscopic     ->  gyroscop
# (m>1) ABLE  ->                  adjustable     ->  adjust
# (m>1) IBLE  ->                  defensible     ->  defens
# (m>1) ANT   ->                  irritant       ->  irrit
# (m>1) EMENT ->                  replacement    ->  replac
# (m>1) MENT  ->                  adjustment     ->  adjust
# (m>1) ENT   ->                  dependent      ->  depend
# (m>1 and (*S or *T)) ION ->     adoption       ->  adopt
# (m>1) OU    ->                  homologou      ->  homolog
# (m>1) ISM   ->                  communism      ->  commun
# (m>1) ATE   ->                  activate       ->  activ
# (m>1) ITI   ->                  angulariti     ->  angular
# (m>1) OUS   ->                  homologous     ->  homolog
# (m>1) IVE   ->                  effective      ->  effect
# (m>1) IZE   ->                  bowdlerize     ->  bowdler
def step4(string):
	if string[-2:] == 'al' and measure(string[:-2]) > 1:
		result = string[:-2]
	elif string[-4:] == 'ance' and measure(string[:-4]) > 1:
		result = string[:-4]
	elif string[-4:] == 'ence' and measure(string[:-4]) > 1:
		result = string[:-4]
	elif string[-2:] == 'er' and measure(string[:-2]) > 1:
		result = string[:-2]
	elif string[-2:] == 'ic' and measure(string[:-2]) > 1:
		result = string[:-2]
	elif string[-4:] == 'able' and measure(string[:-4]) > 1:
		result = string[:-4]
	elif string[-4:] == 'ible' and measure(string[:-4]) > 1:
		result = string[:-4]
	elif string[-3:] == 'ant' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-5:] == 'ement' and measure(string[:-5]) > 1:
		result = string[:-5]
	elif string[-4:] == 'ment' and measure(string[:-4]) > 1:
		result = string[:-4]
	elif string[-3:] == 'ent' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-3:] == 'ion' and string[-4] in 'st' and measure(string[:-4]) > 1:
		result = string[:-3]
	elif string[-2:] == 'ou' and measure(string[:-2]) > 1:
		result = string[:-2]
	elif string[-3:] == 'ism' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-3:] == 'ate' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-3:] == 'iti' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-3:] == 'ous' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-3:] == 'ive' and measure(string[:-3]) > 1:
		result = string[:-3]
	elif string[-3:] == 'ize' and measure(string[:-3]) > 1:
		result = string[:-3]
	else:
		result = string
		
	return result

# Basic test for step4()
def step4_test():
	string_pairs = [('revival', 'reviv'), ('allowance', 'allow'), 
	('inference', 'infer'), ('airliner', 'airlin'), ('gyroscopic', 'gyroscop'),
	('adjustable', 'adjust'), ('defensible', 'defens'), ('irritant', 'irrit'),
	('replacement', 'replac'), ('adjustment', 'adjust'), 
	('dependent', 'depend'), ('adoption', 'adopt'), ('homologou', 'homolog'), 
	('communism', 'commun'), ('activate', 'activ'), ('angulariti', 'angular'),
	('homologous', 'homolog'), ('effective', 'effect'), ('bowdlerize', 'bowdler')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step4, inputs))
	if expected_outputs == outputs:
		print("step4_test() passed")
	else:
		print("step4_test() failed")
		print(expected_outputs)
		print(outputs)

# Step 5a
# (m>1) E     ->                  probate        ->  probat
#                                 rate           ->  rate
# (m=1 and not *o) E ->           cease          ->  ceas
def step5a(string):
	length = len(string)
	if string[-1:] == 'e' and measure(string[:-1]) > 1:
		result = string[:-1]
	elif length >= 4 and string[-1:] == 'e' and measure(string[:-1]) == 1 and not (not vowel(string[:-1], len(string[:-1]) - 3) and	vowel(string[:-1], len(string[:-1]) - 2) and not vowel(string[:-1], len(string[:-1]) - 1) and string[-2:-1] not in 'wxy'):
		result = string[:-1]
	else:
		result = string

	return result

# Basic test for step5a()
def step5a_test():
	string_pairs = [('probate', 'probat'), ('rate', 'rate'), ('cease', 'ceas')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step5a, inputs))
	if expected_outputs == outputs:
		print("step5a_test() passed")
	else:
		print("step5a_test() failed")
		print(expected_outputs)
		print(outputs)


# Step 5b
# (m > 1 and *d and *L) -> single letter
#                                 controll       ->  control
#                                 roll           ->  roll
def step5b(string):
	if measure(string) > 1 and string[-2:] == 'll':
		result = string[:-1]
	else:
		result = string

	return result

def step5b_test():
	string_pairs = [('controll', 'control'), ('roll', 'roll')]
	inputs = [a for (a, b) in string_pairs]
	expected_outputs = [b for (a, b) in string_pairs]
	outputs = list(map(step5b, inputs))
	if expected_outputs == outputs:
		print("step5b_test() passed")
	else:
		print("step5b_test() failed")
		print(expected_outputs)
		print(outputs)

# Given a string, return its measure, m, as defined in the paper cited above.
# A \consonant\ in a word is a letter other than A, E, I, O or U, and other
# than Y preceded by a consonant. (The fact that the term `consonant' is
# defined to some extent in terms of itself does not make it ambiguous.) So in
# TOY the consonants are T and Y, and in SYZYGY they are S, Z and G. If a
# letter is not a consonant it is a \vowel\.

# A consonant will be denoted by c, a vowel by v. A list ccc... of length
# greater than 0 will be denoted by C, and a list vvv... of length greater
# than 0 will be denoted by V. Any word, or part of a word, therefore has one
# of the four forms:

    # CVCV ... C
    # CVCV ... V
    # VCVC ... C
    # VCVC ... V

# These may all be represented by the single form

    # [C]VCVC ... [V]

# where the square brackets denote arbitrary presence of their contents.
# Using (VC){m} to denote VC repeated m times, this may again be written as

    # [C](VC){m}[V].

# m will be called the \measure\ of any word or word part when represented in
# this form. The case m = 0 covers the null word. Here are some examples:

# m=0    TR,  EE,  TREE,  Y,  BY.
# m=1    TROUBLE,  OATS,  TREES,  IVY.
# m=2    TROUBLES,  PRIVATE,  OATEN,  ORRERY.
def measure(string):
	i = 0
	length = len(string)
	# Read as many consonants as possible
	while i < length and not vowel(string, i):
		i += 1
	# We either hit the first vowel or the entire string is composed of consonants or the string is empty
	if i == length:
		return 0
	else:
		# Read as many vowels as possible
		while i < length and vowel(string, i):
			i += 1
		if i == length:
			return 0
		else:
			# Read as many consonants as possible
			while i < length and not vowel(string, i):
				i += 1
			return 1 + measure(string[i:])

def measure_test():
	pairs = [('tr', 0), ('ee', 0), ('tree', 0), ('y', 0), ('by', 0), 
	('trouble', 1), ('oats', 1), ('trees', 1), ('ivy', 1), ('ant', 1),  
	('troubles', 2), ('private', 2), ('oaten', 2), ('orrery', 2), ('', 0), ('a', 0)]
	inputs = [a for (a, b) in pairs]
	expected_outputs = [b for (a, b) in pairs]
	outputs = list(map(measure, inputs))
	if expected_outputs == outputs:
		print("measure_test() passed")
	else:
		print("measure_test() failed")

# Given a string and the position of a character, return true if the character 
# is a vowel and false otherwise. A vowel is any of the characters A, E, I, O, 
# U and Y if it is preceded by a non-vowel (aka consonant)
def vowel(string, position):
	if string[position] in 'aeiou':
		return True
	elif string[position] == 'y' and position > 0 and string[position - 1] not in 'aeiou':
		return True
	else:
		return False

def vowel_test():
	triples = [('toy', 0, False), ('toy', 1, True), ('toy', 2, False), 
	('syzygy', 0, False), ('syzygy', 1, True), ('syzygy', 3, True), 
	('syzygy', 5, True), ('y', 0, False), ('by', 1, True), ('a', 0, True), 
	('b', 0, False)]
	inputs = [(a, b) for (a, b, c) in triples]
	expected_outputs = [c for (a, b, c) in triples]
	outputs = list(map(lambda x: vowel(x[0], x[1]), inputs))
	if expected_outputs == outputs:
		print("vowel_test() passed")
	else:
		print("vowel_test() failed")

def test_all():
	step1a_test()
	step1b_test()
	step1c_test()
	step2_test()
	step3_test()
	step4_test()
	step5a_test()
	step5b_test()
	vowel_test()
	measure_test()
