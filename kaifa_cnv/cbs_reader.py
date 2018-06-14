from collections import namedtuple
import sys

CBS_Item = namedtuple('CBS_Item', ['sample', 'chr', 'start', 'end'])


def cbs_reader(filename):
    with open(filename) as F:
        for line in F:
            #a = tuple(line.strip('\n').split('\t'))
            print (line)
            yield CBS_Item._make(tuple(line.strip('\n').split('\t')))


