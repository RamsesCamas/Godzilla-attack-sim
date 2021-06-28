from itertools import combinations
from math import factorial
import random
import numpy as np
from collections import Counter

#Aplicar distribución uniforme en la arma a escoger

#Aplicar distribución uniforme en la respuesta de Godzilla


get_rnd_uniform= lambda start,end: round(np.random.uniform(start,end))

def run():
    mechas = ['Cherno Alpha','Eva 01','Gigante de acero',
          'Gipsy Danger','Gundam','Jet Jaguar','Mazinger Z',
          'Mechagodzilla','Mechani-Kong','Megazord','Moguera','Voltron']

    all_teams = list(combinations(mechas,3))
    total_combinations = len(all_teams)
    print('Total de combinaciones: ',total_combinations)   

    election = get_rnd_uniform(0,total_combinations)
    elected_team = all_teams[election]
    print(elected_team)
    option = get_rnd_uniform(1,4)
    print(option)
    #Obtener la frecuencia de un elemento
    frecuency = get_total_frec(all_teams,'Mechagodzilla')
    print('Frecuencia de Mecha G: ', frecuency)

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
if __name__ == '__main__':
    run()