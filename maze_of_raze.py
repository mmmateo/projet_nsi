import pyxel
import random
import banque_d_image

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
        '''constructeur de la classe labyrinthe placant les bonus de manière aléatoire, avec p la longueur et q la largeur du labyrinthe en  nombre de cases'''
        self.nb_lignes=p
        self.nb_colonnes=q
        self.tab=[[Case() for i in range(q)] for i in range(p)] 
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
        '''crée un tableau de pixels représentant la labyrinthe, avec chaque case de taille 15 fois 15 pixels, des 0 pour les murs, des 1 pour les pixels vides, des 2 pour les pixels de l'arrivée et d'autres chiffres pour les différents bonus'''
        self.pyxels=[[1 for i in range(self.nb_colonnes*15+1)]for j in range(self.nb_lignes*15+1)]
        for k in range(len(self.tab)):
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
        '''permet de creer un labyrinthe parfait a partir d'un tableau de cases de la classe Case'''
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
    
    def draw(self,perso,tete,lampe,rendu):
        '''Dessine le rendu graphique du labyrinthe grâce au ray-casting en fonction de la position du personnage, la hauteur de sa tete, la distance à laquelle il voit et du type de couleurs'''
        if True:
            a=int((160-(pyxel.atan2(20,2*(40-lampe)))*2)//2+(pyxel.atan2(20,2*(40-lampe)))*2)
            pyxel.rect(0,(max(a,87-lampe))*4+int(tete)*2-2,640,(100+int(tete)-lampe-max(a,87-lampe))*4-int(tete)*2+2,2)
            pyxel.rect(0,(100+int(tete)-lampe)*4,640,40,8)
            pyxel.rect(0,(110+int(tete)-lampe)*4,640,80,14)
            pyxel.rect(0,(130+int(tete)-lampe)*4,640,(200-130+int(tete)-lampe)*4+4,15)
            if rendu=='640':
                pyxel.rect(0,(max(a,87-lampe))*4+int(tete)*2-2,640,(100+int(tete)-lampe-max(a,87-lampe))*4-int(tete)*2+2,8)
                for k in range((max(a,87-lampe))*4+int(tete)*2-2,(100+int(tete)-lampe)*4+2):
                    for l in range(k%2,640+k%2,2):
                        pyxel.pset(l,k,0)
                for k in range((110+int(tete)-lampe)*4,(120+int(tete)-lampe)*4):
                    for l in range(k%2,640+k%2,2):
                        pyxel.pset(l,k,8)
                for k in range((130+int(tete)-lampe)*4,(140+int(tete)-lampe)*4):
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
                        pyxel.rect(i*4,(int((160-(pyxel.atan2(20,2*distance))*2)//2))*4+2*int(tete),4,4*(int((pyxel.atan2(20,2*distance))*2))+int(tete)*2,couleur1)
                                
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
                        pyxel.rect(i*4,(int((160-(pyxel.atan2(20,2*distance))*2)//2))*4+2*int(tete),4,4*(int((pyxel.atan2(20,2*distance))*2))+int(tete)*2,couleur1[0])
                        if couleur1[0]!=couleur1[1]:                           
                            for k in range((int((160-(pyxel.atan2(20,2*distance))*2)//2))*4+2*int(tete),(int((160-(pyxel.atan2(20,2*distance))*2)//2+(pyxel.atan2(20,2*distance))*2))*4+int(tete)*3):
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
        '''constructeur de la classe mob, place la mob en position x,y dans le tableau de pixel du labyrinthe'''
        self.x=x
        self.y=y
        self.direction=random.randint(1,8)
        pyxels[y][x]=5
        
    def cherche_perso(self,perso,pyxels):
        '''cherche le personnage dans un maximum de déplacement définit par l'attribut discrection du personnage, renvoie le pixel ou aller pour arriver le plus rapidement a lui si il est a sa portée et None sinon '''
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
        '''déplace le mob de une case vers le personnage si il est a sa portée, aléatoirement sinon, en mettant a jour le tableau de pixels du labyrinthe en conséquences'''
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
        '''constructeur de la classe Personnage ave cles attibuts x et y pour sa position,
            facing pour la direction ou il regarde, speed pour la vitesse, tete pour la hauteur de sa tete,
            hochement pour savoir dans quelle direction vas bouger sa tete, lampe pour savoir a quelle distance il voit
            et discretion pour savoir a quelle distance il peut etre vu par les monstres de la classe mob'''
        self.x=180
        self.y=180
        self.facing=45
        self.speed=25
        self.hochement='+'
        self.position='debout'
        self.tete=0
        self.lampe=-15
        self.discretion=0
    
    def draw_overlay(self,vitesse_mob,plume,ampoule,oeuil,mob,lenteur):
        '''dessine l'overlay du personnage (affichage du niveau des bonus et du temps) avec des images du module 'banque_d_image' '''
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
        '''met a jour le personnage en fonction des entrées du joueur et de l'aléatoire'''
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
        '''renvoie True si le personnage est sur des pixels de valeur 2 du tableau de pixel du labyrinthe , False sinon
        (True si le personnage a atteint la ligne d'arrivée, False sinon) '''
        if pyxels[self.y//90][self.x//90]==2:
            return True
        return False
        
class App:
    def __init__(self):
        '''constructeur de la classe App avec les attributs laburinthe de la classe Labyrinthe, perso de la classe Personnage,
            rendu un entier définnissant le nombre de couleurs possibles, nb_mob deffinissant le nombre de monstres de la classe
            Monstre dans le tableau liste_mob, vitesse_mob un float définissant leur vitesse,danger un entier définissant si l'on est
            poursuivi par un monstre ou non, instant_lance, un entier vallant le nombre de frame écoulée avant de lancer la partie,
            mode, un string définissant dans quel mode on se situe, temps_fin ,
            un entier vallant le nombre de frame ecoulée avant la fin de la partie et taille, definissant la taille du labyrinthe
            et initialise et lance le module pyxel avec les fonction update et draw de la classe App
            '''
        
        self.labyrinthe=Labyrinthe(5,5)
        self.perso=Personnage()
        self.rendu='160'
        self.nb_mob=1
        self.vitesse_mob=2.5
        self.danger=0
        self.instant_lance=0
        self.mode='menu'
        self.temps_fin=0
        self.taille=5
        self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
        pyxel.init(640,640,'Maze of rays',30)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        '''met a jour les éléments du jeu en fonction du mode dans lequel on est'''
        if self.mode=='jeu':
            if pyxel.frame_count%int(self.vitesse_mob)==0:
                for i in self.liste_mob:
                    if i.update(self.perso,self.labyrinthe.pyxels):
                        self.danger=6
                        
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.temps_fin=pyxel.frame_count
                self.mode='pause'
                pyxel.mouse(True)
                
            if self.danger>0:
                self.danger-=1
                
            self.perso.update(self.labyrinthe.pyxels)
                
            if self.perso.fini(self.labyrinthe.pyxels):
                pyxel.mouse(True)
                self.temps_fin=pyxel.frame_count-self.instant_lance
                self.instant_lance=pyxel.frame_count
                self.mode='win'
                self.labyrinthe=Labyrinthe(self.taille,self.taille)
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
                    self.instant_lance=pyxel.frame_count
                    self.mode='loose'
                    
        elif self.mode=='menu':
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                pyxel.quit()
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>200 and pyxel.mouse_y<300:
                self.mode='jeu'
                self.labyrinthe=Labyrinthe(self.taille,self.taille)
                self.perso=Personnage()
                self.vitesse_mob=2.5
                self.instant_lance=pyxel.frame_count
                pyxel.mouse(False)
                self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>350 and pyxel.mouse_y<450:
                self.mode='parametres'
        elif self.mode=='parametres':
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                self.mode='menu'
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>21 and pyxel.mouse_x<109 and pyxel.mouse_y>281 and pyxel.mouse_y<369 and self.taille>2:
                self.taille-=1
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>531 and pyxel.mouse_x<619 and pyxel.mouse_y>281 and pyxel.mouse_y<369 and self.taille<999:
                self.taille+=1
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>21 and pyxel.mouse_x<109 and pyxel.mouse_y>411 and pyxel.mouse_y<499 and self.nb_mob>0:
                self.nb_mob-=1
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>531 and pyxel.mouse_x<619 and pyxel.mouse_y>411 and pyxel.mouse_y<499 and self.nb_mob<99:
                self.nb_mob+=1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>21 and pyxel.mouse_x<109 and pyxel.mouse_y>148 and pyxel.mouse_y<236:
                if self.rendu=='160':
                    self.rendu='640'
                else:
                    self.rendu='160'
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>531 and pyxel.mouse_x<619 and pyxel.mouse_y>148 and pyxel.mouse_y<236:
                if self.rendu=='160':
                    self.rendu='640'
                else:
                    self.rendu='160'
                        
        elif self.mode=='loose' or self.mode=='win':
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                self.mode='menu'
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>66 and pyxel.mouse_x<584 and pyxel.mouse_y>401 and pyxel.mouse_y<489:
                self.mode='jeu'
                self.instant_lance=pyxel.frame_count
                pyxel.mouse(False)
                self.vitesse_mob=2.5
                self.labyrinthe=Labyrinthe(self.taille,self.taille)
                self.perso=Personnage()
                self.liste_mob=[Mob(random.randint(2,self.labyrinthe.nb_lignes)*15-1,random.randint(2,self.labyrinthe.nb_colonnes)*15-1,self.labyrinthe.pyxels) for i in range(1,self.nb_mob+1)]
        
        elif self.mode=='pause':
            if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>200 and pyxel.mouse_y<300) or pyxel.btnp(pyxel.KEY_SPACE):
                self.mode='jeu'
                pyxel.mouse(False)
                self.instant_lance=self.instant_lance+(pyxel.frame_count-self.temps_fin)
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                self.mode='menu'
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>350 and pyxel.mouse_y<450:
                self.mode='touches'
                
        elif self.mode=='touches':
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                self.mode='pause'
                
    def draw(self):
        '''dessinne le rendu du jeu sur le module pyxel en fonction du mode dans lequel on est et grace aux tableaux du module 'banque_d_image'
        et a la fonction affiche_image'''
        if self.mode=='jeu':
            pyxel.cls(0)
            self.labyrinthe.draw(self.perso,self.perso.tete,self.perso.lampe,self.rendu)
            self.perso.draw_overlay(self.vitesse_mob,banque_d_image.images['plume'],banque_d_image.images['ampoule'],banque_d_image.images['oeuil'],banque_d_image.images['mob'],banque_d_image.images['lenteur'])
            affiche_image(banque_d_image.images[(pyxel.frame_count-self.instant_lance)//18000%10],530,15,5,pyxel.frame_count//30%15+1)
            affiche_image(banque_d_image.images[(pyxel.frame_count-self.instant_lance)//1800%10],550,15,5,pyxel.frame_count//30%15+1)
            affiche_image(banque_d_image.images[':'],570,15,5,pyxel.frame_count//30%15+1)
            affiche_image(banque_d_image.images[(pyxel.frame_count-self.instant_lance)//300%6],590,15,5,pyxel.frame_count//30%15+1)
            affiche_image(banque_d_image.images[(pyxel.frame_count-self.instant_lance)//30%10],610,15,5,pyxel.frame_count//30%15+1)
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
        elif self.mode=='menu':
            pyxel.cls(0)
            if pyxel.frame_count<330:
                affiche_image(banque_d_image.images['logo'],110-int(1.17*1.02**pyxel.frame_count),110-int(1.17*1.02**pyxel.frame_count),int(1.02**pyxel.frame_count),1)
            else:
                pyxel.mouse(True)
                affiche_image(banque_d_image.images['titre'],90,30,10)
                affiche_image(banque_d_image.images['M'],70,30,3)
                if pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>200 and pyxel.mouse_y<300:
                    pyxel.rect(100,200,440,100,11)
                    pyxel.circ(100,250,49,11)
                    pyxel.circ(540,250,49,11)
                else:
                    pyxel.rect(100,200,440,100,10)
                    pyxel.circ(100,250,49,10)
                    pyxel.circ(540,250,49,10)
                affiche_image(banque_d_image.images['commencer'],115,214,12,7)
                if pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>350 and pyxel.mouse_y<450:
                    pyxel.rect(100,350,440,100,12)
                    pyxel.circ(100,400,49,12)
                    pyxel.circ(540,400,49,12)
                else:
                    pyxel.rect(100,350,440,100,10)
                    pyxel.circ(100,400,49,10)
                    pyxel.circ(540,400,49,10)
                affiche_image(banque_d_image.images['parametres'],90,364,12,7)
                if pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                    pyxel.rect(200,525,240,75,8)
                    pyxel.circ(200,562,37,8)
                    pyxel.circ(440,562,37,8)
                else:
                    pyxel.rect(200,525,240,75,10)
                    pyxel.circ(200,562,37,10)
                    pyxel.circ(440,562,37,10)
                affiche_image(banque_d_image.images['quitter'],214,540,8,7)
        elif self.mode=='parametres':
            pyxel.cls(0)
            affiche_image(banque_d_image.images['titre'],90,30,10)
            affiche_image(banque_d_image.images['M'],70,30,3)
            pyxel.rect(170,410,300,90,10)
            pyxel.circ(170,455,44,10)
            pyxel.circ(470,455,44,10)
            if self.nb_mob<99:
                if pyxel.mouse_x>531 and pyxel.mouse_x<619 and pyxel.mouse_y>411 and pyxel.mouse_y<499:
                    pyxel.circ(575,455,44,3)
                else:
                    pyxel.circ(575,455,44,11)
            else:
                pyxel.circ(575,455,44,13)
            if self.nb_mob>0:
                if pyxel.mouse_x>21 and pyxel.mouse_x<109 and pyxel.mouse_y>411 and pyxel.mouse_y<499:
                    pyxel.circ(65,455,44,4)
                else:
                    pyxel.circ(65,455,44,8)
            else:
                pyxel.circ(65,455,44,13)
            affiche_image(banque_d_image.images['+'],553,432,15,7)
            affiche_image(banque_d_image.images['-'],43,432,15,7)
            affiche_image(banque_d_image.images['monstres'],170,435,7,7)
            affiche_image(banque_d_image.images[':'],390,430,10,7)
            affiche_image(banque_d_image.images[self.nb_mob//10],420,432,9,7)
            affiche_image(banque_d_image.images[self.nb_mob%10],460,432,9,7)
            pyxel.rect(170,280,300,90,10)
            pyxel.circ(170,325,44,10)
            pyxel.circ(470,325,44,10)
            if self.taille<999:
                if pyxel.mouse_x>531 and pyxel.mouse_x<619 and pyxel.mouse_y>281 and pyxel.mouse_y<369:
                    pyxel.circ(575,325,44,3)
                else:
                    pyxel.circ(575,325,44,11)
            else:
                pyxel.circ(575,325,44,13)
            if self.taille>2:
                if pyxel.mouse_x>21 and pyxel.mouse_x<109 and pyxel.mouse_y>281 and pyxel.mouse_y<369:
                    pyxel.circ(65,325,44,4)
                else:
                    pyxel.circ(65,325,44,8)
            else:
                pyxel.circ(65,325,44,13)
            affiche_image(banque_d_image.images['+'],553,302,15,7)
            affiche_image(banque_d_image.images['-'],43,302,15,7)
            affiche_image(banque_d_image.images['taille'],170,305,7,7)
            affiche_image(banque_d_image.images[':'],330,300,10,7)
            affiche_image(banque_d_image.images[self.taille//100],370,302,9,7)
            affiche_image(banque_d_image.images[(self.taille//10)%10],400,302,9,7)
            affiche_image(banque_d_image.images[self.taille%10],430,302,9,7)
            pyxel.rect(170,148,300,90,10)
            pyxel.circ(170,192,44,10)
            pyxel.circ(470,192,44,10)
            if pyxel.mouse_x>531 and pyxel.mouse_x<619 and pyxel.mouse_y>148 and pyxel.mouse_y<236:
                pyxel.circ(575,192,44,3)
            else:
                pyxel.circ(575,192,44,11)
            if pyxel.mouse_x>21 and pyxel.mouse_x<109 and pyxel.mouse_y>148 and pyxel.mouse_y<236:
                pyxel.circ(65,192,44,3)
            else:
                pyxel.circ(65,192,44,11)
            affiche_image(banque_d_image.images['>'],560,162,12,7)
            affiche_image(banque_d_image.images['<'],42,162,12,7)
            affiche_image(banque_d_image.images['couleur'],170,173,7,7)
            affiche_image(banque_d_image.images[':'],360,170,10,7)
            if self.rendu=='160':
                affiche_image(banque_d_image.images[1],410,173,7,7)
                affiche_image(banque_d_image.images[6],439,173,7,7)
            else:
                affiche_image(banque_d_image.images[1],400,173,7,7)
                affiche_image(banque_d_image.images[3],429,173,7,7)
                affiche_image(banque_d_image.images[6],457,173,7,7)
            if pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                pyxel.rect(200,525,240,75,11)
                pyxel.circ(200,562,37,11)
                pyxel.circ(440,562,37,11)
            else:
                pyxel.rect(200,525,240,75,10)
                pyxel.circ(200,562,37,10)
                pyxel.circ(440,562,37,10)
            affiche_image(banque_d_image.images['menu'],260,542,8,7)
                
        elif self.mode=='loose':
            pyxel.cls(0)
            pyxel.rect(150,0,5,(pyxel.frame_count-self.instant_lance)*2,8)
            pyxel.rect(50,0,4,(pyxel.frame_count-self.instant_lance)*6,8)
            pyxel.rect(215,0,2,(pyxel.frame_count-self.instant_lance)*4,8)
            pyxel.rect(400,0,1,(pyxel.frame_count-self.instant_lance),8)
            pyxel.rect(500,0,3,(pyxel.frame_count-self.instant_lance)*5,8)
            pyxel.rect(580,0,6,(pyxel.frame_count-self.instant_lance)*3,8)
            if pyxel.frame_count-self.instant_lance<45:
                affiche_image(banque_d_image.images['coeur_vivant'],212,190,12)
            elif pyxel.frame_count-self.instant_lance<90:
                affiche_image(banque_d_image.images['coeur_mort'],200,190,12)
            else:
                pyxel.mouse(True)
                affiche_image(banque_d_image.images['vous etes'],135,10,10,7)
                affiche_image(banque_d_image.images['mort'],205,90,10,7)
                affiche_image(banque_d_image.images['coeur_mort'],200,190,12)
                if pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                        pyxel.rect(200,525,240,75,5)
                        pyxel.circ(200,562,37,5)
                        pyxel.circ(440,562,37,5)
                else:
                    pyxel.rect(200,525,240,75,9)
                    pyxel.circ(200,562,37,9)
                    pyxel.circ(440,562,37,9)
                affiche_image(banque_d_image.images['menu'],260,542,8,7)
                if pyxel.mouse_x>66 and pyxel.mouse_x<584 and pyxel.mouse_y>401 and pyxel.mouse_y<489:
                    pyxel.rect(100,400,440,90,3)
                    pyxel.circ(100,445,44,3)
                    pyxel.circ(540,445,44,3)
                else: 
                    pyxel.rect(100,400,440,90,2)
                    pyxel.circ(100,445,44,2)
                    pyxel.circ(540,445,44,2)
                affiche_image(banque_d_image.images['reessayer'],125,411,11,7)
                
        elif self.mode=='win':
            pyxel.cls(12)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//29)%4)],135,2*(pyxel.frame_count-self.instant_lance)%940-400,10,8)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//20)%4)],35,3*(pyxel.frame_count-self.instant_lance)%990-350,10,10)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//12)%4)],200,5*(pyxel.frame_count-self.instant_lance)%1140-500,10,9)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//15)%4)],385,4*(pyxel.frame_count-self.instant_lance)%744-104,10,10)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//31)%4)],485,2*(pyxel.frame_count-self.instant_lance)%670-30,10,8)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//60)%4)],565,(pyxel.frame_count-self.instant_lance)%670-30,10,9)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//62)%4)],144,(pyxel.frame_count-self.instant_lance)%645-5,10,10)
            affiche_image(banque_d_image.images['confeti_'+str((pyxel.frame_count//19)%4)],300,(3*(pyxel.frame_count-self.instant_lance)%840-200),10,10)
            if pyxel.frame_count-self.instant_lance<self.temps_fin//30:
                affiche_image(banque_d_image.images[((pyxel.frame_count-self.instant_lance)//600)%10],175,210,15,0)
                affiche_image(banque_d_image.images[((pyxel.frame_count-self.instant_lance)//60)%10],235,210,15,0)
                affiche_image(banque_d_image.images[':'],295,210,15,0)
                affiche_image(banque_d_image.images[((pyxel.frame_count-self.instant_lance)//10)%6],355,210,15,0)
                affiche_image(banque_d_image.images[(pyxel.frame_count-self.instant_lance)%10],415,210,15,0)
            else:
                pyxel.mouse(True)
                affiche_image(banque_d_image.images['vous avez'],145,10,10,7)
                affiche_image(banque_d_image.images['gagne'],210,90,10,7)
                affiche_image(banque_d_image.images[((self.temps_fin//30)//600)%10],175,210,15,0)
                affiche_image(banque_d_image.images[((self.temps_fin//30)//60)%10],235,210,15,0)
                affiche_image(banque_d_image.images[':'],295,210,15,0)
                affiche_image(banque_d_image.images[((self.temps_fin//30)//10)%6],355,210,15,0)
                affiche_image(banque_d_image.images[(self.temps_fin//30)%10],415,210,15,0)
                if pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                        pyxel.rect(200,525,240,75,14)
                        pyxel.circ(200,562,37,14)
                        pyxel.circ(440,562,37,14)
                else:
                    pyxel.rect(200,525,240,75,10)
                    pyxel.circ(200,562,37,10)
                    pyxel.circ(440,562,37,10)
                affiche_image(banque_d_image.images['menu'],260,542,8,7)
                
                if pyxel.mouse_x>66 and pyxel.mouse_x<584 and pyxel.mouse_y>401 and pyxel.mouse_y<489:
                    pyxel.rect(100,400,440,90,11)
                    pyxel.circ(100,445,44,11)
                    pyxel.circ(540,445,44,11)
                else: 
                    pyxel.rect(100,400,440,90,8)
                    pyxel.circ(100,445,44,8)
                    pyxel.circ(540,445,44,8)
                affiche_image(banque_d_image.images['reessayer'],120,411,11,7)
        
        elif self.mode=='pause':
            pyxel.cls(0)
            self.labyrinthe.draw(self.perso,self.perso.tete,self.perso.lampe,self.rendu)
            self.perso.draw_overlay(self.vitesse_mob,banque_d_image.images['plume'],banque_d_image.images['ampoule'],banque_d_image.images['oeuil'],banque_d_image.images['mob'],banque_d_image.images['lenteur'])
            affiche_image(banque_d_image.images[(self.temps_fin-self.instant_lance)//18000%10],530,15,5,self.temps_fin//30%15+1)
            affiche_image(banque_d_image.images[(self.temps_fin-self.instant_lance)//1800%10],550,15,5,self.temps_fin//30%15+1)
            affiche_image(banque_d_image.images[':'],570,15,5,self.temps_fin//30%15+1)
            affiche_image(banque_d_image.images[(self.temps_fin-self.instant_lance)//300%6],590,15,5,self.temps_fin//30%15+1)
            affiche_image(banque_d_image.images[(self.temps_fin-self.instant_lance)//30%10],610,15,5,self.temps_fin//30%15+1)
            affiche_image(banque_d_image.images['pause'],180,80,14,7)
            if pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>200 and pyxel.mouse_y<300:
                pyxel.rect(100,200,440,100,11)
                pyxel.circ(100,250,49,11)
                pyxel.circ(540,250,49,11)
            else:
                pyxel.rect(100,200,440,100,3)
                pyxel.circ(100,250,49,3)
                pyxel.circ(540,250,49,3)
            affiche_image(banque_d_image.images['reprendre'],115,214,12,7)
            
            if pyxel.mouse_x>50 and pyxel.mouse_x<590 and pyxel.mouse_y>350 and pyxel.mouse_y<450:
                pyxel.rect(100,350,440,100,10)
                pyxel.circ(100,400,49,10)
                pyxel.circ(540,400,49,10)
            else:
                pyxel.rect(100,350,440,100,9)
                pyxel.circ(100,400,49,9)
                pyxel.circ(540,400,49,9)
            affiche_image(banque_d_image.images['touches'],155,364,12,7)
            
            if pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                pyxel.rect(200,525,240,75,12)
                pyxel.circ(200,562,37,12)
                pyxel.circ(440,562,37,12)
            else:
                pyxel.rect(200,525,240,75,5)
                pyxel.circ(200,562,37,5)
                pyxel.circ(440,562,37,5)
            affiche_image(banque_d_image.images['menu'],255,540,8,7)
            
        elif self.mode=='touches':
           pyxel.cls(0)
           affiche_image(banque_d_image.images['titre'],90,30,10)
           affiche_image(banque_d_image.images['M'],70,30,3)
           if pyxel.mouse_x>163 and pyxel.mouse_x<477 and pyxel.mouse_y>525 and pyxel.mouse_y<600:
                pyxel.rect(200,525,240,75,8)
                pyxel.circ(200,562,37,8)
                pyxel.circ(440,562,37,8)
           else:
                pyxel.rect(200,525,240,75,10)
                pyxel.circ(200,562,37,10)
                pyxel.circ(440,562,37,10)
           affiche_image(banque_d_image.images['retour'],230,540,8,7)
           affiche_image(banque_d_image.images['avancer'],150,120,7,7)
           affiche_image(banque_d_image.images[':'],373,120,8,7)
           affiche_image(banque_d_image.images['reculer'],150,200,7,7)
           affiche_image(banque_d_image.images[':'],373,200,8,7)
           affiche_image(banque_d_image.images['gauche'],40,280,7,7)
           affiche_image(banque_d_image.images[':'],518,280,8,7)
           affiche_image(banque_d_image.images['droite'],40,360,7,7)
           affiche_image(banque_d_image.images[':'],518,360,8,7)
           affiche_image(banque_d_image.images['t_pause'],40,440,7,7)
           affiche_image(banque_d_image.images[':'],377,440,8,7)
           
def affiche_image(tab,x,y,facteur=1,couleur=-1):
    '''fonction qui affiche grace a la bibliotheque pyxel un tableau python en deux dimensions en position x,y
    avec un grossissent entier égal a 'facteur' et en couleur 'couleur' de la bibliotheque pyxel si elle est renseignée'''
    if facteur>0:
        for i in range(0,len(tab)*facteur,facteur):
            for j in range(0,len(tab[i//facteur])*facteur,facteur):
                if tab[i//facteur][j//facteur]!=-1:
                    if couleur==-1:
                        pyxel.rect(x+j,y+i,facteur,facteur,tab[i//facteur][j//facteur])
                    else:
                        pyxel.rect(x+j,y+i,facteur,facteur,couleur)
                        
App()

