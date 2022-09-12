from collections import defaultdict
from pprint import pprint


# TODO zero-index?
_STZ_STATES = '''
0:T1,S2
1:Z1,S2;T2,S3
2:Z1,S2;Z2,S3;T3
3:T1,S2;Z2,S3;Z3,T4
4:S1;T1,S2;Z2,T3;Z3;Z2,T3
5:S1;T1;Z2
6:S1,T2;T2,Z3
7:S1,T2;S2,Z3;T3,Z4
8:T1;S1,Z2;S2,Z3;T3
9:Z1;S1,Z2;S2
10:Z1;S1
11:T1
'''.strip()

STZ_STATES = defaultdict(dict)

last_count_pieces = int(_STZ_STATES.splitlines()[-1].split(':')[0])
print(last_count_pieces)

for line in _STZ_STATES.splitlines():
    count_pieces, defs = line.split(':')
    count_pieces = int(count_pieces)
    defs = defs.split(';')
    for i, statedef in enumerate(defs):
        statedef = statedef.split(',')
        statename = (count_pieces, i)
        for out_edge in statedef:
            piece, nextstateno = out_edge
            nextstateno = int(nextstateno) - 1
            if count_pieces != last_count_pieces:
                nextcountpieces = count_pieces + 1
            else:
                nextcountpieces = 0
            nextstatename = (nextcountpieces, nextstateno)
            STZ_STATES[statename][piece] = nextstatename

# pprint(STZ_STATES)
