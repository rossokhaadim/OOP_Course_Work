from Company import Company
class SystemManage():
    def __init__(self):
        self.users = []
        self.companies = []

    def add_user(self):
        pass

    def add_company_to_system(self, company_name):
        exist = False
        answer = "THE COMPANY IS ADDED SUCCESSFULLY"
        for company in self.companies:
            if company_name == company.name:
                exist = True
                answer = "ERROR. THE COMPANY ALREADY EXISTS"
        if not exist:
            company = Company(company_name)
            self.companies.append(company)
        return answer



    def add_user_access(self):
        pass

    def remove_user_access(self):
        pass



system_manage = SystemManage()