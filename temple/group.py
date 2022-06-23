import math

from temple import temple


class TempleGroup():
    def __init__(self, temple_list: list, start_id: int, goal_id: int) -> None:
        self.start_id = start_id
        self.goal_id = goal_id
        self.temple_item = temple_list
        self.len = len(temple_list)
        self.distance_dict = self.__distance_dict()

    def __getitem__(self, index) -> temple.Temple:
        return self.temple_item[index]

    def __len__(self) -> int:
        return self.len

    def __calc_length(self, t1: temple.Temple, t2: temple.Temple) -> float:
        dx = abs(t1.x - t2.x)
        dy = abs(t1.y - t2.y)
        return math.sqrt(dx**2+dy**2)

    def __distance_dict(self) -> dict:
        distance_dict = {}
        temple_count = len(self.temple_item)
        for start_index in range(temple_count-1):
            for goal_index in range(start_index+1, temple_count):
                start_temple = self[start_index]
                goal_temple = self[goal_index]
                score_id = start_temple.id + goal_temple.id
                distance_dict[score_id] = self.__calc_length(
                    start_temple, goal_temple)
        return distance_dict

    def distance(self, start_id: int, goal_id: int) -> float:
        minv = min(start_id, goal_id)
        maxv = max(start_id, goal_id)
        start_id = str(minv).zfill(2)
        goal_id = str(maxv).zfill(2)
        return self.distance_dict[start_id+goal_id]
