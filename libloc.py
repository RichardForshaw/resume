# get libary location on system
import sys
print(next(filter(lambda x: 'site-packages' in x, sys.path)))
