'''
Created on Jul 10, 2015

@author: cmp670@nyu.edu
Solution to problem three of UCSL Python Lab Challenge 1
'''
#use the constants in the string module
import string

#initialize all counts as zero (is this necessary?)
intUpper = intLower = intWhite = intPunct = intDigit = intOther = 0

strInput = raw_input('String to parse: ')
#loop through string by character and test for membership in various classes
for ctr in strInput:
    if ctr in string.uppercase:
        intUpper += 1
    elif ctr in string.lowercase:
        intLower += 1
    elif ctr in string.whitespace:
        intWhite += 1
    elif ctr in string.punctuation:
        intPunct += 1
    elif ctr in string.digits:
        intDigit += 1
    else:
        intOther += 1
        
print 'UPPER CASE: %d' % intUpper 
print 'LOWER CASE: %d' % intLower 
print 'DIGITS: %d' % intDigit 
print 'PUNCTUATION: %d' % intPunct 
print 'WHITESPACE CHARACTERS: %d' % intWhite 
print 'NONE OF THE ABOVE: %d' % intOther 
