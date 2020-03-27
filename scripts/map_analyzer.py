#!/usr/bin/env python

import rospy
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PointStamped
from project_3.msg import Result
from math import ceil


class Map:
    def __init__(self):
        self.width = None
        self.height = None
        self.resolution = None
        self.origin = None
        self.data = []
        rospy.Subscriber("/map", OccupancyGrid, callback=self.__map_cb)
        self.__ready = False
        self.__wait = rospy.Rate(10)

    def __map_cb(self, map_msg):
        self.width = map_msg.info.width
        self.height = map_msg.info.height
        self.resolution = map_msg.info.resolution
        self.origin = map_msg.info.origin.position
        self.data = map_msg.data
        self.__ready = True

    def wait_until_ready(self):
        while not self.__ready:
            self.__wait.sleep()

    def position_2_index(self, x, y):
        x_cells = int((x - self.origin.x)/self.resolution)
        y_cells = int((y - self.origin.y)/self.resolution)
        index = y_cells*self.width + x_cells
        return int(index)


if __name__ == "__main__":
    def point_cb(point_msg):
        result.x = point_msg.point.x
        result.y = point_msg.point.y
        index = map.position_2_index(result.x, result.y)
        result.value = map.data[index]
        if result.value == -1:
            result.result = "unknown"
        elif result.value == 100:
            result.result = "occupied"
        elif result.value == 0:
            result.result = "free"
        pub.publish(result)

    rospy.init_node("map_analyzer")
    map = Map()
    map.wait_until_ready()
    rospy.loginfo("Ready to receive a point")
    rospy.Subscriber("/clicked_point", PointStamped, callback=point_cb)
    result = Result()
    pub = rospy.Publisher("occupancy_result", Result, queue_size=1)

    rospy.spin()
