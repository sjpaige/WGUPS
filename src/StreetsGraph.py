class StreetsGraph:
    """
    Creates StreetsGraph's that can map out the distances between locations bidirectionally or a single direction.
    Has a subclass of location that holds data that is imported in ImportCSV and is used to construct those objects.

    Time complexity for all in this module is O(1)
    """

    def __init__(self):
        """
        Constructs new StreetsGraphs.
        """
        self.adjacent_locations = {}
        self.street_distances = {}

    def add_address(self, new_address):
        """
        Adds a new address to the list of adjacent locations.
        :param new_address: A new address.
        """
        self.adjacent_locations[new_address] = []

    def get_address(self, location):
        """
        Retrieves the adjacent locations list for the passed location.
        """
        return self.adjacent_locations[location]

    def add_oneway_street(self, from_address, to_address, distance=1.0):
        """
        Adds a one way connection "street" between two locations
        :param from_address: An address at one end of the street.
        :param to_address: An address at the other end of the street.
        :param distance: Distance between the two addresses.
        """
        self.street_distances[(from_address, to_address)] = distance
        self.adjacent_locations[from_address].append(to_address)

    def add_two_way_street(self, a_street, b_street, distance=1.0):
        """
        Adds the same type of connection but in both directions for the same distance
        :param a_street:
        :param b_street:
        :param distance:
        """
        self.add_oneway_street(a_street, b_street, distance)
        self.add_oneway_street(b_street, a_street, distance)

    def clear_data(self):
        """
        Clears out all the data stored in the StreetsGraph.
        """
        self.adjacent_locations.clear()
        self.street_distances.clear()


class Location:
    """
    Small subclass used in the StreetsGraph to hold location data that interacts with the import functions
    in Import CSV.
    """

    def __init__(self, new_place_name, new_address, new_distances):
        """
        Creates new locations for use by the StreetsGraph.
        :param new_place_name: The name of the location.
        :param new_address: The full address of the location.
        :param new_distances: The distances associated with the location.
        """
        self.place_name = new_place_name
        self.address = new_address
        self.distances = new_distances
        self.packages_bound_here = []

    # Blurb to pass out when displaying location data
    def __repr__(self):
        return f"{self.place_name} {self.address}"
