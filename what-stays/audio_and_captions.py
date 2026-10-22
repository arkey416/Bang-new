"""Create original, non-musical foley and exact timed captions."""
from pathlib import Path
import json, re, wave
import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parent
SR=48000
mix=np.zeros((SR*30,2),np.float64)
rng=np.random.default_rng(416)

def place(time,sound,gain=.08,pan=0):
    sound=sound/(max(np.max(np.abs(sound)),1e-9))
    start=round(time*SR); n=min(len(sound),len(mix)-start)
    gains=np.array([np.sqrt((1-pan)/2),np.sqrt((1+pan)/2)])
    mix[start:start+n]+=sound[:n,None]*gain*gains

def rustle(time,duration=.24,gain=.035,pan=0):
    t=np.arange(int(SR*duration))/SR
    noise=rng.standard_normal(len(t))
    noise=sosfilt(butter(2,[700,6500],btype='bandpass',fs=SR,output='sos'),noise)
    envelope=np.sin(np.pi*t/duration)**1.5
    place(time,noise*envelope,gain,pan)

def coin(time,gain=.04,pan=0):
    t=np.arange(int(SR*.24))/SR
    # Inharmonic, quickly decaying metal impact; this is foley, not a musical cue.
    y=sum(np.sin(2*np.pi*f*t)*np.exp(-t*d)*a for f,d,a in [(2181,33,1),(3397,43,.5),(5113,52,.2)])
    y+=rng.standard_normal(len(t))*.1*np.exp(-t*200)
    place(time,y,gain,pan)

def tap(time,gain=.028,pan=0):
    t=np.arange(int(SR*.13))/SR
    n=sosfilt(butter(2,700,fs=SR,output='sos'),rng.standard_normal(len(t)))
    place(time,n*np.exp(-t*48),gain,pan)

# Editorial scene transitions, paper handling, coins, and quiet footfalls only.
rustle(.42,.28,.024)
for t in [.78,1.12,1.46]:coin(t,.026,.3)
rustle(5.20,.30,.032,-.25)
coin(6.22,.034,.1)
rustle(6.83,.35,.022)
coin(7.48,.029,.1)
for t in [9.29,10.26,11.25]:rustle(t,.18,.028,-.4)
for t in [9.75,10.48,11.20,11.89,12.38]:coin(t,.026,.35)
rustle(13.08,.32,.020)
for t in [13.55,14.02,14.49,15.0,15.48,16.04]:tap(t,.014,-.15)
rustle(17.52,.30,.023)
tap(18.35,.024,.15)
rustle(19.90,.28,.025)
for t in [20.48,22.17,22.75,24.34]:tap(t,.028)
rustle(25.82,.32,.022)
coin(27.53,.021,.25)
pcm=np.int16(np.clip(mix,-1,1)*32767)
with wave.open(str(ROOT/'project'/'sfx.wav'),'wb') as f:
    f.setnchannels(2);f.setsampwidth(2);f.setframerate(SR);f.writeframes(pcm.tobytes())

caps=[(.53,1.85,'Bigger paycheck,'),(2.26,4.38,'barely more left\neach month.'),
(5.21,6.74,'Imagine getting a raise,'),(6.86,9.02,'then choosing a\npricier apartment.'),
(9.26,10.78,'That recurring cost'),(10.78,12.75,'can absorb the\nextra income.'),
(13.17,15.53,'Some increases meet\ngenuine needs,'),(15.53,17.38,'like higher\nchildcare costs;'),
(17.61,19.50,'others are optional\nupgrades.'),(20.09,21.61,'A raise still helps,'),
(21.78,22.27,'but track'),(22.27,24.22,'[[income and\nexpenses together]]'),(24.22,25.48,"to see what's left."),
(25.98,27.53,'What makes a\nlifestyle upgrade'),(27.53,30.0,'worth its\nmonthly cost?')]
expected="Bigger paycheck, barely more left each month. Imagine getting a raise, then choosing a pricier apartment. That recurring cost can absorb the extra income. Some increases meet genuine needs, like higher childcare costs; others are optional upgrades. A raise still helps, but track [[income and expenses together]] to see what's left. What makes a lifestyle upgrade worth its monthly cost?"
actual=' '.join(c[2].replace('\n',' ') for c in caps)
assert actual==expected,(actual,expected)
def stamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
srt='\n\n'.join(f'{i+1}\n{stamp(s)} --> {stamp(e)}\n{text}' for i,(s,e,text) in enumerate(caps))+'\n'
(ROOT/'output'/'What-Stays.en.srt').write_text(srt)
(ROOT/'project'/'captions.json').write_text(json.dumps(caps,indent=2))
(ROOT/'project'/'narration.txt').write_text(expected+'\n')
print('Exact caption text verified; 15 cues. Original SFX rendered; no music.')
