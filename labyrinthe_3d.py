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
        self.N=False
        self.O=False
        self.S=False
        self.E=False

class Labyrinthe:
    def __init__(self, p, q):
        self.nb_lignes=p
        self.nb_colonnes=q
        self.tab=[[Case() for i in range(q)] for i in range(p)]
        self.pyxels=[[1 for i in range(q*15+1)]for j in range(p*15+1)]
        self.creer()
        self.soluce=self.solution().lst
        for i in range(len(self.soluce)):
            self.soluce[i]=(self.soluce[i][1],self.soluce[i][0])
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
        for i in range(q*15-14,q*15):
            self.pyxels[i][p*15]=2
            
    def creer(self):
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

    def solution(self):
        pile=Pile()
        dejavu=[[False for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
        pile.empiler((0,0))
        dejavu[0][0]=True
        while not dejavu[self.nb_lignes-1][self.nb_colonnes-1]:
            (i, j) = pile.depiler()
            if self.tab[i][j].S and not dejavu[i+1][j]:
                pile.empiler((i, j))
                pile.empiler((i+1, j))
                dejavu[i+1][j] = True
            elif self.tab[i][j].E and not dejavu[i][j+1]:
                pile.empiler((i, j))
                pile.empiler((i, j+1))
                dejavu[i][j+1] = True
            elif self.tab[i][j].N and not dejavu[i-1][j]:
                pile.empiler((i, j))
                pile.empiler((i-1, j))
                dejavu[i-1][j] = True
            elif self.tab[i][j].O and not dejavu[i][j-1]:
                pile.empiler((i, j))
                pile.empiler((i, j-1))
                dejavu[i][j-1] = True
        return pile
    
    def draw(self,perso):
        for i in range(160):
            balayage=(perso.facing-80+i)%360
            distance=1
            fin=False
            if True:
                while self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage))*distance]==1 and distance<80:
                    distance+=1
                if self.pyxels[perso.y//90+int(pyxel.sin(balayage)*distance)][perso.x//90+int(pyxel.cos(balayage))*distance]==2:
                    fin=True
                if distance<20:
                    for k in range((160-(80-distance)*2)//2,(160-(80-distance)*2)//2+(80-distance)*2):
                        if not fin:
                            pyxel.rect(i,k,1,1,7)
                        else:
                            pyxel.rect(i,k,1,1,11)
                    for k in range((160-(80-distance)*2)//2+(80-distance)*2,160):
                        pyxel.rect(i,k,1,1,13)
                elif distance<40:
                    for k in range((160-(80-distance)*2)//2,(160-(80-distance)*2)//2+(80-distance)*2):
                        if not fin:
                            pyxel.rect(i,k,1,1,6)
                        else:
                            pyxel.rect(i,k,1,1,11)
                    for k in range((160-(80-distance)*2)//2+(80-distance)*2,160):
                        pyxel.rect(i,k,1,1,13)
                elif distance<60:
                    for k in range((160-(80-distance)*2)//2,(160-(80-distance)*2)//2+(80-distance)*2):
                        if not fin:
                            pyxel.rect(i,k,1,1,5)
                        else:
                            pyxel.rect(i,k,1,1,11)
                    for k in range((160-(80-distance)*2)//2+(80-distance)*2,160):
                        pyxel.rect(i,k,1,1,13)
                elif distance<80:
                    for k in range((160-(80-distance)*2)//2,(160-(80-distance)*2)//2+(80-distance)*2):
                        if not fin:
                            pyxel.rect(i,k,1,1,1)
                        else:
                            pyxel.rect(i,k,1,1,11)
                    for k in range((160-(80-distance)*2)//2+(80-distance)*2,160):
                        pyxel.rect(i,k,1,1,13)
                else:
                    for k in range(80,160):
                        pyxel.rect(i,k,1,1,13)
                        
        for i in range(len(self.pyxels)):
            for j in range(len(self.pyxels[i])):          
                if self.pyxels[i][j]!=1:
                    if self.pyxels[i][j]==0:
                        pyxel.rect(j,i,1,1,2)
                    else:
                        pyxel.rect(j,i,1,1,11)
        pyxel.rect(perso.x//90,perso.y//90,1,1,14)   
                    
            
                    
class Personnage:
    def __init__(self):
        self.x=180
        self.y=180
        self.facing=0
        self.speed=45
        
    def draw(self):
        pyxel.rect(self.x//90,self.y//90,1,1,14)
        
    def update(self,pyxels):
        if pyxel.btn(ord('q')):
            self.facing=(self.facing-5)%360
        if pyxel.btn(ord('d')):
            self.facing=(self.facing+5)%360
        if pyxel.btn(ord('o')):
            self.speed=(self.speed-1)%90
        if pyxel.btn(ord('l')):
            self.speed=(self.speed+1)%90
        if pyxel.btn(ord('z')):
            a=self.x
            if self.facing<=90 or self.facing>270:
                if pyxels[self.y//90][self.x//90+int(pyxel.cos(self.facing)*self.speed)//90+1]!=0:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)        
                elif self.x+int(pyxel.cos(self.facing)*self.speed)<(self.x//90)*90+90:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)
                
                else:
                    self.x=(self.x//90)*90+89
                    
            else:
                if pyxels[self.y//90][self.x//90+int(pyxel.cos(self.facing)*self.speed)//90]!=0:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)
                elif self.x+int(pyxel.cos(self.facing)*self.speed)>(self.x//90)*90:
                    self.x+=int(pyxel.cos(self.facing)*self.speed)
                else:
                    self.x=(self.x//90)*90
                    
            if self.facing>180:
                if pyxels[self.y//90+int(pyxel.sin(self.facing)*self.speed)//90][a//90]!=0:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                elif self.y+int(pyxel.sin(self.facing)*self.speed)>(self.y//90)*90:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                else:
                    self.y=(self.y//90)*90
            else:
                if pyxels[self.y//90+int(pyxel.sin(self.facing)*self.speed)//90+1][a//90]!=0:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                elif self.y+int(pyxel.sin(self.facing)*self.speed)<(self.y//90)*90+90:
                    self.y+=int(pyxel.sin(self.facing)*self.speed)
                else:
                    self.y=(self.y//90)*90+89
                    
    def fini(self,pyxels):
        if pyxels[self.y//90][self.x//90]==2:
            return True
        
class App:
    def __init__(self):
        self.labyrinthe=Labyrinthe(5,5)
        self.perso=Personnage()
        self.temps_solution=0
        pyxel.init(160,160)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.perso.update(self.labyrinthe.pyxels)
        if self.perso.fini(self.labyrinthe.pyxels):
            self.labyrinthe=Labyrinthe(5,5)
            self.perso=Personnage()
        if pyxel.btn(ord('1')):
            self.labyrinthe=Labyrinthe(1,1)
            self.perso=Personnage()
        if pyxel.btn(ord('2')):
            self.labyrinthe=Labyrinthe(2,2)
            self.perso=Personnage()
        if pyxel.btn(ord('3')):
            self.labyrinthe=Labyrinthe(3,3)
            self.perso=Personnage()
        if pyxel.btn(ord('4')):
            self.labyrinthe=Labyrinthe(4,4)
            self.perso=Personnage()
        if pyxel.btn(ord('5')):
                self.labyrinthe=Labyrinthe(5,5)
                self.perso=Personnage()
        if pyxel.btn(ord('6')):
            self.labyrinthe=Labyrinthe(6,6)
            self.perso=Personnage()
        if pyxel.btn(ord('7')):
            self.labyrinthe=Labyrinthe(7,7)
            self.perso=Personnage()
        if pyxel.btn(ord('8')):
            self.labyrinthe=Labyrinthe(8,8)
            self.perso=Personnage()
        if pyxel.btn(ord('9')):
            self.labyrinthe=Labyrinthe(9,9)
            self.perso=Personnage()
        if pyxel.btn(ord('0')):
            self.labyrinthe=Labyrinthe(10,10)
            self.perso=Personnage()
            
    def draw(self):
        pyxel.cls(0)
        self.labyrinthe.draw(self.perso)
        if pyxel.btn(112):
            self.labyrinthe.draw_solution()
         

App()
'''
l=Labyrinthe(10,10)
print(l.pyxels)
'''