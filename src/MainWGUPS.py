# Author: Sebastian Paige
# Main module where the delivery program runs
# The menu function operates the functions of the program.
import DataStorage
import ImportCSV
from DeliveryTruck import DeliveryTruck
from DeliveryClock import DeliveryClock

truck2 = DeliveryTruck(2)


def start_up_procedure():
    """
    Resets and imports data for multiple runs so that the data does not get all corrupted.

    Time complexity O(N)
    """
    DataStorage.clear_data()  # clear the data
    truck2.distance_travelled = 0  # reset the truck's distance so that it can run again
    ImportCSV.import_locations()  # import the locations from the csv
    ImportCSV.import_packages()  # import the packages from the csv


def run_delivery():
    """
    Runs a full delivery of the route for a whole workday.

    Time complexity of O(N^2)
    """
    truck2.travel_route()


def check_delivery_status(time_input):
    """
    Allows the program to be stopped at a set time to see the status of all packages for that time so that the all
    the delivery factors can be confirmed.

    Time complexity between O(1) and O(N^2) since the early exit of the delivery algorithm will reduce the load
    :param time_input:
    """
    end_time = DeliveryClock(time_input)
    truck2.travel_route(end_time)
    packages = DataStorage.packages.search("undelivered", True)
    for package in packages:
        print(package)


def look_up():
    """
    Look up a single or multiple packages based on search keywords like the package ID or the delivery address.

    Time complexity up to O(N)
    :return: A single or multiple packages that match the keywords.
    """
    print("enter a search term like: ")
    print(
        "package ID number, delivery address, delivery deadline, delivery city, delivery zip_code code, package weight, "
        "delivery status (e.g., delivered, in route)")
    search_term = input()
    if search_term == "menu":
        menu()
    print("return multiple? t=true / f=false")
    multiple = input()
    if multiple == "t":
        multiple = True
    elif multiple == "f":
        multiple = False

    try:  # Try to search for the package id but if its not an id then it will error
        search_term = int(search_term)
    except ValueError:
        ValueError("")

    # Make sure that the search term is valid
    search_result = DataStorage.packages.search(search_term, multiple)
    if not search_result:
        print("not a valid term try again or menu to go back")
        look_up()
    # If there are multiple results like searching for all package of a weight or certain status then it will show
    if multiple:
        for result in search_result:
            print(result)
    else:
        print(search_result)


# Allows users to check the mileage for partial delivery routes
# Time complexity O(1)
def mileage_check():
    print(f"{truck2} : travelled {truck2.distance_travelled} miles")


def menu():
    """
    Menu controls the program based on user input.

    Time complexity of O(n^2) for each run_delivery() less for early exits other menu items are negligible impact
    """
    print("0 - exit")
    print("1 - run full delivery")
    print("2 - run delivery up to time + all packages display status")
    print("3 - look up package")
    print("4 - check mileage")
    print("5 - reset all data")

    menu_input = input("")

    if menu_input == "0":
        return 0
    if menu_input == "1":
        start_up_procedure()
        run_delivery()
        menu()
    if menu_input == "2":
        print("enter time (H:MM AM/PM) exactly")
        start_up_procedure()
        check_delivery_status(input())
        menu()
    if menu_input == "3":
        look_up()
        menu()
    if menu_input == "4":
        mileage_check()
        menu()
    if menu_input == "5":
        print("resetting data...")
        start_up_procedure()
        menu()


print("importing packages...")
print("importing locations...")
menu()
