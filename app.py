import copy
from typing import List

import click
import emoji
from PyInquirer import prompt

from data import *

def get_node_attr(station_name: str, last_node: Node, final_state: str) -> Node:
  station_node = copy.copy(paris_subway[station_name])
  idx_last_node = int(last_node.station[1:])-1
  idx_station_node = int(station_node.station[1:])-1
  idx_final_state = int(final_state[1:])-1

  station_node.estimate_cost = estimate_sym_matrix[idx_station_node, idx_final_state]
  station_node.real_cost_so_far = last_node.real_cost_so_far + real_sym_matrix[idx_station_node, idx_last_node]
  station_node.parent = last_node.station
  station_node.path_so_far = last_node.path_so_far + [station_name]

  return station_node


def askStation(message: str):
  station = prompt(
    [
      {
        'type': 'list',
        'name': 'station',
        'message': message,
        'choices': ['E' + str(i + 1) for i in range(14)]
      }
    ]
  )

  return station


@click.command()
def search_route():
  initial_state = askStation('From which station?')['station']
  final_state = askStation('To which station?')['station']

  initial_node: Node = paris_subway[initial_state]
  initial_node.path_so_far = [initial_node.station]
  frontier: List[Node] = list([initial_node])

  while frontier:
    
    current_node = frontier[0]
    click.echo(f'Current node is {current_node.station}')
    del frontier[0]
    
    if current_node.station == final_state:
      click.echo(f'We found a good path from {initial_state} to {final_state}! {emoji.emojize(":train:")}')
      click.echo(f"Take this path {' --> '.join(current_node.path_so_far)} and it will take you around {round(current_node.real_cost_so_far*60)} minutes to get there!")
      return
    
    # Children nodes
    connections = [connection for connection in current_node.connections if connection != current_node.parent] # exclude parent node
    if connections:
      children_nodes = [get_node_attr(child, current_node, final_state) for child in connections]
    else:
      print(f'End of line for node {current_node.station} \n')
      continue

    # Append node to frontier and sort according to total cost
    frontier.extend(children_nodes)
    frontier.sort(key=lambda x: (x.real_cost_so_far + x.estimate_cost))
    print(f'Sorted frontier {[(node.station, f"Total cost {round(node.real_cost_so_far + node.estimate_cost, 2)}", f"Parent node {node.parent}") for node in frontier]} \n')

  click.echo(f"Sorry, there is no path connecting these stations {emoji.emojize(':disappointed_face:')}")

if __name__ == "__main__":
  search_route()