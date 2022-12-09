from datetime import datetime
import uuid
from pytz import timezone

class supp_tickets():


    def __init__(self,req):
        self.supp_id  =req.get('supp_id',None)
        self.trip_id   = req.get('trip_id',None)
        self.logistics_rep_id = req.get('logistics_rep_id',None)
        self.logistics_org_id  = req.get('logistics_org_id',None)
        self.trx_emp_id  = req.get('trx_emp_id',"")
        self.img_record_before  = req.get('img_record_before',None)
        self.img_record_after  = req.get('img_record_after',None)
        self.job_description  = req.get('job_description',None)
        self.ticket_start_tstamp = req.get('ticket_start_tstamp',None)
        self.ticket_end_tstamp  = req.get('ticket_end_tstamp',None)
        self.geo_fence_truck_enroute_tstamp   = req.get('geo_fence_truck_enroute_tstamp',None)
        self.geo_fence_mechanic_enroute_tstamp = req.get('geo_fence_mechanic_enroute_tstamp',None)
        self.geo_fence_mechanic_arrival_tstamp = req.get('geo_fence_mechanic_arrival_tstamp',None)
        self.driver_rating  = req.get('driver_rating',None)
        self.logistics_org_rating = req.get('logistics_org_rating',None)
        self.trx_emp_rating  = req.get('trx_emp_rating',None)
        self.mechanic_rating = req.get('mechanic_rating',None)
        self.offer_id  = req.get('offer_id',None)
        self.tags =  req.get('tags',None)
        self.status = 0




    def get_current_date(self):

        #We Are going to use US/Eastern as UTC -4 Timezone from Pytz database.
        string = str( datetime.now(timezone('US/Eastern')) )
        string = string[:-6] # removing -4:00 of the timezone from the datetime
        return string
 
    def set_current_tstamp(self):

        #We Are going to use US/Eastern as UTC -4 Timezone from Pytz database.
        string = str( datetime.now(timezone('US/Eastern')) )
        string = string[:-6] # removing -4:00 of the timezone from the datetime
        self.ticket_start_tstamp = string
        return []

    def check_date_obj(self,date):
        try:
            date = str(datetime.fromisoformat(date))
            return date
        except:
            return 'err'



 
    def check_offer_id(self):
        li = []
        
        if self.offer_id == None or len(self.offer_id) == 0 or len(self.offer_id) > 200:
            li.append('Offer ID cannot be empty or more than 200 characters')

        return li



    def check_trip_id(self):
        li = []
        
        if self.trip_id == None or len(self.trip_id) == 0 or len(self.trip_id) > 200:
            li.append('Trip ID cannot be empty or more than 200 characters')

        return li



    def check_logistics_org_id(self):
        li = []
        
        if self.logistics_org_id == None or len(self.logistics_org_id) == 0 or len(self.logistics_org_id) > 200:
            li.append('Logistics Organistaion ID cannot be empty or more than 200 characters')

        return li



    def check_logistics_rep_id(self):
        li = []
        
        if self.logistics_rep_id == None or len(self.logistics_rep_id) == 0 or len(self.logistics_rep_id) > 200:
            li.append('Logistics Member ID cannot be empty or more than 200 characters')

        return li


        
    def check_driver_id(self):
        li = []
        
        if  self.driver_id == None or  len(self.driver_id) == 0 or len(self.driver_id) > 200 :
            li.append('Driver id cannot be empty or more than 200 characters')

        return li



    def check_supp_id(self):
        li = []
        
        if  self.supp_id == None or  len(self.supp_id) == 0 or len(self.supp_id) > 200:
            li.append('Logistics Organistaion ID cannot be empty or more than 200 characters')

        return li




    def check_trx_emp_id(self):
        li = []
        
        if  self.trx_emp_id == None or  len(self.trx_emp_id) == 0 or len(self.trx_emp_id) > 200:
            li.append('TRx Member ID cannot be empty or more than 200 characters')

        return li



    def check_job_descr(self):
        li = []
        
        if len(self.job_description) > 500:
            li.append('Job description cannot be more than 500 words')

        return li


    def check_tags(self):
        li = []
        try:
            tag_list = self.tags.split(',')
        except:
            return li

        for x in tag_list:
            if not(x.isdigit()):
                li.append('{} is not a valid tag'.format(x))

        return li

    def set_check_img_record_before(self):
        li = []
        
        if self.img_record_before is None:
            li.append('You need to upload image with the support ticket')

        key = ''
        if self.logistics_org_id is not None:
            key = 'log/org/'+ str(self.logistics_org_id) + '/supp_id/'
        elif self.logistics_org_id:
            key = 'log/com/' + str(self.logistics_rep_id) + '/supp_id/'
        
        self.img_record_before = key

        return li

    def set_check_img_record_after(self):
        li = []
        
        if self.img_record_after is None:
            li.append('You need to upload image with the support ticket')

        key = ''
        if self.logistics_org_id is not None:
            key = 'log/org/'+ str(self.logistics_org_id) + '/supp_id/'
        elif self.logistics_org_id:
            key = 'log/com/' + str(self.logistics_rep_id) + '/supp_id/'
        
        self.img_record_after = key

        return li

    def check_status(self):
        pass



    def check_img_record_after(self):
        pass

    def check_ticket_start_tstamp(self):
        pass
    def check_ticket_end_tstamp(self):
        pass
    def check_geo_fence_truck_enroute_tstamp(self):
        pass
    def check_geo_fence_mechanic_enroute_tstamp(self):
        pass
    def check_driver_rating(self):
        pass
    def check_logistics_org_rating(self):
        pass
    def check_mechanic_rating(self):
        pass

    def check_status(self):
        pass




    def verify_org_ticket_all(self):
        err_log = {}
        err_log['trip_id'] = []
        err_log['logistics_rep_id'] = []
        err_log['logistics_org_id'] = []
        err_log['job_description'] = []
        err_log['tags'] = []
        err_log['ticket_start_tstamp'] = []


        err_log['trip_id']=self.check_trip_id()
        err_log['logistics_org_id'] = self.check_logistics_org_id()
        err_log['logistics_rep_id'] = self.check_logistics_rep_id()
        err_log['job_description'] = self.check_job_descr()
        err_log['tags'] = self.check_tags()
        err_log['ticket_start_tstamp'] =self.set_current_tstamp()
        err_log['img_record_before'] = self.set_check_img_record_before() 



        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log

    def verify_work_approval_data(self):
        err_log = {}
        err_log['trip_id'] = []
        err_log['logistics_rep_id'] = []
        err_log['logistics_org_id'] = []
        err_log['job_description'] = []
        err_log['tags'] = []
        err_log['ticket_start_tstamp'] = []


        err_log['trip_id']=self.check_trip_id()
        err_log['logistics_org_id'] = self.check_logistics_org_id()
        err_log['logistics_rep_id'] = self.check_logistics_rep_id()
        err_log['job_description'] = self.check_job_descr()
        err_log['tags'] = self.check_tags()
        err_log['ticket_start_tstamp'] =self.set_current_tstamp()
        err_log['img_record_after'] = self.set_check_img_record_after() 



        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log

    def get_profile_org_ticket_all(self):
        profile = {
            'trip_id' : self.trip_id, 
            'logistics_rep_id' : self.logistics_rep_id,
            'logistics_org_id' : self.logistics_org_id,
            'img_record_before' : self.img_record_before,
            'job_description' : self.job_description,
            'ticket_start_tstamp' : self.ticket_start_tstamp,
            'tags' : self.tags,
            'status' : self.status
        }

        return profile


    def verify_com_ticket_all(self):
        err_log = {}
        err_log['trip_id'] = []
        err_log['logistics_rep_id'] = []
        err_log['job_descr'] = []
        err_log['tags'] = []
        err_log['ticket_start_tstamp'] = []


        err_log['trip_id']=self.check_trip_id()
        err_log['logistics_rep_id'] = self.check_logistics_rep_id()
        err_log['job_descr'] = self.check_job_descr()
        err_log['tags'] = self.check_tags()
        err_log['ticket_start_tstamp'] =self.set_current_tstamp()


        #check if any error 
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)

        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log


    def get_profile_com_ticket_all(self):
        profile = {
            'trip_id' : self.trip_id, 
            'logistics_rep_id' : self.logistics_rep_id,
            'img_record_before' : self.img_record_before,
            'job_descr' : self.job_descr,
            'ticket_start_tstamp' : self.ticket_start_tstamp,
            'tags' : self.tags,
            'status' : self.status
        }

        return profile