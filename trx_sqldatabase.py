#import mysql.connector
#from mysql.connector import errorcode
import mysql.connector
from mysql.connector import errorcode
import json
import geo_funcs



class trxmysql_dbb:
    def __init__(self):
        self.cnx = ''
        
    def set_connection(self):
        try:
            self.cnx = mysql.connector.connect(user='root',
                                        password='N@passwd#123',
                                        host=   '18.221.103.132',
                                        database='temp')
            
        except Exception as e:
            print('cnx',e)
            return {"err":"Could not proceed with the request at the moment."}   



    def check_services_users_availablity(self,user_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            #getting offer mechanic availablity
            print("ASOIDSAIDJSAOI")
            sql = "SELECT status from services_users where id=%s"
            #cur.execute(sql,('e844187d-2a18-4760-9374-ae6691d3767e',))
            cur.execute(sql,(user_id,))
            print(cur.statement)
            status = cur.fetchone()
            print('status',status,'\n')

            if status['status'] != 0:
                return {"err":'Mechanic is not available'}
            
            return {}


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}




    def trx_get_supp_ticket(self,s_ticket,op):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        #sql = "SELECT * FROM support_ticket where trx_emp_id = NULL"
        try:
            result = None
    
            if s_ticket == None or s_ticket == '':
                if op == 'not-assigned':
                    sql = "SELECT * FROM support_tickets where trx_emp_id is NULL and status != 2 LIMIT 10"
                    cur.execute(sql)
                    result = cur.fetchall()
                elif op == 'assigned':
                    print("IN assigned")
                    sql = "SELECT * FROM support_tickets where trx_emp_id is NOT NULL and status != 2  LIMIT 10"
                    cur.execute(sql)
                    result = cur.fetchall()
                else:
                    print("IN completed")
                    sql = "SELECT * FROM support_tickets where status=2 LIMIT 10  "
                    cur.execute(sql)
                    result = cur.fetchall()
            
            
            else:
                sql =  'SELECT * FROM support_tickets where supp_id = %s'
                cur.execute(sql,(s_ticket,))
                result = cur.fetchall()
                print(result)
                print(cur.statement)
        
            #additional data
            for x in result:
                #getting trip
                trip_id = (x['trip_id'],)
                sql = "SELECT * from trips where trip_id = %s"
                cur.execute(sql,trip_id)
                x['trip_id'] = cur.fetchone()
                x['trip_id']['coor_current'] = geo_funcs.geohash_to_point(x['trip_id'].get('coor_current',""))

                #getting driver name
                driver_id = (x['trip_id']['driver_id'],)
                sql = "SELECT * from logistics_users where id = %s"
                cur.execute(sql,driver_id)
                x['driver_id'] = cur.fetchone()

                #getting logistics emp name
                if x['logistics_rep_id'] != None:
                    logistics_rep_id = (x['logistics_rep_id'],)
                    sql = "SELECT * from logistics_users where id = %s"
                    cur.execute(sql,logistics_rep_id)
                    x['logistics_rep_id'] = cur.fetchone()

                print(x['trx_emp_id'])
                if x['trx_emp_id'] != None:
                    trx_emp_id = (x['trx_emp_id'],)
                    sql = "SELECT * from trx where id = %s"
                    cur.execute(sql,trx_emp_id)
                    x['trx_emp_id'] = cur.fetchone()
                    print(x['trx_emp_id'])

                    
                if x['offer_id'] != None:
                    offer_id =  (x['offer_id'],)
                    sql = "SELECT * from support_tickets_offers where offer_id = %s"
                    cur.execute(sql,offer_id)
                    x['offer_id'] = cur.fetchone()

                    mechanic_id = (x['offer_id']['mechanics_user_id'],)
                    sql = "SELECT * from services_users where id = %s"
                    cur.execute(sql,mechanic_id)
                    x['offer_id']['mechanics_user_id'] = cur.fetchone()
                    x['offer_id']['mechanics_user_id']['coor_current'] = geo_funcs.geohash_to_point(x['offer_id']['mechanics_user_id'].get('coor_current',None)) 


                    mechanic_org_id = (x['offer_id']['mechanics_org_id'],)
                    sql = "SELECT * from services_orgs where org_id = %s"
                    cur.execute(sql,mechanic_org_id)
                    x['offer_id']['mechanics_org_id'] = cur.fetchone()

                if x['logistics_org_id'] != None:
                    logistics_org_id = (x['logistics_org_id'],)
                    sql = "SELECT * from logistics_orgs where org_id = %s"
                    cur.execute(sql,logistics_org_id)
                    x['logistics_org_id'] = cur.fetchone()

            return {"res":result}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

#not to be used again without concent
    def __trx_get_supp_ticket(self,s_ticket,op):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        #sql = "SELECT * FROM support_ticket where trx_emp_id = NULL"
        try:
            result = None
            print(s_ticket,type(s_ticket))
    
            if s_ticket == None or s_ticket == '':
                if op == 'not-assigned':
                    sql = "SELECT * FROM support_tickets where trx_emp_id is NULL and status != 2 LIMIT 10"
                    cur.execute(sql)
                    result = cur.fetchall()
                elif op == 'assigned':
                    sql = "SELECT * FROM support_tickets where trx_emp_id is NOT NULL and status != 2  LIMIT 10"
                    cur.execute(sql)
                    result = cur.fetchall()
                else:
                    sql = "SELECT * FROM support_tickets where status=2 LIMIT 10"
                    cur.execute(sql)
                    result = cur.fetchall()

            else:
                sql =  'SELECT * FROM support_tickets where supp_id = %s'
                cur.execute(sql,(s_ticket,))
                result = cur.fetchall()
                if result != []:
                    print(result)
                    trip_id = result[0]['trip_id']

                    sql =  'SELECT * FROM trips where trip_id = %s'
                    cur.execute(sql,(trip_id,))
                    result.append(cur.fetchall()[0])

            
            print(cur.statement)

            return {"res":result}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}




    def get_4_prec_hash(self,s_ticket,t_ticket):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}



        try:
            box = None
            if s_ticket != None:
                sql = " SELECT trip_id from support_tickets where supp_id = %s"
                cur.execute(sql,(s_ticket,))
                trip_id = cur.fetchone()
                trip_id = trip_id['trip_id']
                print(trip_id)

                sql = "SELECT coor_current from trips  where trip_id = %s"
                cur.execute(sql,(trip_id,))
                box = cur.fetchone()
                box = box['coor_current']
            else:
                sql = "SELECT coor_current from trips  where trip_id = %s"
                cur.execute(sql,(t_ticket,))
                box = cur.fetchone()
                box = box['coor_current']
                print(box)



            box = box[0:4]
            box = box + '%'
            print(box)
            sql =  'SELECT coor_current,id,org_id from services_users where coor_current  like %s LIMIT 10'

            cur.execute(sql,(box,))
            print(cur.statement)
            return {'res':cur.fetchall()}


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}


    def get_4_prec_hash_services(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}



        try:
            box = None
  
            sql = " SELECT coor_current from services_users where id=%s"
            cur.execute(sql,(id,))
            coor_current = cur.fetchone()
            coor_current = coor_current['coor_current']
            print(coor_current)



            box = coor_current[0:4]
            box = box + '%'
            print(box)
            sql =  'SELECT * from trips where coor_current  like %s  LIMIT 10'#and status=3

            cur.execute(sql,(box,))
            print(cur.statement)

            res_trips = cur.fetchall()
            supp_list = []
            for x in res_trips:
                sql = "SELECT * FROM support_tickets where trip_id = %s "#and status=0
                cur.execute(sql,(x['trip_id'],))
                print(cur.statement)
                temp = cur.fetchone()
                print(temp)
                if temp!=None:
                    z = {**x, **temp}
                    supp_list.append(z)

            return {'res':supp_list}


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}



    def update_img_before(self,data):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            sql =  'UPDATE support_tickets SET img_record_before = %s WHERE supp_id = %s'

            cur.execute(sql,(data['img_record_before'],data['supp_id']))
            print(self.cnx.commit(),"TRANSACTED")



        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}








    def register_support_event(self,data):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:

            #CHECK IF ALREADY A support ticket is open for a trip
            trip_check_sql = "SELECT supp_id FROM support_tickets where trip_id=%s and status=1"

            cur.execute(trip_check_sql,(data['trip_id'],))
            dup_entry = cur.fetchone()
            print(cur.statement)
            print('DUPLICATE',dup_entry)
            

            if dup_entry:
                return{'err':"A support ticket '{}' is already open for trip '{}'".format(dup_entry['supp_id'],data['trip_id'])}

            
            if data['tags'] != '':
                #split tags in list
                args = data['tags'].split(',')
                in_p=', '.join(list(map(lambda x: '%s', args)))
                sql =  'SELECT id FROM repair_jobs WHERE id in (%s)'

                sql = sql % in_p

                cur.execute(sql,args)

                res = cur.fetchall()

                res_args = []
                for x in res:
                    res_args.append(str(x['id']))
                
                print(res_args)
                remain_arg = [item for item in args if item not in res_args]
                print(remain_arg)

                print(cur.statement)
            
            
            insert_supp_query=("INSERT INTO support_tickets(trip_id,logistics_org_id,logistics_rep_id,img_record_before,job_description,ticket_start_tstamp,tags,status)"
                            "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
                            
                            
                            

            cur.execute(insert_supp_query,(data['trip_id'],data['logistics_org_id'],data['logistics_rep_id'],data['img_record_before'],data['job_description'],data['ticket_start_tstamp'],data['tags'],data['status']))
            supp_id = cur.lastrowid
            print(supp_id)
            print(self.cnx.commit(),"TRANSACTED")

            return {'supp_id':supp_id}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}


    ###
    def get_support_ticket_offers(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)
        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #getting offer availablity
            query = "SELECT * FROM support_tickets_offers WHERE offer_id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()

            print ('Records',records,'\n')
            #getting offer mechanic availablity
            print("ASOIDSAIDJSAOI")
            sql = "SELECT status from services_users where id=%s"
            #cur.execute(sql,('e844187d-2a18-4760-9374-ae6691d3767e',))
            cur.execute(sql,(records['mechanics_user_id'],))
            print(cur.statement)
            status = cur.fetchone()
            print('status',status,'\n')
            if status['status'] != 0:
                return 'Mechanic is not available',{}
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}


    def get_support_ticket_offers_chat(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #getting offer availablity
            query = "SELECT * FROM support_tickets_offers WHERE offer_id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()

           
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_vehicless(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #getting offer availablity
            query = "SELECT * FROM vehicles WHERE org_id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()

           
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}          

    def get_support_ticket(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #getting offer availablity
            query = "SELECT * FROM support_tickets WHERE supp_id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()

           
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}                   

    def get_support_ticket_offers_all(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            query = "SELECT * FROM support_tickets_offers WHERE supp_id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()

            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_trip_id(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            get_trip_id = (
                "SELECT trip_id FROM support_tickets WHERE supp_id = %s"
                )
            cur.execute(get_trip_id,(id,))

            #get_log_org_res = cur.fetchone()


            trip_id = cur.fetchone()
            #trip_id = get_log_org_res[0]  
    
            cur.close()
            self.cnx.commit()
            return {},trip_id
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_driver_id_from_trip_id(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            get_driver_id = (
                "SELECT driver_id FROM trips WHERE trip_id = %s"
                )
            cur.execute(get_driver_id,(id,))

            #get_log_org_res = cur.fetchone()


            driver_id = cur.fetchone()
            #trip_id = get_log_org_res[0]  
    
            cur.close()
            self.cnx.commit()
            return {},driver_id
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_tripss(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            get_driver_id = (
                "SELECT * FROM trips WHERE trip_id = %s"
                )
            cur.execute(get_driver_id,(id,))

            #get_log_org_res = cur.fetchone()


            driver_id = cur.fetchone()
            #trip_id = get_log_org_res[0]  
    
            cur.close()
            self.cnx.commit()
            return {},driver_id
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}                 

    def get_log_users(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = "SELECT * FROM logistics_users WHERE id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()
           
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_sev_users(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = "SELECT * FROM services_users WHERE id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()
           
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_trx_user(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = "SELECT * FROM trx WHERE id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            ## fetching all records from the 'cursor' object
            records = cur.fetchone()
           
    
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}         

    def get_repair_jobs(self):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}


        try:
            query = ("SELECT id,name FROM repair_jobs")
            cur.execute(query)
            return {"repair_jobs":cur.fetchall()}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def get_support_tickets(self,org_id):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)
        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}


        try:
            query = ("SELECT * FROM support_tickets WHERE logistics_org_id = %s ")
        
            cur.execute( query,(org_id,))
            return {"support_tickets":cur.fetchall()}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def get_supp_id(self,id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            get_trip_id = (
                "SELECT * FROM support_tickets WHERE supp_id = %s"
                )
            cur.execute(get_trip_id,(id,))

            #get_log_org_res = cur.fetchone()


            data = cur.fetchone()
            #trip_id = get_log_org_res[0]  
    
            cur.close()
            self.cnx.commit()
            return {},data
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def add_rep(self,supp_id,logistics_rep_id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            
            print('from function')
            print(supp_id,logistics_rep_id)
            sql = "UPDATE support_tickets SET logistics_rep_id= %s  WHERE supp_id = %s"
            val = (logistics_rep_id, supp_id)

            cur.execute(sql, val)
            self.cnx.commit()
                      

        except mysql.connector.Error as err:
            print("PRINTING ERROR 1")
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR 2")
            print(e)
            return {"err":"Unexpected error"}

    def create_org(self,data_log,data_user):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)
        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            insert_user = (
                "INSERT INTO logistics_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                
                )
            insert_user_res = cur.execute(insert_user,(data_user['logistics_user']['id'], data_user['logistics_user']['org_id'], data_user['logistics_user']['f_name'], data_user['logistics_user']['m_name'], data_user['logistics_user']['l_name'], data_user['logistics_user']['date_created'], data_user['logistics_user']['last_acc'], data_user['logistics_user']['status'], data_user['logistics_user']['roles']))



            insert_user_profile = (
                "INSERT INTO logistics_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                
                )
            insert_user_profile_res = cur.execute( insert_user_profile,(data_user['logistics_user_profile']['id'], data_user['logistics_user_profile']['role'], data_user['logistics_user_profile']['date_created'], data_user['logistics_user_profile']['last_acc'], data_user['logistics_user_profile']['status'], data_user['logistics_user_profile']['permanent_address'], data_user['logistics_user_profile']['contact_num'], data_user['logistics_user_profile']['state'], data_user['logistics_user_profile']['city'], data_user['logistics_user_profile']['country'], data_user['logistics_user_profile']['email']))


            print(data_log)
            insert_log_org = (
                "INSERT INTO logistics_orgs(owner_id, org_name, status, country, state, city, contact_num, permanent_address, zip_code, date_established, date_created) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"
                )
            insert_log_org_res = cur.execute( insert_log_org, (data_log['logistics_org']['owner_id'], data_log['logistics_org']['org_name'], data_log['logistics_org']['status'], data_log['logistics_org']['country'], data_log['logistics_org']['state'], data_log['logistics_org']['city'], data_log['logistics_org']['contact_num'], data_log['logistics_org']['permanent_address'], data_log['logistics_org']['zip_code'], data_log['logistics_org']['date_established'], data_log['logistics_org']['date_created']) )
            org_id = cur.lastrowid
            print("ORG_ID",org_id)
            
            
            insert_org_id = ("UPDATE logistics_users SET org_id = %s WHERE id = %s")

            insert_org_id_res = cur.execute( insert_org_id,(org_id,data_user['logistics_user']['id']))

            print(self.cnx.commit(),"TRANSACTED")
            cur.close()

            return {"org_id":org_id}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def create_support_tickets_offers(self,data):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}
        print("HEREARPOAE")
        
        try:
           
            insert_supp_ticket_offer = (
                "INSERT INTO support_tickets_offers(supp_id, mechanics_org_id, mechanics_user_id, job_description, coor_start, coor_end,  date_created, mechanic_est_time_arrival, mechanic_est_job_completion_time, sys_job_completion_time,sys_mech_arrival_time,quote,status) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                
                )
            insert_log_org_res = cur.execute( insert_supp_ticket_offer, (data['supp_id'], data['mechanic_org_id'], data['mechanic_user_id'], data['job_desc'], data['coor_start'], data['coor_end'], data['date_created'], data['mechanic_est_time_arrival'], data['mechanic_est_job_completion_time'], data['sys_job_completion_time'], data['sys_mech_arrival_time'], data['quote'], data['status']) )
            offer_id = cur.lastrowid
            print("offer_id",offer_id)
            

            print(self.cnx.commit(),"TRANSACTED")
            cur.close()

            return {},{"offer_id":offer_id}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}},{}
            else:
                return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}


    def trx_create_support_tickets_offers(self,data,trx_user_id):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}
        print("HEREARPOAE")
        
        try:
           
            insert_supp_ticket_offer = (
                "INSERT INTO support_tickets_offers(supp_id, mechanics_org_id, mechanics_user_id, job_description, coor_start, coor_end,  date_created, mechanic_est_time_arrival, mechanic_est_job_completion_time, sys_job_completion_time,sys_mech_arrival_time,quote,status,trx_emp_id) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                
                )
            insert_log_org_res = cur.execute( insert_supp_ticket_offer, (data['supp_id'], data['mechanic_org_id'], data['mechanic_user_id'], data['job_desc'], data['coor_start'], data['coor_end'], data['date_created'], data['mechanic_est_time_arrival'], data['mechanic_est_job_completion_time'], data['sys_job_completion_time'], data['sys_mech_arrival_time'], data['quote'], data['status'],trx_user_id))
            offer_id = cur.lastrowid
            print("offer_id",offer_id)
            

            print(self.cnx.commit(),"TRANSACTED")
            cur.close()

            return {},{"offer_id":offer_id}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}},{}
            else:
                return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def update_quote(self,offer_id,quote):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
        
            sql = "UPDATE support_tickets_offers SET quote= %s  WHERE offer_id = %s"
            val = (quote, offer_id)

            cur.execute(sql, val)
            self.cnx.commit()
            cur.close()                  

        except mysql.connector.Error as err:
            print("PRINTING ERROR 1")
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR 2")
            print(e)
            return {"err":"Unexpected error"}


    def update_supp_ticket_offers_status(self,offer_id,status,services_id):
        try:
            cur = self.cnx.cursor(buffered=True)
        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            print("PRINTING FROM UPDATE STATUS")
            print(offer_id,status)
            sql = "UPDATE support_tickets_offers SET status= %s  WHERE offer_id = %s"
            val = (status, offer_id)
            cur.execute(sql, val)
            print("PRINTING FROM UPDATE STATUS 2")
            #Blocking mechanic
            sql = "UPDATE services_users SET status=2  WHERE id = %s"
            val = (services_id,)
            cur.execute(sql, val)
            print("PRINTING FROM UPDATE STATUS 3")
            self.cnx.commit()
            print("PRINTING FROM UPDATE STATUS 4")
            cur.close()              

        except mysql.connector.Error as err:
            print("PRINTING ERROR 1")
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR 2")
            print(e)
            return {"err":"Unexpected error"}

    def update_supp_ticket_status(self,supp_id,status):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            print("PRINTING FROM UPDATE STATUS")
            print(supp_id,status)
            sql = "UPDATE support_tickets SET status= %s  WHERE supp_id = %s"
            val = (status, supp_id)

            cur.execute(sql, val)
            self.cnx.commit()
            cur.close()              

        except mysql.connector.Error as err:
            print("PRINTING ERROR 1")
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR 2")
            print(e)
            return {"err":"Unexpected error"}         


    def update_supp_ticket_offer_id(self,offer_id,supp_id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            print("PRINTING FROM UPDATE offer_id")
            print(offer_id,supp_id)
            sql = "UPDATE support_tickets SET offer_id= %s  WHERE supp_id = %s"
            val = (offer_id,supp_id)

            cur.execute(sql, val)
            self.cnx.commit()
            cur.close()            

        except mysql.connector.Error as err:
            print("PRINTING ERROR 1")
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR 2")
            print(e)
            return {"err":"Unexpected error"}                

    def get_log_org(self,org_id):
        #Add user
        print(org_id,"ASIDJOIASDJ")
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        try:
            result  = {}
            #get_org_status = ("SELECT * FROM logistics_orgs WHERE org_id=%s  UNION SELECT * FROM logistics_users WHERE org_id=%s")
            get_org_status = ("SELECT * FROM logistics_orgs WHERE org_id=%s")

            get_org_status_res = cur.execute( get_org_status,(org_id,))
            result['org'] = cur.fetchall()

            get_emp_status = ("SELECT * FROM logistics_users WHERE org_id=%s")
            get_org_status_res = cur.execute( get_emp_status,(org_id,))
            result['employees']= cur.fetchall()
            

            cur.close()
            return result

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}



    def get_log_orgs(self):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:

            get_org_status = ("SELECT * FROM logistics_orgs ORDER BY date_created  LIMIT 10")
            get_org_status_res = cur.execute( get_org_status)
            result = cur.fetchall()
            cur.close()
            return result

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}



    def get_log_company(self,owner_id):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            result  = {}
            #get_org_status = ("SELECT * FROM logistics_orgs WHERE org_id=%s  UNION SELECT * FROM logistics_users WHERE org_id=%s")
            get_company_status = ("SELECT * FROM logistics_users WHERE id=%s and roles LIKE '%$2%'")

            get_org_status_res = cur.execute( get_company_status,(owner_id,))
            result['owner'] = cur.fetchall()

            get_emp_status = ("SELECT * FROM logistics_users_profiles WHERE id=%s and role='2'")
            get_org_status_res = cur.execute( get_emp_status,(owner_id,))
            result['owner_profile']= cur.fetchall()
            

            cur.close()
            return result

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}




    def get_log_companies(self):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            result  = {}
            #get_org_status = ("SELECT * FROM logistics_orgs WHERE org_id=%s  UNION SELECT * FROM logistics_users WHERE org_id=%s")
            get_company_status = ("SELECT * FROM logistics_users WHERE roles LIKE '%$2%' ORDER BY date_created  LIMIT 10")

            get_org_status_res = cur.execute( get_company_status)
            result['owners'] = cur.fetchall()
            

            cur.close()
            return result

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}














    def get_services_orgs_status(self,op,org_id):
        #Add user
        print(org_id,"ASIDJOIASDJ")
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            if op == 0:
                get_org_status = ("SELECT * FROM services_orgs WHERE status='100' ORDER BY date_created  LIMIT 10" )

                get_org_status_res = cur.execute( get_org_status)
                result = cur.fetchall()
                cur.close()
                return result
            
            elif op == 1:
                result = {}
                get_org_status = ("SELECT * FROM services_orgs WHERE org_id = %s")
                get_org_status_res = cur.execute( get_org_status,(org_id,))
                result['org'] = cur.fetchall()

                get_org_status = ("SELECT * FROM services_users WHERE org_id = %s")
                get_org_status_res = cur.execute( get_org_status,(org_id,))
                result['employees'] = cur.fetchall()
                cur.close()
                return result



            elif op == 2:
                get_org_status = ("SELECT * FROM services_orgs WHERE status = '0' ORDER BY date_created  LIMIT 10")
                get_org_status_res = cur.execute( get_org_status)
                result = cur.fetchall()
                print(result)
                cur.close()
                return result

            else:
                return {"err":"Unexpected error"}
            
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}








    def get_services_company_status(self,op,user_id):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if op == 0:
                get_companies_status = ("SELECT * FROM services_users WHERE status='100' and roles LIKE '%$3%' ORDER BY date_created  LIMIT 10" )

                get_org_status_res = cur.execute( get_companies_status)
                result = cur.fetchall()
                cur.close()
                return result

            
            elif op == 1:
                result = {}
                get_company_status = ("SELECT * FROM services_users WHERE id = %s and roles LIKE '%$3%'")
                get_company_status_res = cur.execute( get_company_status,(user_id,))
                result['org'] = cur.fetchall()

                get_company_status = ("SELECT * FROM services_users_profiles WHERE id = %s and role='3'")
                get_company_status_res = cur.execute( get_company_status,(user_id,))
                result['employees'] = cur.fetchall() 
                cur.close()
                return result


            elif op == 2:
                get_org_status = ("SELECT * FROM services_users WHERE status='0' and roles LIKE '%$3%' ORDER BY date_created  LIMIT 10")
                get_org_status_res = cur.execute( get_org_status)
                result = cur.fetchall()
                cur.close()
                return result


            else:
                return {"err":"Unexpected error"}
           


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

 





    def action_services_org_status(self,op,org_id):
        print(op,type(op))
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)
        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if op == 0:
                update_org_stat = ("UPDATE services_orgs SET status = %s WHERE org_id = %s")
                insert_org_id_res = cur.execute( update_org_stat,("0",org_id))

                print(self.cnx.commit(),"TRANSACTED 0")
                cur.close()
                return {"success":"approved"}
            elif op == 1:
                update_org_stat = ("UPDATE services_orgs SET status = %s WHERE org_id = %s")
                insert_org_id_res = cur.execute( update_org_stat,("200",org_id))

                print(self.cnx.commit(),"TRANSACTED 1")
                cur.close()
                return {"success":"denied"}
            else:
                return {"err":"Wrong format"}

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}






    def action_services_company_status(self,op,user_id):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if op == 0:
                update_company_stat = ("UPDATE services_users SET status = %s WHERE id = %s")
                insert_org_id_res = cur.execute( update_company_stat,("0",user_id))

                print(self.cnx.commit(),"TRANSACTED 0")
                cur.close()
                return {"success":"approved"}

            elif op == 1:
                update_company_stat = ("UPDATE services_users SET status = %s WHERE id = %s")
                insert_org_id_res = cur.execute( update_company_stat,("200",user_id))

                print(self.cnx.commit(),"TRANSACTED 1")
                cur.close()
                return {"success":"denied"}

            else:
                return {"err":"Wrong format"}


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}






    def add_vehicle(self,data):

        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}


        try:
            get_org_id = ("SELECT org_id from logistics_users where id = %s")
            get_org_id_res = cur.execute( get_org_id,(data['user_id'],))
            org_id = cur.fetchone()[0]

            if org_id == None:
                insert_user_vehicle = ("INSERT INTO vehicles(user_id,vin,type,status)"
                "VALUES (%s, %s, %s, %s)"
                )

                insert_user_vehicle_res = cur.execute( insert_user_vehicle,(data['user_id'],data['vin'],data['type'],data['status']))

            else:
                insert_org_vehicle = ("INSERT INTO vehicles(org_id,vin,type,status)"
                "VALUES (%s, %s, %s, %s)"
                )
                insert_org_vehicle_res = cur.execute( insert_org_vehicle,(org_id,data['vin'],data['type'],data['status']))



            print(self.cnx.commit(),"TRANSACTED")
            cur.close()


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"vehicle_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}


        



    def add_org_driver(self,data):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:



            insert_driver = (
                "INSERT INTO logistics_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                
                )
            insert_user_res = cur.execute(insert_driver,(data['logistics_user']['id'], data['logistics_user']['org_id'], data['logistics_user']['f_name'], data['logistics_user']['m_name'], data['logistics_user']['l_name'], data['logistics_user']['date_created'], data['logistics_user']['last_acc'], data['logistics_user']['status'], data['logistics_user']['roles']))


            insert_driver_profile = (
                "INSERT INTO logistics_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email,dot_num,license_number) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s,%s, %s)"
                
                )

            insert_user_profile_res = cur.execute( insert_driver_profile,(data['logistics_user_profile']['id'], data['logistics_user_profile']['role'], data['logistics_user_profile']['date_created'], data['logistics_user_profile']['last_acc'], data['logistics_user_profile']['status'], data['logistics_user_profile']['permanent_address'], data['logistics_user_profile']['contact_num'], data['logistics_user_profile']['state'], data['logistics_user_profile']['city'], data['logistics_user_profile']['country'], data['logistics_user_profile']['email'],data['logistics_user_profile']['dot_num'],data['logistics_user_profile']['license_number']))


            print(self.cnx.commit(),"TRANSACTED")
            cur.close()


        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_user_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}


        

    def reg_driver_company(self,data_user,insert_to):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if insert_to == "logistics_user":
                print(" INSERTING TO LOGISTICS USERS")
                print(data_user)
                insert_user = (
                    "INSERT INTO logistics_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data_user['logistics_user']['id'], data_user['logistics_user']['org_id'], data_user['logistics_user']['f_name'], data_user['logistics_user']['m_name'], data_user['logistics_user']['l_name'], data_user['logistics_user']['date_created'], data_user['logistics_user']['last_acc'], data_user['logistics_user']['status'], data_user['logistics_user']['roles']))
            

            if insert_to == "logistics_user_profile_2":
                print(" INSERTING TO LOGISTICS USERS_PROFILES_2")
                print(data_user)
                insert_user_profile = (
                    "INSERT INTO logistics_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email,dot_num,license_number) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['logistics_user_profile_2']['id'], data_user['logistics_user_profile_2']['role'], data_user['logistics_user_profile_2']['date_created'], data_user['logistics_user_profile_2']['last_acc'], data_user['logistics_user_profile_2']['status'], data_user['logistics_user_profile_2']['permanent_address'], data_user['logistics_user_profile_2']['contact_num'], data_user['logistics_user_profile_2']['state'], data_user['logistics_user_profile_2']['city'], data_user['logistics_user_profile_2']['country'], data_user['logistics_user_profile_2']['email'], data_user['logistics_user_profile_2']['dot_num'], data_user['logistics_user_profile_2']['license_number']))

            if insert_to == "logistics_user_profile_6":
                print(" INSERTING TO LOGISTICS USERS_PROFILES_3")
                print(data_user)
                insert_user_profile = (
                    "INSERT INTO logistics_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email,dot_num,license_number) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['logistics_user_profile_6']['id'], data_user['logistics_user_profile_6']['role'], data_user['logistics_user_profile_6']['date_created'], data_user['logistics_user_profile_6']['last_acc'], data_user['logistics_user_profile_6']['status'], data_user['logistics_user_profile_6']['permanent_address'], data_user['logistics_user_profile_6']['contact_num'], data_user['logistics_user_profile_6']['state'], data_user['logistics_user_profile_6']['city'], data_user['logistics_user_profile_6']['country'], data_user['logistics_user_profile_6']['email'], data_user['logistics_user_profile_6']['dot_num'], data_user['logistics_user_profile_6']['license_number']))
            print(self.cnx.commit(),"TRANSACTED")
            cur.close()
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def create_emp(self,data_user,insert_to):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if insert_to == "logistics_user":
                print(" INSERTING TO LOGISTICS USERS")
                print(data_user)
                insert_user = (
                    "INSERT INTO logistics_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data_user['logistics_user']['id'], data_user['logistics_user']['org_id'], data_user['logistics_user']['f_name'], data_user['logistics_user']['m_name'], data_user['logistics_user']['l_name'], data_user['logistics_user']['date_created'], data_user['logistics_user']['last_acc'], data_user['logistics_user']['status'], data_user['logistics_user']['roles']))
            

            if insert_to == "logistics_user_profile_5":
                print(" INSERTING TO LOGISTICS USERS_PROFILES_2")
                print(data_user)
                insert_user_profile = (
                    "INSERT INTO logistics_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email,dot_num,license_number) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['logistics_user_profile_2']['id'], data_user['logistics_user_profile_2']['role'], data_user['logistics_user_profile_2']['date_created'], data_user['logistics_user_profile_2']['last_acc'], data_user['logistics_user_profile_2']['status'], data_user['logistics_user_profile_2']['permanent_address'], data_user['logistics_user_profile_2']['contact_num'], data_user['logistics_user_profile_2']['state'], data_user['logistics_user_profile_2']['city'], data_user['logistics_user_profile_2']['country'], data_user['logistics_user_profile_2']['email'], data_user['logistics_user_profile_2']['dot_num'], data_user['logistics_user_profile_2']['license_number']))

            print(self.cnx.commit(),"TRANSACTED")
            cur.close()
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def reg_mechanic_solo(self,data_user,insert_to):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if insert_to == "services_user":
                print(" INSERTING TO SERVICES USERS")
                insert_user = (
                    "INSERT INTO services_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data_user['services_user']['id'], data_user['services_user']['org_id'], data_user['services_user']['f_name'], data_user['services_user']['m_name'], data_user['services_user']['l_name'], data_user['services_user']['date_created'], data_user['services_user']['last_acc'], data_user['services_user']['status'], data_user['services_user']['roles']))


            if insert_to == "services_user_profile_3":
                insert_user_profile = (
                    "INSERT INTO services_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['services_user_profile_3']['id'], data_user['services_user_profile_3']['role'], data_user['services_user_profile_3']['date_created'], data_user['services_user_profile_3']['last_acc'], data_user['services_user_profile_3']['status'], data_user['services_user_profile_3']['permanent_address'], data_user['services_user_profile_3']['contact_num'], data_user['services_user_profile_3']['state'], data_user['services_user_profile_3']['city'], data_user['services_user_profile_3']['country'], data_user['services_user_profile_3']['email']))

            if insert_to == "services_user_profile_7":
                insert_user_profile = (
                    "INSERT INTO services_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['services_user_profile_7']['id'], data_user['services_user_profile_7']['role'], data_user['services_user_profile_7']['date_created'], data_user['services_user_profile_7']['last_acc'], data_user['services_user_profile_7']['status'], data_user['services_user_profile_7']['permanent_address'], data_user['services_user_profile_7']['contact_num'], data_user['services_user_profile_7']['state'], data_user['services_user_profile_7']['city'], data_user['services_user_profile_7']['country'], data_user['services_user_profile_7']['email']))
            
            print(self.cnx.commit(),"TRANSACTED")
            cur.close()
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_users":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR")
            print(e)
            return {"err":"Unexpected error"}
    



    def reg_driver_solo(self,data_user,insert_to):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if insert_to == "logistics_user":
                print(" INSERTING TO SERVICES USERS")
                insert_user = (
                    "INSERT INTO logistics_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data_user['logistics_user']['id'], data_user['logistics_user']['org_id'], data_user['logistics_user']['f_name'], data_user['logistics_user']['m_name'], data_user['logistics_user']['l_name'], data_user['logistics_user']['date_created'], data_user['logistics_user']['last_acc'], data_user['logistics_user']['status'], data_user['logistics_user']['roles']))



            if insert_to == "logistics_user_profile_6":
                insert_user_profile = (
                    "INSERT INTO logistics_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['logistics_user_profile']['id'], data_user['logistics_user_profile']['role'], data_user['logistics_user_profile']['date_created'], data_user['logistics_user_profile']['last_acc'], data_user['logistics_user_profile']['status'], data_user['logistics_user_profile']['permanent_address'], data_user['logistics_user_profile']['contact_num'], data_user['logistics_user_profile']['state'], data_user['logistics_user_profile']['city'], data_user['logistics_user_profile']['country'], data_user['logistics_user_profile']['email']))
            
            print(self.cnx.commit(),"TRANSACTED")
            cur.close()
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_users":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR")
            print(e)
            return {"err":"Unexpected error"}

    def create_trx_user(self,data_user):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
           
            print(" INSERTING TO TRX USERS")
            insert_user = (
                "INSERT INTO trx(id,roles,f_name,l_name,email,contact_num,date_created,last_acc,status) "
                "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                
                )
            insert_user_res = cur.execute(insert_user,(data_user['trx_user']['id'], data_user['trx_user']['roles'], data_user['trx_user']['f_name'], data_user['trx_user']['l_name'], data_user['trx_user']['email'], data_user['trx_user']['contact_num'], data_user['trx_user']['date_created'], data_user['trx_user']['last_acc'], data_user['trx_user']['status']))

            print(self.cnx.commit(),"TRANSACTED")
            cur.close()

        
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_users":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR")
            print(e)
            return {"err":"Unexpected error"}        

    def reg_mechanic_org(self,data,insert_to,id):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:

            if insert_to == "services_user":
                print(" INSERTING TO SERVICES USERS")
                print(data)
                insert_user = (
                    "INSERT INTO services_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data['services_user']['id'], data['services_user']['org_id'], data['services_user']['f_name'], data['services_user']['m_name'], data['services_user']['l_name'], data['services_user']['date_created'], data['services_user']['last_acc'], data['services_user']['status'], data['services_user']['roles']))

                print(self.cnx.commit(),"TRANSACTED")
                cur.close()

                return {},{"message" : "Record Created Successfully"}

            if insert_to == "services_user_profile_1":
                print(" INSERTING TO SERVICES USERS_PROFILES")
                print(data)
                insert_user_profile = (
                    "INSERT INTO services_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data['services_user_profile_1']['id'], data['services_user_profile_1']['role'], data['services_user_profile_1']['date_created'], data['services_user_profile_1']['last_acc'], data['services_user_profile_1']['status'], data['services_user_profile_1']['permanent_address'], data['services_user_profile_1']['contact_num'], data['services_user_profile_1']['state'], data['services_user_profile_1']['city'], data['services_user_profile_1']['country'], data['services_user_profile_1']['email']))

                print(self.cnx.commit(),"TRANSACTED")
                cur.close()
                return {},{"message" : "Record Created Successfully"}
            if insert_to == "services_orgs":
                print(" INSERTING TO SERVICES_ORGS")
                print(data)
                insert_log_org = (
                    "INSERT INTO services_orgs(owner_id, org_name, status, country, state, city, contact_num, permanent_address, zip_code, date_established, date_created) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"
                    
                    )
                print("Doing that org ID thing1")
                insert_log_org_res = cur.execute( insert_log_org, (id, data['services_org']['org_name'], data['services_org']['status'], data['services_org']['country'], data['services_org']['state'], data['services_org']['city'], data['services_org']['contact_num'], data['services_org']['permanent_address'], data['services_org']['zip_code'], data['services_org']['date_established'], data['services_org']['date_created']) )
                print("PRINTING ORG ID")
                org_id = cur.lastrowid
                print("Doing that org ID thing2")
                insert_org_id = ("UPDATE services_users SET org_id = %s WHERE id = %s")

                insert_org_id_res = cur.execute( insert_org_id,(cur.lastrowid,id))

                print("PRINTING ORG ID")
                
                print(org_id)

                print(self.cnx.commit(),"TRANSACTED")
                cur.close()
                return {},org_id
            #cur.lastrowid
            #SET org_id in logistics_users

            
            
        
            #print(self.cnx.commit(),"TRANSACTED")
            #cur.close()

        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_org_err":"Record already exist for user"}},{}
            else:
                return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}    




    def add_mechanic_org(self,data_user,insert_to):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if insert_to == "services_user":
                print(" INSERTING TO SERVICES USERS")
                insert_user = (
                    "INSERT INTO services_users(id, org_id, f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data_user['services_user']['id'], data_user['services_user']['org_id'], data_user['services_user']['f_name'], data_user['services_user']['m_name'], data_user['services_user']['l_name'], data_user['services_user']['date_created'], data_user['services_user']['last_acc'], data_user['services_user']['status'], data_user['services_user']['roles']))


            if insert_to == "services_user_profile_7":
                insert_user_profile = (
                    "INSERT INTO services_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['services_user_profile_7']['id'], data_user['services_user_profile_7']['role'], data_user['services_user_profile_7']['date_created'], data_user['services_user_profile_7']['last_acc'], data_user['services_user_profile_7']['status'], data_user['services_user_profile_7']['permanent_address'], data_user['services_user_profile_7']['contact_num'], data_user['services_user_profile_7']['state'], data_user['services_user_profile_7']['city'], data_user['services_user_profile_7']['country'], data_user['services_user_profile_7']['email']))

            
            print(self.cnx.commit(),"TRANSACTED")
            cur.close()
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_users":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR")
            print(e)
            return {"err":"Unexpected error"}

    def trx_create_mechanic(self,data_user,insert_to):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        try:
            if insert_to == "services_user":
                print(" INSERTING TO SERVICES USERS")
                insert_user = (
                    "INSERT INTO services_users(id,  f_name, m_name, l_name, date_created, last_acc, status, roles) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"
                    
                    )
                insert_user_res = cur.execute(insert_user,(data_user['services_user']['id'],  data_user['services_user']['f_name'], data_user['services_user']['m_name'], data_user['services_user']['l_name'], data_user['services_user']['date_created'], data_user['services_user']['last_acc'], data_user['services_user']['status'], data_user['services_user']['roles']))


            if insert_to == "services_user_profile_7":
                insert_user_profile = (
                    "INSERT INTO services_users_profiles(id, role,  date_created, last_acc, status, permanent_address, contact_num, state, city,country, email) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s)"
                    
                    )
                insert_user_profile_res = cur.execute( insert_user_profile,(data_user['services_user_profile_7']['id'], data_user['services_user_profile_7']['role'], data_user['services_user_profile_7']['date_created'], data_user['services_user_profile_7']['last_acc'], data_user['services_user_profile_7']['status'], data_user['services_user_profile_7']['permanent_address'], data_user['services_user_profile_7']['contact_num'], data_user['services_user_profile_7']['state'], data_user['services_user_profile_7']['city'], data_user['services_user_profile_7']['country'], data_user['services_user_profile_7']['email']))

            
            print(self.cnx.commit(),"TRANSACTED")
            cur.close()
                
        except mysql.connector.Error as err:
            print("PRINTING ERROR")
            print(err)
            print(err.errno)
            if err.errno == 1062:
                return {"err":{"logistics_users":"Record already exist for user"}}
            else:
                return {"err":"Unexpected error"}
        except Exception as e:
            print("PRINTING ERROR")
            print(e)
            return {"err":"Unexpected error"}          

    def insert_logistics_users(self,data,id,roles):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
               

        try:
            print("I am fron insert")
            print(data)
            add_entry    = ("INSERT INTO logistics_users"
                        "(id,org_id,roles,f_name,m_name,l_name,date_created,last_acc,status) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

            data_entry = (id,data['org_id'],roles, data['f_name'],data['m_name'],data['l_name'],data['date_created'],data['last_acc'],data['status'])
            cur.execute(add_entry,data_entry)
            self.cnx.commit()
            cur.close()
        except:
            return {"err":"unable to connect to db"}





    def insert_logistics_users_profiles(self,data,id,role):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            add_entry    = ("INSERT INTO logistics_users_profiles"
                        "(id,role,dot_num,liscence_number,permanent_address,contact_num,country,state,city,email,rating,total_reviews,date_created,last_acc,status) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            data_entry = (id,role,data['dot_num'], data['liscence_number'],data['permanent_address'],data['contact_num'],data['country'],data['state'],data['city'],data['email'],data['rating'],data['total_reviews'],data['date_created'],data['last_acc'],data['status'])
            cur.execute(add_entry,data_entry)
            self.cnx.commit()
            cur.close()
        except:
            return {"err":"unable to connect to db"}




    def insert_services_users(self,data,id,roles):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            print("From services_users")
            print(data)
            add_entry    = ("INSERT INTO services_users"
                        "(id,org_id,roles,f_name,m_name,l_name,date_created,last_acc,status) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")

            data_entry = (id,data['org_id'],roles, data['f_name'],data['m_name'],data['l_name'],data['date_created'],data['last_acc'],data['status'])
            cur.execute(add_entry,data_entry)
            self.cnx.commit()
            cur.close()
        except:
            return {"err":"unable to connect to db"}





    def insert_services_users_profiles(self,data,id,role):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}


        print("HEREARPOAE")
        try:
            print("from services_users_profiles")
            add_entry    = ("INSERT INTO services_users_profiles"
                        "(id,role,permanent_address,contact_num,country,state,city,email,rating,total_reviews,date_created,last_acc,status) "
                        "VALUES (%s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

            data_entry = (id,role,data['permanent_address'],data['contact_num'],data['country'],data['state'],data['city'],data['email'],data['rating'],data['total_reviews'],data['date_created'],data['last_acc'],data['status'])
            cur.execute(add_entry,data_entry)
            self.cnx.commit()
            cur.close()
        except:
            return {"message":"unable to connect to db"}




    def create_trip(self,data):
        #Add user
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}
        
        print(data)
        exe_plan = 0
        try:
            if data['logistics_org_id']:
                pass
        except:
            exe_plan = 1

        print(exe_plan)
        if exe_plan == 0:
            try:
                print("BEFORE")
                update_vehicle_status = "UPDATE vehicles SET status = %s  WHERE  vehicle_id = %s and status = 0"
                cur.execute(update_vehicle_status,(1,data['vehicle_id']))
                print("AFTER")
                if not(cur.rowcount):
                    print("ROW COUNT",cur.rowcount)
                    return {'err':"Vehicle not available"}


                insert_log_trip = (
                    "INSERT INTO trips(logistics_org_id, driver_id, vehicle_id, addr_start, addr_end,addr_current,coor_start,coor_end,coor_current, est_time, date_created, status) "
                    "VALUES ( %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s)"
                    
                    )
                print(data['addr_start'], data['addr_end'],data['addr_current'])
                insert_log_trip_res = cur.execute(insert_log_trip,(data['logistics_org_id'], data['driver_id'], data['vehicle_id'], data['addr_start'], data['addr_end'],data['addr_current'],data['coor_start'],data['coor_end'],data['coor_current'], data['est_time'], data['date_created'], data['status']))




                print(self.cnx.commit(),"TRANSACTED")
                cur.close()



            except mysql.connector.Error as err:
                print(err)
                print(err.errno)
                if err.errno == 1062:
                    return {"err":{"trip_err":"Record already exist for trip"}}
                else:
                    return {"err":"Unexpected error"}
            except Exception as e:
                print(e)
                return {"err":"Unexpected error"}


        
        #exe_plan 1
        elif exe_plan == 1:

            try:
                insert_solo_trip = (
                    "INSERT INTO trips(driver_id, vehicle_id, addr_start, addr_end, est_time, date_created, status) "
                    "VALUES ( %s, %s, %s,%s, %s, %s, %s)"
                    
                    )
                insert_log_trip_res = cur.execute(insert_solo_trip,( data['driver_id'], data['vehicle_id'], data['addr_start'], data['addr_end'], data['est_time'], data['date_created'], data['status']))


                print(self.cnx.commit(),"TRANSACTED")
                cur.close()



            except mysql.connector.Error as err:
                print(err)
                print(err.errno)
                if err.errno == 1062:
                    return {"err":{"trip_err":"Record already exist for trip"}}
                else:
                    return {"err":"Unexpected error"}
            except Exception as e:
                print(e)
                return {"err":"Unexpected error"}
        
        else:
            print("FAILED EXECUTION of exe_plan in trips mysql")
            return {"err":"Unexpected error"}



    
    def get_logistics_org(self,org_id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            get_log_org = (
                "SELECT org_id,org_name,country,state,city,contact_num,permanent_address,zip_code,date_established,rating,total_reviews FROM logistics_orgs WHERE org_id = %s"
                )
            cur.execute(get_log_org,(org_id,))

            get_log_org_res = cur.fetchone()


            profile = {
                "org_id":get_log_org_res[0],
                "org_name":get_log_org_res[1],
                "country":get_log_org_res[2],
                "state":get_log_org_res[3],
                "city":get_log_org_res[4],
                "contact_num":get_log_org_res[5],
                "permanent_address":get_log_org_res[6],
                "zip_code":get_log_org_res[7],
                "date_established":get_log_org_res[8],
                "rating":get_log_org_res[9],
                "total_reviews":get_log_org_res[10]
            }    
    
            cur.close()

            return profile





        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}




    def get_logistics_org_employee(self,org_id,emp_id = ''):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            print('emp_id',emp_id)
            if emp_id == '':

                get_log_org_emp = (
                    "SELECT id,f_name,m_name,l_name,roles FROM logistics_users WHERE org_id = %s"
                    )
                cur.execute(get_log_org_emp,(org_id,))

                get_log_org_emp_res = cur.fetchall()
                
                record_list = []
                for x in get_log_org_emp_res:
                    profile = {
                        "id":x[0],
                        "f_name":x[1],
                        "m_name":x[2],
                        "l_name":x[3],
                        "roles":x[4]
                    }
                    record_list.append(profile)

                cur.close()

                return record_list
            
            elif emp_id != '':
                
                get_log_org_emp = (
                    "SELECT id,f_name,m_name,l_name,roles FROM logistics_users WHERE id = %s "
                    )
                cur.execute(get_log_org_emp,(emp_id,))

                get_log_org_emp_res = cur.fetchone()




                get_log_org_emp_profiles = (
                    "SELECT role,dot_num,license_number,date_created,permanent_address,contact_num,country,state,city,email,rating,total_reviews FROM logistics_users_profiles WHERE id = %s"
                    )
                cur.execute(get_log_org_emp_profiles,(emp_id,))

                get_log_org_emp_prof_res = cur.fetchall()
                print(get_log_org_emp_prof_res)

                profile = {
                        "id":get_log_org_emp_res[0],
                        "f_name":get_log_org_emp_res[1],
                        "m_name":get_log_org_emp_res[2],
                        "l_name":get_log_org_emp_res[3],
                        "roles":get_log_org_emp_res[4],
                        "profile_roles":[]
                    }
                print(get_log_org_emp_prof_res)


                for x in get_log_org_emp_prof_res:
                    roles = {
                            "role":x[0],
                            "dot_num":x[1],
                            "license_number":x[2],
                            "date_created":x[3],
                            "permanent_address":x[4],
                            "contact_num":x[5],
                            "country":x[6],
                            "state":x[7],
                            "city":x[8],
                            "email":x[9],
                            "rating":x[10],
                            "total_reviews":x[11],
                    }
                    profile['profile_roles'].append(roles)

 
                cur.close()

                return profile
                



        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}



    def get_log_vehicles(self,org_id,user_id,vehicle_id):
        print(vehicle_id,"ASJDOIJOIAES")
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}


        try:
            if org_id != '':
                if vehicle_id != '':
                    print('IN ORG EVHICLe')
                    get_log_usr_vehicle = (
                    "SELECT vehicle_id,vin,type,status FROM vehicles WHERE org_id = %s and vehicle_id = %s"
                    )

                    cur.execute(get_log_usr_vehicle,(org_id,vehicle_id))

                    get_log_usr_vehicle_res = cur.fetchall()
                

                else:
                    print('NOT IN ORG EVHICLe')
                    get_log_org_vehicle = (
                        "SELECT vehicle_id,vin,type,status FROM vehicles WHERE org_id = %s"
                        )
                    cur.execute(get_log_org_vehicle,(org_id,))

                    get_log_usr_vehicle_res = cur.fetchall()




                record_list = []
                for x in get_log_usr_vehicle_res:
                    profile = {
                    "vehicle_id":x[0],
                    "vin":x[1],
                    "type":x[2],
                    "status":x[3]
                    }
                    record_list.append(profile)

                return record_list
            




            
            elif org_id == '':
                if vehicle_id != "":
                    
                    get_log_usr_vehicle = (
                    "SELECT vehicle_id,vin,type,status FROM vehicles WHERE user_id = %s and vehicle_id = %s"
                    )

                    cur.execute(get_log_usr_vehicle,(user_id,vehicle_id))

                    get_log_usr_vehicle_res = cur.fetchall()

                else:

                    get_log_usr_vehicle = (
                        "SELECT vehicle_id,vin,type,status FROM vehicles WHERE user_id = %s"
                        )
                    cur.execute(get_log_usr_vehicle,(user_id,))

                    get_log_usr_vehicle_res = cur.fetchall()



                record_list = []
                for x in get_log_usr_vehicle_res:
                    profile = {
                    "vehicle_id":x[0],
                    "vin":x[1],
                    "type":x[2],
                    "status":x[3]
                    }
                    record_list.append(profile)

                return record_list
                

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}



    ##Associate driver account
    
    def get_logistics_users(self,id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            get_log_org = (
                "SELECT org_id,roles,f_name,m_name,l_name,date_created,last_acc,status FROM logistics_users WHERE id = %s"
                )
            cur.execute(get_log_org,(id,))

            get_log_org_res = cur.fetchone()


            profile = {
                "org_id"            :get_log_org_res[0],
                "roles"             :get_log_org_res[1],
                "f_name"            :get_log_org_res[2],
                "m_name"            :get_log_org_res[3],
                "l_name"            :get_log_org_res[4],
                "date_created"      :get_log_org_res[5],
                "last_acc"          :get_log_org_res[6],
                "status"            :get_log_org_res[7],
            }    
    
            cur.close()
            self.cnx.commit()
            return {},profile
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}
    

    def get_logistics_users_profiles(self,id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            get_log_org = (
                "SELECT role,dot_num,license_number,date_created,last_acc,status,permanent_address,contact_num,country,state,city,email,rating,total_reviews FROM logistics_users_profiles WHERE id = %s"
                )
            cur.execute(get_log_org,(id,))

            get_log_org_res = cur.fetchone()


            profile = {
                "role"              :get_log_org_res[0],
                "dot_num"           :get_log_org_res[1],
                "license_number"   :get_log_org_res[2],
                "date_created"      :get_log_org_res[3],
                "last_acc"          :get_log_org_res[4],
                "status"            :get_log_org_res[5],
                "permanent_address" :get_log_org_res[6],
                "contact_num"       :get_log_org_res[7],
                "country"           :get_log_org_res[8],
                "state"             :get_log_org_res[9],
                "city"              :get_log_org_res[10],
                "email"             :get_log_org_res[11],
                "rating"            :get_log_org_res[12],
                "total_reviews"     :get_log_org_res[13],

            }    
    
            cur.close()

            return {},profile
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def associate_driver(self,id,org_id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            
            print('from function')
            print(org_id,id)
            sql = "UPDATE logistics_users SET org_id= %s  WHERE id = %s"
            val = (org_id, id)

            cur.execute(sql, val)
            self.cnx.commit()
                      

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def update_logistics_org(self,data_org,org_id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            for x in data_org['logistics_org']:
                if x == "org_name":

                    sql = "UPDATE logistics_orgs SET org_name= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['org_name'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "state":

                    sql = "UPDATE logistics_orgs SET state= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['state'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "city":

                    sql = "UPDATE logistics_orgs SET city= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['city'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "country":

                    sql = "UPDATE logistics_orgs SET country= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['country'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "permanent_address":

                    sql = "UPDATE logistics_orgs SET permanent_address= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['permanent_address'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "contact_num":

                    sql = "UPDATE logistics_orgs SET contact_num= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['contact_num'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                
                if x == "zip_code":

                    sql = "UPDATE logistics_orgs SET zip_code= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['zip_code'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()          
                
                if x == "date_established":

                    sql = "UPDATE logistics_orgs SET date_established= %s  WHERE org_id = %s"
                    val = (data_org['logistics_org']['date_established'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                      

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}


    def update_services_org(self,data_org,org_id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            for x in data_org['services_org']:
                if x == "org_name":

                    sql = "UPDATE services_orgs SET org_name= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['org_name'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "state":

                    sql = "UPDATE services_orgs SET state= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['state'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "city":

                    sql = "UPDATE services_orgs SET city= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['city'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "country":

                    sql = "UPDATE services_orgs SET country= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['country'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "permanent_address":

                    sql = "UPDATE services_orgs SET permanent_address= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['permanent_address'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "contact_num":

                    sql = "UPDATE services_orgs SET contact_num= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['contact_num'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                
                if x == "zip_code":

                    sql = "UPDATE services_orgs SET zip_code= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['zip_code'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()          
                
                if x == "date_established":

                    sql = "UPDATE services_orgs SET date_established= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['date_established'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "services_types":

                    sql = "UPDATE services_orgs SET services_types= %s  WHERE org_id = %s"
                    val = (data_org['services_org']['services_types'], org_id)

                    cur.execute(sql, val)
                    self.cnx.commit()    

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def update_driver(self,data_org,id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            for x in data_org['logistics_user_profile_6']:
                if x == "liscence_number":
                    print("I am from update driver")
                    sql = "UPDATE logistics_users_profiles SET liscence_number= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['liscence_number'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                
                if x == "permanent_address":

                    sql = "UPDATE logistics_users_profiles SET permanent_address= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['permanent_address'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "contact_num":

                    sql = "UPDATE logistics_users_profiles SET contact_num= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['contact_num'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "country":

                    sql = "UPDATE logistics_users_profiles SET country= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['country'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "state":

                    sql = "UPDATE logistics_users_profiles SET state= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['state'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "city":

                    sql = "UPDATE logistics_users_profiles SET city= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['city'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "dot_num":

                    sql = "UPDATE logistics_users_profiles SET dot_num= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['dot_num'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "f_name":

                    sql = "UPDATE logistics_users SET f_name= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['f_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "m_name":

                    sql = "UPDATE logistics_users SET m_name= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['m_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "l_name":

                    sql = "UPDATE logistics_users SET l_name= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_6']['l_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()             
                                                     
                      

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def update_mechanic(self,data_org,id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            for x in data_org['services_user_profile_7']:
                
                if x == "permanent_address":

                    sql = "UPDATE services_users_profiles SET permanent_address= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['permanent_address'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "contact_num":

                    sql = "UPDATE services_users_profiles SET contact_num= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['contact_num'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "country":

                    sql = "UPDATE services_users_profiles SET country= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['country'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "state":

                    sql = "UPDATE services_users_profiles SET state= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['state'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "city":

                    sql = "UPDATE services_users_profiles SET city= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['city'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                

                if x == "f_name":

                    sql = "UPDATE services_users SET f_name= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['f_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "m_name":

                    sql = "UPDATE services_users SET m_name= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['m_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "l_name":

                    sql = "UPDATE services_users SET l_name= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_7']['l_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()             
                                                     
                      

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}  

    def update_solo_owner_services(self,data_org,id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            for x in data_org['services_user_profile_3']:
                
                if x == "permanent_address":

                    sql = "UPDATE services_users_profiles SET permanent_address= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['permanent_address'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "contact_num":

                    sql = "UPDATE services_users_profiles SET contact_num= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['contact_num'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "country":

                    sql = "UPDATE services_users_profiles SET country= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['country'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "state":

                    sql = "UPDATE services_users_profiles SET state= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['state'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "city":

                    sql = "UPDATE services_users_profiles SET city= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['city'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                

                if x == "f_name":

                    sql = "UPDATE services_users SET f_name= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['f_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "m_name":

                    sql = "UPDATE services_users SET m_name= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['m_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "l_name":

                    sql = "UPDATE services_users SET l_name= %s  WHERE id = %s"
                    val = (data_org['services_user_profile_3']['l_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()             
                                                     
                      

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}


    def update_solo_owner_logistics(self,data_org,id):
        try:
            cur = self.cnx.cursor(buffered=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            for x in data_org['logistics_user_profile_2']:
                if x == "liscence_number":
                    print("I am from update driver")
                    sql = "UPDATE logistics_users_profiles SET liscence_number= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['liscence_number'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                
                if x == "permanent_address":

                    sql = "UPDATE logistics_users_profiles SET permanent_address= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['permanent_address'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "contact_num":

                    sql = "UPDATE logistics_users_profiles SET contact_num= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['contact_num'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "country":

                    sql = "UPDATE logistics_users_profiles SET country= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['country'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "state":

                    sql = "UPDATE logistics_users_profiles SET state= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['state'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "city":

                    sql = "UPDATE logistics_users_profiles SET city= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['city'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()
                if x == "dot_num":

                    sql = "UPDATE logistics_users_profiles SET dot_num= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['dot_num'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "f_name":

                    sql = "UPDATE logistics_users SET f_name= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['f_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "m_name":

                    sql = "UPDATE logistics_users SET m_name= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['m_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()

                if x == "l_name":

                    sql = "UPDATE logistics_users SET l_name= %s  WHERE id = %s"
                    val = (data_org['logistics_user_profile_2']['l_name'], id)

                    cur.execute(sql, val)
                    self.cnx.commit()             
                                                     
                      

        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}

    def get_trx_users(self):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = "SELECT * FROM trx"

            ## getting records from the table
            cur.execute(query)

            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_trx_users_filter_by_role(self,roles):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = f"SELECT * FROM trx where roles=\"{roles}\""

            ## getting records from the table
            cur.execute(query)

            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_logistic_users_filter_by_role(self,roles, org_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = f"SELECT * FROM logistics_users where roles=\"{roles}\" AND org_id=\"{org_id}\""

            ## getting records from the table
            cur.execute(query)

            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def get_service_users_filter_by_role(self,roles,org_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = f"SELECT * FROM services_users where roles=\"{roles}\" AND org_id=\"{org_id}\""

            ## getting records from the table
            cur.execute(query)

            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            
    
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}


    def get_trip_by_driver_id(self,driver_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            query = f"SELECT * FROM trips where driver_id='{driver_id}'  AND trips.`status`=1"
            ## getting records from the table
            cur.execute(query)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}      



    def delete_vehicle1(self, vehicle_id,user_id, org_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()

            print("connection of database")
            # query = f"SELECT * FROM trips where id='{id}'"
            if org_id == None:
                query = f"DELETE FROM vehicles where vehicle_id={vehicle_id} and user_id = {user_id}"
            
            else:
                query = f"DELETE FROM vehicles where vehicle_id={vehicle_id} and org_id = {org_id}"
            
            
            ## getting records from the table
            cur.execute(query)
            self.cnx.commit()
            
            ## fetching all records from the 'cursor' object
            records = "Deleted Succesfully"
            #users = {}
            #count = 1
            ## Showing the data
            return {}, records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def delete_logistic_user1(self, id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            # query = f"SELECT * FROM trips where id='{id}'"
            query = f"DELETE FROM logistics_users where id='{id}'"
            # getting records from the table
            cur.execute(query)
            self.cnx.commit()
            # fetching all records from the 'cursor' object
            records = "Deleted Succesfully logistic user"
            users = {}
            count = 1
            # Showing the data
            return {}, records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}



    def trx_login_user_details(self,id):

        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            query = "SELECT id,f_name,m_name,l_name,roles FROM trx where id = %s"

            ## getting records from the table
            cur.execute(query,(id,))
            print(cur.statement)

            ## fetching all records from the 'cursor' object
            record = cur.fetchone()

            ## Showing the data
            print(record)
            return {"res":record}
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"}      
    


    def list_support_ticket_for_machenics_logistics(self, supp_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            query = f"""SELECT users.id,users.f_name,users.m_name,users.l_name,users.roles,users.date_created,users.last_acc,users.last_acc,users.`status`,users.coor_current
                        FROM support_tickets AS ticket
                        INNER JOIN support_tickets_offers AS offers
                        ON ticket.offer_id = offers.offer_id
                        INNER JOIN services_users AS users
                        ON offers.mechanics_user_id = users.id
                        WHERE ticket.supp_id = {supp_id}"""
            ## getting records from the table
            cur.execute(query)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def list_support_ticket_for_machenics_trx(self, supp_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            query = f"""SELECT users.id,users.f_name,users.m_name,users.l_name,users.roles,users.date_created,users.last_acc,users.last_acc,users.`status`,users.coor_current
                        FROM support_tickets AS ticket
                        INNER JOIN support_tickets_offers AS offers
                        ON ticket.offer_id = offers.offer_id
                        INNER JOIN services_users AS users
                        ON offers.mechanics_user_id = users.id
                        WHERE ticket.supp_id = {supp_id}"""
            ## getting records from the table
            cur.execute(query)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            users = {}
            count = 1
            ## Showing the data
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}

    def update_vehicle(self ,vin,type,status,vehicle_id, org_id, user_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            if org_id != None:
                query = f"""UPDATE vehicles SET vin = '{vin}', type = '{type}', status = {status}  WHERE vehicle_id = {vehicle_id} AND org_id = {org_id}"""
                
            else:
                query = f"""UPDATE vehicles SET vin = '{vin}', type = '{type}', status = {status}  WHERE vehicle_id = {vehicle_id} AND user_id = {user_id}"""
            
            cur.execute(query)
            self.cnx.commit()
            records = "Vehicle Update successful"
            users = {}
            count = 1
            ## Showing the data
            return {},records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}


    # def delete_vehicle1(self, vehicle_id,user_id, org_id):
    #     try:
    #         cur = self.cnx.cursor(buffered=True,dictionary=True)

    #     except Exception as e:
    #         print(e)
    #         self.set_connection()
    #         return {"err":"Couldnot reach database. Please try again"},{}

    #     try:
    #         #result = cur.execute("SELECT * FROM trx")
    #         #record = cur.fetchall()
    #         print("connection of database")
    #         # query = f"SELECT * FROM trips where id='{id}'"
    #         if org_id != None:
    #             query = f"DELETE FROM vehicles where vehicle_id={vehicle_id} AND org_id = {org_id}"""                
    #         else:
    #             query = f"DELETE FROM vehicles where vehicle_id={vehicle_id} AND user_id = {user_id}"""
            
    #         ## getting records from the table
    #         cur.execute(query)
    #         self.cnx.commit()
    #         ## fetching all records from the 'cursor' object
    #         records = "Deleted Succesfully"
    #         users = {}
    #         count = 1
    #         ## Showing the data
    #         return {}, records
    #     except mysql.connector.Error as err:
    #         print(err)
    #         print(err.errno)
    #         return {"err":"Unexpected error"},{}
    #     except Exception as e:
    #         print(e)
    #         return {"err":"Unexpected error"},{}

    def delete_trx_user1(self, id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            # query = f"SELECT * FROM trips where id='{id}'"
            query = f"UPDATE  trx set status=100 WHERE id =\"{id}\""
            
            # getting records from the table
            cur.execute(query)
            self.cnx.commit()
            # fetching all records from the 'cursor' object
            records = "Deleted Succesfully trx user"
            users = {}
            count = 1
            # Showing the data
            return {}, records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}



    def delete_service_user(self, id, org_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            # query = f"SELECT * FROM trips where id='{id}'"
            query = f"UPDATE  services_users set status=100 WHERE id =\"{id}\" AND org_id=\"{org_id}\""
            # getting records from the table
            cur.execute(query)
            self.cnx.commit()
            # fetching all records from the 'cursor' object
            records = "Deleted Succesfully Service user"
            users = {}
            count = 1
            # Showing the data
            return {}, records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}


        
    def delete_logistics_user(self, id, org_id):
        try:
            cur = self.cnx.cursor(buffered=True,dictionary=True)

        except Exception as e:
            print(e)
            self.set_connection()
            return {"err":"Couldnot reach database. Please try again"},{}

        try:
            #result = cur.execute("SELECT * FROM trx")
            #record = cur.fetchall()
            print("connection of database")
            # query = f"SELECT * FROM trips where id='{id}'"
            # query = f"SET foreign_key_checks = 0; DELETE FROM logistics_users WHERE id ='{id}'"
            query = f"UPDATE  logistics_users set status=100 WHERE id =\"{id}\" AND org_id=\"{org_id}\""
            # getting records from the table
            cur.execute(query)
            self.cnx.commit()
            # fetching all records from the 'cursor' object
            records = "Deleted Succesfully Logistics user"
            users = {}
            count = 1
            # Showing the data
            return {}, records
        except mysql.connector.Error as err:
            print(err)
            print(err.errno)
            return {"err":"Unexpected error"},{}
        except Exception as e:
            print(e)
            return {"err":"Unexpected error"},{}