# DataStorage module connects the different types of data in the WGUPS program
# and controls the level of response in the output
from StreetsGraph import StreetsGraph
from DeliveryClock import DeliveryClock
from HashTable import HashTable


streets_map = StreetsGraph() # A undirected weighted graph data type for mapping the streets
workday_clock = DeliveryClock("8:00 AM") # Custom clock
packages = HashTable() # A self implremented hash table to store all the package data
dev_response_enabled= False #Use to show more detailed output for the programs
number_of_packages_in_data = 0

# Searches the streets map and returns a specified location
# this is a convienent interface with the streets_map locations
# Time complexity of O(N) based on the number of locations in the input
def search_map(name_or_address):
    #search N items for the search term match
    for location in streets_map.adjacent_locations:
        if location.place_name == name_or_address:
            return location
        if location.address == name_or_address:
            return location
    return None

# Control of certain program outputs when creating WGUPS so that there output is not clogged with
# lots of line by line print statements for all different functions.
def dev_response(to_print):
    if dev_response_enabled:
        print(to_print)

# Clean up the data between different functions using it so that the program wont give out bad output
# when dealing with the program running multiple outputs in a single session.
# Time complexity of O(1)
def clear_data():
    streets_map.clear_data()
    packages.clear_data()
    number_of_packages_in_data = 0