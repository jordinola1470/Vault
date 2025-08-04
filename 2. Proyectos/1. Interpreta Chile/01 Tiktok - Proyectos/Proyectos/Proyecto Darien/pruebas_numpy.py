import numpy as np
import random as ran
import math
answers = ran.randint(1,19)
times_click = math.ceil(answers/3)
lista_click = [1] + [x+3 for x in range(answers) if (x % 3 == 1)]
print(lista_click)
print(range(1,answers))
for j in range(1,answers):
    print(j)
print("Prueba error de rango:")
for i in range(9):
    if i % 3 == 1:
        print(i)
print(answers)
lista_click = [1] + [x+3 for x in range(answers) if (x % 3 == 1)]
print(lista_click[:len(lista_click)-1])
lista = list(range(9))
print(lista)