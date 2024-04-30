import Company
from Floor import Floor

class Building(Company):
    def __init__(self, building_name, need_access):
        self.address = building_name
        self.need_access = need_access
        self.floors = []

    def add_floor_to_building(self, floor_number, need_access):
        answer = "THE FLOOR IS ADDED SUCCESSFULLY"
        for floor in self.floors:
            if floor_number == floor.floor_number:
                answer = "ERROR. THIS FLOOR ALREADY IN THE SYSTEM"
            else:
                floor = Floor(floor_number, need_access)
                self.floors.append(floor)