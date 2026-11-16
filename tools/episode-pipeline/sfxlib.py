import numpy as np, wave
sr=44100; R=np.random.RandomState(5)
class Mix:
    def __init__(s,T): s.a=np.zeros(int(sr*T))
    def add(s,t,x,g=1.0):
        i=max(0,int(t*sr)); x=x[:max(0,len(s.a)-i)]; s.a[i:i+len(x)]+=x*g
    def save(s,p):
        a=np.tanh(s.a*1.2)*.5; w=wave.open(p,"w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a*32767).astype(np.int16).tobytes()); w.close()
def whoosh(d=.32):
    n=int(sr*d); t=np.linspace(0,1,n); k=np.cumsum(R.randn(n)); k-=np.linspace(k[0],k[-1],n); k/=abs(k).max()+1e-9; hp=np.diff(np.r_[0,k])*8+k*.3; return hp/abs(hp).max()*np.sin(np.pi*t)**2
def hit(f=70,d=.35):
    n=int(sr*d); t=np.arange(n)/sr; return np.sin(2*np.pi*(f*t+40*(1-np.exp(-t*30))/30))*np.exp(-t*11)+R.randn(n)*np.exp(-t*60)*.5
def pop(f=880,d=.09):
    n=int(sr*d); t=np.arange(n)/sr; return np.sin(2*np.pi*f*t*(1+t*4))*np.exp(-t*45)
def ding(f=1568,d=.6):
    n=int(sr*d); t=np.arange(n)/sr; return (np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.5*t))*np.exp(-t*7)
def paper(d=.06):
    n=int(sr*d); t=np.arange(n)/sr; return R.randn(n)*np.exp(-t*70)
def drone(d,f=55):
    n=int(sr*d); t=np.arange(n)/sr; x=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.01*t); return x*np.minimum(1,t/.5)*np.minimum(1,(d-t)/.3)
def glitch(d=.25):
    n=int(sr*d); x=R.randn(n)*(R.rand(n//400+1).repeat(400)[:n]>.5); return x*.6
def pad(d,fs=(196,247,294)):
    n=int(sr*d); t=np.arange(n)/sr; x=sum(np.sin(2*np.pi*f*t) for f in fs)/3; return x*np.minimum(1,t/1)*np.minimum(1,(d-t)/1)
def alarm(d=1.5):
    n=int(sr*d); t=np.arange(n)/sr; return np.sign(np.sin(2*np.pi*(700+250*np.sign(np.sin(2*np.pi*2.5*t)))*t))*.4*np.minimum(1,(d-t)/.1)
def thud(d=.25):
    n=int(sr*d); t=np.arange(n)/sr; return np.sin(2*np.pi*90*t*np.exp(-t*3))*np.exp(-t*18)
def typing(d, rate=14):
    n=int(sr*d); x=np.zeros(n)
    for j in range(int(d*rate)):
        i=int((j/rate+R.rand()*.03)*sr); c=paper(.02)*.6; x[i:i+len(c)]+=c[:max(0,n-i)]
    return x
def endcard(m,T3):
    m.add(T3,whoosh(.4),.4); m.add(T3+.6,pop(1000,.08),.6); m.add(T3+1.25,pop(1000,.08),.6); m.add(T3+1.28,ding(),.4)
