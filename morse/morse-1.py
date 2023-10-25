
from collections import OrderedDict

cd1 = "a aaa, e, i i, ooo ooo ooo, u u uuu, enne en, es es es, tee, el elle el el, er erre er, cee ce cee ce, delta de de, emme emme, pe pee pee pe, ve ve ve vee, beta be be be, gamma gamma ge, ha ha ha ha, ef ef effe ef, quu quu qu quu, ji jota jota jota, kappa ka kappa, we wee wee, exxe ex ex exxe, ypsilon y ypsilon ypsilon, zeta zeta ze ze"

dit,dah = "■","■■■"
example = "the space between words is seven units"

cd2 = cd1.split (",")
cd3 = [s.strip() for s in cd2]
cd5 = [list(OrderedDict((k, True) for k in s if k != " ")) for s in cd3]
cd6 = [[c for c in s if c not in "aeiou" or len(s)==1][0] for s in cd5]
cd7 = [(a,[dit if len (x) < 3 else dah for x in b.split(" ")]) 
           for a,b in zip (cd6,cd3)]
cd8 = {a:" ".join (b) for a,b in cd7}
cd9 = [(3*" ").join([cd8[c] for c in w]) for w in example.split(" ")]
cd10 = (7*" ").join(cd9)


print ("cd2:",cd2)
print ("cd3:",cd3)
print ("cd5:",cd5)
print ("cd6:",cd6)
print ("cd7:",cd7)
print ("cd8:",cd8)
print ("cd9:",cd9)
print ("cd10:",cd10)

"""
cd2: ['a aaa', ' e', ' i i', ' ooo ooo ooo', ' u u uuu', ' enne en', ' es es es', ' tee', ' el elle el el', ' er erre er', ' cee ce cee ce', ' delta de de', ' emme emme', ' pe pee pee pe', ' ve ve ve vee', ' beta be be be', ' gamma gamma ge', ' ha ha ha ha', ' ef ef effe ef', ' quu quu qu quu', ' ji jota jota jota', ' kappa ka kappa', ' we wee wee', ' exxe ex ex exxe', ' ypsilon y ypsilon ypsilon', ' zeta zeta ze ze']
cd3: ['a aaa', 'e', 'i i', 'ooo ooo ooo', 'u u uuu', 'enne en', 'es es es', 'tee', 'el elle el el', 'er erre er', 'cee ce cee ce', 'delta de de', 'emme emme', 'pe pee pee pe', 've ve ve vee', 'beta be be be', 'gamma gamma ge', 'ha ha ha ha', 'ef ef effe ef', 'quu quu qu quu', 'ji jota jota jota', 'kappa ka kappa', 'we wee wee', 'exxe ex ex exxe', 'ypsilon y ypsilon ypsilon', 'zeta zeta ze ze']
cd5: [['a'], ['e'], ['i'], ['o'], ['u'], ['e', 'n'], ['e', 's'], ['t', 'e'], ['e', 'l'], ['e', 'r'], ['c', 'e'], ['d', 'e', 'l', 't', 'a'], ['e', 'm'], ['p', 'e'], ['v', 'e'], ['b', 'e', 't', 'a'], ['g', 'a', 'm', 'e'], ['h', 'a'], ['e', 'f'], ['q', 'u'], ['j', 'i', 'o', 't', 'a'], ['k', 'a', 'p'], ['w', 'e'], ['e', 'x'], ['y', 'p', 's', 'i', 'l', 'o', 'n'], ['z', 'e', 't', 'a']]
cd6: ['a', 'e', 'i', 'o', 'u', 'n', 's', 't', 'l', 'r', 'c', 'd', 'm', 'p', 'v', 'b', 'g', 'h', 'f', 'q', 'j', 'k', 'w', 'x', 'y', 'z']
cd7: [('a', ['■', '■■■']), ('e', ['■']), ('i', ['■', '■']), ('o', ['■■■', '■■■', '■■■']), ('u', ['■', '■', '■■■']), ('n', ['■■■', '■']), ('s', ['■', '■', '■']), ('t', ['■■■']), ('l', ['■', '■■■', '■', '■']), ('r', ['■', '■■■', '■']), ('c', ['■■■', '■', '■■■', '■']), ('d', ['■■■', '■', '■']), ('m', ['■■■', '■■■']), ('p', ['■', '■■■', '■■■', '■']), ('v', ['■', '■', '■', '■■■']), ('b', ['■■■', '■', '■', '■']), ('g', ['■■■', '■■■', '■']), ('h', ['■', '■', '■', '■']), ('f', ['■', '■', '■■■', '■']), ('q', ['■■■', '■■■', '■', '■■■']), ('j', ['■', '■■■', '■■■', '■■■']), ('k', ['■■■', '■', '■■■']), ('w', ['■', '■■■', '■■■']), ('x', ['■■■', '■', '■', '■■■']), ('y', ['■■■', '■', '■■■', '■■■']), ('z', ['■■■', '■■■', '■', '■'])]
cd8: {'a': '■ ■■■', 'e': '■', 'i': '■ ■', 'o': '■■■ ■■■ ■■■', 'u': '■ ■ ■■■', 'n': '■■■ ■', 's': '■ ■ ■', 't': '■■■', 'l': '■ ■■■ ■ ■', 'r': '■ ■■■ ■', 'c': '■■■ ■ ■■■ ■', 'd': '■■■ ■ ■', 'm': '■■■ ■■■', 'p': '■ ■■■ ■■■ ■', 'v': '■ ■ ■ ■■■', 'b': '■■■ ■ ■ ■', 'g': '■■■ ■■■ ■', 'h': '■ ■ ■ ■', 'f': '■ ■ ■■■ ■', 'q': '■■■ ■■■ ■ ■■■', 'j': '■ ■■■ ■■■ ■■■', 'k': '■■■ ■ ■■■', 'w': '■ ■■■ ■■■', 'x': '■■■ ■ ■ ■■■', 'y': '■■■ ■ ■■■ ■■■', 'z': '■■■ ■■■ ■ ■'}
cd9: ['■■■   ■ ■ ■ ■   ■', '■ ■ ■   ■ ■■■ ■■■ ■   ■ ■■■   ■■■ ■ ■■■ ■   ■', '■■■ ■ ■ ■   ■   ■■■   ■ ■■■ ■■■   ■   ■   ■■■ ■', '■ ■■■ ■■■   ■■■ ■■■ ■■■   ■ ■■■ ■   ■■■ ■ ■   ■ ■ ■', '■ ■   ■ ■ ■', '■ ■ ■   ■   ■ ■ ■ ■■■   ■   ■■■ ■', '■ ■ ■■■   ■■■ ■   ■ ■   ■■■   ■ ■ ■']
cd10: ■■■   ■ ■ ■ ■   ■       ■ ■ ■   ■ ■■■ ■■■ ■   ■ ■■■   ■■■ ■ ■■■ ■   ■       ■■■ ■ ■ ■   ■   ■■■   ■ ■■■ ■■■   ■   ■   ■■■ ■       ■ ■■■ ■■■   ■■■ ■■■ ■■■   ■ ■■■ ■   ■■■ ■ ■   ■ ■ ■       ■ ■   ■ ■ ■       ■ ■ ■   ■   ■ ■ ■ ■■■   ■   ■■■ ■       ■ ■ ■■■   ■■■ ■   ■ ■   ■■■   ■ ■ ■
"""

