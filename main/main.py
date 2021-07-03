from itertools import combinations
from itertools import chain
import numpy as np
from collections import Counter
from fractions import Fraction
import pandas as pd
from tkinter import *
from tkinter import font
from pandastable import Table
from tkinter import messagebox
from PIL import Image, ImageTk

#Cambiar a variables para hacerlas parametrizadas
mechas = ['Cherno Alpha','Eva 01','Gigante de acero',
          'Gipsy Danger','Gundam','Jet Jaguar','Mazinger Z',
          'Mechagodzilla','Mechani-Kong','Megazord','Moguera','Voltron']

mecha_attacks = {    1:'Combate cuerpo a cuerpo',
               2:'Arma de destrucción masiva',
               3:'Arma cuerpo a cuerpo',
               4:'Arma a distancia'
               }

godzilla_actions = {    1:'Morder',
                        2:'Nada',
                        3:'Coletazo',
                        4:'Aliento atómico',
                        5:'Zarpazo'}


get_rnd_uniform= lambda start,end: round(np.random.uniform(start-0.5,end+.5))

summary_battle = lambda team,mecha_attack,godzilla_attack: [team,mecha_attack,godzilla_attack]


def godzilla_turn(mecha_attack):
    god_keys = list(godzilla_actions.keys())
    god_chose = 0
    if mecha_attack%2==0:
        #Ataque a distancia
        keys_god = [key for key in god_keys if key%2==0]
        god_chose = get_rnd_uniform(keys_god[0],keys_god[-1])
    else:
        #Ataque cercano
        keys_god = [key for key in god_keys if key%2!=0]
        god_chose = get_rnd_uniform(keys_god[0],keys_god[-1])
    godzilla_move = godzilla_actions.get(god_chose)
    return godzilla_move

def classic_prob():
    god_keys = list(godzilla_actions.keys()) 

    odd_g_keys = [key for key in god_keys if key%2!=0]
    pair_g_keys = [key for key in god_keys if key%2==0]
    odd_matrix = []
    pair_matrix = []
    

    for key in mecha_attacks.keys():
        if key%2!=0:
            odd_matrix.append(odd_g_keys)
        else:
            pair_matrix.append(pair_g_keys)

    frec_odd = dict(Counter(chain(*odd_matrix)))
    frec_pair = dict(Counter(chain(*pair_matrix)))
    all_frec = frec_odd.copy()
    all_frec.update(frec_pair)
    total_config = sum(list(frec_pair.values()) + list(frec_odd.values()))

    counting_table = {'Salida':[],'Probabilidad':[],'Redondeado':[]}
    for key in godzilla_actions.keys():
        prob = f'{all_frec.get(key)}/{total_config}'
        prob_r = Fraction(f'{all_frec.get(key)}/{total_config}').limit_denominator()
        counting_table.get('Salida').append(f'P({godzilla_actions.get(key)})')
        counting_table.get('Probabilidad').append(prob)
        counting_table.get('Redondeado').append(prob_r)
    return counting_table

def sub_prob():
    god_keys = list(godzilla_actions.keys()) 
    weapon_keys= list(mecha_attacks.keys())

    odd_g_keys = [key for key in god_keys if key%2!=0]
    pair_g_keys = [key for key in god_keys if key%2==0]
    sub_weapons = {}
    
    sub_res = {}
    for key in weapon_keys:
        pair_god_probs = []
        odd_god_probs = []
        sub_weapons[key] = 1/len(weapon_keys)
        if key%2==0:
            for _ in pair_g_keys:
                pair_god_probs.append(1/len(pair_g_keys))
            multi_pos = [x * sub_weapons.get(key) for x in pair_god_probs]
            sub_res[f'{key}'] = (sub_weapons.get(key),multi_pos,sum(multi_pos))
        else: 
            for _ in odd_g_keys:
                odd_god_probs.append(1/len(odd_g_keys))
            multi_pos = [x * sub_weapons.get(key) for x in odd_god_probs]
            sub_res[f'{key}'] = (sub_weapons.get(key),multi_pos,sum(multi_pos))
    all_sub_prob = {}
    total = 0
    for key in sub_res.keys():
        sub_tuple = sub_res.get(key)
        option_pos = str(Fraction(sub_tuple[0]))
        list_pos = sub_tuple[1]

        list_pos = [str(Fraction(x).limit_denominator()) for x in list_pos]
        res_pos = str(Fraction(sub_tuple[2]))
        total += sub_tuple[2]
        all_sub_prob[key] = (option_pos,list_pos,res_pos)
    all_sub_prob['total'] = total
    return all_sub_prob

def empiric_prob():
    #Conteo
    all_teams = list(combinations(mechas,3))
    total_combinations = len(all_teams)
    #print('Total de combinaciones: ',total_combinations)   

    election = get_rnd_uniform(0,total_combinations)
    if election >= total_combinations:
        election= total_combinations-1
    elected_team = all_teams[election]
    #print(election)
    #print('El Equipo escogido es: ',elected_team)

    #Fase 1
    weapons_keys = list(mecha_attacks.keys())
    option = get_rnd_uniform(weapons_keys[0],weapons_keys[-1])
    weapon = mecha_attacks.get(option)    
    
    #Segunda fase
    god_attack = godzilla_turn(option)
    summary = summary_battle(elected_team,weapon,god_attack)
    return summary

def get_frequency(my_list,item):
    frec = dict(Counter(my_list))
    item_frec= frec.get(item)
    return item_frec

get_e_prob =  lambda frec,size: get_e_prob(0,size) if frec == None else frec/size

#Probabilidad Clásica
def run_classic():
    n_window = createNewWindow()
    f1 = Frame(n_window)
    counting_table = classic_prob()
    df_classic_prob = pd.DataFrame(counting_table)
    TestApp(df_classic_prob,f1)
    print(df_classic_prob)

#Probabilidad Subjetiva
def run_subjective():
    n_window = createNewWindow()
    f1 = Frame(n_window)
    sub_prob_table = sub_prob()
    df_sub_prob = pd.DataFrame(sub_prob_table).transpose()
    df_sub_prob.columns = ['Mecha Ataque','Prob. Godzilla','Prob. Total']
    TestApp(df_sub_prob,f1)
    print(df_sub_prob)

#Probabilidad empírica
def run_simulation():
    if entry1.get() == '':
        messagebox.showinfo(message="Ingrése un número", title="Error")
    else:
        n = int(entry1.get())
        sim_godzilla_attacks =[]
        for i in range(n):
            summary = empiric_prob()
            sim_godzilla_attacks.append(summary[2])
        results = {'Acciones':[],'Probabilidad':[]}   
        for i in godzilla_actions.keys():
            frec = get_frequency(sim_godzilla_attacks,godzilla_actions.get(i))
            e_prob = get_e_prob(frec,len(sim_godzilla_attacks))
            results.get('Acciones').append(godzilla_actions.get(i))
            results.get('Probabilidad').append("{:.2%}".format(e_prob))
        results_df = pd.DataFrame(results)
        n_window = createNewWindow()
        f1 = Frame(n_window)
        TestApp(results_df,f1)

def createNewWindow():
    newWindow = Toplevel(root)
    return newWindow

class TestApp(Frame):
    """Basic test frame for the table"""
    def __init__(self,df,frame, parent=None):
        self.parent = parent
        Frame.__init__(self)
        self.main = self.master
        self.main.geometry('1280x720+200+100')
        self.main.title('Simulación Godzilla')
        
        frame.pack(fill=BOTH,expand=1)
        self.table = pt = Table(frame, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

if __name__ == '__main__':
    
    root = Tk()
    root.title('Simulación Godzilla')
    root.geometry('1280x720')
    btn_font = font.Font(size=14)
    btn_classic = Button(root,text='Calcular por Probabilidad Clásica',
                    width=27,height=1,command=run_classic)
    btn_classic['font'] = btn_font
    btn_classic.place(x=10,y=650)

    btn_subjetive = Button(root,text='Calcular por Probabilidad Subjetiva',
                    width=27,height=1,command=run_subjective)
    btn_subjetive['font'] = btn_font
    btn_subjetive.place(x=460,y=650)

    btn_empiric = Button(root,text='Calcular por Probabilidad Empírica',
                    width=27,height=1,command=run_simulation)
    btn_empiric['font'] = btn_font
    btn_empiric.place(x=910,y=650)
    
    entry1 = Entry(root)
    entry1.place(x=910,y=500)

    entrada = Label(root,text='Ingresar numero de veces que se realizará\n la simulación',height=2)
    entrada.place(x=900,y=450)
    entrada['font'] = btn_font

    image1 = Image.open("godzilla.jpg")
    test = ImageTk.PhotoImage(image1) 
    label1 = Label(image=test)
    label1.image = test  
    label1.place(x=600, y=0)
    image2 = Image.open("mecha.jpg")
    image2 = image2.resize((500,350))
    test = ImageTk.PhotoImage(image2) 
    label1 = Label(image=test)
    label1.image = test  
    label1.place(x=0, y=0)
    root.mainloop()