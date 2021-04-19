"""
The DataStorage module connects the different types of data in the WGUPS program and controls the level of response in
the output.
"""
from StreetsGraph import StreetsGraph
from DeliveryClock import DeliveryClock
from HashTable import HashTable

streets_map = StreetsGraph()  # A undirected weighted graph data type for mapping the streets
workday_clock = DeliveryClock("8:00 AM")  # Custom clock
packages = HashTable()  # A self implemented hash table to store all the package data
dev_response_enabled = False  # Use to show more detailed output for the programs
number_of_packages_in_data = 0


def search_map(name_or_address):
    """
    Searches the streets map and returns a specified location. This is a convenient interface with the streets_map
    locations. Time complexity of O(N) based on the number of locations in the input.
    :param name_or_address: a string search key
    :return: The location that matches the search key
    """
    # search N items for the search term match
    for location in streets_map.adjacent_locations:
        if location.place_name == name_or_address:
            return location
        if location.address == name_or_address:
            return location
    return None


def dev_response(to_print):
    """
    Control of certain program outputs when creating WGUPS so that there output is not clogged with lots of line by
    line print statements for all different functions.
    :param to_print:
    :return:
    """
    if dev_response_enabled:
        print(to_print)


def clear_data():
    """
    Clean up the data between different functions using it so that the program wont give out bad output when dealing
    with the program running multiple times in a single session.

    Time complexity of O(1)
    """
    streets_map.clear_data()
    packages.clear_data()
