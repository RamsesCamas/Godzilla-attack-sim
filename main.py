from itertools import combinations
from math import factorial
import random
import numpy as np

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
    top_teams = all_teams[0:10:2]
    print(top_teams)
    option = get_rnd_uniform(1,4)
    print(option)


if __name__ == '__main__':
    run()