import DataStorage


# A basic chaining hash table data structure that is used to store packages and retrieve them in a more
# efficient way than a regular list would be able to. Allows data to be retrieved very quickly.
class HashTable:

    def __init__(self, table_size=10):
        self.table = []
        for n in range(table_size):
            self.table.append([])

    # Searches the hash table for the data that matches the key, can return multiple results
    # for example searching "undelivered" will return a list of key, item tuples that all match
    # the search parameter, while searching for a package id of 1 would return only a single item
    # in the search results list
    # This method has a worst case time complexity of O(N) but has a best case of O(1)
    def search(self, key, mutilple=False):
        search_results = []
        bin = hash(key) % len(self.table) # bin is the location along the table itself where the value has be stored
        bin_collection = self.table[bin] # bin_collection is the whole chain of items

        for key_item_pair in bin_collection: #looks through the chain for a key and item pair where the key matches
            if key == key_item_pair[0]:
                if mutilple:
                    search_results.append(key_item_pair[1])
                else:
                    search_results = key_item_pair[1]
        return search_results

    # insert the item into the correct spot in the hash table
    # this one uses chaining because it reads well and makes it convenient to search and return values
    # Time complexity of O(1)
    def insert(self, key, item):
        bin = hash(key) % len(self.table) # this creates the index where the item will be stored and retrieved from
        bin_collection = self.table[bin] # the list at the index found by hashing

        bin_collection.append((key, item)) # put the item into the end of the list called chaining

    # remove method takes the key and finds the proper bucket then removes from it
    # Worst case time complexity of O(N) but a best case of O(1)
    def remove(self, key, item):

        bin = hash(key) % len(self.table)
        bin_collection = self.table[bin]

        # Once the index has been established by the key the whole chain must be searched, can contain up to N items
        for key_item_pair in bin_collection:
            if key == key_item_pair[0]:
                if item == key_item_pair[1]:
                    bin_collection.remove(key_item_pair)
                    break

    # Define the display when calling the string to be printed
    def __str__(self):
        index = 0
        display_string = "\n"
        for bin in self.table:
            display_string = display_string + "%2d : %s \n" % (index, bin)
            index = index + 1

            display_string = display_string + " \n"
        return display_string

# Purge all data from the hashtable
    def clear_data(self):
        self.table.clear()