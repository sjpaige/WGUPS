from DeliveryClock import DeliveryClock
import StreetsGraph
import DataStorage


# The package data type holds all of the data for an individual package and has important methods for parsing
# the raw data into more complex or usable forms.
# Time complexity for all items here is O(1) other than the search_ functions but unless the special note
# data field has a huge N that would not have a large impact
class Package:

    def __init__(self, new_id, address, city, state, zip, delivery_deadline, mass_kilo, special_notes,
                 delivery_status="undelivered"):
        self.id = int(new_id)
        self.address = address
        self.city = city
        self.state = state
        self.zip = int(zip)
        self.delivery_deadline = delivery_deadline
        self.mass_kilo = str(mass_kilo) + " kg"
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.location = DataStorage.search_map(f"{self.address} ({self.zip})")
        self.time_delivered = None
        self.package_importance = self.find_importance()
        self.require_truck = self.search_required_truck(special_notes)
        self.delayed = self.search_delayed_time(special_notes)
        self.deliver_with = self.search_deliver_with(special_notes)
        self.wrong_address = self.search_wrong_address(special_notes)

    # Add a location to the package that corresponds to the address
    def add_location(self, new_location):
        self.location = new_location

    # Add a time when the package was finally delivered
    def add_delivered_time(self, new_time):
        self.time_delivered = DeliveryClock(new_time)

    # find the initial importance value which is important to being able to
    def find_importance(self):
        delivery_deadline_metric = DeliveryClock(self.delivery_deadline).total_minutes_value
        return delivery_deadline_metric

    # Heuristic to adjust the importance of the package
    def adjust_importance(self, current_location):
        distance = DataStorage.streets_map.street_distances[current_location, self.location]
        self.package_importance = float(distance)

    # Parse the special note text for any required trucks
    def search_required_truck(self, note=""):
        if note.__contains__("Can only be on"):
            truck_index = note.find("truck")
            required_truck_id = note[truck_index + 6:truck_index + 7]
            return int(required_truck_id)
        return None

    # Parse the speical note text for any delays
    def search_delayed_time(self, note=""):
        if note.__contains__("Delayed"):
            find_clock_index = note.find(":")
            hour = note[find_clock_index - 2:find_clock_index]
            minute = note[find_clock_index + 1:find_clock_index + 3]
            am_or_pm = note[find_clock_index + 4:find_clock_index + 6].upper()
            clock_gen_text = f"{hour}:{minute} {am_or_pm}"
            return DeliveryClock(clock_gen_text)
        return None

    # Parse he special note text for any wrong address
    def search_wrong_address(self, note=""):
        if note.__contains__("Wrong address"):
            return True
        return False

    # Parse the special note text for any packages that must be delivered with this one
    def search_deliver_with(self, note=""):
        if note.__contains__("Must be delivered with"):
            deliver_with_ids = note.replace("Must be delivered with", " ", 1).rsplit(',')
            deliver_with_list = []
            for id in deliver_with_ids:
                deliver_with_list.append(int(id))
            return deliver_with_list
        return []

    # Define the display when calling the string to be printed
    def __repr__(self):
        return f"id:{self.id} current_status:{self.delivery_status} time_delivered: {self.time_delivered} destination: {self.address} {self.city} {self.state} {self.zip} " \
               f"notes: {self.special_notes}"

    # Defines the less-than functionality
    def __lt__(self, other):
        return self.package_importance < other.package_importance
