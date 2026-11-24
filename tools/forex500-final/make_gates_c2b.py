import sys, shutil, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_e2e import rz, wz, f32, N
WS=Path('.').resolve()
img=WS/'images'
# B: one machine-word patch of VIDX=12 value word (N+2 offset 32+12=44)
shutil.copy2(img/'2048_SCAN_FRX5_A', img/'2048_SCAN_FRX5_B')
z2=rz(str(img/'2048_SCAN_FRX5_B'), N+2)
z2[44]=f32(9999.0)&((1<<48)-1)
wz(str(img/'2048_SCAN_FRX5_B'), N+2, z2)
# C: byte-identical restore
shutil.copy2(img/'2048_SCAN_FRX5_A', img/'2048_SCAN_FRX5_C')
for n in ['2048_SCAN_FRX5_A','2048_SCAN_FRX5_B','2048_SCAN_FRX5_C']:
    print(n, hashlib.sha256((img/n).read_bytes()).hexdigest())
