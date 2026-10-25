#!/usr/bin/env python3
"""Read RGDS+ physical volume keys; apply ALSA mixer volume (not only openbor_volume)."""
import os,sys,glob,struct,select,subprocess,time
node=sys.argv[1] if len(sys.argv)>1 else '/sys/class/anbernic_misc/openbor_volume'
EV_KEY=1; UP=115; DOWN=114
fds=[]
for path in sorted(glob.glob('/dev/input/event*')):
 try:
  f=os.open(path,os.O_RDONLY|os.O_NONBLOCK)
  fds.append(f)
 except OSError: pass
print('[AUDIO] event devices:',len(fds),flush=True)
fmt='llHHi'; size=struct.calcsize(fmt)
level=6

def set_level(n):
 global level
 level=max(0,min(10,n))
 try:
  with open(node,'w') as f:f.write(str(level)+'\n')
 except OSError:pass
 # Smooth, usable 11-step curve. Avoid the previous double attenuation.
 pct=(0, 8, 15, 23, 32, 42, 53, 64, 76, 88, 100)[level]
 for mixer in ('Master','PCM','Speaker','Playback'):
  try:
   r=subprocess.run(['amixer','-q','sset',mixer,str(pct)+'%'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=1)
   if r.returncode==0:
    print('[AUDIO]',level,'/10 mixer',mixer,pct,'%',flush=True)
    return
  except (OSError,subprocess.TimeoutExpired):pass
 print('[AUDIO] mixer ALSA nao acessivel; apenas sysfs atualizado',flush=True)
set_level(level)
buffers={fd:b'' for fd in fds}
try:
 while True:
  if not fds:time.sleep(5);continue
  ready,_,_=select.select(fds,[],[],1)
  for fd in ready:
   try:data=os.read(fd,4096)
   except OSError:continue
   buffers[fd]+=data
   while len(buffers[fd])>=size:
    item,buffers[fd]=buffers[fd][:size],buffers[fd][size:]
    _,_,kind,code,value=struct.unpack(fmt,item)
    if kind==EV_KEY and value==1 and code in (UP,DOWN):set_level(level+(1 if code==UP else -1))
finally:
 for fd in fds:os.close(fd)
