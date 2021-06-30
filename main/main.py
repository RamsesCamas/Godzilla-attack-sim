from itertools import combinations
from math import factorial
import random
import numpy as np
from collections import Counter
from fractions import Fraction

#Cambiar a variables para hacerlas parametrizadas
MECHAS = ['Cherno Alpha','Eva 01','Gigante de acero',
          'Gipsy Danger','Gundam','Jet Jaguar','Mazinger Z',
          'Mechagodzilla','Mechani-Kong','Megazord','Moguera','Voltron']

WEAPONS = {    1:'Combate cuerpo a cuerpo',
               2:'Arma cuerpo a cuerpo',
               3:'Arma a distancia',
               4:'Arma de destrucción masiva'}

GODZILLA_ACTIONS = {    1:'Morder',
                        2:'Zarpazo',
                        3:'Coletazo',
                        4:'Nada',
                        5:'Aliento atómico'}

get_rnd_uniform= lambda start,end: round(np.random.uniform(start,end))

def godzilla_turn(mecha_attack):
    god_chose = 0
    if mecha_attack==1 or mecha_attack ==2:
        god_chose = get_rnd_uniform(1,3)
    elif mecha_attack==3 or mecha_attack ==4:
        god_chose = get_rnd_uniform(4,5)
    godzilla_move = GODZILLA_ACTIONS.get(god_chose)
    return godzilla_move

def get_total_frec(teams,mecha):
    temp_frec = 0
    all_frec = {}
    team_size = len(teams[0])
    for i in range(0,team_size): 
        frecs = Counter(j[i] for j in teams)
        mecha_frec = frecs[mecha]
        all_frec[f'pos {i}'] = mecha_frec
        temp_frec += mecha_frec
    all_frec['total'] = temp_frec
    return all_frec

def run():

    #Conteo
    all_teams = list(combinations(MECHAS,3))
    total_combinations = len(all_teams)
    print('Total de combinaciones: ',total_combinations)   

    election = get_rnd_uniform(0,total_combinations)
    elected_team = all_teams[election]
    print('El Equipo escogido es: ',elected_team)

    #Fase 1
    option = get_rnd_uniform(1,4)
    print('Arma escogida: ',WEAPONS.get(option))

    #Obtener la frecuencia de un elemento
    frecuency = get_total_frec(all_teams,'Mechagodzilla')
    #print('Frecuencia de Mecha G: ', frecuency)
    posi_team = frecuency.get('total')/(len(all_teams[0])*total_combinations)
    posi_fraction = Fraction(posi_team).limit_denominator()
    print(f'Posibilidad de un Mecha de estar en el equipo:\nDecimal:{round(posi_team,3)}\nFracción: {posi_fraction} ')
    
    #Segunda fase
    print('Turno de Godzilla')
    god_attack = godzilla_turn(option)
    print('Godzilla realiza: ',god_attack)

#	CANR010711HCSMJMA1

def summary_battle(team,mecha_attack,godzilla_attack):
    summary = [team,mecha_attack,godzilla_attack]


#Hacer histograma para ver la forma de la curva de las probabilidades

if __name__ == '__main__':
    run()