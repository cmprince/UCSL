'''
Created on Jul 1, 2015

@author: cmp
'''

x = input('x?')
y = input('y?')

a = [[i*j for i in xrange(y)] for j in xrange(x)]

print a
 

if __name__ == '__main__':
    pass