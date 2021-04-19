import math
import DataStorage
from DeliveryClock import DeliveryClock


class DeliveryTruck:
    """ A delivery truck that can deliver packages to different locations

    has knowledge of its location, has packages, has methods to load truck
    to travel its route and to deliver the packages.
    """
    available_drivers = 2
    package_limit = 16
    speed_mph = 18
    trucks_in_fleet = 3

# Constructor for delivery trucks
# Time complexity O(N) due to the search_map() where N is the number of locations in the map
    def __init__(self, truck_id_number):
        self.truck_id_number = truck_id_number
        self.packages = []
        self.assigned_driver = False
        self.distance_travelled = 0.0
        self.hub = DataStorage.search_map("Western Governors University")
        DataStorage.dev_response(f"{self} hub: {self.hub}")
        self.current_location = None
        self.next_location = None

# Assigns a driver to the truck
# O(1)
    def assign_driver(self):
        self.assigned_driver = True
        DeliveryTruck.available_drivers -= 1

# Calculates the travel time for a trip
# returns the time in minutes
# Time complexity of O(1)
    def calc_travel_time(self, distance):
        return (distance / self.speed_mph) * 60

# Checks to make sure that the package can be loaded onto the truck
# and returns true if it is ok to be loaded onto the truck
# Time complexity of O(1) except for an edge case where there is a significant N of packages
# that would be attached as deliver_with's then it would be closer to O(N)
    def ok_to_load(self, package):
        # package must not have aldready been delivered
        if package.delivery_status != "undelivered":
            return False
        # package must not be delayed or if it is then present time should have progressed past the delay
        if package.delayed:
            if package.delayed.compare_time(DataStorage.workday_clock) > 0:
                return False
        # add any packages that must be delivered alongside
        if package.deliver_with:
            # if this was misused then it would slow down this function
            for id in package.deliver_with:
                other_package = DataStorage.packages.search(id)
                if self.ok_to_load(other_package):  # check they meet same critera
                    self.load_package(other_package)
        # package is restricted to a truck and this isnt that truck then do not load
        if package.require_truck:
            if package.require_truck != self.truck_id_number:
                return False

        # handles the wrong address turns it into a delay
        if package.wrong_address:
            package = DataStorage.packages.search(9)
            self.issue_address_correction(package, "410 S State St", "Salt Lake City", "UT", 84111, "10:20 AM")
            package.wrong_address = None
            return False
        # if the package has passed all tests then it is ok to load
        return True

# Load the packages from the warehouse given
# Time complexity O(1) due to early end but it must be run N / 16 number of times to eventually deliver all
# the packages.
    def load_truck(self, warehouse):

        for package in warehouse:
            if self.ok_to_load(package):
                self.load_package(package)
                if len(self.packages) >= self.package_limit:
                    break

# Choose the next package do deliver based on the importance self_adjusting heuristic
# which is a combination of the package's delivery deadline multiplied times the distance to its
# location.
# Time complexity O(N)
    def choose_next_package(self):
        for package in self.packages:
            package.adjust_importance(self.current_location)

        self.packages.sort()
        return self.packages.pop(0)

# Defines how the truck travels the route and reloads more packages until all have been delivered
# the earlyend parameter allows the program to be stopped early and see which are still undelivered
# worst case time complextiy O(N^2)
    def travel_route(self, earlyend=None):
        self.hub = DataStorage.search_map("Western Governors University")
        self.current_location = self.hub
        warehouse = DataStorage.packages.search("undelivered", True)
        number_of_trips = math.ceil(DataStorage.number_of_packages_in_data / self.package_limit)
        while number_of_trips > 0:
            if self.current_location != self.hub:
                self.return_to_hub()
            self.load_truck(warehouse) #O(N)
            while self.packages: #O(N)
                if earlyend:
                    if DataStorage.workday_clock.compare_time(earlyend)  >= -11:
                        return None
                package = self.choose_next_package() #O(N)
                self.deliver_package(package)
            number_of_trips -= 1

        DataStorage.workday_clock = DeliveryClock("8:00 AM")
        print(f"Making deliveries...")
        print(f"total distance for all deliveries: {self.distance_travelled} miles")

# Returns the truck to the hub when it is out of packages and adds that distance to the total distance travelled
# Time complexity of O(1)
    def return_to_hub(self):
        location_distance = float(DataStorage.streets_map.street_distances[self.current_location, self.hub])
        self.distance_travelled = self.distance_travelled + location_distance
        DataStorage.dev_response(f"{self} returned from {self.current_location} {location_distance} to {self.hub}")
        self.current_location = self.hub

# Loads a package onto the truck and updates its status
# Time complexity O(N) due to calling update_package_status()
    def load_package(self, package):
        self.packages.append(package)
        package.delivery_status = "in-route"
        self.update_package_status(package, "undelivered", "in-route")

# Delivers a package to its destination
# Time complexity of O(1)
    def deliver_package(self, package):
        self.next_location = package.location #look to destination
        trip_distance = float(DataStorage.streets_map.street_distances[self.current_location, self.next_location])
        trip_duration = self.calc_travel_time(trip_distance) #
        DataStorage.workday_clock.add_time_minutes_only(trip_duration)
        self.distance_travelled = self.distance_travelled + trip_distance
        package.time_delivered = DeliveryClock(DataStorage.workday_clock.__str__()) #progress clock
        package.delivery_status = "delivered"
        DataStorage.packages.insert("delivered", package)
        DataStorage.dev_response(f"{package} {trip_distance} miles {self} {self.current_location} to {self.next_location} ")
        self.current_location = package.location
        # print(package)

    # Update the status of a package in the hashtable not really great
    # Time complexity of O(N) due to calling a search of the hashtable on the status key
    def update_package_status(self, package, old_status, new_status):
        search_results = DataStorage.packages.search(old_status, True)
        search_results.remove(package)
        DataStorage.packages.insert(new_status, package)

    # changes a wrong address for specified package into a delay once the new address has be received
    # Time complexity O(1)
    def issue_address_correction(self, package, new_address, new_city, new_state, new_zip, delayed_until):
        package.address = new_address
        package.city = new_city
        package.state = new_state
        package.zip = new_zip
        package.location = DataStorage.search_map(f"{new_address} ({package.zip})")
        package.delayed = DeliveryClock(delayed_until)


    # A depiction of the truck for printing out
    # Time complexity of O(1)
    def __repr__(self):
        return "truck " + str(self.truck_id_number)
