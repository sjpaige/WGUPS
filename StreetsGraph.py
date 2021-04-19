
# Creates StreetsGraph's that can map out the distances between locations bidirectionally or a single direction.
# Has a subclass of location that holds data that is imported in ImportCSV and is used to construct those objects.
# Time complexity for all in this module is O(1)
class StreetsGraph:
    def __init__(self):
        self.adjacent_locations={}
        self.street_distances={}

# Adds a new address to the list of adjacent locations
    def add_address(self, new_address):
        self.adjacent_locations[new_address] = []

# returns the location specified
    def get_address(self, location):
        return self.adjacent_locations[location]

# Adds a one way connection "street" between two locations
    def add_oneway_street(self, from_address, to_address, distance=1.0):
        self.street_distances[(from_address,to_address)] = distance
        self.adjacent_locations[from_address].append(to_address)

# Adds the same type of connection but in both directions for the same distance
    def add_twoway_street(self, a_street, b_street, distance=1.0):
        self.add_oneway_street(a_street,b_street,distance)
        self.add_oneway_street(b_street,a_street,distance)

# Wipes out all the data stored in the StreetsGraph
    def clear_data(self):
        self.adjacent_locations.clear()
        self.street_distances.clear()

# Small subclass used in the StreetsGraph to hold location data that interacts with the import functions in Import CSV
class Location:

# Constructor for the locations
    def __init__(self, new_place_name, new_address, new_distances):
        self.place_name = new_place_name
        self.address = new_address
        self.distances = new_distances
        self.packages_bound_here=[]

# Blurb to pass out when displaying location data
    def __repr__(self):
        return f"{self.place_name} {self.address}"
