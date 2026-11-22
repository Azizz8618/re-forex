#!/usr/bin/env python3
"""FINAL Step-4 proof: ARRAY + internal SUBROUTINE (monitor-side call path).

* Monitor-side call path: rebuilt GIVTRAN/SETTRAN text installed as NEWCOMP*
  4.12 catalog at zone 0o2350; *TRANS:OURMRK*,,412350 loads our body
  (tests 66/78 recipe, all on disk copies).
* ARRAY A(1..3): body[0o41+k-1] -> RAM BASE+body = 0o2020+.
  body[9] RH = ARX A(index): address computed as base + index-1.
* SUBROUTINE at body[0o21] (RAM 0o2000) owns the *64 print word; entered by
  VJM from body[11].  Zeroing its first word removes the console line.
"""
import os, sys
from pathlib import Path
WORK=Path('/tmp/.private/azizz/opencode/re-forex-limit-array'); RUN=WORK/'run78'
sys.path.insert(0,'/home/azizz/Yandex.Disk/re-forex/tests/plan-f77/78-extended-window')
os.environ['WIN78_WORK']=str(RUN); os.environ['TMPDIR']='/dev/shm'
import harness as h
BASE=0o1757; XTA=0x008000; ARX=0x00b000; STO=0; GOST=0o2006; ARR=0o41
RET=0o6700000002200000; OBJ12=0o0064200402200000; MASK=(1<<48)-1
def wh(a,b,c,d): return (h.half(a,b)<<24)|h.half(c,d)
def vjm(a): return (0o14<<16)|(((a>>8)&0xf)<<8)|(a&0xff)
SUB=0o2000; SUB_BODY=0o21

def build(index,val,zero=False):
    a_body=ARR+index-1; a=BASE+a_body
    p={9:wh(XTA,GOST,ARX,a),            # ACC = G1 + A(index)
       10:wh(ARX,BASE+0o42,STO,GOST),   # ACC += N-units ; G1 = ACC
       ARR:0,ARR+1:0,ARR+2:0,a_body:(val<<40)&MASK,
       11:(vjm(SUB)<<24)|0,             # VJM -> subroutine (owns the print)
       13:RET,                          # after return: end task
       SUB_BODY:OBJ12,                  # subroutine: *64 print
       SUB_BODY+1:RET}                  # subroutine: uj 0(15) return
    if zero: p[SUB_BODY]=0
    return p,dict(index=index,a_body=a_body,a_adr=a,val=val,sub=SUB)

CASES=[
 ('idx2',   2,3,False,'A(2)=3, sub live'),
 ('idx3',   3,5,False,'A(3)=5 (index changed)'),
 ('zeroA',  2,0,False,'A(2)=0'),
 ('zerosub',2,3,True, 'subroutine first word zeroed'),
]
lines=[]
for name,idx,val,zs,note in CASES:
    p,meta=build(idx,val,zs)
    r=h.run_case('fin2_'+name,body_patch=p,a1=0,a2=1,core=True,core_skip=6,timeout=130)
    line='%-8s rc=%-6s printed=%-18r end=%-5s note=%s'%(name,r['rc'],r['printed'],r['end'],note)
    print(line,flush=True); print('   %r'%meta,flush=True)
    lines.append(line+'\n   %r'%meta)
    (WORK/('fin2_'+name+'_out.txt')).write_text(r['out'])
(WORK/'final_proof2_results.txt').write_text('\n'.join(lines)+'\n')
