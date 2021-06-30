from itertools import combinations
from itertools import chain
from math import factorial
import random
from pandas.core.indexes import multi
import numpy as np
from collections import Counter
from fractions import Fraction
import pandas as pd

#Cambiar a variables para hacerlas parametrizadas
MECHAS = ['Cherno Alpha','Eva 01','Gigante de acero',
          'Gipsy Danger','Gundam','Jet Jaguar','Mazinger Z',
          'Mechagodzilla','Mechani-Kong','Megazord','Moguera','Voltron']

WEAPONS = {    1:'Combate cuerpo a cuerpo',
               2:'Arma de destrucción masiva',
               3:'Arma cuerpo a cuerpo',
               4:'Arma a distancia'
               }

GODZILLA_ACTIONS = {    1:'Morder',
                        2:'Nada',
                        3:'Coletazo',
                        4:'Aliento atómico',
                        5:'Zarpazo'}

get_rnd_uniform= lambda start,end: round(np.random.uniform(start,end))

summary_battle = lambda team,mecha_attack,godzilla_attack: [team,mecha_attack,godzilla_attack]


#posi_fraction = Fraction(decimal).limit_denominator()

def godzilla_turn(mecha_attack):
    god_keys = list(GODZILLA_ACTIONS.keys())
    god_chose = 0
    if mecha_attack%2==0:
        #Ataque a distancia
        keys_god = [i for i in god_keys if i%2==0]
        god_chose = get_rnd_uniform(keys_god[0],keys_god[-1])
    else:
        #Ataque cercano
        keys_god = [i for i in god_keys if i%2!=0]
        god_chose = get_rnd_uniform(keys_god[0],keys_god[-1])
    godzilla_move = GODZILLA_ACTIONS.get(god_chose)
    return godzilla_move

def classic_prob():
    god_keys = list(GODZILLA_ACTIONS.keys()) 

    odd_g_keys = [i for i in god_keys if i%2!=0]
    pair_g_keys = [i for i in god_keys if i%2==0]
    odd_matrix = []
    pair_matrix = []

    for i in WEAPONS.keys():
        if i%2!=0:
            odd_matrix.append(odd_g_keys)
        else:
            pair_matrix.append(pair_g_keys)

    frec_odd = dict(Counter(chain(*odd_matrix)))
    frec_pair = dict(Counter(chain(*pair_matrix)))
    all_frec = frec_odd.copy()
    all_frec.update(frec_pair)
    total_config = sum(list(frec_pair.values()) + list(frec_odd.values()))

    counting_table = {'Salida':[],'Probabilidad':[],'Redondeado':[]}
    for i in GODZILLA_ACTIONS.keys():
        prob = f'{all_frec.get(i)}/{total_config}'
        prob_r = Fraction(f'{all_frec.get(i)}/{total_config}').limit_denominator()
        counting_table.get('Salida').append(f'P({GODZILLA_ACTIONS.get(i)})')
        counting_table.get('Probabilidad').append(prob)
        counting_table.get('Redondeado').append(prob_r)
    return counting_table

def sub_prob():
    god_keys = list(GODZILLA_ACTIONS.keys()) 
    weapon_keys= list(WEAPONS.keys())

    odd_g_keys = [i for i in god_keys if i%2!=0]
    pair_g_keys = [i for i in god_keys if i%2==0]
    sub_weapons = {}
    
    sub_res = {}
    for i in weapon_keys:
        pair_god_probs = []
        odd_god_probs = []
        sub_weapons[i] = 1/len(weapon_keys)
        if i%2==0:
            for _ in pair_g_keys:
                pair_god_probs.append(1/len(pair_g_keys))
            multi_pos = [x * sub_weapons.get(i) for x in pair_god_probs]
            sub_res[f'{i}'] = (sub_weapons.get(i),multi_pos,sum(multi_pos))
        else: 
            for _ in odd_g_keys:
                odd_god_probs.append(1/len(odd_g_keys))
            multi_pos = [x * sub_weapons.get(i) for x in odd_god_probs]
            sub_res[f'{i}'] = (sub_weapons.get(i),multi_pos,sum(multi_pos))
    all_sub_prob = {}
    total = 0
    for i in sub_res.keys():
        sub_tuple = sub_res.get(i)
        option_pos = str(Fraction(sub_tuple[0]))
        list_pos = sub_tuple[1]

        list_pos = [str(Fraction(x).limit_denominator()) for x in list_pos]
        res_pos = str(Fraction(sub_tuple[2]))
        total += sub_tuple[2]
        all_sub_prob[i] = (option_pos,list_pos,res_pos)
    all_sub_prob['total'] = total
    return all_sub_prob

def empiric_prob():
    #Conteo
    all_teams = list(combinations(MECHAS,3))
    total_combinations = len(all_teams)
    #print('Total de combinaciones: ',total_combinations)   

    election = get_rnd_uniform(0,total_combinations)
    if election == total_combinations:
        election-=1
    elected_team = all_teams[election]
    #print(election)
    #print('El Equipo escogido es: ',elected_team)

    #Fase 1
    weapons_keys = list(WEAPONS.keys())
    option = get_rnd_uniform(weapons_keys[0],weapons_keys[-1])
    weapon = WEAPONS.get(option)    
    
    #Segunda fase
    god_attack = godzilla_turn(option)
    summary = summary_battle(elected_team,weapon,god_attack)
    return summary

def get_frequency(my_list,item):
    frec = dict(Counter(my_list))
    item_frec= frec.get(item)
    return item_frec

get_e_prob =  lambda frec,size: frec/size

#Hacer histograma para ver la forma de la curva de las probabilidades

if __name__ == '__main__':
    
    #Probabilidad Clásica
    counting_table = classic_prob()
    df_classic_prob = pd.DataFrame(counting_table)
    #print(df_classic_prob)

    #Probabilidad Subjetiva
    sub_prob_table = sub_prob()
    df_sub_prob = pd.DataFrame(sub_prob_table).transpose()
    df_sub_prob.columns = ['Mecha Ataque','Prob. Godzilla','Prob. Total']
    #print(df_sub_prob)

    #Probabilidad empírica
    n = int(input('Ingrese el número de simulaciones a realizar: '))
    sim_godzilla_attacks =[]
    for i in range(n):
        summary = empiric_prob()
        sim_godzilla_attacks.append(summary[2])
    all_e_prob = []    
    frec = get_frequency(sim_godzilla_attacks,'Morder')
    print('Frecuencia de Morder: ',frec)
    e_prob = get_e_prob(frec,len(sim_godzilla_attacks))
    all_e_prob.append(e_prob)
    print('Probabilidad de Morder: ',"{:.2%}".format(e_prob))

    frec = get_frequency(sim_godzilla_attacks,'Nada')
    print('Frecuencia de Nada: ',frec)
    e_prob = get_e_prob(frec,len(sim_godzilla_attacks))
    all_e_prob.append(e_prob)
    print('Probabilidad de Nada: ',"{:.2%}".format(e_prob))

    frec = get_frequency(sim_godzilla_attacks,'Coletazo')
    print('Frecuencia de Coletazo: ',frec)
    e_prob = get_e_prob(frec,len(sim_godzilla_attacks))
    all_e_prob.append(e_prob)
    print('Probabilidad de Coletazo: ',"{:.2%}".format(e_prob))

    frec = get_frequency(sim_godzilla_attacks,'Aliento atómico')
    print('Frecuencia de Aliento atómico: ',frec)
    e_prob = get_e_prob(frec,len(sim_godzilla_attacks))
    all_e_prob.append(e_prob)
    print('Probabilidad de Aliento atómico: ',"{:.2%}".format(e_prob))

    frec = get_frequency(sim_godzilla_attacks,'Zarpazo')
    print('Frecuencia de Zarpazo: ',frec)
    e_prob = get_e_prob(frec,len(sim_godzilla_attacks))
    all_e_prob.append(e_prob)
    print('Probabilidad de Zarpazo: ',"{:.2%}".format(e_prob))

    print('suma total: ',sum(all_e_prob))