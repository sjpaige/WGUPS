import math
import DataStorage
from DeliveryClock import DeliveryClock


class DeliveryTruck:
    """ A delivery truck that can deliver packages to different locations,
    has knowledge of its location, has packages, has methods to load truck
    to travel its route and to deliver the packages.
    """
    available_drivers = 2
    package_limit = 16
    speed_mph = 18
    trucks_in_fleet = 3

    def __init__(self, truck_id_number):
        """
        Constructs delivery trucks.

        Time complexity O(N) due to the search_map() where N is the number of locations in the map
        :param truck_id_number:
        """
        self.truck_id_number = truck_id_number
        self.packages = []
        self.assigned_driver = False
        self.distance_travelled = 0.0
        self.hub = DataStorage.search_map("Western Governors University")
        DataStorage.dev_response(f"{self} hub: {self.hub}")
        self.current_location = None
        self.next_location = None

    def assign_driver(self):
        """
        Assigns a driver to the truck

        O(1)
        """
        self.assigned_driver = True
        DeliveryTruck.available_drivers -= 1

    def calc_travel_time(self, distance):
        """
        Calculates the travel time for a trip

        Time complexity of O(1)
        :param distance: the distance traveled by the truck
        :return: how long it took to travel the distance
        """
        return (distance / self.speed_mph) * 60

    def ok_to_load(self, package):
        """
        Checks to make sure that the package can be loaded onto the truck and returns true if it is ok to be
        loaded onto the truck.

        Time complexity of O(1) except for an edge case where there is a significant N of packages
        that would be attached as deliver_with's then it would be closer to O(N).

        :param package: That is being checked for loading.
        :return: True if the package has passed all checks.
        """

        # package must not have already been delivered
        if package.delivery_status != "undelivered":
            return False
        # package must not be delayed or if it is then present time should have progressed past the delay
        if package.delayed:
            if package.delayed.compare_time(DataStorage.workday_clock) > 0:
                return False
        # add any packages that must be delivered alongside
        if package.deliver_with:
            # if this was misused then it would slow down this function
            for package_id in package.deliver_with:
                other_package = DataStorage.packages.search(package_id)
                if self.ok_to_load(other_package):  # check they meet same criteria
                    self.load_package(other_package)
        # package is restricted to a truck and this isn't that truck then do not load
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

    def load_truck(self, warehouse):
        """
        Load the packages from the warehouse onto the delivery truck while the truck still has room.
        :param warehouse: that contains packages

        Time complexity O(1) due to early end but it must be run N / 16 number of times to eventually deliver all
        the packages.
        """
        for package in warehouse:
            if self.ok_to_load(package):
                self.load_package(package)
                if len(self.packages) >= self.package_limit:
                    break

    def choose_next_package(self):
        """
        Choose the next package to deliver based on the scale of the self_adjusting heuristic
        which is a combination of the package's delivery deadline multiplied by the distance to its
        destination.

        Time complexity O(N)
        :return: Package to be delivered next based on importance metric.
        """
        for package in self.packages:
            package.adjust_importance(self.current_location)

        self.packages.sort()
        return self.packages.pop(0)

    def travel_route(self, early_end=None):
        """
        Defines how the truck travels the route and reloads more packages until all have been delivered the early_end
        parameter allows the program to be stopped early and see which are still undelivered.

        Worst Case Time Complexity: O(N^2)

        :param early_end: Used in the condition that the simulation should be stopped early to check the status.
        """
        self.hub = DataStorage.search_map("Western Governors University")
        self.current_location = self.hub
        warehouse = DataStorage.packages.search("undelivered", True)
        number_of_trips = math.ceil(DataStorage.number_of_packages_in_data / self.package_limit)
        while number_of_trips > 0:
            if self.current_location != self.hub:
                self.return_to_hub()
            self.load_truck(warehouse)  # O(N)
            while self.packages:  # O(N)
                if early_end:
                    if DataStorage.workday_clock.compare_time(early_end) >= -11:
                        return None
                package = self.choose_next_package()  # O(N)
                self.deliver_package(package)
            number_of_trips -= 1

        DataStorage.workday_clock = DeliveryClock("8:00 AM")
        print(f"Making deliveries...")
        print(f"total distance for all deliveries: {self.distance_travelled} miles")

    def return_to_hub(self):
        """
        Returns the truck to the hub when it is out of packages and adds that distance to the total distance travelled.

        Time complexity of O(1)
        """
        location_distance = float(DataStorage.streets_map.street_distances[self.current_location, self.hub])
        self.distance_travelled = self.distance_travelled + location_distance
        DataStorage.dev_response(f"{self} returned from {self.current_location} {location_distance} to {self.hub}")
        self.current_location = self.hub

    def load_package(self, package):
        """
        Loads a package onto the truck and updates its status

        Time complexity O(N) due to calling update_package_status()
        """
        self.packages.append(package)
        package.delivery_status = "in-route"
        self.update_package_status(package, "undelivered", "in-route")

    def deliver_package(self, package):
        """
        Delivers a package to its destination.

        Time complexity of O(1)

        """

        self.next_location = package.location  # look to destination
        trip_distance = float(DataStorage.streets_map.street_distances[self.current_location, self.next_location])
        trip_duration = self.calc_travel_time(trip_distance)  #
        DataStorage.workday_clock.add_time_minutes_only(trip_duration)
        self.distance_travelled = self.distance_travelled + trip_distance
        package.time_delivered = DeliveryClock(DataStorage.workday_clock.__str__())  # progress clock
        package.delivery_status = "delivered"
        DataStorage.packages.insert("delivered", package)
        DataStorage.dev_response(
            f"{package} {trip_distance} miles {self} {self.current_location} to {self.next_location} ")
        self.current_location = package.location

    def update_package_status(self, package, old_status, new_status):
        """
        Update the status of a package in the hashtable not really great
        Time complexity of O(N) due to calling a search of the hashtable on the status key
        :param package:
        :param old_status:
        :param new_status:
        :return:
        """
        search_results = DataStorage.packages.search(old_status, True)
        search_results.remove(package)
        DataStorage.packages.insert(new_status, package)

    def issue_address_correction(self, package, new_address, new_city, new_state, new_zip, delayed_until):
        """
        changes a wrong address for specified package into a delay once the new address has be received

        Time complexity O(1)

        :param package:
        :param new_address:
        :param new_city:
        :param new_state:
        :param new_zip:
        :param delayed_until:
        :return:
        """
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
