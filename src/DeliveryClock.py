import math


class DeliveryClock:
    """
    A class that creates clocks to track the time it takes the truck to make its deliveries.

    Creates the clock using a text string ie "8:00 AM" and does limited error handling bad input so use it properly.
    Built this way because a default python clock or time calculation was not simple enough or created specifically to
    interact with the travel_route() method.
    """

    def __init__(self, time_as_text):
        """
        Creates new DeliverClock's by reading in a string formatted HH:MM AM/PM

        Time complexity of O(1)
        :param time_as_text: a string formatted HH:MM AM/PM
        """
        clock_parts = parse_string_time(time_as_text)
        self.hour = int(clock_parts.pop(0))
        self.minute = int(clock_parts.pop(0))
        self.am_or_pm = clock_parts.pop(0)

        if self.am_or_pm == "PM":
            if self.hour != 12:
                self.hour += 12

        if self.am_or_pm == "AM":
            if self.hour == 12:
                self.hour = 0

        self.total_minutes_value = int((self.hour * 60) + self.minute)

    # Handles bad input for the clock class a bit weirdly, therefore unused.
    # Time complexity of O(1)
    # def apply_clock_rules(self):
    #
    #     if self.hour > 12 | self.hour < 1:
    #         print("hour_field_error: hour must be between 1 and 12.")
    #         exit()
    #     if self.minute > 59 | self.minute < 0:
    #         print("minute_field_error: minutes must be between 0 and 59.")
    #         exit()
    #     if self.am_or_pm != "AM" & self.am_or_pm != "PM":
    #         print("afternoon_field_error: value must be AM or PM")
    #         exit()

    def compare_time(self, other_time):
        """
        Allows two clocks to be compared to one another.

        example:
        clock1 = 8:00 AM = 480 minutes
        clock2 = 8:10 AM = 490 minutes
        480 - 490 = -10
        clock two is later clock

        Time complexity of O(1)
        :param other_time: the time being compared
        :return: the result as an integer of total minutes elapsed
        during the day
        """
        return self.total_minutes_value - other_time.total_minutes_value

    def __str__(self):
        """
        Overrides the default method. Controls how the clock displays itself when printed out.
        Time complexity O(1)
        :return: the proper format for the clock as a string.
        """
        if self.hour > 12:
            hour_string = str(self.hour - 12)
        else:
            hour_string = str(self.hour)

        if self.minute < 10:
            minute_string = "0" + str(self.minute)
        else:
            minute_string = str(self.minute)

        return hour_string + ":" + minute_string + " " + self.am_or_pm

    def add_time_minutes_only(self, minutes):
        """
        Adds a set amount of minutes to the clock and progresses time while tracking if its AM or PM designed to
        work with each iteration of the travel route method so that each destinations travel time can increment
        the overall workday clock.

        Time complexity O(1)

        :param minutes: being added
        :return: the new time
        """
        minutes = math.ceil(minutes)  # get rid of pesky seconds upwards
        self.total_minutes_value += minutes
        self.hour = self.total_minutes_value // 60
        self.minute = self.total_minutes_value % 60

        am_pm_changeover_noon = 12 * 60  # 12 noon in minutes
        am_pm_changeover_midnight = 24 * 60
        self.total_minutes_value = self.total_minutes_value % am_pm_changeover_midnight

        if self.total_minutes_value >= am_pm_changeover_noon:
            self.am_or_pm = "PM"
        else:
            self.am_or_pm = "AM"


def parse_string_time(time_text="12:00 AM"):
    """
    Digests the text input into distinct parts for use in the creation of clocks. Also handles the data from the
    csv file using EOD for END OF DAY which is 5:00 PM.

    Time complexity of O(1)
    :param time_text: a string representation of a time in HH:MM AM/PM format.
    :return: a list of the parts of the clock
    """
    if time_text == "EOD":
        time_text = "5:00 PM"

    text = time_text.split(":")
    hour = text.pop(0)
    temp = text.pop(0).split(" ")
    minute = temp.pop(0)
    am_or_pm = temp.pop(0)

    time_segments = [hour, minute, am_or_pm]

    return time_segments
