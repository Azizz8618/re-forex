import re, sys
base = int(sys.argv[1], 8)
fm257 = base + 256
iret = base + 248
cfg = {'@FM257@': format(fm257, '08o'), '@IRET@': format(iret, '08o')}
src = open('/var/tmp/p7c-arfa-lib/lib/p7ceng.mad').read()
for k, v in cfg.items():
    src = src.replace(k, v)
# fix literal format: right half must be exactly 8 octal digits
src = re.sub(r'=:00000000 00([0-7]{4,8})',
             lambda m: '=:00000000 ' + format(int(m.group(1), 8), '08o'),
             src)
src = re.sub(r',ATX,([0-7]{4,8})\b',
             lambda m: ',ATX,' + format(int(m.group(1), 8), '08o'),
             src)
parts = [p for p in re.split(r'(?=^  Z[A-Z0-9]+:,NAME,)', src, flags=re.M) if p.strip()]
out = []
out.append("шифр 419999 зс5^\nлен 60(2348-wr)^\nееВ1а3\n*name P7CLIB\n*call yesmemory\n*perso:602300\n*no list\n")
for p in parts:
    out.append("*assembler\n" + p.rstrip() + "\n        ,END,\n")
out.append("*forex\n" + open('/var/tmp/p7c-arfa-lib/lib/p7clib.f').read())
out.append("*to perso:602320\n*end file\n``````\nеконец\n")
open('/var/tmp/p7c-arfa-lib/build/lib.b6', 'w').write(''.join(out))
print('base=%s fm257=%s iret=%s sections=%d' % (oct(base), oct(fm257), oct(iret), len(parts)))
