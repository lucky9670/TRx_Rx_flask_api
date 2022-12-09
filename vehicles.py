import re
from datetime import datetime
import uuid
from pytz import timezone

class log_vehicles():
    
    def __init__(self,req):
        self.vehicle_id = None
        self.vin = req.get('vin','')
        self.type = req.get('type','')
        self.status = None
        self.org_id = None
        self.user_id = None



    def insert_org_id(self,org_id):
        if org_id != '' or org_id != None:
            self.org_id  =  org_id
            return 0
        else:
            return 1


    def insert_user_id(self,owner_id):
        if owner_id != '' or owner_id != None:
            self.user_id  =  owner_id
            return 0
        else:
            return 1





    def validate_vehicle(self):

        err_log = {}
        err_log['vin'] = []
        err_log['type'] = []

        #verify vin
        if len(self.vin) == 0 or len(self.vin) >=201:
            err_log['vin'].append("Vehicle Identification Number cannot be emty or more than 200 words")


        #verify type
        if len(self.type) == 0 or len(self.type) >=101:
            err_log['type'].append("Vehicle type cannot be emty or more than 200 words")

        if self.type  not in  supp_vehicles:
            print("ASDASDASD")
            err_log['type'].append("Vehicle type '{}' not found.".format(self.type))

        self.status = 0



        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log




    def get_vehicle_profile(self):
        vehicle = {
            "vin":self.vin,
            "type":self.type,
            "status":self.status ,
            "user_id":self.user_id,
            "org_id":self.org_id
        }
        return vehicle
















supp_vehicles = ['Truck','Trailer']