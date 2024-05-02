############################################
# CS4386 Semester B, 2022-2023 
# Assignment 1 # 
# Name: JIANG XIN 
# Student ID: 56643608
############################################
import copy 
from math import inf as infinity
import random

import numpy as np
import time
from copy import deepcopy as dcp

class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name
    def get_isAI(self):
        return self.isAI
    def get_symbole(self):
        return self.symbole
    def get_score(self):
        return self.score
    def add_score(self,score):
        self.score+=score

    def available_cells(self,state,player):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if (cell is None):
                    cells.append([x, y])
        return cells
    
    def get_move(self,state,player):
        start_time = time.time()
        next_move = Tree_56643608().strategy(state,player,t=start_time)
        return next_move  
    


class Node_56643608:
############################################
# CS4386 Semester B, 2022-2023 
# Assignment 1 # 
# Name: JIANG XIN 
# Student ID: 56643608
############################################

    #tree node of MCST
    def __init__(self,parent=None):
        self.score   = 0
        self.sum     = 0
        self.visit   = 0
        self.wins    = 0
        self.uct     = 100
        self.parent  = parent
        self.sons    = {} 
        
    def is_root(self):
        return self.parent  == None
    def is_leaf(self):
        return self.sons =={}
    
    def update(self,win,score):
        self.sum += score
        self.visit+=1
        self.score = (score + self.sum)/self.visit
        self.wins+=win     
    
    def selection(self):
        m_uct=-10000000
        m_k = None
        for k,o in self.sons.items():
            #uct should based on score to scale the score gap with opponent large
            o.uct = o.score/12+o.wins/(o.visit+0.001) +(2)*np.sqrt(np.log(self.visit+1)/(o.visit+0.001))
            if o.uct >m_uct:
                m_uct=o.uct
                m_k = k
        return m_k
    
    def expansion(self,cells):
        for cell in cells:
            self.sons[cell] = Node_56643608(self)
    
    def backpropagation(self,win:bool,score:int):
        self.update(win,score)
        if not self.is_root():
            score=-score
            self.parent.backpropagation(score>0,score)

class Tree_56643608:
############################################
# CS4386 Semester B, 2022-2023 
# Assignment 1 # 
# Name: JIANG XIN 
# Student ID: 56643608
############################################
    class Evaluator:
        def available_cells(self,board,player):
            cells=[]
            for x in range(6):
                for y in range(6):
                    if (board[x][y] is None):
                        if ((player=="X") and ((x+y)%2==0)) or ((player=="O") and ((x+y)%2==1)):
                            cells.append((x, y))
            return cells
        def available_cells_both(self,board,player):
            cells=[]
            cells_opponent=[]
            for x in range(6):
                for y in range(6):
                    if (board[x][y] is None):
                        if ((player=="X") and ((x+y)%2==0)) or ((player=="O") and ((x+y)%2==1)):
                            cells.append((x, y))
                        else:
                            cells_opponent.append((x, y))
            return cells,cells_opponent
        
        def alignement_cell(self,board,cell):  
            score=0
            x,y = cell[0],cell[1]    
            #1.check horizontal
            if((board[x][0] != None) and (board[x][1] != None) and  (board[x][2]!= None) and (board[x][3] != None) and (board[x][4] != None) and (board[x][5]  != None)):  
                score+=6
                #print("horizontal 6")
            else:
                if (board[x][0] != None) and (board[x][1] != None) and  (board[x][2]!= None) and (board[x][3] == None):
                    if y==0 or y==1 or y==2:
                        score+=3
                        #print("1horizontal 3")
                elif (board[x][0] == None) and (board[x][1] != None) and  (board[x][2]!= None) and (board[x][3] != None) and (board[x][4] == None):
                    if y==1 or y==2 or y==3:
                        score+=3
                        #print("2horizontal 3")
                elif  (board[x][1] == None) and (board[x][2] != None) and  (board[x][3]!= None) and (board[x][4] != None) and (board[x][5] == None):
                    if y==2 or y==3 or y==4:
                        score+=3
                        #print("3horizontal 3")
                elif  (board[x][2] == None) and  (board[x][3]!= None) and (board[x][4] != None) and (board[x][5] != None):
                    if y==3 or y==4 or y==5:
                        score+=3
                        #print("4horizontal 3")       
            #2.check vertical
            if((board[0][y] != None) and (board[1][y] != None) and (board[2][y] != None) and (board[3][y] != None) and (board[4][y]!= None) and (board[5][y]!= None)):
                score+=6
                #print("vertical 6")
            else:
                if (board[0][y] != None) and (board[1][y] != None) and  (board[2][y]!= None) and (board[3][y] == None):
                    if x==0 or x==1 or x==2:
                        score+=3
                        #print("1vertical 3")
                elif (board[0][y] == None) and (board[1][y] != None) and  (board[2][y]!= None) and (board[3][y] != None) and (board[4][y] == None):
                    if x==1 or x==2 or x==3:
                        score+=3
                        #print("2vertical 3")
                elif (board[1][y] == None) and (board[2][y] != None) and  (board[3][y]!= None) and (board[4][y] != None) and (board[5][y] == None):
                    if x==2 or x==3 or x==4:
                        score+=3
                        #print("3vertical 3")
                elif  (board[2][y] == None) and  (board[3][y]!= None) and (board[4][y] != None) and (board[5][y] != None):
                    if x==3 or x==4 or x==5:
                        score+=3
                        #print("4vertical 3")
            return score

        def full(self,board):
            for b in board:
                for c in b:
                    if c ==None:
                        return False
            return True

    
    def __init__(self):
        self.root = Node_56643608()
        self.eval = self.Evaluator()
    
    def random_arr(self,n):
        #shuffle
        array = [i for i in range(n)] 
        random.shuffle(array) 
        return array
    
    def quickout(self,board,player):
        #random play chess to evaluate the result
        score = 0
        oppoent = "O" if player=="X" else "X"
        cells,cells_oppoent = self.eval.available_cells_both(board,player)
        l_m,l_o = len(cells),len(cells_oppoent)
        seq_me = self.random_arr(l_m)
        seq_oppoent = self.random_arr(l_o)
        
        
        i = 0 
        while i < l_m and i < l_o: 
            cell = cells[seq_me[i]]
            board[cell[0]][cell[1]] = player
            score+= self.eval.alignement_cell(board,cell)
            
            cell = cells_oppoent[seq_oppoent[i]]
            board[cell[0]][cell[1]] = oppoent
            score -= self.eval.alignement_cell(board,cell)
            i += 1 
        if i < l_m: 
            cell = cells[seq_me[i]]
            board[cell[0]][cell[1]] = player
            score+= self.eval.alignement_cell(board,cell)
        if i < l_o: 
            cell = cells_oppoent[seq_oppoent[i]]
            board[cell[0]][cell[1]] = oppoent
            score-= self.eval.alignement_cell(board,cell)
        return score
          
    def playout_limit(self,board,player,t):   
        curr = self.root
        score = 0
        level=0
        while(time.time()-t<9.8):
            level+=1
            #depth limitation
            if level>3:
                s = self.quickout(board,player)
                score += s
                score = -score
                curr.backpropagation(score>0,score)
                break
            #expansion
            if curr.is_leaf():
                cells = self.eval.available_cells(board,player)
                curr.expansion(cells)
            #backpropagation
            if curr.sons == {}:
                if self.eval.full(board):
                    score=-score
                    if time.time()-t<9.8:
                        curr.backpropagation(score>0,score)
                    break
            cell = curr.selection()
            node = curr.sons[cell]
            board[cell[0]][cell[1]] = player
            player = "O" if player=="X" else "X"
            
            score+= self.eval.alignement_cell(board,cell)
            curr = node
            score*=-1
        
    def strategy(self,board,player,t=None):
        if t==None:
            t = time.time()
        cnt=0
        while(time.time()-t<9.8):
            cnt+=1
            self.playout_limit(dcp(board),player,t)
        m_k=None
        m_s=-100000000
        #highest score son
        for k,e in self.root.sons.items():
            s = e.score
            if s>=m_s:
                m_s = s
                m_k = k
        return m_k
