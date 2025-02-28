from tkinter import *
from math import *

#on construit les bases de l'interface
fenetre=Tk()
H,W=500,500
LIST=[]
LISTSPE=[]
ptot = PanedWindow(fenetre, orient = HORIZONTAL)
paned = PanedWindow(ptot, orient = VERTICAL)
canvas=Canvas(paned, height=H, width=W)
VALEUR = StringVar(fenetre, "X**2+3*X+4")
label = Entry(paned, text = VALEUR)
paned.add(canvas)
paned.add(label)
X=0
PRECISION=3
MODULEREF=1000
ECHELLE=100

COEFF = {}

def C(a,b):
    if (a,b) in COEFF.keys():
        return COEFF[(a,b)]
    if a==0 :
        COEFF[(a,b)] = 0
        return COEFF[(a,b)]
    if b==1 :
        COEFF[(a,b)] = a
        return COEFF[(a,b)]
    if b==0 :
        COEFF[(a,b)] = 1
        return COEFF[(a,b)]
    if a<b:
        COEFF[(a,b)] = 0
        return COEFF[(a,b)]
    COEFF[(a,b)] = C(a-1,b-1) + C(a-1,b)
    return COEFF[(a,b)]
ListeBernoulli = [1]
for m in range(1,1000):
    pass
    K=0
    if 2<m and m%2 == 1:
        ListeBernoulli.append(0)
    else:
        for k in range(m):
            K+= C(m+1,k)*ListeBernoulli[k]
        ListeBernoulli.append(-K/(m+1))

def GammaComplexe(x):
    if x==int(x.real):
        return 0
    a=1
    for k in range(1,1000):
        a*= (1+1/k)**x / (1+x/k)
    return a/x

def DigammaComplexe(x):
    if x == int(x.real):
        return 0
    y = GammaComplexe(x)
    h = 0.0001
    return (GammaComplexe(x+h)-y)/h/y

# def ZetaComplexe(x):
#     if x.real == int(x.real):
#         return 0
#     L = GammaComplexe(x)
#     if L==0:
#         return 0
#     return 1/(x-1) + L +

# fonction = lambda x: DigammaComplexe(x)

exp = lambda x : e**x
cos = lambda x : (exp(1j*x)+exp(1j*(-x)))/2
sin = lambda x : (exp(1j*x)-exp(1j*(-x)))/2j
def tan(x):
    c=cos(x)
    if c !=0:
        return sin(x)/c
    return 10000

fonction = lambda x: x**2

def afficherlegende():
    global LISTSPE
    for i in LISTSPE:
        canvas.delete(i)
    LISTSPE=[canvas.create_line(W/2,0,W/2,H),canvas.create_line(0,H/2,W,H/2)]
    for l in range(-4,5):
        i=l*H//8 / ECHELLE
        LISTSPE.append(canvas.create_text(i*ECHELLE+H//2, W//2, fill='white',text=i))
        LISTSPE.append(canvas.create_text(H//2, -i*ECHELLE+W//2, fill='white',text=i))

def effacerpixels():
    for i in LIST:
        canvas.delete(i)
    LIST=[]

def afficherpixel(x,y,color):
    LIST.append(canvas.create_rectangle(x,y,x+PRECISION,y+PRECISION,fill=color,width=0))

def distribution(valeur,centre):
    return exp(-abs((valeur-centre)**2/2))
def distribution2(valeur,centre):
    return 1/(1+(valeur-centre)**2)
def distribution3(valeur,centre):
    return log(2)/log(2+abs(valeur-centre))
def distribution(valeur,centre):
    return abs(cos(abs((valeur-centre)/2)))

def affichercomplex():
    global fonction
    for i in range(-H//2,H//2):
        for j in range(-W//2,W//2):
            if i%PRECISION==0 and j%PRECISION==0:
                afficherpixel(i+H//2,-j+W//2,genererfonction(fonction(i/ECHELLE+1j*j/ECHELLE)))

    afficherlegende()

def sgn(r):
    return r/abs(r)
def arg(r):
    if r==0:
        return 0
    x,y=r.real,r.imag
    if x==0:
        return pi/2*sgn(r.imag)
    if x>0:
        return atan(y/x)
    if y>0:
        return pi+atan(y/x)
    return -pi+atan(y/x)

def genererfonction(complexe):
    m = abs(complexe)
    a = arg(complexe)
    if complexe == 0:
        return '#FFFFFF'
    pourcentage= (distribution(a,0), distribution(a,2*pi/3), distribution(a,-2*pi/3) )
    l='#'
    for i in pourcentage:
        a=hex(int(255*i*exp(-(m/MODULEREF))))
        if len(a)==4:
            l+=a[2]
            l+=a[3]
        else:
            l+='00'
    return l.upper()

def recuplabel(*arg):
    global fonction
    texte=label.get()
    txt = "lambda X:"+texte
    fonction=eval(txt)
    fenetre.title('Polynome complexe : {0}'.format(texte))
    affichercomplex()

def validentree(*arg):
    global h,ECHELLE, PRECISION, MODULEREF
    ECHELLE = int(h.get())
    PRECISION=int(Et3.get())
    MODULEREF=int(Et2.get())
    recuplabel()

def validechelle(*args):
    VALEUR.set('e**(1j*arg(X))')
    recuplabel()

# finalisation de l'interface
bouton=Button(paned, text='ok', command=recuplabel)
paned.add(bouton)
paned.pack()

paned2=PanedWindow(ptot, orient = VERTICAL)
h=StringVar(fenetre,ECHELLE)
lbl = Label(paned2, text='Echelle')
paned2.add(lbl)
ech = Entry(paned2, text = h)
paned2.add(ech)
lb = Label(paned2,text='Module de référence')
paned2.add(lb)
VALEUR2=StringVar(fenetre, MODULEREF)
Et2 = Entry(paned2, text=VALEUR2)
paned2.add(Et2)
lb = Label(paned2,text="Taille d'un pixel")
paned2.add(lb)
VALEUR3=StringVar(fenetre, PRECISION)
Et3 = Entry(paned2, text=VALEUR3)
paned2.add(Et3)
bt=Button(paned2, text='ok', command=validentree)
paned2.add(bt)
bt = Button(paned2, text='Voir échelle', command = validechelle)
paned2.add(bt)

ptot.add(paned)


ptot.add(paned2)
ptot.pack()

affichercomplex()
fenetre.mainloop()