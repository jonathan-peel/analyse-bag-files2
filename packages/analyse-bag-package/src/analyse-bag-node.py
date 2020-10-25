#!/usr/bin/env python3

import os
import rosbag
import numpy as np

"""This node analysis a rosbag bag and prints a formatted dictionary of the
   number of messages and time periods between the messages for each topic.
   The data is also saved as a dictionary for potential later use, and it is
   printed according to the specific format outlined in Exercise 19.
"""

# Extract the bag name from the runtime environment variable
bag_name = os.environ["BAG_NAME"]
bag = rosbag.Bag("mounted-vol/{}".format(bag_name))

# Initialise the dictionary containing all the data
bag_data = {}

# Loop through each of the topics present in the bag
for topic in bag.get_type_and_topic_info()[1].keys():
    # Find the number of messages in this topic
    num_messages = bag.get_message_count(topic)

    # Collect a list of the timestamps for each message in this topic
    timestamps = []
    for msg in bag.read_messages(topic):
        timestamps.append(msg[2])

    # Use the timestamps to find the time differences (period) between each
    # message
    time_diffs_secs = []
    for i in range(num_messages-1):
        time_diff = timestamps[i+1] - timestamps[i]
        time_diffs_secs.append(time_diff.to_sec())

    # Calculate statistical properties of the messages
    min_ = min(time_diffs_secs)
    max_ = max(time_diffs_secs)
    average = np.average(time_diffs_secs)
    median = np.median(time_diffs_secs)

    # Assemble the topic data into the bag_data dictionary
    bag_data[topic] = {
        "num_messages": num_messages,
        "period" : {
            "min" : min_,
            "max" : max_,
            "average": average,
            "median": median
        }
    }

    # Print the topic data in the form specified in Exercise 19
    print(topic)
    print("  num_messages: {}".format(str(num_messages)))
    print("    period:")
    print("      min: {}".format(str(round(min_, 2))))
    print("      max: {}".format(str(round(max_, 2))))
    print("      average: {}".format(str(round(average, 2))))
    print("      median: {}".format(str(round(median, 2))))
    print("")

# Close the bag
bag.close()
