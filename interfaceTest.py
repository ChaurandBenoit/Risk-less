# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import sqlite3 
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import tkinter as tk
from tkinter import ttk

import numpy as np
from scipy.stats import norm

import datetime
import time


from math import sqrt
from scipy.stats import invgauss
from scipy.stats import norm
from math import pi
from math import exp
from random import uniform


LARGE_FONT= ("Calibri", 15)
#ML_Teta retourne les coefficients Teta obtenus par l'entrainement 
def ML_Teta(Xinit,Yinit) :
            
            X= np.concatenate((np.ones((len(Xinit),1)),Xinit),axis=1)
            
            Y=Yinit
            
            Teta= np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),Y)
            print("Les coefficients Teta sont : \n",Teta)
            print("\n")
            return(Teta)
        
        # ML_Prevision retourne la valeur prevesionnelle d'une action en fonction de ses valeures X actuelles
def ML_Prevision(coeff,Xactuel) : 
            X=np.concatenate((np.ones((1,1)),Xactuel),axis=1)
            resultat=X.T*coeff
            resultat=sum(resultat)
            print("La valeur prévisionnelle ou estimée de cette action est de:",resultat,"euros")
            return resultat
            
        #Meme fonction que ML_Prevision sauf qu'elle affiche en plus les actions passées(entrainement), actuelle et prévisionelle
def ML_Prevision_and_affichage(coeff,Xactuel,Yinit,self,Company) : 
            X=np.concatenate((np.ones((1,1)),Xactuel),axis=1)
            resultat=X.T*coeff 
            print(resultat)
            resultat=sum(resultat)
            global photo1
            global photo2
            imagepoucehaut = tk.PhotoImage(file="poucehaut.GIF")
            photo1 = tk.Label(self, image=imagepoucehaut)
            photo1.config(bg="cadet blue")
            photo1.image = imagepoucehaut
            imagepoucebas = tk.PhotoImage(file="poucebas.GIF")
            photo2 = tk.Label(self, image=imagepoucebas)
            photo2.config(bg="cadet blue")
            photo2.image = imagepoucebas
            
            print("Le prix de l'action simulé est de ",resultat,"euros")
            print(" ")
            Xactuel=Xactuel.T
            
            for i in range (0,len(Yinit)) :
                      plt.plot([i],[Yinit[i]],'bo')
            
            plt.plot([len(Yinit)],Xactuel[len(Xactuel)-1],'go',label="prix actuel")     
            plt.plot([len(Yinit)+1],[resultat],'ro',label="prix estimé")
            plt.legend()
            plt.title("Evolution du prix de l'action")
            
            if self.peutAfficher == True:
                root = tk.Toplevel()
                lb = tk.Label(root, text="Evolution du prix de l'action de l'entreprise "+ Company)
             
                fig = Figure((5,4), dpi=100)
                canvas = FigureCanvasTkAgg(fig, master=root)
                axes = fig.add_subplot(111)
             
                toolbar = NavigationToolbar2TkAgg(canvas, root)
                for i in range (0,len(Yinit)) :
                          axes.plot([i],[Yinit[i]],'bo')
                axes.plot([len(Yinit)],Xactuel[len(Xactuel)-1],'go',label="prix actuel")
                axes.plot([len(Yinit)+1],[resultat],'ro',label="prix estimé")
                axes.legend()
                lb.pack()
                canvas._tkcanvas.pack()
                
            
                profit=resultat-Xactuel[len(Xactuel)-1]
                profit_=100*profit/Xactuel[len(Xactuel)-1]
                
                
                global label
                label = tk.Label(self, text="Le prix de l'action simulé est de "+ str(resultat).strip('[]') +" euros", font="arial 10")
                #label.pack(pady=10,padx=10)
                label.grid(row=40, column=20, pady=10)
                label.configure(bg="cadet blue", font="Century 13 bold")
                if profit>0:
                    
                    print("Nous estimons que le cours de l'action va augmenter , nous vous conseillons donc d'investir au prix actuel de :",Xactuel[len(Xactuel)-1]," euros")
                    print(" ")
                    global lb1
                    lb1 = tk.Label(self, text="Nous estimons que le cours de l'action va augmenter , nous vous conseillons donc d'investir au prix actuel de :" + str(Xactuel[len(Xactuel)-1]).strip('[]') + " euros", font="arial 10")
                    lb1.grid(row=41, column=20, pady=10)
                    lb1.configure(bg="cadet blue", font="Century 13 bold")
                                 
                    global lb2
                    lb2 = tk.Label(self, text=" L'investissment devrait vous rapporter à court terme "+ str(profit).strip('[]') +" euros soit " + str(profit_).strip('[]') + " %", font="arial 10")
                    lb2.grid(row=42, column=20, pady=10)
                    lb2.configure(bg="cadet blue", font="Century 13 bold")
                    photo1.grid(row = 43, column =20)
                             
                    print(" L'investissment devrait vous rapporter à court terme ",profit , "euros soit ", profit_,"%" )
                else :
                   
                   print("Nous estimons que le cours de l'action va baisser , nous vous conseillons donc de ne pas investir.")
                   global lb3
                   lb3 = tk.Label(self, text="Nous estimons que le cours de l'action va baisser , nous vous conseillons donc de ne pas investir.", font="arial 10")
                   lb3.configure(bg="cadet blue", font="Century 13 bold")
                   lb3.grid(row=42, column=20, pady=10)
                   photo2.grid(row = 43, column =20, pady=10)
                   
                return resultat
                tk.mainloop()
                self.peutAfficher = False
        
        # Phase de Test et visualisation de chaque erreur quadratique et la moyenne des erreurs normales et  quadratique
def ML_Test(coeff,Xtest,Ytest):
             quadra_error=0
             
             for i in range (0,len(Xtest)):
                 last_quadra_error=((ML_Prevision(coeff,np.array([Xtest[i]]))-Ytest[i])**2)
               
                 quadra_error=quadra_error + last_quadra_error
                 
                
                 plt.plot(i,last_quadra_error,'bo',label="erreur quadratique")
             
             quadra_error= quadra_error/(len(Xtest))
            
             print("\n")
             print("Les valeures réelles des actions estimées ci-dessus sont : \n",Ytest)
             print("\n")
             print("La moyenne des erreurs quadratique est de ",quadra_error)
             return quadra_error
         
        
        # Enlevez les commentaires pour : afficher les coefficients Teta
        #ML_Teta(X1,Y1)
            
        # Enlevez les commentaires pour : afficher chaque erreur quadratique et la moyenne des erreurs quadratiques
        #ML_Test(ML_Teta(X1,Y1),X1Test,Y1Test)
         
        # Enlevez les commentaires pour : afficher le cours des actions d'entrainement(passées), actuelle et previsionelle (en fonction de la valeur actuelle)   
    #ML_Prevision_and_affichage(ML_Teta(X1,Y1),X0,Y1)
             
        # Enlevez les commentaires pour : afficher le cours de l'action previsionelle (en fonction de la valeur actuelle)   
        #ML_Prevision(ML_Teta(X1,Y1),X01)
        
def Vol():
        conn = sqlite3.connect('PPE.db')
        c = conn.cursor()
        
        def create_table():
            c.execute('CREATE TABLE IF NOT EXISTS entreeX(nom_action varchar(20) not null, acid int not null, benefice int,  actifs int, dividendes int,    prix_recent  decimal(7,3) not null, constraint entree_pk primary key (nom_action,acid))')
            c.execute('CREATE TABLE IF NOT EXISTS sortieY(nom_action varchar(20) not null, acid int not null, prix_réel int not null, constraint sortie_pk primary key (nom_action,acid), constraint sortie_fk_nom_action foreign key (nom_action) references entreeX (nom_action),constraint sortie_fk_acid foreign key (acid) references entreeX (acid))')
        def data_entry():
            
            #X0 et X01
            #X0= np.array([[5000,23000,11,5,2000]]) 
            #X01=np.array([[2000,20000,10,5,1300]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 1, 5000, 23000, 11, 2000)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 2, 2000, 20000, 10,  1300)")
            
            
            
            #X1
            #X1= np.array([[2000,20000,10,5,1200],[2200,20002,11,5,1400],[2400,30002,20,5,1700],[2800,20002,11,5,1450],[2400,23002,11,6,1440],[2300,24002,11,6,1700]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 3, 2100, 20000, 10,  1200)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 4, 2200, 20002, 11,  1400)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 5, 2400, 30002, 20,  1700)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 6, 2800, 20002, 11,  1450)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 7, 2400, 23002, 11,  1440)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 8, 2300, 24002, 11,  1700)")
            
            
            #Y1
            #Y1=np.array([[1300],[1500],[1540],[1600],[1700],[1870]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 3, 1300)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 4, 1500)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 5, 1540)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 6, 1600)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 7, 1700)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 8, 1870)")
            
            
            
            
            #X1test
            #X1Test=np.array([[2000,20000,10,5,1300],[2200,20002,11,5,1500],[2400,30002,20,5,1720]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 9, 2000, 20000, 10,  1300)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 10, 2200, 20002, 11,  1500)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 11, 2400, 30002, 20,  1720)")
           
            
            
            #Y1test
            #Y1Test=np.array([[1350],[1570],[1590]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 9, 1350)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 10, 1570)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 11, 1590)")
            
            conn.commit()
        create_table()
        data_entry()  
        
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 3'):
                X2= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 4'):
                X3= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 5'):
                X4= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 6'):
                X5= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 7'):
                X6= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 8'):
                X7= np.array([row[5]]) 
        #p = [2000, 1300, 1200, 1400, 1700, 1450, 1440, 1700, 1300, 1500, 1720] #n prix connus de l'action sur une période
        p=np.concatenate((X2,X3,X4,X5,X6,X7),axis=0)
        r = [] #(n-1) rendements 
        rm = 0 #rendement moyen sur la période
        v = 0 # volatilité
        
        for i in range(0,len(p)-1):
            rtemp = p[i+1]/p[i] - 1
            r.append(rtemp)
            
        for i in range(0, len(r)):
            rm += (r[i])
            
        rm /= len(r)
        
        for i in range(0, len(r)):
            v += ((r[i] - rm)**2)/len(r)
        
        X0=np.array([1800,v,rm,1/12])
        return X0
    

def Volatilite(self):
        #crée une databse si elle n'existe pas
        conn = sqlite3.connect('PPE.db')
        c = conn.cursor()
        
        def create_table():
            c.execute('CREATE TABLE IF NOT EXISTS entreeX(nom_action varchar(20) not null, acid int not null, benefice int,  actifs int, dividendes int,    prix_recent  decimal(7,3) not null, constraint entree_pk primary key (nom_action,acid))')
            c.execute('CREATE TABLE IF NOT EXISTS sortieY(nom_action varchar(20) not null, acid int not null, prix_réel int not null, constraint sortie_pk primary key (nom_action,acid), constraint sortie_fk_nom_action foreign key (nom_action) references entreeX (nom_action),constraint sortie_fk_acid foreign key (acid) references entreeX (acid))')
        def data_entry():
            
            #X0 et X01
            #X0= np.array([[5000,23000,11,5,2000]]) 
            #X01=np.array([[2000,20000,10,5,1300]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 1, 5000, 23000, 11, 2000)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 2, 2000, 20000, 10,  1300)")
            
            
            
            #X1
            #X1= np.array([[2000,20000,10,5,1200],[2200,20002,11,5,1400],[2400,30002,20,5,1700],[2800,20002,11,5,1450],[2400,23002,11,6,1440],[2300,24002,11,6,1700]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 3, 2100, 20000, 10,  1200)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 4, 2200, 20002, 11,  1400)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 5, 2400, 30002, 20,  1700)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 6, 2800, 20002, 11,  1450)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 7, 2400, 23002, 11,  1440)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 8, 2300, 24002, 11,  1700)")
            
            
            #Y1
            #Y1=np.array([[1300],[1500],[1540],[1600],[1700],[1870]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 3, 1300)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 4, 1500)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 5, 1540)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 6, 1600)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 7, 1700)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 8, 1870)")
            
            
            
            
            #X1test
            #X1Test=np.array([[2000,20000,10,5,1300],[2200,20002,11,5,1500],[2400,30002,20,5,1720]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 9, 2000, 20000, 10,  1300)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 10, 2200, 20002, 11,  1500)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 11, 2400, 30002, 20,  1720)")
           
            
            
            #Y1test
            #Y1Test=np.array([[1350],[1570],[1590]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 9, 1350)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 10, 1570)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 11, 1590)")
            
            conn.commit()
        create_table()
        data_entry()  
        
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 3'):
                X2= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 4'):
                X3= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 5'):
                X4= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 6'):
                X5= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 7'):
                X6= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 8'):
                X7= np.array([row[5]]) 
        #p = [2000, 1300, 1200, 1400, 1700, 1450, 1440, 1700, 1300, 1500, 1720] #n prix connus de l'action sur une période
        p=np.concatenate((X2,X3,X4,X5,X6,X7),axis=0)
        r = [] #(n-1) rendements 
        rm = 0 #rendement moyen sur la période
        v = 0 # volatilité
        
        for i in range(0,len(p)-1):
            rtemp = p[i+1]/p[i] - 1
            r.append(rtemp)
            
        for i in range(0, len(r)):
            rm += (r[i])
            
        rm /= len(r)
        
        for i in range(0, len(r)):
            v += ((r[i] - rm)**2)/len(r)
        
        if self.peutAfficher == True:
            v = sqrt(v)
            global lbr
            lbr = tk.Label(self, text="Rendement moyen : " + str(round(rm*100, 2)) + "%", font="arial 10")
            #lbr.pack(pady=10,padx=10)
            lbr.grid(row=44, column=20, pady=10)
            lbr.configure(bg="cadet blue", font="Century 25 bold")
            global lbv
            lbv = tk.Label(self, text="Volatité : " + str(round(v*100, 2)) + "%", font="arial 10")
            #lbv.pack(pady=15,padx=10)
            lbv.grid(row=43, column=20, pady=10)
            lbv.configure(bg="cadet blue", font="Century 25 bold")
            root = tk.Toplevel()
            lbl = tk.Label(root, text="Historique des 6 derniers prix de l'action Airbus",font="arial 10")
            fig = Figure((5,4), dpi=100)
            canvas = FigureCanvasTkAgg(fig, master=root)
            axes = fig.add_subplot(111)
             
            toolbar = NavigationToolbar2TkAgg(canvas, root)
             
            axes.plot(p, label="prix de l'action")
            axes.legend()
            lbl.pack()
            canvas._tkcanvas.pack()
             
            tk.mainloop()
            self.peutAfficher = False
        #label.after(1000,label.pack_forget())
        
       
        print ("Rendement moyen : " + str(round(rm*100, 2)) + "%")
        print("Volatité : " + str(round(v*100, 2)) + "%")
        
        X0=np.array([1700,v,rm,1/12])
        return X0
        
        
        
        
        
        
        #for i in range(0, len(r)):
        #    print(r[i])
def Vol2():
        conn = sqlite3.connect('PPE.db')
        c = conn.cursor()
        
        def create_table2():
            c.execute('CREATE TABLE IF NOT EXISTS entreeX(nom_action varchar(20) not null, acid int not null, benefice int,  actifs int, dividendes int,    prix_recent  decimal(7,3) not null, constraint entree_pk primary key (nom_action,acid))')
            c.execute('CREATE TABLE IF NOT EXISTS sortieY(nom_action varchar(20) not null, acid int not null, prix_réel int not null, constraint sortie_pk primary key (nom_action,acid), constraint sortie_fk_nom_action foreign key (nom_action) references entreeX (nom_action),constraint sortie_fk_acid foreign key (acid) references entreeX (acid))')
        def data_entry2():
            
            #X0 et X01
            #X0= np.array([[5000,23000,11,5,2000]]) 
            #X01=np.array([[2000,20000,10,5,1300]])
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 12, 5000, 23000, 11,  4000)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 13, 2000, 20000, 10,  200)")
            
            
            
            #X1
            #X1= np.array([[2000,20000,10,5,1200],[2200,20002,11,5,1400],[2400,30002,20,5,1700],[2800,20002,11,5,1450],[2400,23002,11,6,1440],[2300,24002,11,6,1700]])
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 14, 2100, 20000, 10,  3200)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 15, 2200, 20002, 11,  3400)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 16, 2400, 30002, 20,  3700)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 17, 2800, 20002, 11,  3450)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 18, 2400, 23002, 11,  3440)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 19, 2300, 24002, 11,  3700)")
            
            
            #Y1
            #Y1=np.array([[1300],[1500],[1540],[1600],[1700],[1870]])
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 14, 3300)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 15, 3500)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 16, 3540)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 17, 3600)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 18, 3700)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 19, 3870)")
            
            
            
            
            #X1test
            #X1Test=np.array([[2000,20000,10,5,1300],[2200,20002,11,5,1500],[2400,30002,20,5,1720]])
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 20, 2000, 20000, 10,  3300)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 21, 2200, 20002, 11,  3500)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 22, 2400, 30002, 20,  3720)")
           
            
            
            #Y1test
            #Y1Test=np.array([[1350],[1570],[1590]])
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 20, 3350)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 21, 3570)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 22, 3590)")
            
            conn.commit()
            
        create_table2()
        data_entry2()  
        
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 14'):
                X2= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 15'):
                X3= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 16'):
                X4= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 17'):
                X5= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 18'):
                X6= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 19'):
                X7= np.array([row[5]]) 
        #p = [2000, 1300, 1200, 1400, 1700, 1450, 1440, 1700, 1300, 1500, 1720] #n prix connus de l'action sur une période
        p=np.concatenate((X2,X3,X4,X5,X6,X7),axis=0)
        r = [] #(n-1) rendements 
        rm = 0 #rendement moyen sur la période
        v = 0 # volatilité
        
        for i in range(0,len(p)-1):
            rtemp = p[i+1]/p[i] - 1
            r.append(rtemp)
            
        for i in range(0, len(r)):
            rm += (r[i])
            
        rm /= len(r)
        
        for i in range(0, len(r)):
            v += ((r[i] - rm)**2)/len(r)
        
        X0=np.array([1700,v,rm,1/12])
        return X0 
    
def Volatilite2(self):
        conn = sqlite3.connect('PPE.db')
        c = conn.cursor()
        
        def create_table2():
            c.execute('CREATE TABLE IF NOT EXISTS entreeX(nom_action varchar(20) not null, acid int not null, benefice int,  actifs int, dividendes int,    prix_recent  decimal(7,3) not null, constraint entree_pk primary key (nom_action,acid))')
            c.execute('CREATE TABLE IF NOT EXISTS sortieY(nom_action varchar(20) not null, acid int not null, prix_réel int not null, constraint sortie_pk primary key (nom_action,acid), constraint sortie_fk_nom_action foreign key (nom_action) references entreeX (nom_action),constraint sortie_fk_acid foreign key (acid) references entreeX (acid))')
        def data_entry2():
            
            #X0 et X01
            #X0= np.array([[5000,23000,11,5,2000]]) 
            #X01=np.array([[2000,20000,10,5,1300]])
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 12, 5000, 23000, 11,  4000)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 13, 2000, 20000, 10,  200)")
            
            
            
            #X1
            #X1= np.array([[2000,20000,10,5,1200],[2200,20002,11,5,1400],[2400,30002,20,5,1700],[2800,20002,11,5,1450],[2400,23002,11,6,1440],[2300,24002,11,6,1700]])
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 14, 2100, 20000, 10,  3200)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 15, 2200, 20002, 11,  3400)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 16, 2400, 30002, 20,  3700)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 17, 2800, 20002, 11,  3450)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 18, 2400, 23002, 11,  3440)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 19, 2300, 24002, 11,  3700)")
            
            
            #Y1
            #Y1=np.array([[1300],[1500],[1540],[1600],[1700],[1870]])
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 14, 3300)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 15, 3500)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 16, 3540)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 17, 3600)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 18, 3700)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 19, 3870)")
            
            
            
            
            #X1test
            #X1Test=np.array([[2000,20000,10,5,1300],[2200,20002,11,5,1500],[2400,30002,20,5,1720]])
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 20, 2000, 20000, 10,  3300)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 21, 2200, 20002, 11,  3500)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 22, 2400, 30002, 20,  3720)")
           
            
            
            #Y1test
            #Y1Test=np.array([[1350],[1570],[1590]])
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 20, 3350)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 21, 3570)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 22, 3590)")
            
            conn.commit()
            
        create_table2()
        data_entry2()  
        
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 14'):
                X2= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 15'):
                X3= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 16'):
                X4= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 17'):
                X5= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 18'):
                X6= np.array([row[5]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 19'):
                X7= np.array([row[5]]) 
        #p = [2000, 1300, 1200, 1400, 1700, 1450, 1440, 1700, 1300, 1500, 1720] #n prix connus de l'action sur une période
        p=np.concatenate((X2,X3,X4,X5,X6,X7),axis=0)
        r = [] #(n-1) rendements 
        rm = 0 #rendement moyen sur la période
        v = 0 # volatilité
        
        for i in range(0,len(p)-1):
            rtemp = p[i+1]/p[i] - 1
            r.append(rtemp)
            
        for i in range(0, len(r)):
            rm += (r[i])
            
        rm /= len(r)
        
        for i in range(0, len(r)):
            v += ((r[i] - rm)**2)/len(r)
        
        if self.peutAfficher == True:
            v = sqrt(v)
            
            global lbrp
            lbrp = tk.Label(self, text="Rendement moyen : " + str(round(rm*100, 2)) + "%", font="Century 13 bold")
            #lbr.pack(pady=10,padx=10)
            global rdm 
            rdm= str(round(rm*100,2))
            lbrp.grid(row=44, column=20, pady=10)
            lbrp.configure(bg="cadet blue", font="Century 13 bold")
            global lbvp
            lbvp = tk.Label(self, text="Volatité : " + str(round(v*100, 2)) + "%", font="Century 13 bold")
            global vp2
            vp2 = str(round(v*100,2))
            #lbv.pack(pady=15,padx=10)
            lbvp.grid(row=43, column=20, pady=10)
            lbvp.configure(bg="cadet blue", font="Century 13 bold")
               
            root = tk.Toplevel()
            lbl = tk.Label(root, text="Historique des 6 derniers prix de l'action Peugeot",font="Century 13 bold")
            fig = Figure((5,4), dpi=100)
            canvas = FigureCanvasTkAgg(fig, master=root)
            axes = fig.add_subplot(111)
             
            toolbar = NavigationToolbar2TkAgg(canvas, root)
             
            axes.plot(p, label="prix de l'action")
            axes.legend()
            lbl.pack()
            canvas._tkcanvas.pack()
             
            tk.mainloop()
            self.peutAfficher = False
        #label.after(1000,label.pack_forget())
        
             
        print ("Rendement moyen : " + str(round(rm*100, 2)) + "%")
        print("Volatité : " + str(round(v*100, 2)) + "%")
        
        X0=np.array([1700,v,rm,1/12])
        return X0 
        
   

class RiskApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="risk.ico")
        tk.Tk.wm_title(self, "Risk-Less")
        
        
        container = tk.Frame(self)
        container.pack(side="top", expand = True)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, PageOne, PageTwo,
                  PageLinearRegression, PageRidgeRegression, PageRandomForest,
                  PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Risk-Less", font=LARGE_FONT)
#        label.pack(pady=50)
        label.grid(row=0, column=1, pady=50)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        image1 = tk.PhotoImage(file="logo.GIF")
        self.config(bg ="cadet blue")
        photo = tk.Label(self, image=image1)
        photo.config(bg="cadet blue")
        photo.image = image1
        photo.grid(row = 2, column =0)
        buttonstyle = ttk.Style()
        buttonstyle.configure('TButton', font="Century 32", background="black")
       
        button = ttk.Button(self, text="Value At Risk",
                            command=lambda: controller.show_frame(PageOne))
                            
        #button.pack(side="left",padx=30)
        button.grid(row=1, column=1, pady=50)

        button2 = ttk.Button(self, text="Machine Learning",
                            command=lambda: controller.show_frame(PageTwo))
        #button2.pack(side="right",padx=10)
        button2.grid(row=2, column=1, pady=50)


        button3 = ttk.Button(self, text="Volatilité",
                            command=lambda: controller.show_frame(PageThree))
        #button3.pack(padx=30)
        button3.grid(row=3, column=1, pady=50)
        
        
class PageOne(tk.Frame):

    
         
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg ="cadet blue")
        label = tk.Label(self, text="   Value at Risk", font=LARGE_FONT)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        #label.pack(pady=10,padx=10)
        label.grid(row=10, column=20, pady=50)
        image1 = tk.PhotoImage(file="retour.GIF")
#        photo = tk.Label(self, image=image1)
#        photo.config(bg="cadet blue")
#        photo.image = image1
        button1 = ttk.Button(self, image=image1,
                            command=lambda: controller.show_frame(HomePage))
        button1.image = image1
#        button1 = ttk.Button(self, text="Back to Home",
#                            command=lambda: controller.show_frame(HomePage))
   
        button1.grid(row = 0, column =0)
        
        buttonr= ttk.Button(self,text="Var Airbus",command= self.runVaR)
        buttonr.grid(row = 20, column =20)
        
        buttonvr2= ttk.Button(self,text="Var Peugeot",command= self.runVaR2)
        buttonvr2.grid(row = 25, column =20)
        
        self.peutAfficher = True
       
     
        
    def runVaR(self):
#        if self.peutAfficher == True:
#            label = tk.Label(self,text="En Construction", font=LARGE_FONT)
#            label.grid(row=30, column=20, pady=50)
#            label.config(bg="cadet blue")
#            lbren = tk.Label(self, text="Rendement moyen : " + rdm + "%", font="arial 10")
#            #lbv.pack(pady=15,padx=10)
#            lbren.grid(row=43, column=20, pady=10)
#            lbren.configure(bg="cadet blue", font="Century 13")
#            #print(rdm)
#            print(vp2)
#            self.peutAfficher = False
        def affichage(tab):
            print ("Prix",tab[0])
            print ("Volatilité",tab[1])
            print ("Rendement Moyen",tab[2])
            print ("Echeance",tab[3])
    

        def prixsimulé(tab,rand,l) :
            price=[ 0 for i in range(0,30,1)]
            var=0
            for i in range(0,30,1):
                price[i] =tab[0]*np.exp((tab[2]-0.5*tab[1]**2)*l[i]+tab[1]*l[i]*rand[i])
               
            var=min(price)-tab[0]
            print ("La var est de ",var)
            labelvr = tk.Label(self, text="  La var pour l'entreprise Airbus est de " + str(var).strip('[]'), font="arial 10")
            #label.pack(pady=10,padx=10)
            labelvr.grid(row=100, column=20, pady=100)
            labelvr.configure(bg="cadet blue", font="Century 25 bold")
            
        
            
            
#        
        def var(X0) :
    
            affichage(X0)
            rand=[uniform(0,1)  for i in range(0,30,1)]
            l=[i/30 for i in range(0,30,1)]
            print (rand)
            rand=norm.ppf(rand)    
            print(rand)  
            prixsimulé(X0,rand,l)
        
        
        var(Vol())
    
    def runVaR2(self):
#        if self.peutAfficher == True:
#            label = tk.Label(self,text="En Construction", font=LARGE_FONT)
#            label.grid(row=30, column=20, pady=50)
#            label.config(bg="cadet blue")
#            lbren = tk.Label(self, text="Rendement moyen : " + rdm + "%", font="arial 10")
#            #lbv.pack(pady=15,padx=10)
#            lbren.grid(row=43, column=20, pady=10)
#            lbren.configure(bg="cadet blue", font="Century 13")
#            #print(rdm)
#            print(vp2)
#            self.peutAfficher = False
        def affichage(tab):
            print ("Prix",tab[0])
            print ("Volatilité",tab[1])
            print ("Rendement Moyen",tab[2])
            print ("Echeance",tab[3])
    

        def prixsimulé(tab,rand,l) :
            price=[ 0 for i in range(0,30,1)]
            var=0
            for i in range(0,30,1):
                price[i] =tab[0]*np.exp((tab[2]-0.5*tab[1]**2)*l[i]+tab[1]*l[i]*rand[i])
               
            var=min(price)-tab[0]
            print ("La var est de ",var)
            labelvr2 = tk.Label(self, text="La var pour l'entreprise Peugeot est de " + str(var).strip('[]'), font="arial 10")
            #label.pack(pady=10,padx=10)
            labelvr2.grid(row=100, column=20, pady=100)
            labelvr2.configure(bg="cadet blue", font="Century 25 bold")
            
        
            
            
#        
        def var(X0) :
    
            affichage(X0)
            rand=[uniform(0,1)  for i in range(0,30,1)]
            l=[i/30 for i in range(0,30,1)]
            print (rand)
            rand=norm.ppf(rand)    
            print(rand)  
            prixsimulé(X0,rand,l)
        
        
        var(Vol2())


               
class PageTwo(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg ="cadet blue")
        label = tk.Label(self, text="Machine Learning", font=LARGE_FONT)
        label.configure(bg="cadet blue")
#        label.pack(pady=10,padx=10)
        label.grid(row=10, column=20, pady=50)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        image1 = tk.PhotoImage(file="retour.GIF")
#        photo = tk.Label(self, image=image1)
#        photo.config(bg="cadet blue")
#        photo.image = image1
        button1 = ttk.Button(self, image=image1,
                            command=lambda: controller.show_frame(HomePage))
        button1.image = image1
#        button1.pack(anchor="ne")
        button1.grid(row = 0, column =0)

        button2 = ttk.Button(self, text="Régression linéaire",
                           command=lambda: controller.show_frame(PageLinearRegression))
        button2.grid(row = 20, column =20)
        button3 = ttk.Button(self, text="Régression linéaire Ridge",
                           command=lambda: controller.show_frame(PageRidgeRegression))
        button3.grid(row = 22, column =20,pady=20)
        button4 = ttk.Button(self, text="Random forest",
                           command=lambda: controller.show_frame(PageRandomForest))
        button4.grid(row = 23, column =20,pady=5)
#        button2.pack()
#        label2 = tk.Label(self,text="Montant souhaité:", font=("arial",10,"bold"), fg="red")
#        label2.pack(side="left")
#        
#        montant = tk.StringVar()
#        entry = tk.Entry(self,textvariable=montant)
#        entry.pack()
#        button3 = ttk.Button(self,textvariable=montant)
#        button3.pack()
        
        self.peutAfficher = True 
        self.peutAfficher2 = True 

class PageLinearRegression(tk.Frame):
   
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg ="cadet blue")
        label = tk.Label(self, text="Machine Learning", font=LARGE_FONT)
        label.configure(bg="cadet blue")
#        label.pack(pady=10,padx=10)
        label.grid(row=10, column=20, pady=50)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        image1 = tk.PhotoImage(file="retour.GIF")
#        photo = tk.Label(self, image=image1)
#        photo.config(bg="cadet blue")
#        photo.image = image1
        button1 = ttk.Button(self, image=image1,
                            command=lambda: controller.show_frame(HomePage))
        button1.image = image1
#        button1.pack(anchor="ne")
        button1.grid(row = 0, column =0)

        button2 = ttk.Button(self, text="Airbus",
                           command=self.runML)
        button2.grid(row = 20, column =20)
        button3 = ttk.Button(self, text="CLEAR",
                           command=self.effacer)
        button3.grid(row = 22, column =20,pady=20)
        button4 = ttk.Button(self, text="Peugeot",
                           command=self.runML2)
        button4.grid(row = 23, column =20,pady=5)
#        button2.pack()
#        label2 = tk.Label(self,text="Montant souhaité:", font=("arial",10,"bold"), fg="red")
#        label2.pack(side="left")
#        
#        montant = tk.StringVar()
#        entry = tk.Entry(self,textvariable=montant)
#        entry.pack()
#        button3 = ttk.Button(self,textvariable=montant)
#        button3.pack()
        
        self.peutAfficher = True 
        self.peutAfficher2 = True 
        
    def effacer(self):
        photo1.grid_forget()
        photo2.grid_forget()
        label.grid_forget()
        lb3.grid_forget()
        lb1.grid_forget()
        lb2.grid_forget()
    
    def runML(self): 
        
        def create_table():
            conn = sqlite3.connect('PPE.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS entreeX(nom_action varchar(20) not null, acid int not null, benefice int,  actifs int, dividendes int,    prix_recent  decimal(7,3) not null, constraint entree_pk primary key (nom_action,acid))')
            c.execute('CREATE TABLE IF NOT EXISTS sortieY(nom_action varchar(20) not null, acid int not null, prix_réel int not null, constraint sortie_pk primary key (nom_action,acid), constraint sortie_fk_nom_action foreign key (nom_action) references entreeX (nom_action),constraint sortie_fk_acid foreign key (acid) references entreeX (acid))')
        def data_entry():
                
            conn = sqlite3.connect('PPE.db')
            c = conn.cursor()
            #X0 et X01
            #X0= np.array([[5000,23000,11,5,2000]]) 
            #X01=np.array([[2000,20000,10,5,1300]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 1,368750000,93311000000,0,39.7)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 2, 368750000,93311000000,0.6,41.44)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 12, 5000, 23000, 11,  4000)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 13, 2000, 20000, 10,  200)")
                    
                    
            #X1
            #X1= np.array([[2000,20000,10,5,1200],[2200,20002,11,5,1400],[2400,30002,20,5,1700],[2800,20002,11,5,1450],[2400,23002,11,6,1440],[2300,24002,11,6,1700]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 3, 368750000,93311000000,0,47.59)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 4, 368750000,93311000000,0,55.81)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 5, 587500000,96102000000,0,52.41)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 6, 587500000,96102000000,0,52.41)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 7, 587500000,96102000000,0,49.76)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 8, 587500000,96102000000,0,41.35)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 14, 2100, 20000, 10,  3200)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 15, 2200, 20002, 11,  3400)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 16, 2400, 30002, 20,  3700)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 17, 2800, 20002, 11,  3450)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 18, 2400, 23002, 11, 3440)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 19, 2300, 24002, 11,  3700)")
                    
                    
            #Y1
            #Y1=np.array([[1300],[1500],[1540],[1600],[1700],[1870]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 3, 55.81)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 4, 52.41)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 5, 48.72)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 6, 49.76)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 7, 41.35)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 8, 60.36)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 14, 3300)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 15, 3500)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 16, 3540)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 17, 3600)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 18, 3700)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 19, 3870)")
                    
                    
                    
            #X1test
            #X1Test=np.array([[2000,20000,10,5,1300],[2200,20002,11,5,1500],[2400,30002,20,5,1720]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 9, 587500000,96102000000,0,41.35)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 10, 674500000,106681000000,0,60.36)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 11, 674500000,106681000000,1.2,59.61)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 20, 2000, 20000, 10,  3300)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 21, 2200, 20002, 11,  3500)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 22, 2400, 30002, 20,  3720)")
                              
                    
                    
            #Y1test
            #Y1Test=np.array([[1350],[1570],[1590]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 9, 60.36)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 10, 59.61)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 11, 53.99)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 20, 3350)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 21, 3570)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 22, 3590)")
                    
            conn.commit()
                
        create_table()
        data_entry()  
          
        conn = sqlite3.connect('PPE.db')
        c = conn.cursor()   
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 1'):
            X0= np.array([[row[2],row[3],row[4],row[5]]]) 
        print("\nX0 values:\n", X0)
        print("\n")
            
        for row in c.execute('SELECT * FROM entreeX where nom_action= "Airbus" AND acid = 2'):
            X01= np.array([[row[2],row[3],row[4],row[5]]]) 
        print("X01 values:\n", X01)
        #print(row[0])
        
        #Xtest=np.concatenate((X0,X01),axis=0)
        #print("\nXtest\n", Xtest)
            
        #X1
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 3'):
            X1a= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 4'):
            X1b= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 5'):
            X1c= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 6'):
            X1d= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 7'):
            X1e= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 8'):
            X1f= np.array([[row[2],row[3],row[4],row[5]]])
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 14'):
            X1ap= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 15'):
            X1bp= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 16'):
            X1cp= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 17'):
            X1dp= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 18'):
            X1ep= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 19'):
            X1fp= np.array([[row[2],row[3],row[4],row[5]]]) 
        X1=np.concatenate((X1a,X1b,X1c,X1d,X1e,X1f,X1ap,X1bp,X1cp,X1dp,X1ep,X1fp),axis=0)
        print("\nX1 values:\n", X1)
        print("\n")
            
            
        #X1test
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 9'):
            X1testa= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 10'):
            X1testb= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 11'):
            X1testc= np.array([[row[2],row[3],row[4],row[5]]]) 
        X1test=np.concatenate((X1testa,X1testb,X1testc),axis=0)
        print("\nX1test values:\n", X1test)
        print("\n")
        
        
        #Y1
        
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 3'):
            Y1a= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 4'):
            Y1b= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 5'):
            Y1c= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 6'):
            Y1d= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 7'):
            Y1e= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 8'):
                   Y1f= np.array([[row[2]]]) 
                
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 14'):
                   Y1ap= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 15'):
                  Y1bp= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 16'):
                   Y1cp= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 17'):
                   Y1dp= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 18'):
                   Y1ep= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 19'):
                   Y1fp= np.array([[row[2]]]) 
        
        Y1=np.concatenate((Y1a,Y1b,Y1c,Y1d,Y1e,Y1f,Y1ap,Y1bp,Y1cp,Y1dp,Y1ep,Y1fp),axis=0)
        Y1bis=np.concatenate((Y1a,Y1b,Y1c,Y1d,Y1e,Y1f),axis=0)
        print("\nY1:",Y1)
            
            #Y1test
            
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 9'):
                   Y1testa= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 10'):
                   Y1testb= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 11'):
                   Y1testc= np.array([[row[2]]]) 
        
        Y1test=np.concatenate((Y1testa,Y1testb,Y1testc),axis=0)
        print("\nY1test:",Y1test)
        
        ML_Prevision_and_affichage(ML_Teta(X1,Y1),X01,Y1bis,self,"Airbus")

            

    def runML2(self): 
        
        def create_table():
            conn = sqlite3.connect('PPE.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS entreeX(nom_action varchar(20) not null, acid int not null, benefice int,  actifs int, dividendes int,    prix_recent  decimal(7,3) not null, constraint entree_pk primary key (nom_action,acid))')
            c.execute('CREATE TABLE IF NOT EXISTS sortieY(nom_action varchar(20) not null, acid int not null, prix_réel int not null, constraint sortie_pk primary key (nom_action,acid), constraint sortie_fk_nom_action foreign key (nom_action) references entreeX (nom_action),constraint sortie_fk_acid foreign key (acid) references entreeX (acid))')
        def data_entry():
                
            conn = sqlite3.connect('PPE.db')
            c = conn.cursor()
            #X0 et X01
            #X0= np.array([[5000,23000,11,5,2000]]) 
            #X01=np.array([[2000,20000,10,5,1300]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 1, 5000, 23000, 11,  2000)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 2, 2000, 20000, 10,  1300)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 12, 5000, 23000, 11,  4000)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 13, 2000, 20000, 10,  200)")
                    
                    
            #X1
            #X1= np.array([[2000,20000,10,5,1200],[2200,20002,11,5,1400],[2400,30002,20,5,1700],[2800,20002,11,5,1450],[2400,23002,11,6,1440],[2300,24002,11,6,1700]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 3, 2100, 20000, 10,  1200)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 4, 2200, 20002, 11,  1400)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 5, 2400, 30002, 20,  1700)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 6, 2800, 20002, 11,  1450)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 7, 2400, 23002, 11,  1440)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 8, 2300, 24002, 11,  1700)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 14, 2100, 20000, 10,  3200)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 15, 2200, 20002, 11,  3400)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 16, 2400, 30002, 20,  3700)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 17, 2800, 20002, 11,  3450)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 18, 2400, 23002, 11, 3440)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 19, 2300, 24002, 11,  3700)")
                    
                    
            #Y1
            #Y1=np.array([[1300],[1500],[1540],[1600],[1700],[1870]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 3, 1300)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 4, 1500)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 5, 1540)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 6, 1600)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 7, 1700)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 8, 1870)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 14, 3300)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 15, 3500)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 16, 3540)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 17, 3600)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 18, 3700)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 19, 3870)")
                    
                    
                    
            #X1test
            #X1Test=np.array([[2000,20000,10,5,1300],[2200,20002,11,5,1500],[2400,30002,20,5,1720]])
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 9, 2000, 20000, 10, 1300)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 10, 2200, 20002, 11,  1500)")
            c.execute("REPLACE INTO entreeX VALUES('Airbus', 11, 2400, 30002, 20,  1720)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 20, 2000, 20000, 10,  3300)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 21, 2200, 20002, 11,  3500)")
            c.execute("REPLACE INTO entreeX VALUES('Peugeot', 22, 2400, 30002, 20,  3720)")
                              
                    
                    
            #Y1test
            #Y1Test=np.array([[1350],[1570],[1590]])
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 9, 1350)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 10, 1570)")
            c.execute("REPLACE INTO sortieY VALUES('Airbus', 11, 1590)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 20, 3350)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 21, 3570)")
            c.execute("REPLACE INTO sortieY VALUES('Peugeot', 22, 3590)")
                    
            conn.commit()
                
        create_table()
        data_entry()  
          
        conn = sqlite3.connect('PPE.db')
        c = conn.cursor()  
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 12'):
                X0= np.array([[row[2],row[3],row[4],row[5]]]) 
        
            
        for row in c.execute('SELECT * FROM entreeX where nom_action= "Airbus" AND acid = 2'):
            X01= np.array([[row[2],row[3],row[4],row[5]]]) 
        print("X01 values:\n", X01)
        #print(row[0])
        
        #Xtest=np.concatenate((X0,X01),axis=0)
        #print("\nXtest\n", Xtest)
            
        #X1
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 3'):
            X1a= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 4'):
            X1b= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 5'):
            X1c= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 6'):
            X1d= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 7'):
            X1e= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 8'):
            X1f= np.array([[row[2],row[3],row[4],row[5]]])
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 14'):
            X1ap= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 15'):
            X1bp= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 16'):
            X1cp= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 17'):
            X1dp= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 18'):
            X1ep= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Peugeot" AND acid = 19'):
            X1fp= np.array([[row[2],row[3],row[4],row[5]]]) 
        X1=np.concatenate((X1a,X1b,X1c,X1d,X1e,X1f,X1ap,X1bp,X1cp,X1dp,X1ep,X1fp),axis=0)
        print("\nX1 values:\n", X1)
        print("\n")
            
            
        #X1test
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 9'):
            X1testa= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 10'):
            X1testb= np.array([[row[2],row[3],row[4],row[5]]]) 
        for row in c.execute('SELECT * FROM entreeX where nom_action="Airbus" AND acid = 11'):
            X1testc= np.array([[row[2],row[3],row[4],row[5]]]) 
        X1test=np.concatenate((X1testa,X1testb,X1testc),axis=0)
        print("\nX1test values:\n", X1test)
        print("\n")
        
        
        #Y1
        
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 3'):
            Y1a= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 4'):
            Y1b= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 5'):
            Y1c= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 6'):
            Y1d= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 7'):
            Y1e= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 8'):
                   Y1f= np.array([[row[2]]]) 
                
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 14'):
                   Y1ap= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 15'):
                  Y1bp= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 16'):
                   Y1cp= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 17'):
                   Y1dp= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 18'):
                   Y1ep= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Peugeot" AND acid = 19'):
                   Y1fp= np.array([[row[2]]]) 
        
        Y1=np.concatenate((Y1a,Y1b,Y1c,Y1d,Y1e,Y1f,Y1ap,Y1bp,Y1cp,Y1dp,Y1ep,Y1fp),axis=0)
        Y1bis=np.concatenate((Y1ap,Y1bp,Y1cp,Y1dp,Y1ep,Y1fp),axis=0)
        print("\nY1:",Y1)
            
            #Y1test
            
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 9'):
                   Y1testa= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 10'):
                   Y1testb= np.array([[row[2]]]) 
        for row in c.execute('SELECT * FROM sortieY where nom_action= "Airbus" AND acid = 11'):
                   Y1testc= np.array([[row[2]]]) 
        
        Y1test=np.concatenate((Y1testa,Y1testb,Y1testc),axis=0)
        print("\nY1test:",Y1test)
        
        ML_Prevision_and_affichage(ML_Teta(X1,Y1),X0,Y1bis,self,"Peugeot")
                        
    
                   
class PageRidgeRegression(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg ="cadet blue")
        label = tk.Label(self, text="Ridge", font=LARGE_FONT)
        label.configure(bg="cadet blue")
#        label.pack(pady=10,padx=10)
        label.grid(row=10, column=20, pady=50)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        image1 = tk.PhotoImage(file="retour.GIF")
#        photo = tk.Label(self, image=image1)
#        photo.config(bg="cadet blue")
#        photo.image = image1
        button1 = ttk.Button(self, image=image1,
                            command=lambda: controller.show_frame(PageTwo))
        button1.image = image1
#        button1.pack(anchor="ne")
        button1.grid(row = 0, column =0)

#        button2 = ttk.Button(self, text="Airbus",
#                           command=self.runML)
#        button2.grid(row = 20, column =20)
#        button3 = ttk.Button(self, text="CLEAR",
#                           command=self.effacer)
#        button3.grid(row = 22, column =20,pady=20)
#        button4 = ttk.Button(self, text="Peugeot",
#                           command=self.runML2)
#        button4.grid(row = 23, column =20,pady=5)
#       
      

class PageRandomForest(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.config(bg ="cadet blue")
        label = tk.Label(self, text="Random Forest", font=LARGE_FONT)
        label.configure(bg="cadet blue")
        label.grid(row=10, column=20, pady=50)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        image1 = tk.PhotoImage(file="retour.GIF")

        button1 = ttk.Button(self, image=image1,
                            command=lambda: controller.show_frame(PageTwo))
        button1.image = image1
        button1.grid(row = 0, column =0)
        button2 = ttk.Button(self, text="RandomForest",
                           command=self.RFf)
        button2.grid(row = 20, column =20)
        
       
    def RFf(self):
         
        from sklearn.ensemble import RandomForestRegressor # Import the model we are using
        import numpy as np
        import pandas as pd  
        X01=np.array([[1015000000,22689,1.41,92.13]])
        
        
        df = pd.read_csv('testML.csv')  # mettre le nom du fichier csv
        df.head()  
        df.describe() 
        
        y1 = df['prixreel'] 
        x1 = df.drop('prixreel', axis=1, inplace=False)
        
        X1rf = pd.DataFrame(x1)
        Y1rf = pd.DataFrame(y1)
        rf = RandomForestRegressor(n_estimators=1000, oob_score=True, random_state=0)# Instantiate model with 500 decision trees
        
        rf.fit(X1rf, np.ravel(Y1rf)) #Train the model on training data

        predictions = rf.predict(X01)
        #return result
        print("L'algortihme de Random Forest nous donne une prédiction du cours de l'action de " + str(predictions)+"euros")
        labelrf = tk.Label(self, text="L'algortihme de Random Forest nous donne une prédiction du cours de l'action de " + str(predictions).strip('[]')+" euros", font="arial 10")
            #label.pack(pady=10,padx=10)
        labelrf.grid(row=40, column=20, pady=10)
        labelrf.configure(bg="cadet blue", font="Century 13 bold")

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg ="cadet blue")
        label = tk.Label(self, text="Volatilité", font=LARGE_FONT)
#        label.configure(bg="cadet blue")
#        label.pack(pady=10,padx=10)
        label.grid(row=10, column=20, pady=50)
        label.config(bg="cadet blue",fg="black", font ="Algerian 75 bold")
        image1 = tk.PhotoImage(file="retour.GIF")
#        photo = tk.Label(self, image=image1)
#        photo.config(bg="cadet blue")
#        photo.image = image1
        button1 = ttk.Button(self, image=image1,
                            command=lambda: controller.show_frame(HomePage))
        button1.image = image1
#        button1 = ttk.Button(self, text="Back to Home",
#                            command=lambda: controller.show_frame(HomePage))
        #button1.pack(anchor="ne")
        button1.grid(row = 0, column =0)
        button2 = ttk.Button(self, text="Airbus",
                           command=self.runVol)
        #button2.pack()
        button2.grid(row = 20, column =20)
        
        buttonv2 = ttk.Button(self, text="Peugeot",
                           command=self.runVol2)
        buttonv2.grid(row = 23, column =20,pady=5)
        
#        buttond = ttk.Button(self, text="Clear",
#                          command=self.effacer)
#        buttond = ttk.Button(self, text="Clear")
#        buttond.grid(row = 24, column =20,pady=5)
 
        self.peutAfficher = True 
        
#    def effacer(self):
#        lbr.grid_forget()
#        lbv.grid_forget()
#        lbrp.grid_forget()
#        lbvp.grid_forget()
        
    def runVol(self):
         Volatilite(self)
    def runVol2(self):
         Volatilite2(self)

            
        
def tick(time1=''):
    time2=time.strftime('%H:%M:%S')
    if time2!=time1:
        time1=time2
        clock_frame.config(text=time2)
        clock_frame.after(200,tick)

if __name__ == "__main__":
 
    
    app = RiskApp()
    app.geometry("1200x800+200+200")
    app.config(bg ="cadet blue")
    #app.wm_title("Risk-Less")
    #app.iconbitmap('risk.ico')
    #image = tk.PhotoImage(file="binary.gif")
    #label = tk.Label(image=image)
    #label.pack(pady=70)
    clock_frame = tk.Label(app,bg="white",font=('times',10,'bold'))
    clock_frame.pack(fill='both')
    tick()
    app.mainloop()