class HashTable:
    """
    A basic chaining hash table data structure that is used to store packages and retrieve them in a more efficient
    way than a regular list would be able to. Allows data to be retrieved very quickly.
    """

    def __init__(self, table_size=10):
        self.table = []
        for n in range(table_size):
            self.table.append([])

    def search(self, key, multiple=False):
        """
        Searches the hash table for the data that matches the key, can return multiple results
        for example searching "undelivered" will return a list of key, item tuples that all match
        the search parameter, while searching for a package id of 1 would return only a single item
        in the search results list

        This method has a worst case time complexity of O(N) but has a best case of O(1)

        :param key:
        :param multiple:
        :return:
        """
        search_results = []
        holding_bin = hash(key) % len(self.table)  # holding_bin is the location along the table itself where the value has be stored
        bin_collection = self.table[holding_bin]  # bin_collection is the whole chain of items

        for key_item_pair in bin_collection:  # looks through the chain for a key and item pair where the key matches
            if key == key_item_pair[0]:
                if multiple:
                    search_results.append(key_item_pair[1])
                else:
                    search_results = key_item_pair[1]
        return search_results

    def insert(self, key, item):
        """
        insert the item into the correct spot in the hash table this one uses chaining because it reads well and
        makes it convenient to search and return values

        time complexity of O(1)

        :param key:
        :param item:
        :return:
        """
        bin = hash(key) % len(self.table)  # this creates the index where the item will be stored and retrieved from
        bin_collection = self.table[bin]  # the list at the index found by hashing

        bin_collection.append((key, item))  # put the item into the end of the list called chaining

    def remove(self, key, item):
        """
        remove method takes the key and finds the proper bucket then removes from it
        Worst case time complexity of O(N) but a best case of O(1)
        :param key:
        :param item:
        :return:
        """

        bin = hash(key) % len(self.table)
        bin_collection = self.table[bin]

        # Once the index has been established by the key the whole chain must be searched, can contain up to N items
        for key_item_pair in bin_collection:
            if key == key_item_pair[0]:
                if item == key_item_pair[1]:
                    bin_collection.remove(key_item_pair)
                    break

    def __str__(self):
        """
        Define the display when calling the string to be printed
        :return:
        """
        index = 0
        display_string = "\n"
        for bin in self.table:
            display_string = display_string + "%2d : %s \n" % (index, bin)
            index = index + 1

            display_string = display_string + " \n"
        return display_string

    def clear_data(self):
        """
        Purge all data from the hashtable
        :return:
        """
        self.table.clear()
