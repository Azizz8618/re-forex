#!/usr/bin/env python3
"""FINAL: high-RAM array + internal subroutine, called from body[9].

Measured map (probe_map/probe_fill): zone N+3 word k -> RAM 0o30114+k for
k=0..0o71 (58 words); zones N+4..N+40 have NO RAM image at our entry.
MODA (structured UTC, 0x093000|addr) sets M20 so ARX can read the high array.
"""
import os,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
W=Path(os.environ.get('ZONE80_WORK',
    tempfile.mkdtemp(prefix='zone80-',
                     dir=os.environ.get('TMPDIR','/tmp'))))
os.environ['WIN78_WORK']=str(W/'cases')
os.environ.setdefault('TMPDIR','/dev/shm')
sys.path.insert(0,str(HERE))
import harness as h
XTA=0x008000; ARX=0x00b000; STO=0; GOST=0o2006; H=0o30114
OBJ12=0o0064200402200000; RET=0o6700000002200000
ARR=0o41; AOFF=0o40; NOFF=0o44; SUBOFF=0o30; NWORD=58
MASK=(1<<48)-1

def wh(a,b,c,d): return (h.half(a,b)<<24)|h.half(c,d)
def jump(a):
    """Structured 15-bit UJ/VJM, reg 0 (proven by baseline 03104067)."""
    return (0x0C<<16)|(((a>>8)&0x7f)<<8)|(a&0xff)
def mo(addr): return 0x090000|addr
def build(idx=2, val=3, zfirst=False, zsub=False):
    a_ram=H+AOFF+idx-1; n_ram=H+NOFF
    z={0:(h.half(XTA,GOST)<<24)|mo(0o30000),
       1:(h.half(ARX,a_ram&0o7777)<<24)|mo(0o30000),
       2:(h.half(ARX,n_ram&0o7777)<<24)|mo(0),
       3:(h.half(STO,GOST)<<24)|jump(H+SUBOFF),
       4:RET,
       AOFF+0:0, AOFF+1:0, AOFF+2:0, AOFF+idx-1:(val<<40)&MASK,
       NOFF:(1<<40)&MASK,
       SUBOFF:OBJ12, SUBOFF+1:RET}
    if zfirst: z[0]=0
    if zsub: z[SUBOFF]=0
    reserved=set(z)
    for k in range(NWORD):
        if k not in reserved: z[k]=0o777700000000|k
    return z

def run(name, *, idx=2,val=3,zfirst=False,zsub=False,core=True,mtr=None):
    z=build(idx,val,zfirst,zsub)
    r=h.run_case(name, body_patch={9:(jump(H)<<24)|0}, zone_patches={3:z},
                 a1=0,a2=0, core=core, core_skip=6, mtr=mtr, timeout=220)
    return r,z

def main():
    cases=[('fin_hi_val3', 2,3,False,False,'41 1.00 3.00','array value 3'),
           ('fin_hi_val5', 2,5,False,False,'61 1.00 3.00','array value 5'),
           ('fin_hi_idx3', 3,7,False,False,'81 1.00 3.00','index 2->3, A(3)=7'),
           ('fin_hi_zeroA',2,0,False,False,'11 1.00 3.00','array value 0'),
           ('fin_hi_zfirst',2,3,True,False,None,'routine first word zeroed'),
           ('fin_hi_zsub',  2,3,False,True,None,'subroutine first word zeroed')]
    out=[]
    for name,idx,val,zf,zs,want,note in cases:
        r,z=run(name,idx=idx,val=val,zfirst=zf,zsub=zs)
        good=(r['printed']==want and r['end'])
        line='%-16s idx=%d val=%d print=%-18r want=%-18r end=%-5s %s'%(
            name,idx,val,r['printed'],want,r['end'],'OK' if good else 'FAIL')
        print(line,flush=True); out.append(line+'\n')
        (W/(name+'_out.txt')).write_text(r['out'])
        if r['core']:
            d=r['core'].read_bytes()
            ram=[int.from_bytes(d[i:i+6],'big') for i in range(0,len(d),6)]
            bad=[k for k in z if ram[H+k]!=z[k]]
            (W/(name+'_core.txt')).write_text(
                'word_count=%d  first_ram=%o  last_ram=%o  mismatch=%d\n'%(NWORD,H,H+NWORD-1,len(bad))+
                ''.join('zone3[%03o] RAM %06o = %016o\n'%(k,H+k,ram[H+k]) for k in sorted(z)))
            print('   CORE: words=%d mismatches=%d'%(NWORD,len(bad)),flush=True)
    (W/'final_results.txt').write_text(''.join(out))
    r,z=run('fin_hi_mtr', core=False, mtr=('%o'%(H-0o14),'%o'%(H+0o60),'60',0))
    lines=[l for l in r['out'].splitlines() if l.startswith('MTR ')]
    (W/'final_mtr.txt').write_text('\n'.join(lines)+'\n')
    print('MTR: %d lines, PCs %s'%(len(lines),sorted(set(l[4:9] for l in lines))[:12]),flush=True)
    return 0

if __name__=='__main__': sys.exit(main())
