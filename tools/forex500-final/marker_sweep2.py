#!/usr/bin/env python3
"""docs/120 marker sweep of suspect cells on the PASSING Task-1 image."""
import os, shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_e2e import rz, wz, N, Z3, MASK
WS = Path(__file__).resolve().parent.parent
DISPAK='/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'
SHARE=Path('/usr/local/share/besm6')
BODY=[0o536,0o537,0o654,0o655,0o656,0o657,0o660,0o661,0o662,0o663,
      0o664,0o665,0o666,0o667,0o670,0o671,0o672,0o673,0o674,0o675,
      0o676,0o677,0o716]
N2=[153,154,155]
def br(i):
    if i<0o604: return 0o2223+(i-0o224)
    if i<0o1236: return 0o2621+(i-0o604)
    if i<0o1617: return 0o21066+(i-0o1237)
    if i<0o1627: return 0o21452+(i-0o1617)
    return 0o21467+(i-0o1630)
def mk(k,base): return (base + k*0o000020004010) & MASK
case=sys.argv[1] if len(sys.argv)>1 else 'SW2'
src=WS/'images/2048_B9_A'; dst=WS/'images'/f'2048_{case}'
shutil.copy2(src,dst)
b=rz(str(dst),N+1); z=rz(str(dst),N+2)
for k,i in enumerate(BODY): b[i]=mk(k,0o200000000001)
for k,o in enumerate(N2): z[o]=mk(k,0o300000000001)
wz(str(dst),N+1,b); wz(str(dst),N+2,z)
d=WS/'oracle'/case
if d.exists(): shutil.rmtree(d)
(d/'disks').mkdir(parents=True);(d/'home').mkdir()
shutil.copy2(dst,d/'disks'/'2048')
for f in ('2053','2099'): shutil.copy2(SHARE/f,d/'disks'/f)
shutil.copy2(WS/'decks/deck_B9_A.b6',d/'job.b6')
env=dict(os.environ,HOME=str(d/'home'),BESM6_PATH=str(d/'disks'),
         BESM6_DD_DEBUG='1',BESM6_CORE_ON_PC='022555',BESM6_CORE_SKIP='0')
with open(d/'out.txt','wb') as f:
    r=subprocess.run(['timeout','-s','KILL','90',DISPAK,'-l','job.b6'],cwd=d,env=env,
                     stdout=f,stderr=subprocess.STDOUT)
print('rc',r.returncode)
corep=d/'core-pc.bin'
if not corep.exists(): print('NO CORE'); sys.exit(2)
core=corep.read_bytes()
def w(a): return int.from_bytes(core[a*6:a*6+6],'big')
print('--- BODY ---')
for k,i in enumerate(BODY):
    exp=mk(k,0o200000000001); got=w(br(i))
    print(f'body[{i:04o}] RAM {br(i):05o} {"KEEP" if got==exp else "OVERWRITTEN"} exp={exp:016o} got={got:016o}')
print('--- N+2 ---')
for k,o in enumerate(N2):
    exp=mk(k,0o300000000001); got=w(0o21637+o)
    print(f'N2[{o:o}] RAM {0o21637+o:05o} {"KEEP" if got==exp else "OVERWRITTEN"} exp={exp:016o} got={got:016o}')
print('--- result ---')
for l in (d/'out.txt').read_text(errors='replace').splitlines():
    if l.strip().startswith('21') or 'КОНЕЦ' in l: print(l)
