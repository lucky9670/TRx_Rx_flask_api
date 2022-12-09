import re
from datetime import datetime
import uuid
from pytz import timezone

#custom imports
import geo_funcs





class drv_trps():

    def __init__(self,req):
        self.trip_id = ('trip_id',"")
        self.logistics_org_id = None
        self.driver_id = req.get('driver_id',"")
        self.vehicle_id = req.get('vehicle_id',"")
        self.status = None
        self.coor_start  = req.get('coor_start',None)
        self.coor_end = req.get('coor_end',None)
        self.coor_current = req.get('coor_current',None)
        self.addr_start  = req.get('addr_start',"")
        self.addr_end  = req.get('addr_end',"")
        self.addr_current = req.get('addr_current',"")
        self.trip_start_tstamp = req.get('trip_start_tstamp',"")
        self.trip_end_tstamp =req.get('trip_end_tstamp',"")
        self.est_time  = req.get('est_time',"")
        self.driver_rating = None
        self.date_created = None

    def get_current_date(self):

        #We Are going to use US/Eastern as UTC -4 Timezone from Pytz database.
        string = str( datetime.now(timezone('US/Eastern')) )
        string = string[:-6] # removing -4:00 of the timezone from the datetime
        return string
 

    def check_date_obj(self,date):
        try:
            date = str(datetime.fromisoformat(date))
            return date
        except:
            return 'err'



 
    def verify_trip_id(self):
        li = []
        
        if len(self.trip_id) == 0 or len(self.trip_id) > 200:
            li.append('Trip ID cannot be empty or more than 200 characters')

        return li


    def verify_logistics_org_id(self):
        li = []
        
        if len(self.logistics_org_id) == 0 or len(self.logistics_org_id) > 200:
            li.append('Logistics Organistaion ID cannot be empty or more than 200 characters')

        return li




        
    def verify_driver_id(self):
        li = []
        
        if len(self.driver_id) == 0 or len(self.driver_id) > 200 :
            li.append('Driver id cannot be empty or more than 200 characters')

        return li




    def verify_vehicle_id(self):
        li = []
        self.vehicle_id = rep_empty_spaces(str(self.vehicle_id))
        
        if len(self.vehicle_id) == 0 or len(self.vehicle_id) > 200 :
            li.append('Vehicle id cannot be empty or more than 200 characters')

        return li



    def verify_addr_current(self):
        li = []
        self.addr_current = rep_empty_spaces(str(self.addr_current))
        
        if len(self.addr_current) == 0 or len(self.addr_current) > 433 :
            li.append('Address current cannot be empty or more than 433 characters')

        return li




    def verify_addr_start(self):
        li = []
        self.addr_start = rep_empty_spaces(str(self.addr_start))
        
        if len(self.addr_start) == 0 or len(self.addr_start) > 433 :
            li.append('Address start cannot be empty or more than 433 characters')

        return li


    def verify_addr_end(self):
        li = []
        self.addr_end = rep_empty_spaces(str(self.addr_end))
        
        if len(self.addr_end) == 0 or len(self.addr_end) > 433 :
            li.append('Address end cannot be empty or more than 433 characters')

        return li


    def verify_est_time(self):
        li = []

        if self.est_time != "":
            check =  self.check_date_obj(self.est_time)
            if check != "err":
                self.est_time = check
            else:
                li.append('Estimated time should be of format YYYY-MM-DD.')
        else:
            li.append('Estimated time cannot be empty.')

        return li



    def verify_coor_current(self):
        li = []
        surpress= 0
        if self.coor_current == None:
            surpress = 1
            li.append('Current Coordinates cannot be empty.')
        elif self.coor_current != None and not(isinstance(self.coor_current,list)) :
            surpress = 1
            li.append('Current Coordinates must be an instance of list [lat,long].')

            

        #converting to geohash

        if surpress != 1:
            check = geo_funcs.point_to_geohash(self.coor_current)
            if check != 1:
                self.coor_current = check
            else:
                li.append('Cannot convert coordinates to geohash.')


            




        return li


    def verify_coor_start(self):
        li = []
        surpress = 0

        if self.coor_start == None:
            surpress = 1
            li.append('Start Coordinates cannot be empty.')
        elif self.coor_start != None and not(isinstance(self.coor_start,list)):
            surpress = 1
            li.append('Start Coordinates must be an instance of list [lat,long].')
        

        #converting to geohash
        if surpress != 1:
            check = geo_funcs.point_to_geohash(self.coor_start)
            if check != 1:
                self.coor_start = check
            else:
                li.append('Cannot convert coordinates to geohash.')
        return li


    def verify_coor_end(self):
        li = []
        surpress = 0

        if self.coor_end == None:
            surpress = 1
            li.append('End Coordinates cannot be empty.')
        elif self.coor_end != None and not(isinstance(self.coor_end,list)) :
            surpress = 1
            li.append('End Coordinates must be an instance of list [lat,long].')


        if surpress != 1:
            check = geo_funcs.point_to_geohash(self.coor_end)
            if check != 1:
                self.coor_end = check
            else:
                li.append('Cannot convert coordinates to geohash.')

        return li


 
    def verify_create_trip(self,org_id = '',driver_id = ''): #Driver
        err_log = {}

        self.logistics_org_id = org_id

        if (org_id == None or org_id == '') and (driver_id == None or driver_id == ''):
            return {'err':'System Error'} 

        if org_id == '' or org_id == None:
            self.driver_id = driver_id
        else:    
            self.logistics_org_id = org_id
            err_log['logistics_org_id'] = self.verify_logistics_org_id()
        
        
        err_log['driver_id'] = self.verify_driver_id()
        err_log['vehicle_id'] = self.verify_vehicle_id()
        err_log['addr_start'] = self.verify_addr_start()
        err_log['addr_end'] = self.verify_addr_end()
        err_log['addr_current'] = self.verify_addr_current()
        err_log['coor_start'] = self.verify_coor_start()
        err_log['coor_end'] = self.verify_coor_end()
        err_log['coor_current'] = self.verify_coor_current()
        err_log['est_time'] = self.verify_est_time()
        print(self.driver_id)
        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log



    def verify_start_trip(self,org_id = '', driver_id = ''): 
        err_log = {}

        self.logistics_org_id = org_id

        if (org_id == None or org_id == '') and (driver_id == None or driver_id == ''):
            return {'err':'System Error'} 

        if org_id == '' or org_id == None:
            self.driver_id = driver_id
        else:    
            self.logistics_org_id = org_id
            err_log['logistics_org_id'] = self.verify_logistics_org_id()



        err_log['trip_id'] = self.verify_trip_id()



        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log









    def verify_stop_trip(self,org_id = '', driver_id = ''): 
        err_log = {}
        
        self.logistics_org_id = org_id

        if (org_id == None or org_id == '') and (driver_id == None or driver_id == ''):
            return {'err':'System Error'} 

        if org_id == '' or org_id == None:
            self.driver_id = driver_id
        else:    
            self.logistics_org_id = org_id
            err_log['logistics_org_id'] = self.verify_logistics_org_id()


        err_log['trip_id'] = self.verify_trip_id()



        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log


    def create_trip_profile(self):

        #setting trip profile
        self.date_created = self.get_current_date()
        self.status = 0

        profile = {
            "logistics_org_id":self.logistics_org_id ,
            "driver_id":self.driver_id,
            "vehicle_id":self.vehicle_id,
            "status":self.status,
            "addr_start":self.addr_start,
            "addr_end":self.addr_end,
            "addr_current":self.addr_current,
            "coor_start":self.coor_start,
            "coor_end":self.coor_end,
            "coor_current":self.coor_current,
            "est_time":self.est_time,
            "date_created":self.date_created
        }

        if self.logistics_org_id == '' or self.logistics_org_id == None:
            del profile['logistics_org_id']

        return profile




    def start_trip_profile(self):

        #setting trip profile
        self.trip_start_tstamp = self.get_current_date()
        self.status = 1

        profile = {
            "logistics_org_id":self.logistics_org_id ,
            "trip_id":self.trip_id ,
            "driver_id":self.driver_id,
            "status":self.status,
            "trip_start_tstamp":self.trip_start_tstamp
        }

        if self.logistics_org_id == '' or self.logistics_org_id == None:
            del profile['logistics_org_id']
        else:
            del profile['driver_id']


        return profile



    def stop_trip_profile(self):

        #setting trip profile
        self.trip_end_tstamp = self.get_current_date()
        self.status = 2

        profile = {
            "logistics_org_id":self.logistics_org_id ,
            "trip_id":self.trip_id ,
            "driver_id":self.driver_id,
            "status":self.status,
            "trip_end_tstamp":self.trip_end_tstamp
        }

        if self.logistics_org_id == '' or self.logistics_org_id == None:
            del profile['logistics_org_id']
        else:
            del profile['driver_id']


        return profile





def rep_empty_spaces(word):
	start=0
	end = len(word) -1
	
	for x in range(0,len(word)-1):
		if word[x] != " ":
			start = x
			break
	
	for x in range(len(word)-1,start,-1):
		if word[x] != " ":
			end = x
			break
	return word[start:end + 1]