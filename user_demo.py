import re
from datetime import datetime
import uuid
from pytz import timezone

class demo_users:

    def __init__(self,data):
        #self.org_id = org_id
        self.org_name = data['org_name']
        #self.owner_id = owner_id
        #self.status = 0
        #self.country = country
        #self.state = state
        #self.city = city
        #self.contact_num = contact_num
        #self.permanent_address = permanent_address
        #self.zip_code = zip_code
        #self.date_established = date_established
        #self.rating = None
        #self.total_reviews = None
        #self.date_created = None
        

    def set_date_created(self):# Donot Invoke for Import Dataset Operation 

        #We Are going to use US/Eastern as UTC -4 Timezone from Pytz database.
        string = str( datetime.now(timezone('US/Eastern')) )
        string = string[:-6] # removing -4:00 of the timezone from the datetime
        self.date_created = string
        print(self.date_created)


    def verify_org_data_all(self):
        err_log = {}
        err_log['org_name']         = []
        err_log['country']          = []
        err_log['zip_code']         = []
        err_log['date_established'] = []
        err_log['org_name']         = []
        err_log['org_name']         = []
        print(" FRPM DEMO")
        #verify org_name:
        #remove empty spaces from start and end
        self.org_name = self.rep_empty_spaces(str(self.org_name))


        #verify org_name:
        if len(self.org_name) > 0 and len(self.org_name) <= 64:
            pass
        else:
            err_log['org_name'].append('Organistaion name cannot be empty or more than 64 words')

    

        return {},err_log


    def rep_empty_spaces(self,word):
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
