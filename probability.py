#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 23:48:35 2024

@author: jazz
"""
# from itertools import permutations
class Item:
    def __init__(self, 
                 chance,
                 proc_coefficient,
                 damage):

        self.chance = chance
        self.proc_coefficient = proc_coefficient  
        self.damage = damage
#Creating Items
atg_missile_mk = Item(0.1, 1.0, 3.0)
ukulele = Item(0.2, 2.0, 6.0)
dang = Item(0.3, 3.0, 9.0)

items = [atg_missile_mk, ukulele, dang]

def permute(items):
    result = []

    if (len(items) == 1):
        return [items[:]]

    for i in range(len(items)):
        n = items.pop(0)

        perms = permute(items)

        for perm in perms:
            perm.append(n)
        result.extend(perms)
        items.append(n)
    
    return result

def translate_to_numbers(result):
    value =[] 
    for i in range(len(result)):
        row=[]
        for j in range(len(result[0])):
             row.append(result[i][j].chance)
             row.append(result[i][j].proc_coefficient)
        value.append(row)
    return value

def max_chain_prob(value):
    chain = value[0]
    answer=[]
    prob = 1
    for i in range(len(chain)):
        prob = prob * chain[i]
    for j in range(len(chain)):
        answer.append(prob/chain[j])
    return answer 

def rest_chain_prob(value):
    chain = []
    prob = 1
    i=0
    p=[]
    length = len(value)
    b=[]
    n=1
    while n<=length:
        for sublist in value:
            first_product = 1.0
            for num in sublist[:-n]:
                first_product *= num
            last_product = (1 - (sublist[-n] * sublist[-n+1]))
            result = first_product * last_product
            b.append(result*100)
        n=n+2

    return b
            

result = permute(items)
value = translate_to_numbers(result)
answer = max_chain_prob(value)
b = rest_chain_prob(value)
print(b)
