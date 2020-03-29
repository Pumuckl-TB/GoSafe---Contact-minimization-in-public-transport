# Import libraries
from __future__ import print_function
from ortools.graph import pywrapgraph
import numpy as np
import random
from random import seed
from random import randint
import argparse


def argparse_func():

  argp = argparse.ArgumentParser()
  argp.add_argument('--start_nodes', required=False, default = [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 3])
  argp.add_argument('--end_nodes', required=False, default = [1, 2, 3, 4, 5, 4, 3, 2, 1, 0, 5])
  argp.add_argument('--capacities', required=False, default = [2, 3, 1, 3, 1, 3, 3, 4, 1, 2, 2])
  argp.add_argument('--true_time', required=False, default = [2, 2, 1, 4, 2, 3, 2, 4, 4, 6, 3])
  ns = argp.parse_args()

  start_nodes, end_nodes, capacities, true_time = \
    ns.start_nodes, ns.end_nodes, ns.capacities, ns.true_time

  return start_nodes, end_nodes, capacities, true_time


def main(requ, morerequ=None ):

  start_nodes, end_nodes, capacities, true_time = argparse_func()
  n = len(true_time)
  if morerequ == None:
  	print('no overlap with previous request')
  	listofzeros = [0] * n
  	penalized_time = [x + y for x, y in zip(true_time, listofzeros)]
  
  
  else: 
    print("overlap with previous request")
    listofzeros = [0] * n
    for i in morerequ:  
      for j in i:
        for j_1, value_start in enumerate(start_nodes):
          for j_2, value_end in enumerate(end_nodes):
            if value_start ==j[0] and value_end ==j[1] and j_1 == j_2:
              listofzeros[j_1] +=1
    
    people_in_the_system_at_location = listofzeros

    penalized_time = [x + y*y for x, y in zip(true_time, people_in_the_system_at_location)]

  
  # Define an array of supplies at each node.
  # passenger requests origin and target +1 at node at which he starts -1 at node at which he arrived 
  supplies = [0] * np.max(start_nodes + end_nodes) 
  supplies[requ[0]] = 1
  supplies[requ[1]] = -1
    

  # Instantiate a SimpleMinCostFlow solver. 
  min_cost_flow = pywrapgraph.SimpleMinCostFlow()

  # Add each arc.
  for i in range(0, len(start_nodes)):
    min_cost_flow.AddArcWithCapacityAndUnitCost(start_nodes[i], end_nodes[i], capacities[i], penalized_time[i])

  # Add node supplies.
  for i in range(0, len(supplies)):
    min_cost_flow.SetNodeSupply(i, supplies[i])

  # Initiate arrays
  xpath = []
  total_true_time = []
  index = []
  cost_total=0
  cum_time_in_path=0

  # Find the minimum cost flow - run the optimizer & extract optimization path
  if min_cost_flow.Solve() == min_cost_flow.OPTIMAL:

    # Print optimization results
    print('Minimum penalized time:', min_cost_flow.OptimalCost())
    print('')
    print('  Arc    Flow / Capacity  Cost')
    for i in range(min_cost_flow.NumArcs()):
      cost = min_cost_flow.Flow(i) * min_cost_flow.UnitCost(i)
      print('%1s -> %1s   %3s  / %3s       %3s' % (
          min_cost_flow.Tail(i),
          min_cost_flow.Head(i),
          min_cost_flow.Flow(i),
          min_cost_flow.Capacity(i),
          cost))
      if min_cost_flow.Flow(i) != 0: 
        index.append(i)
        cost_total = cost_total + cost
        print(cost_total)
        cum_time_in_path += true_time[i]
        xpath.append((min_cost_flow.Tail(i), min_cost_flow.Head(i), requ[2]+cum_time_in_path)) 
        
  else:
    print('There was an issue with the min cost flow input.')

  
  true_time = [true_time[i] for i in index]
  total_true_time = sum(true_time)
  time_of_arrival = requ[2] + total_true_time

  return xpath, time_of_arrival




if __name__ == '__main__':
  
  start_nodes, end_nodes, capacities, true_time = argparse_func()

  # Create list of random itinerary inquiriries
  lst = []
  for i in range(1,20):
    n = randint(1,5)
    lst.append(n)

  lst = lst[:] 
  seen = set() 
  for i in range(len(lst)):
      if (lst[i] <= lst[i-1]): 
          lst[i] = lst[i-1] + 1 
          while lst[i] in seen:
            lst[i] += 1  
      seen.add(lst[i])   

  requ = []
  for i in lst:
    a, b = random.sample(range(0, 5), 2)
    requ.append((a,b, i)) 
  print("I want to go this way: = {}" .format(requ))


  list_xpath=[]

  for i in range(len(requ)):
    all_formerpaths=[]

    if i==0:
      print("\n request {}" .format(i))
      xpath, time_of_arrival = main(requ[i])
      list_xpath.append(xpath)

    else:

      if requ[i-1][2] < time_of_arrival:
        print("\n request {}" .format(i))

        for i in range(len(list_xpath)):
          if i == len(list_xpath):
            break

          all_formerpaths.append(list_xpath[i])
          
        xpath, time_of_arrival = main(requ[i], all_formerpaths)
        list_xpath.append(xpath)
      
      else:
        print("\n request {}" .format(i))
        xpath, time_of_arrival = main(requ[i])
        list_xpath.append(xpath)

