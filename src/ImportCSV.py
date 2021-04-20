import csv
import pathlib
from Package import Package
import DataStorage
from HashTable import HashTable
from StreetsGraph import *


def import_packages():
    """
    A function to import csv data into the program

    Takes a set file that contains the package data and reads it into the program
    then it loads it into the hashtable and generates Package objects.
    18N+6
    Time complexity of O(N)
    """
    with open((pathlib.Path.cwd() / "src/data/PackageFile.csv")) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        imported_data = list(readCSV)  # import the package data
        num_of_package_data_points = 7

        # data points in each package times the number of packages in the data
        # so that there is limited collisions
        package_space = len(imported_data) * num_of_package_data_points

        DataStorage.packages = HashTable(package_space)
        num_of_packages = 0

        # Read the data into the package objects
        for row in imported_data:
            package_id = row[0]
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            delivery_deadline = row[5]
            mass_kilo = row[6]
            special_notes = row[7]

            # Create a new package
            package = Package(package_id, address, city, state, zip_code, delivery_deadline, mass_kilo, special_notes)
            # Insert package into the hashtable
            DataStorage.packages.insert(package.id, package)
            DataStorage.packages.insert(package.address, package)
            DataStorage.packages.insert(package.city, package)
            DataStorage.packages.insert(package.state, package)
            DataStorage.packages.insert(package.zip, package)
            DataStorage.packages.insert(package.delivery_deadline, package)
            DataStorage.packages.insert(package.mass_kilo, package)
            DataStorage.packages.insert(package.delivery_status, package)
            # track number of packages created
            num_of_packages = num_of_packages + 1

        DataStorage.number_of_packages_in_data = num_of_packages


def import_locations():
    """
    Import the locations and distances from the CSV file and load them into a StreetsGraph this method was chosen
    since it was much easier to import from the CSV than directly from and excel file, and the data could be cleaned up.

    2N^2 + 5N + 4
    This method has a time complexity of O(N^2)
    """
    temp_holding = list()
    with open((pathlib.Path.cwd() / "src/data/DistanceTable.csv")) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        # Assuming the data is formatted correctly there would be N rows equivalent to N Locations
        for row in readCSV:
            temp_holding.append(row)

        # print(temp_holding)
        places_list = temp_holding.pop(0)

        # N items
        for location in temp_holding:
            # print(location)
            name = location.pop(0)

            address = location.pop(0)
            # print(location)
            distances = []
            for distance in temp_holding:
                distances.append(location.pop(0))
            # print(location)
            new_location = Location(name, address, distances)
            DataStorage.streets_map.add_address(new_location)

        # N items * N Items to get the map of distances
        for location in DataStorage.streets_map.adjacent_locations:
            index = 0
            for other_location in DataStorage.streets_map.adjacent_locations:
                DataStorage.streets_map.add_twoway_street(location, other_location, location.distances[index])
                index = index + 1
