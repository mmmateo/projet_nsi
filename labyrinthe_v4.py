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
        self.creer()
        self.soluce=self.solution().lst
        for i in range(len(self.soluce)):
            self.soluce[i]=(self.soluce[i][1],self.soluce[i][0])
        
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
    
    def draw(self):
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):          
                if self.tab[i][j].N==False:
                    pyxel.rect(j*15,i*15,16,1,0)
                if self.tab[i][j].S==False:
                    pyxel.rect(j*15,(i+1)*15,16,1,0)
                if self.tab[i][j].E==False:
                    pyxel.rect((j+1)*15,i*15,1,16,0)
                if self.tab[i][j].O==False:
                    pyxel.rect((j)*15,i*15,1,16,0)
        
        pyxel.rect(0,1,1,4,0)
      
    def draw_solution(self):
        for i in range(len(self.soluce)):
            if i!=len(self.soluce)-1:
                l=(self.soluce[i][0]-self.soluce[i+1][0],self.soluce[i][1]-self.soluce[i+1][1])
                if l==(-1,0):
                    pyxel.rect(self.soluce[i][0]*15+7,self.soluce[i][1]*15+7,17,2,8)
                if l==(1,0):
                    pyxel.rect(self.soluce[i+1][0]*15+7,self.soluce[i+1][1]*15+7,17,2,8)
                if l==(0,-1):
                    pyxel.rect(self.soluce[i][0]*15+7,self.soluce[i][1]*15+7,2,17,8)
                if l==(0,1):
                    pyxel.rect(self.soluce[i+1][0]*15+7,self.soluce[i+1][1]*15+7,2,17,8)
                    
class Personnage:
    def __init__(self):
        self.x=90
        self.y=180
        self.facing=0
        self.s=45
        
    def draw(self):
        pyxel.rect(self.x//90,self.y//90,1,1,14)
        
    def update(self):
        if pyxel.btn(ord('q')):
            self.facing=(self.facing-5)%360
        if pyxel.btn(ord('d')):
            self.facing=(self.facing+5)%360
        if pyxel.btn(ord('o')):
            self.s=(self.s-1)%90
        if pyxel.btn(ord('l')):
            self.s=(self.s+1)%90
        if pyxel.btn(ord('z')):
            a=self.x
            if self.facing<=90 or self.facing>270:
                if pyxel.pget(self.x//90+int(pyxel.cos(self.facing)*self.s)//90+1,self.y//90)!=0:
                    self.x+=int(pyxel.cos(self.facing)*self.s)
                elif self.x+int(pyxel.cos(self.facing)*self.s)<(self.x//90)*90+90:
                    self.x+=int(pyxel.cos(self.facing)*self.s)
                else:
                    self.x=(self.x//90)*90+89
            else:
                if pyxel.pget(self.x//90+int(pyxel.cos(self.facing)*self.s)//90,self.y//90)!=0:
                    self.x+=int(pyxel.cos(self.facing)*self.s)
                elif self.x+int(pyxel.cos(self.facing)*self.s)>(self.x//90)*90:
                    self.x+=int(pyxel.cos(self.facing)*self.s)
                else:
                    self.x=(self.x//90)*90
                    
            if self.facing>180:
                if pyxel.pget(a//90,self.y//90+int(pyxel.sin(self.facing)*self.s)//90)!=0:
                    self.y+=int(pyxel.sin(self.facing)*self.s)
                elif self.y+int(pyxel.sin(self.facing)*self.s)>(self.y//90)*90:
                    self.y+=int(pyxel.sin(self.facing)*self.s)
                else:
                    self.y=(self.y//90)*90
            else:
                if pyxel.pget(a//90,self.y//90+int(pyxel.sin(self.facing)*self.s)//90+1)!=0:
                    self.y+=int(pyxel.sin(self.facing)*self.s)
                elif self.y+int(pyxel.sin(self.facing)*self.s)<(self.y//90)*90+90:
                    self.y+=int(pyxel.sin(self.facing)*self.s)
                else:
                    self.y=(self.y//90)*90+89
                    
        print (self.facing,self.s,self.x,self.y)
        
    def fini(self):
        if pyxel.pget(self.x//90,self.y//90)==11:
            return True
        
class App:
    def __init__(self):
        self.labyrinthe=Labyrinthe(10,10)
        self.perso=Personnage()
        self.temps_solution=0
        pyxel.init(151,151)
        pyxel.run(self.update, self.draw)
        
    def update(self):
        self.perso.update()
        if self.perso.fini():
            self.labyrinthe=Labyrinthe(10,10)
            self.perso=Personnage()
            
    def draw(self):
        pyxel.cls(7)
        self.labyrinthe.draw()
        if pyxel.btn(112):
            self.labyrinthe.draw_solution()
        self.perso.draw()
        pyxel.rect(self.labyrinthe.nb_colonnes*15,self.labyrinthe.nb_lignes*15-14,1,14,11) 

App()
