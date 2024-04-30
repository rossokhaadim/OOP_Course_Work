from Office import Office

import Building

class Floor(Building.Building):
    def __init__(self, floor_number, need_access):
        self.floor_number = floor_number
        self.need_access = need_access
        self.offices = []

    def add_office_to_floor(self, office_number, need_access):
        answer = "THE OFFICE IS ADDED SUCCESSFULLY"
        for office in self.offices:
            if office_number == office.office_number:
                answer = "ERROR. THIS OFFICE ALREADY IN THE SYSTEM"
            else:
                office = Office(office_number, need_access)
                self.offices.append(office)