'''
Created on Jul 1, 2015

@author: cmp670@nyu.edu
Solution to problem one of UCSL Python Lab Challenge 1
'''

#Loop until a valid entry is given
while True:
    try:
        x, y = input('Numbers?')
        x = int(x)
        y = int(y)
        break
    except:
        print('Invalid number or type of entries')

#Use list comprehension to generate the list-of-lists
a = [[i*j for i in xrange(y)] for j in xrange(x)]

print a