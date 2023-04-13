import pyxel
import random

class Pile:
    """ définition d'une pile à l'aide de la classe List """
    def __init__(self):
        """constructeur de la classe Pile : cree une pile vide"""
        self.lst = []

    def est_vide(self):
        """renvoie un booleen indiquant si la pile est vide ou non """
        return self.lst == []

    def empiler(self, x):
        """empile x sur la pile"""
        self.lst.append(x)

    def depiler(self):
        """depile et renvoie l'élément au sommet de la pile"""
        if self.est_vide():
            raise ValueError("pile vide")
        return self.lst.pop()

 
class Case:
    def __init__(self):
        '''constructeur d'une case du labyrinthe avec pour attribut les quatres points cardinaux(False si le mur est present et True si il est cassé)'''
        self.N=False
        self.O=False
        self.S=False
        self.E=False
        self.contenu=None

class Labyrinthe:
    def __init__(self, p, q):
        '''constructeur de la classe labyrinthe'''
        self.nb_lignes=p
        self.nb_colonnes=q
        self.tab=[[Case() for i in range(q)] for i in range(p)] #tableau 2d de cases de la classe Case (l'ensemble crée le labyrinthe)
        a=0
        while a!=q**2//5:
            b=(random.randint(1,p-2),random.randint(1,q-2))
            if self.tab[b[0]][b[1]].contenu==None:
                c=random.randint(1,4)
                if c==1:
                    self.tab[b[0]][b[1]].contenu=9
                elif c==2:
                    self.tab[b[0]][b[1]].contenu=10
                elif c==3:
                    self.tab[b[0]][b[1]].contenu=8
                else:
                    self.tab[b[0]][b[1]].contenu=14
                a+=1
        self.creer()
        self.load_pyxels()
            
    def load_pyxels(self):
        self.pyxels=[[1 for i in range(self.nb_colonnes*15+1)]for j in range(self.nb_lignes*15+1)]
        for k in range(len(self.tab)):# rempli le tableau des pixels grace au tableau de case (assigne 1 si le pixel est vide et 0 si c'est un mur)
            for j in range(len(self.tab[k])):
                if self.tab[k][j].N!=True:
                    for l in range(j*15,j*15+16):
                        self.pyxels[k*15][l]=0
                if self.tab[k][j].S!=True:
                    for l in range(j*15,j*15+16):
                        self.pyxels[k*15+15][l]=0
                if self.tab[k][j].E!=True:
                    for l in range(k*15,k*15+16):
                        self.pyxels[l][j*15+15]=0
                if self.tab[k][j].O!=True:
                    for l in range(k*15,k*15+16):
                        self.pyxels[l][j*15]=0
                if self.tab[k][j].contenu!=None:
                    self.pyxels[k*15+8][j*15+8]=self.tab[k][j].contenu
                    
        for i in range(self.nb_colonnes*15-14,self.nb_colonnes*15):
            self.pyxels[i][self.nb_lignes*15]=2
            
    def creer(self):
        '''permet de creer un labyrinthe parfait'''
        pile = Pile()
        dejavu = [[False for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
        i,j=random.randint(0,self.nb_lignes-1),random.randint(0,self.nb_colonnes-1)
        pile.empiler((i,j))
        dejavu[i][j]=True
        while not pile.est_vide():
            t=[]
            x=pile.depiler()
            if x[0]-1>=0 and dejavu[x[0]-1][x[1]]==False:
                t.append('N')
            if x[0]+1<self.nb_colonnes and dejavu[x[0]+1][x[1]]==False:
                t.append('S')
            if x[1]-1>=0 and dejavu[x[0]][x[1]-1]==False:
                t.append('O')
            if x[1]+1<self.nb_colonnes and dejavu[x[0]][x[1]+1]==False:
                t.append('E')
            if t!=[]:
                a=t[random.randint(0,len(t)-1)]
                if a=='N':
                   self.tab[x[0]][x[1]].N=True
                   dejavu[x[0]-1][x[1]]=True
                   self.tab[x[0]-1][x[1]].S=True
                   pile.empiler(x)
                   pile.empiler((x[0]-1,x[1]))
                
                elif a=='S':
                   self.tab[x[0]][x[1]].S=True
                   dejavu[x[0]+1][x[1]]=True
                   self.tab[x[0]+1][x[1]].N=True
                   pile.empiler(x)
                   pile.empiler((x[0]+1,x[1]))
                
                elif a=='O':
                   self.tab[x[0]][x[1]].O=True
                   dejavu[x[0]][x[1]-1]=True
                   self.tab[x[0]][x[1]-1].E=True
                   pile.empiler(x)
                   pile.empiler((x[0],x[1]-1))
                   
                elif a=='E':
                   self.tab[x[0]][x[1]].E=True
                   dejavu[x[0]][x[1]+1]=True
                   self.tab[x[0]][x[1]+1].O=True
                   pile.empiler(x)
                   pile.empiler((x[0],x[1]+1))
    
    def draw(self,perso,tete,hauteur,lampe,rendu):
        '''dessine le rendu en 3d'''
        if True:
            a=int((160-(pyxel.atan2(20,2*(40-lampe)))*2)//2+(pyxel.atan2(20,2*(40-lampe)))*2)+hauteur
            pyxel.rect(0,(max(a,87+hauteur-lampe))*4+int(tete)*2-2,640,(100+int(tete)+hauteur-lampe-max(a,87+hauteur-lampe))*4-int(tete)*2+2,2)
            pyxel.rect(0,(100+int(tete)+hauteur-lampe)*4,640,40,8)
            pyxel.rect(0,(110+int(tete)+hauteur-lampe)*4,640,80,14)
            pyxel.rect(0,(130+int(tete)+hauteur-lampe)*4,640,(200-130+int(tete)+hauteur-lampe)*4+4,15)
            if rendu=='640':
                pyxel.rect(0,(max(a,87+hauteur-lampe))*4+int(tete)*2-2,640,(100+int(tete)+hauteur-lampe-max(a,87+hauteur-lampe))*4-int(tete)*2+2,8)
                for k in range((max(a,87+hauteur-lampe))*4+int(tete)*2-2,(100+int(tete)+hauteur-lampe)*4+2):
                    for l in range(k%2,640+k%2,2):
                        pyxel.pset(l,k,0)
                for k in range((110+int(tete)+hauteur-lampe)*4,(120+int(tete)+hauteur-lampe)*4):
                    for l in range(k%2,640+k%2,2):
                        pyxel.pset(l,k,8)
                for k in range((130+int(tete)+hauteur-lampe)*4,(140+int(tete)+hauteur-lampe)*4):
                    for l in range(k%2,640+k%2,2):
                        pyxel.pset(l,k,14)
            def dist(i):
                return -i[0]            
            bonus=[]            
            for i in range(0,160):
                balayage=(perso.facing-80+i)%360
                distance=1
                fin=False
                angle=False
                if rendu=='160':
                    while self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]!=0 and self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]!=2 and distance<40:
                        if bonus==[] or bonus[-1][2]!=i:
                            if self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==9:
                                bonus.append((distance,9,i))
                            elif self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==10:
                                bonus.append((distance,10,i))
                            elif self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==5:
                                bonus.append((distance,13,i))
                            elif self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==14:
                                bonus.append((distance,14,i))
                            elif self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==8:
                                bonus.append((distance,8,i))
                        distance+=1
                    if self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==2:
                        fin=True
                    if (perso.y//90+int(pyxel.sin(balayage)*distance))%15==0 and (perso.x//90+int(pyxel.cos(balayage)*distance))%15==0:
                        angle=True
                    if distance-lampe<10:
                        if not fin:
                            couleur1=7
                        else:
                            couleur1=11
                    elif distance-lampe<20:
                        if not fin:
                            couleur1=6
                        else:
                            couleur1=11
                    elif distance-lampe<30:
                        if not fin:
                            couleur1=5
                        else:
                            couleur1=3
                    elif distance-lampe<40 and distance<40:
                        if not fin:
                            couleur1=1
                        else:
                            couleur1=3
                    else:
                        if not fin:
                            couleur1=0
                        else:
                            couleur1=3
                            
                    if angle==True:
                        couleur1=0
                        
                    if distance-lampe<40:
                        pyxel.rect(i*4,(int((160-(pyxel.atan2(20,2*distance))*2)//2)+hauteur)*4+2*int(tete),4,4*(int((pyxel.atan2(20,2*distance))*2)+hauteur)+int(tete)*2,couleur1)
                                
                else:
                    while self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]!=0 and self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]!=2 and distance<40:
                        if bonus==[] or bonus[-1][2]!=i:
                            if self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==9:
                                bonus.append((distance,9,i))
                            elif self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==10:
                                bonus.append((distance,10,i))
                            elif self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==5:
                                bonus.append((distance,13,i))
                        distance+=1
                    if self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage)*distance)]==2:
                        fin=True
                    if (perso.y//90+int(pyxel.sin(balayage)*distance))%15==0 and (perso.x//90+int(pyxel.cos(balayage)*distance))%15==0:
                        angle=True
                    if distance-lampe<5:
                        if not fin:
                            couleur1=(7,7)
                        else:
                            couleur1=(7,11)
                    elif distance-lampe<10:
                        if not fin:
                            couleur1=(7,6)
                        else:
                            couleur1=(11,11)
                    elif distance-lampe<15:
                        if not fin:
                            couleur1=(6,6)
                        else:
                            couleur1=(11,11)
                    elif distance-lampe<20:
                        if not fin:
                            couleur1=(6,5)
                        else:
                            couleur1=(11,3)
                    elif distance-lampe<25:
                        if not fin:
                            couleur1=(5,5)
                        else:
                            couleur1=(11,3)
                    elif distance-lampe<30:
                        if not fin:
                            couleur1=(5,1)
                        else:
                            couleur1=(3,3)
                    elif distance-lampe<35:
                        if not fin:
                            couleur1=(1,1)
                        else:
                            couleur1=(3,3)
                    elif distance-lampe<40 and distance<40:
                        if not fin:
                            couleur1=(1,0)
                        else:
                            couleur1=(3,0)
                            
                    if angle==True:
                        couleur1=(0,0)
                        
                    if distance-lampe<40 and distance<40:
                        pyxel.rect(i*4,(int((160-(pyxel.atan2(20,2*distance))*2)//2)+hauteur)*4+2*int(tete),4,4*(int((pyxel.atan2(20,2*distance))*2)+hauteur)+int(tete)*2,couleur1[0])
                        if couleur1[0]!=couleur1[1]:                           
                            for k in range((int((160-(pyxel.atan2(20,2*distance))*2)//2)+hauteur)*4+2*int(tete),(int((160-(pyxel.atan2(20,2*distance))*2)//2+(pyxel.atan2(20,2*distance))*2)+hauteur)*4+int(tete)*3):
                                for r in range(0+k%2,4+k%2,2):
                                    pyxel.pset(i*4+r,k,couleur1[1])
            bonus.sort(key=dist)
            for k in bonus:
                if k[0]-lampe<40:
                    if k[1]==13:
                        pyxel.elli(int(k[2]*4-(660//k[0])),80*4-(660//k[0])*2,(660//k[0])*2,int((660//k[0])*4*(abs(pyxel.cos(pyxel.frame_count*7))+1)/1.5),k[1])
                    else:
                        pyxel.circ(k[2]*4,80*4,660//k[0],k[1])  
                
class Mob:
    def __init__(self,x,y,pyxels):
        self.x=x
        self.y=y
        self.direction=random.randint(1,8)
        pyxels[y][x]=5
        
    def cherche_perso(self,perso,pyxels):
        new_pyxels=[]
        b=False
        gauche=max(perso.x//90-45+perso.discretion,0)
        droite=min(perso.x//90+45-perso.discretion,len(pyxels[0]))
        haut=max(perso.y//90-45+perso.discretion,0)
        bas=min(perso.y//90+45-perso.discretion,len(pyxels))
        for i in range(haut,bas):
            nvelle_ligne=[]
            for j in range(gauche,droite):
                if pyxels[i][j]!=0:
                    if i==perso.y//90 and j==perso.x//90:
                        nvelle_ligne.append(0)
                    elif i==self.y and j==self.x:
                        nvelle_ligne.append(-3)
                        b=True
                    else:
                        nvelle_ligne.append(-1)
                else:
                    nvelle_ligne.append(-2)
            new_pyxels.append(nvelle_ligne)
        if b==False:
            return None
        
        for k in range(45-perso.discretion):
            z=random.randint(1,4)
            if z==4:
                for i in range(len( new_pyxels)):
                    for j in range(len(new_pyxels[0])):
                        if new_pyxels[i][j]==k:
                            if i-1>0:
                                a=new_pyxels[i-1][j]
                                if a==-1:
                                    new_pyxels[i-1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y+1)
                            if i+1<len(new_pyxels):
                                a=new_pyxels[i+1][j]
                                if a==-1:
                                    new_pyxels[i+1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y-1)
                            if j-1>0:
                                a=new_pyxels[i][j-1]
                                if a==-1:
                                    new_pyxels[i][j-1]=k+1
                                elif a==-3:
                                    return(self.x+1,self.y)
                            if j+1<len(new_pyxels[0]):
                                a=new_pyxels[i][j+1]
                                if a==-1:
                                    new_pyxels[i][j+1]=k+1
                                elif a==-3:
                                    return(self.x-1,self.y)
            elif z==2:
                for i in range(len( new_pyxels)-1,-1,-1):
                    for j in range(len(new_pyxels[0])):
                        if new_pyxels[i][j]==k:
                            if i-1>0:
                                a=new_pyxels[i-1][j]
                                if a==-1:
                                    new_pyxels[i-1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y+1)
                            if i+1<len(new_pyxels):
                                a=new_pyxels[i+1][j]
                                if a==-1:
                                    new_pyxels[i+1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y-1)
                            if j-1>0:
                                a=new_pyxels[i][j-1]
                                if a==-1:
                                    new_pyxels[i][j-1]=k+1
                                elif a==-3:
                                    return(self.x+1,self.y)
                            if j+1<len(new_pyxels[0]):
                                a=new_pyxels[i][j+1]
                                if a==-1:
                                    new_pyxels[i][j+1]=k+1
                                elif a==-3:
                                    return(self.x-1,self.y)
                                
            elif z==3:
                for i in range(len( new_pyxels)):
                    for j in range(len(new_pyxels[0])-1,-1,-1):
                        if new_pyxels[i][j]==k:
                            if i-1>0:
                                a=new_pyxels[i-1][j]
                                if a==-1:
                                    new_pyxels[i-1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y+1)
                            if i+1<len(new_pyxels):
                                a=new_pyxels[i+1][j]
                                if a==-1:
                                    new_pyxels[i+1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y-1)
                            if j-1>0:
                                a=new_pyxels[i][j-1]
                                if a==-1:
                                    new_pyxels[i][j-1]=k+1
                                elif a==-3:
                                    return(self.x+1,self.y)
                            if j+1<len(new_pyxels[0]):
                                a=new_pyxels[i][j+1]
                                if a==-1:
                                    new_pyxels[i][j+1]=k+1
                                elif a==-3:
                                    return(self.x-1,self.y)                 
            else:
                for i in range(len( new_pyxels)-1,-1,-1):
                    for j in range(len(new_pyxels[0])-1,-1,-1):
                        if new_pyxels[i][j]==k:
                            if i-1>0:
                                a=new_pyxels[i-1][j]
                                if a==-1:
                                    new_pyxels[i-1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y+1)
                            if i+1<len(new_pyxels):
                                a=new_pyxels[i+1][j]
                                if a==-1:
                                    new_pyxels[i+1][j]=k+1
                                elif a==-3:
                                    return(self.x,self.y-1)
                            if j-1>0:
                                a=new_pyxels[i][j-1]
                                if a==-1:
                                    new_pyxels[i][j-1]=k+1
                                elif a==-3:
                                    return(self.x+1,self.y)
                            if j+1<len(new_pyxels[0]):
                                a=new_pyxels[i][j+1]
                                if a==-1:
                                    new_pyxels[i][j+1]=k+1
                                elif a==-3:
                                    return(self.x-1,self.y)
                                
        return None
    def update(self,perso,pyxels):
        a=self.cherche_perso(perso,pyxels)
        if a!=None:
            pyxels[self.y][self.x]=1
            pyxels[a[1]][a[0]]=5
            self.x=a[0]
            self.y=a[1]
            return True
        else:
            case=(0,0)
            if self.direction==1:
                if pyxels[self.y-1][self.x]==1:
                    case=(self.x,self.y-1)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==2:
                if pyxels[self.y-1][self.x+1]==1:
                    case=(self.x+1,self.y-1)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==3:
                if pyxels[self.y][self.x+1]==1:
                    case=(self.x+1,self.y)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==4:
                if pyxels[self.y+1][self.x+1]==1:
                    case=(self.x+1,self.y+1)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==5:
                if pyxels[self.y+1][self.x]==1:
                    case=(self.x,self.y+1)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==6:
                if pyxels[self.y+1][self.x-1]==1:
                    case=(self.x-1,self.y+1)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==7:
                if pyxels[self.y][self.x-1]==1:
                    case=(self.x-1,self.y)
                else:
                    self.direction=random.randint(1,8)
            elif self.direction==8:
                if pyxels[self.y-1][self.x-1]==1:
                    case=(self.x-1,self.y-1)
                else:
                    self.direction=random.randint(1,8)
                    
            if case!=(0,0):
                if random.randint(1,15)==3:
                    self.direction=random.randint(1,8)
                else:
                    pyxels[case[1]][case[0]]=5
                    pyxels[self.y][self.x]=1
                    self.x=case[0]
                    self.y=case[1]
            return False
class Personnage:
    def __init__(self):
        self.x=180
        self.y=180
        self.facing=45
        self.speed=25
        self.tete=0
        self.hochement='+'
        self.position='debout'
        self.hauteur=0
        self.aug_hauteur=0
        self.lampe=-15
        self.discretion=0
        
    def draw(self):
        pyxel.rect(self.x//90,self.y//90,1,1,14)
    
    def draw_overlay(self,vitesse_mob,plume,ampoule,oeuil,mob,lenteur):
        affiche_image(plume,12,14,2)
        pyxel.rect(43,14,90,30,12)
        pyxel.rect(45,16,86,26,8)
        pyxel.rect(45,16,int(86*(self.speed-25)/42),26,11)
        affiche_image(ampoule,140,14,2)
        pyxel.rect(171,14,90,30,12)
        pyxel.rect(173,16,86,26,8)
        pyxel.rect(173,16,int(86*(self.lampe+15)/20),26,11)
        affiche_image(oeuil,268,14,2)
        pyxel.rect(299,14,90,30,12)
        pyxel.rect(301,16,86,26,8)
        pyxel.rect(301,16,int(86*(self.discretion)/40),26,11)
        affiche_image(mob,396,14,2)
        affiche_image(lenteur,410,28)
        pyxel.rect(427,14,90,30,12)
        pyxel.rect(429,16,86,26,8)
        pyxel.rect(429,16,int(86*(vitesse_mob-2.5)/2.8),26,11)
    def update(self,pyxels):
        if self.hochement=='+':
                if self.tete<1.6:
                    if random.randint(0,100)==0:
                        self.tete+=0.5
                else:
                    self.hochement='-'
        else:
            if self.tete>-1.6:
                 if random.randint(0,100)==0:
                    self.tete-=0.5
            else:
                 self.hochement='+'
                 
            
        if pyxel.btn(ord('q')):
            self.facing=(self.facing-4)%360
        if pyxel.btn(ord('d')):
            self.facing=(self.facing+4)%360
        if pyxel.btn(ord('z')):
            if self.hochement=='+':
                if self.tete<1.6:
                    self.tete+=0.3
                else:
                    self.hochement='-'
            else:
                if self.tete>-1.6:
                    self.tete-=0.3
                else:
                    self.hochement='+'
            a=self.x
            if self.facing<=90 or self.facing>270:
                if pyxels[self.y//90][self.x//90+1]!=0:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)        
                elif self.x+int(pyxel.cos(self.facing)*self.speed)<(self.x//90)*90+90:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)
                
                else:
                    self.x=(self.x//90)*90+89
                    
            else:
                if pyxels[self.y//90][self.x//90-1]!=0:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)
                elif self.x+int(pyxel.cos(self.facing)*self.speed)>(self.x//90)*90:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)
                else:
                    self.x=(self.x//90)*90
                    
            if self.facing>180:
                if pyxels[self.y//90-1][a//90]!=0:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                elif self.y+int(pyxel.sin(self.facing)*self.speed)>(self.y//90)*90:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                else:
                    self.y=(self.y//90)*90
            else:
                if pyxels[self.y//90+1][a//90]!=0:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                elif self.y+int(pyxel.sin(self.facing)*self.speed)<(self.y//90)*90+90:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                else:
                    self.y=(self.y//90)*90+89
                    
        elif pyxel.btn(ord('s')):
            if self.hochement=='+':
                if self.tete<1.6:
                    self.tete+=0.3
                else:
                    self.hochement='-'
            else:
                if self.tete>-1.6:
                    self.tete-=0.3
                else:
                    self.hochement='+'
            a=self.x
            if self.facing<=90 or self.facing>270:
                if pyxels[self.y//90][self.x//90-1]!=0:
                    self.x-=int(pyxel.cos(self.facing)*self.speed)        
                elif self.x-int(pyxel.cos(self.facing)*self.speed)>(self.x//90)*90:
                    self.x-=int(pyxel.cos(self.facing)*self.speed)
                
                else:
                    self.x=(self.x//90)*90+1
                    
            else:
                if pyxels[self.y//90][self.x//90+1]!=0:
                    self.x-=int(pyxel.cos(self.facing)*self.speed)
                elif self.x-int(pyxel.cos(self.facing)*self.speed)<(self.x//90)*90+90:
                    self.x-=int(pyxel.cos(self.facing)*self.speed)
                else:
                    self.x=(self.x//90)*90+89
                    
            if self.facing>180:
                if pyxels[self.y//90+1][a//90]!=0:
                    self.y-=int(pyxel.sin(self.facing)*self.speed)
                elif self.y-int(pyxel.sin(self.facing)*self.speed)<(self.y//90)*90+90:
                    self.y-=int(pyxel.sin(self.facing)*self.speed)
                else:
                    self.y=(self.y//90)*90+89
            else:
                if pyxels[self.y//90-1][a//90]!=0:
                    self.y-=int(pyxel.sin(self.facing)*self.speed)
                elif self.y-int(pyxel.sin(self.facing)*self.speed)>(self.y//90)*90:
                    self.y-=int(pyxel.sin(self.facing)*self.speed)
                else:
                    self.y=(self.y//90)*90+1        
                    
    def fini(self,pyxels):
        if pyxels[self.y//90][self.x//90]==2:
            return True
        
class App:
    def __init__(self):
        self.labyrinthe=Labyrinthe(5,5)
        self.perso=Personnage()
        self.temps_solution=0
        self.rendu='160'
        self.nb_mob=1
        self.vitesse_mob=2.5
        self.danger=0
        self.instant_lance=0
        self.mode='menu'
        self.parametre=False
        self.taille=5
        self.images={}
        self.images['logo']=[[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9],
 [9,-1,9,-1,-1,-1,-1,-1,-1,9,-1,-1,-1,-1,-1,-1,9],
 [9,-1,9,-1,9,9,9,9,-1,9,-1,9,9,9,9,-1,9],
 [9,-1,9,-1,-1,9,-1,9,-1,9,-1,9,-1,-1,-1,-1,9],
 [9,-1,9,9,-1,9,-1,9,-1,9,-1,9,-1,9,-1,9,9],
 [9,-1,-1,-1,-1,9,-1,9,-1,-1,-1,9,-1,9,-1,-1,9],
 [9,-1,9,9,9,9,-1,9,9,9,9,9,-1,9,9,-1,9],
 [9,-1,-1,-1,-1,-1,-1,-1,9,-1,-1,-1,-1,-1,9,-1,9],
 [9,9,9,9,9,9,9,-1,9,9,9,9,9,9,9,-1,9],
 [9,-1,-1,-1,-1,-1,9,-1,9,-1,-1,-1,-1,-1,-1,-1,9],
 [9,-1,9,9,9,-1,9,9,9,-1,9,9,9,9,9,9,9],
 [9,-1,-1,-1,9,-1,-1,-1,-1,-1,9,-1,-1,-1,-1,-1,9],
 [9,9,9,-1,9,9,9,9,9,9,9,-1,9,9,9,-1,9],
 [9,-1,9,-1,-1,-1,-1,-1,-1,-1,9,-1,9,-1,-1,-1,9],
 [9,-1,9,9,9,9,9,9,9,-1,9,-1,9,-1,9,9,9],
 [9,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,9,-1,-1,-1,9],
 [9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,-1,9]]
        self.images['plume']=[[-1]*15,[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,13,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,13,4,7,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,13,7,4,7,13,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1,13,4,13,13,-1,-1],[-1,-1,-1,-1,-1,-1,-1,13,7,13,4,13,-1,-1,-1],[-1,-1,-1,-1,-1,13,-1,7,13,4,13,7,13,-1,-1],[-1,-1,-1,-1,13,7,13,13,4,13,7,13,-1,-1,-1],[-1,-1,-1,-1,7,7,13,4,13,13,-1,-1,-1,-1,-1],[-1,-1,13,13,7,13,4,7,7,7,13,-1,-1,-1,-1],[-1,-1,-1,13,4,4,13,7,13,-1,-1,-1,-1,-1,-1],[-1,4,4,4,13,13,7,13,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,13,13,-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1]*15]
        self.images['oeuil']=[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, 0, 0, 11, 11,11, 0, 0, -1, -1, -1, -1],[-1, -1, 0, 0, 7, 11, 11, 0, 11, 11, 7, 0, 0, -1, -1],[-1, 0, 13, 7, 11, 11, 0, 0, 0, 11, 11, 7, 13, 0, -1],[0, 7, 7, 7, 11, 11, 0, 0, 0, 11, 11, 7, 7, 7, 0],[0, 7, 7, 7, 11, 11, 0, 0, 0, 11, 11, 7, 7, 7, 0],[-1, 0, 13, 7, 11, 11, 0, 0, 0, 11, 11, 7, 13, 0, -1],[-1, -1, 0, 0, 7, 11, 11, 0, 11, 11, 7, 0, 0, -1, -1],[-1, -1, -1, -1, 0, 0, 11, 11,11, 0, 0, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
        self.images['ampoule']=[[ -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1],[ -1, -1, -1, 0, 0, 10, 10, 10, 10, 0, 0, -1, -1, -1],[ -1, -1, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, -1, -1],[ -1, -1, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, -1, -1],[ -1, 0, 10, 10, 10, 0, 10, 10, 0, 10, 10, 10, 0, -1],[ -1, 0, 10, 10, 0, 10, 0, 0, 10, 0, 10, 10, 0, -1],[ -1, 0, 10, 10, 0, 10, 10, 10, 10, 0, 10, 10, 0, -1],[ -1, 0, 10, 10, 10, 0, 10, 10, 0, 10, 10, 10, 0, -1],[ -1, -1, 0, 10, 10, 0, 10, 10, 0, 10, 10, 0, -1, -1],[ -1, -1, 0, 10, 10, 0, 10, 10, 0, 10, 10, 0, -1, -1],[ -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],[ -1, -1, -1, 0, 13, 13, 13, 13, 13, 13, 0, -1, -1, -1],[ -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1],[ -1, -1, -1, -1, 0, 13, 13, 13, 13, 0, -1, -1, -1, -1],[ -1, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1]]
        self.images['mob']=[[-1, -1, -1, -1, -1, -1, 13, 13, 13, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, 13, 13, 13, 13, 13, -1, -1, -1, -1, -1],[-1, -1, -1, -1, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1, -1],[-1, -1, -1, -1, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, 13, 13, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1],[-1, -1, -1, -1, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1, -1],[-1, -1, -1, -1, 13, 13, 13, 13, 13, 13, 13, -1, -1, -1, -1],[-1, -1, -1, -1, -1, 13, 13, 13, 13, 13, -1, -1, -1, -1, -1],[-1, -1, -1, -1, -1, -1, 13, 13, 13, -1, -1, -1, -1, -1, -1]]
        self.images['lenteur']=[[-1, -1, -1, -1, -1, 6, 6, 6, 6, 6, -1, -1, -1, -1, -1, -1],[-1, -1, -1, -1, 6, 0, 0, 0, 0, 0, 6, -1, -1, -1, -1, -1],[-1, -1, -1, 6, 0, 0, 0, 0, 0, 0, 0, 6, -1, -1, -1, -1],[-1, -1, 6, 0, 0, 7, 7, 0, 0, 0, 0, 0, 6, -1, -1, -1],[-1, -1, 6, 0, 0, 7, 7, 0, 0, 0, 0, 0, 6, -1, -1, -1],[-1, -1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, -1, -1, -1],[-1, -1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, -1, -1, -1],[-1, -1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, -1, -1, -1],[-1, -1, -1, 6, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, -1, -1],[-1, -1, -1, -1, 6, 0, 0, 0, 0, 0, 6, -1, 6, 6, -1, -1],[-1, -1, -1, -1, -1, 6, 6, 6, 6, 6, 0, 6, 0, 0, 6, 6],[-1, 6, 6, 6, -1, -1, -1, -1, -1, -1, 6, 6, 6, 6, -1, 6],[6, 0, 0, 0, 6, -1, -1, -1, -1, -1, -1, -1, -1, 6, 6, 6],[6, 0, 0, 0, 6, -1, -1, -1, -1, -1, -1, -1, -1, 6, 6, -1],[6, 0, 0, 0, 6, -1, 6, 6, -1, 6, 6, -1, 6, 6, -1, -1],[-1, 6, 6, 6, 6, -1, 6, 6, -1, 6, 6, 6, 6, 6, -1, -1]]
        self.images[1]=[[-1, 10, -1], [10, 10, -1], [-1, 10, -1], [-1, 10, -1], [-1, 10, -1]]
        self.images[2]=[[10, 10, -1], [-1, -1, 10], [-1, 10, -1], [10, -1, -1], [10, 10, 10]]
        self.images[3]=[[10, 10, -1], [-1, -1, 10], [-1, 10, -1], [-1, -1, 10], [10, 10, -1]]
        self.images[4]=[[10, -1, 10], [10, -1, 10], [10, 10, 10], [-1, -1, 10], [-1, -1, 10]]
        self.images[5]=[[10, 10, 10], [10, -1, -1], [10, 10, -1], [-1, -1, 10], [10, 10, -1]]
        self.images[6]=[[-1, 10, 10], [10, -1, -1], [10, 10, 10], [10, -1, 10], [10, 10, 10]]
        self.images[7]=[[10, 10, 10], [-1, -1, 10], [-1, 10, -1], [10, -1, -1], [10, -1, -1]]
        self.images[8]=[[10, 10, 10], [10, -1, 10], [10, 10, 10], [10, -1, 10], [10, 10, 10]]
        self.images[9]=[[10, 10, 10], [10, -1, 10], [10, 10, 10], [-1, -1, 10], [10, 10, -1]]
        self.images[0]=[[-1, 10, 10], [10, -1, 10], [10, -1, 10], [10, -1, 10], [10, 10, -1]]
        self.images[':']=[[-1, -1, -1], [-1, 10, -1], [-1, -1, -1], [-1, 10, -1], [-1, -1, -1]]
        self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
        pyxel.init(640,640,'toujours aucune idée',30,pyxel.KEY_ESCAPE)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.mode=='jeu':
            if pyxel.frame_count%int(self.vitesse_mob)==0:
                for i in self.liste_mob:
                    if i.update(self.perso,self.labyrinthe.pyxels):
                        self.danger=6

            if self.danger>0:
                self.danger-=1
            if pyxel.btnp(ord('m')):
                if self.rendu=='160':
                    self.rendu='640'
                else:
                    self.rendu='160'
                
            self.perso.update(self.labyrinthe.pyxels)
                
            if self.perso.fini(self.labyrinthe.pyxels):
                self.mode='menu'
                self.labyrinthe=Labyrinthe(5,5)
                self.perso=Personnage()
                self.vitesse_mob=2.5
                self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
            
            if pyxel.btn(ord('5')):
                self.labyrinthe=Labyrinthe(5,5)
                self.perso=Personnage()
                self.vitesse_mob=2.5
                self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
            if pyxel.btn(ord('0')):
                self.labyrinthe=Labyrinthe(100,100)
                self.perso=Personnage()
                self.vitesse_mob=2.5
                self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
            if self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu==9:
                self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu=None
                self.labyrinthe.load_pyxels()
                if self.perso.speed<67:
                    self.perso.speed+=6
            if self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu==10:
                self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu=None
                self.labyrinthe.load_pyxels()
                if self.perso.lampe<5:
                    self.perso.lampe+=2
            if self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu==14:
                self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu=None
                self.labyrinthe.load_pyxels()
                if self.perso.discretion<40:
                    self.perso.discretion+=5
            if self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu==8:
                self.labyrinthe.tab[self.perso.y//90//15][self.perso.x//90//15].contenu=None
                self.labyrinthe.load_pyxels()
                if self.vitesse_mob<5.3:
                    self.vitesse_mob+=0.7
            for i in self.liste_mob:        
                if abs(i.x-self.perso.x//90)<=1 and abs(i.y-self.perso.y//90)<=1:
                    self.labyrinthe=Labyrinthe(5,5)
                    self.perso=Personnage()
                    self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
        else:
            if self.parametre==False:
                pass
            elif self.parametre==True:
                pass
            
            
            
            
            
    def draw(self):
        '''
        pyxel.text(0,0,'ce',10)
        tab=[]
        for i in range(6):
            tab_2=[]
            for j in range(9):
                a=pyxel.pget(j,i)
                if a==10:
                    tab_2.append(10)
                else:
                    tab_2.append(-1)
            tab.append(tab_2)
        print(tab)
        '''
        if self.mode=='jeu':
            pyxel.cls(0)
            self.labyrinthe.draw(self.perso,self.perso.tete,self.perso.hauteur,self.perso.lampe,self.rendu)
            self.perso.draw_overlay(self.vitesse_mob,self.images['plume'],self.images['ampoule'],self.images['oeuil'],self.images['mob'],self.images['lenteur'])
            affiche_image(self.images[(pyxel.frame_count-self.instant_lance)//18000%10],530,15,5,pyxel.frame_count//30%15+1)
            affiche_image(self.images[(pyxel.frame_count-self.instant_lance)//1800%10],550,15,5,pyxel.frame_count//30%15+1)
            affiche_image(self.images[':'],570,15,5,pyxel.frame_count//30%15+1)
            affiche_image(self.images[(pyxel.frame_count-self.instant_lance)//300%6],590,15,5,pyxel.frame_count//30%15+1)
            affiche_image(self.images[(pyxel.frame_count-self.instant_lance)//30%10],610,15,5,pyxel.frame_count//30%15+1)
            if self.danger>0:
                pyxel.rect(0,0,640,7,8)
                pyxel.rect(0,0,7,640,8)
                pyxel.rect(0,633,640,7,8)
                pyxel.rect(633,0,7,640,8)
                if pyxel.frame_count%24<12:
                    pyxel.rect(7,7,626,4,7)
                    pyxel.rect(7,7,4,626,7)
                    pyxel.rect(7,629,626,4,7)
                    pyxel.rect(629,7,4,626,7)
        else:
            pyxel.cls(0)
            if self.parametre==False:
                if pyxel.frame_count<330:
                    affiche_image(self.images['logo'],110-int(1.17*1.02**pyxel.frame_count),110-int(1.17*1.02**pyxel.frame_count),int(1.02**pyxel.frame_count))
                    pyxel.pset(13,13,13)
                else:
                    pass
            elif self.parametre==True:
                pass
                
def affiche_image(tab,x,y,facteur=1,couleur=-1):
    if facteur>0:
        for i in range(0,len(tab)*facteur,facteur):
            for j in range(0,len(tab[i//facteur])*facteur,facteur):
                if tab[i//facteur][j//facteur]!=-1:
                    if couleur==-1:
                        pyxel.rect(x+j,y+i,facteur,facteur,tab[i//facteur][j//facteur])
                    else:
                        pyxel.rect(x+j,y+i,facteur,facteur,couleur)
App()
