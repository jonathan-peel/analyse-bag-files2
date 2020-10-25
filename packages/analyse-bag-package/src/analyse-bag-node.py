#!/usr/bin/env python3

print("Python script running ...")

import os
import rosbag

bag_name = os.environ["BAG_NAME"]
bag = rosbag.Bag("mounted-vol/{}".format(bag_name))

for topic in bag.get_type_and_topic_info()[1].keys():
    num_messages = bag.get_message_count(topic)
    print(topic)
    print("  num_messages: {}".format(str(num_messages)))
    

bag.close()
