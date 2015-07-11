'''
Created on Jul 10, 2015

@author: cmp670@nyu.edu
Solution to problem two of UCSL Python Lab Challenge 1
'''

strInput = raw_input('Enter a string to parse: ')
listWords = strInput.split()

#removes duplicates:
setWords = set(listWords)
#sort and rejoin with single spaces
print ' '.join(sorted(setWords))