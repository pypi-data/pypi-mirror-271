import click
import requests
from connectifycli.graph.graph import Graph
from connectifycli.utils.json import convert_to_graph

@click.group()
def main():
    pass

@main.command()
@click.argument("hash")
def run(hash):
    response = requests.post("", data={})
    if(response.status_code != 200):
        exit("Error retrieving graph")
        
    graph: Graph = convert_to_graph(response.json())
    # run code to for graphs
    


    
