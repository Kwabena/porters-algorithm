# Script for generating dictionaries from a corpus
# One dictionary is generated directly from the corpus without stemming
# while the other is generated after the words in the corpus are stemmed
# with Porter's algorithm
# This file also contains code for generating basic information about 
# the two dictionaries and comparing them
#
# Author: Kwabena Antwi-Boasiako
# June 2017

from porter import *
from collections import Counter
import re

# Read the culture corpus and build a dictionary from it 
# without first stemming the entries
f = open('corpus-culture', 'r')
corpus = f.read()
f.close()
entries1 = re.split('[^a-zA-Z]', corpus)
entries1 = list(map(str.lower, entries1)) # Convert all emtroes to lowercase equivalents
entries1 = list(filter(lambda x: len(x) > 0, entries1)) # Keep only non-empty entries

# Build dictionary of entries with their corresponding frequencies
entries_with_frequencies1 = Counter()
for entry in entries1:
	entries_with_frequencies1[entry] += 1

d1 = dict(entries_with_frequencies1) # Old dictionary (without stemming)

# Form new dictionary where entries are first stemmed with Porter's algorithm
entries2 = list(map(step1a, entries1))
entries2 = list(map(step1b, entries2))
entries2 = list(map(step1c, entries2))
entries2 = list(map(step2, entries2))
entries2 = list(map(step3, entries2))
entries2 = list(map(step4, entries2))
entries2 = list(map(step5a, entries2))
entries2 = list(map(step5b, entries2))

entries_with_frequencies2 = Counter()
for entry in entries2:
	entries_with_frequencies2[entry] += 1

d2 = dict(entries_with_frequencies2) # New dictionary (after stemming)

# See what entries were mapped to after stemming
# To know what a string STRING was stemmed to, type mappings['STRING']
mappings = dict([(entries1[i], entries2[i]) for i in range(len(entries1))])

# Print the number of (unique) entries in both dictionaries
print("Number of entries in both dictionaries")
print(len(d1))
print(len(d2))

# Print the 10 most common entries in each dictionary with
# their corresponding frequencies
print("Most frequent entries in both dictionaries")
print(entries_with_frequencies1.most_common(10))
print(entries_with_frequencies2.most_common(10))

# Print the number of entries in each dictionary with frequencies 
# 1, 2, 3, 4, and 5
for i in [1, 2, 3, 4, 5]:
	f1 = len([v for v in d1.values() if v == i])
	f2 = len([v for v in d2.values() if v == i])
	print("Number of entries with frequency " + repr(i) + ': ' + repr(f1) + '\t' + repr(f2))

# The new dictionary has the empty string occurring a number of times
# even though the old dictionary does not contain it. This is because
# the corpus produces the entry 's' when it is broken into words and
# 's' is stemmed to the empty string by step1a of Porter's algorithm. 
# The line below tests that indeed all the empty strings in the new 
# dictionary result from the 's'es in the old dictionary or in the corpus
eses = [index for (index, entry) in enumerate(entries1) if entry == 's']
empties = [index for (index, entry) in enumerate(entries2) if entry == '']
assert(eses == empties)

# Similarly, the line below should also return True since the 
# frequencies of the two entries should be the same unless another
# entry is stemmed to 's', which does not appear to happen
assert(d1['s'] == d2[''])

# Print the frequencies of the entries in the two 
# dictionaries to  different files for plotting of charts
f = open('frequencies1.txt', 'w')
f.write(repr(list(d1.values())))
f.close()

f = open('frequencies2.txt', 'w')
f.write(repr(list(d2.values())))
f.close()
