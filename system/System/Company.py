from User import User
from Building import Building
class Company(User):
    def __init__(self, company_name):
        self.company_name = company_name
        self.buildings = []

    def add_building_to_company(self, building_address, need_access):
        answer = "THE COMPANY IS ADDED SUCCESSFULLY"
        for building in self.buildings:
            if building_address == building.address:
                answer = "ERROR. THIS BUILDING ALREADY IN THE SYSTEM"
            else:
                building = Building(building_address, need_access)
                self.buildings.append(building)