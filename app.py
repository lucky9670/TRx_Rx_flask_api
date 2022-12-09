from flask import Flask, request,json,Response,make_response,render_template
from flask_cors import CORS, cross_origin
import requests
import logging
#logging.basicConfig(filename='../record.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

 
 

import cognito_logistics_org,trx_sqldatabase,logistics_orgs,logistics_users,user_demo,vehicles,driver_trips,trx_users,support_tickets,support_tickets_offers
import cognito_services_org,cognito_trx_help_center,services_orgs,services_users,chat_service,location_service

import trx_s3_class

#import cognito_logistics_org,trx_sqldatabase,logistics_orgs,logistics_users,user_demo,vehicles,driver_trips
#import 
#import requests

app = Flask(__name__)
CORS(app)

msql = trx_sqldatabase.trxmysql_dbb()
print(msql.set_connection())


#cache control
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#cahche control



### Authorizer


## Authorizer for services
from functools import wraps
def authorizer(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.cookies.get('token')
        token = request.headers.get('Authorization')
        # jwt is passed in the request header
        ##class
        cognitoObj = cognito_services_org.cognito()
        if not token:
            return {"message" : "Missing Token"}
        else:
            err,claims = cognitoObj.validate_token(token)
            if(err):
                return err
            else:
                print("printing decorated")
                print(*args)
                print(**kwargs)
                return  f(claims, *args, **kwargs)
                
    return decorated



## Authorizer for logistics
def authorizer_logistics(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #token = request.cookies.get('token')
        token = request.headers.get('Authorization')
        # jwt is passed in the request header
        ##class
        cognitoObj = cognito_logistics_org.cognito()
        if not token:
            return {"message" : "Missing Token"}
        else:
            err,claims = cognitoObj.validate_token(token)
            if(err):
                return err
            else:
                print("printing decorated")
                print(*args)
                print(**kwargs)
                return  f(claims, *args, **kwargs)
                
    return decorated

## Authorizer for trx help center
def authorizer_trx(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = request.headers.get('Authorization')
        #token = request.cookies.get('token')
        # jwt is passed in the request header
        ##class
        cognitoObj = cognito_trx_help_center.cognito()
        if not token:
            return {"message" : "Missing Token"}
        else:
            err,claims = cognitoObj.validate_token(token)
            if(err):
                return err
            else:
                print("printing decorated")
                print(*args)
                print(**kwargs)
                return  f(claims, *args, **kwargs)
                
    return decorated          


@app.route('/')
def domain_main():
    return {'message':"WELCOME TO TRXADDA API"}


@app.route('/homee')
def homee():

    mechanics_user_id = "5a5425bc-66cc-4c51-a284-01bc25b8cdd4"
    err2,sev_user_data =  msql.get_sev_users(mechanics_user_id)
    if(err2):
        return {'err':err2}
    print("Printing result")
    mechanic_name = sev_user_data['f_name']
    return mechanic_name



########### signup

@app.route('/trx/admin/signup', methods=['POST'])
def sign_up_trx():
    req         = request.get_json()
    email       = req.get('email')
    password    = req.get('password')
    #confirmation_code = req.get('confirmation_code')
    ### class 
    cognitoObj = cognito_trx_help_center.cognito()
    err,passwd = cognitoObj.password_check(password)
    if(err):
        return err
    data = {
        'password'  : password,
        'email'     : email,
        'roles'      : "4",
        
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.sign_up(data)
    if(err):
        return {'err':err}
    else:
        
        return {'result' : "signup successfully"}

@app.route('/trx/signup/confirm', methods=['POST'])
def confirm_sign_up_trx():
    req         = request.get_json()
    email       = req.get('email')
    password    = req.get('password')
    confirmation_code    = req.get('confirmation_code')
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_trx_help_center.cognito()
    
    data = {
        'password'  : password,
        'email'     : email,
        'confirmation_code' : confirmation_code
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.confirm_signup(data)
    if(err):
        return {'err':err}
    else:
        return {'message' : 'signup confirmation successful' }

@app.route('/services/signup/confirm', methods=['POST','GET'])
def confirm_sign_up_services():
    req         = request.get_json()
    email       = req.get('email')
    password    = req.get('password')
    confirmation_code    = req.get('confirmation_code')
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_services_org.cognito()
    org_name = req.get('org_name')
    data = {
        'password'  : password,
        'email'     : email,
        'confirmation_code' : confirmation_code
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.confirm_signup(data)
    if(err):
        return {'err':err}
    else:
        
        return {'result' : "Signup Confirmed successfully"}        



@app.route('/logistics/signup/confirm', methods=['POST'])
def confirm_sign_up_logistics():
    req         = request.get_json()
    email       = req.get('email')
    password    = req.get('password')
    confirmation_code    = req.get('confirmation_code')
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_logistics_org.cognito()
    org_name = req.get('org_name')
    data = {
        'password'  : password,
        'email'     : email,
        'confirmation_code' : confirmation_code
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.confirm_signup(data)
    if(err):
        return {'err':err}
    else:
        
        return {'result' : "Signup Confirmed successfully"}


@app.route('/states', methods=['POST'])
def give_states():
    req         = request.get_json()
    
    err={}
    #confirmation_code = req.get('confirmation_code')
    ### class
    log_user_drv = logistics_users.log_users(req)
    err['logistics_user_err'] = log_user_drv.verify_country()
    print("HERE")
    if err['logistics_user_err'] == {}:
        del err['logistics_user_err']

    if err != {}:
        return {"err":err}

    country = log_user_drv.get_states()        
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
   
        
    return {'result' :country} 

@app.route('/cities', methods=['POST'])
def give_cities():
    req         = request.get_json()
    
    err = {}
    #confirmation_code = req.get('confirmation_code')
    ### class
    log_user_drv = logistics_users.log_users(req)
    err['logistics_user_err'] = log_user_drv.verify_states()
    print("HERE")
    if err['logistics_user_err'] == {}:
        del err['logistics_user_err']

    if err != {}:
        return {"err":err}

    cities = log_user_drv.get_cities()        
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
   
        
    return {'result' : cities} 
############# LOGIN
@app.route('/trx/user/login/forcepassword', methods=['POST'])
def login_force_password():
    req         = request.get_json()

    try:
        email       = req.get('email','')
    except Exception as e:
        print(e)
        return {'err':"email was not sent."}
    
    try:    
        password    = req.get('password','')
    except Exception as e:
        print(e)
        return {'err':"password was not sent."}

    
    if email == '' or password == '':
        return {'err':"email or password cannot be empty"}
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_trx_help_center.cognito()
    err,passwd = cognitoObj.password_check(password)
    if(err):
        return err
    data = {
        'password'  : password,
        'email'     : email,
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.login_password(data)
    if(err):
        return {'err':err}
    else:
        return {'result' : "Password Changed successfully"}

@app.route('/trx/user/login', methods=['POST'])
def login_trx():
    req         = request.get_json()

    try:
        email       = req.get('email','')
    except Exception as e:
        print(e)
        return {'err':"email was not sent."}
    
    try:    
        password    = req.get('password','')
    except Exception as e:
        print(e)
        return {'err':"password was not sent."}

    
    if email == '' or password == '':
        return {'err':"email or password cannot be empty"}
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_trx_help_center.cognito()
    err,passwd = cognitoObj.password_check(password)
    if(err):
        return {'err':err}
    data = {
        'password'  : password,
        'email'     : email,
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.login(data)
    print(result)

    if(err):
        return err
    print(result.get('email_verified',None))
    if result.get('email_verified',None) == False:
        return {"message":"Email is not verified"}

    id_token = result['AuthenticationResult']['IdToken']
    
    #Decripting token to get id to be searched in MySQL
    err,claims = cognitoObj.validate_token(id_token)
    if(err):
        return err

    print(claims['sub'])

    #Passing id to trx emp table to get user details

    check = msql.trx_login_user_details(claims['sub'])

    if check.get('err',None) != None:
        return check

    print(check)
    response = make_response({"token": id_token,'profile':check['res']})
    response.set_cookie( "token", id_token ,secure=False,domain='.trxadda.com')
    response.set_cookie( "token", id_token ,secure=False,domain='127.0.0.1')
    response.headers['Authorization'] = id_token
    return response

@app.route('/services/login', methods=['POST'])
def login_services():
    req         = request.get_json()

    try:
        email       = req.get('email','')
    except Exception as e:
        print(e)
        return {'err':"email was not sent."}
    
    try:    
        password    = req.get('password','')
    except Exception as e:
        print(e)
        return {'err':"password was not sent."}

    
    if email == '' or password == '':
        return {'err':"email or password cannot be empty"}
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_services_org.cognito()
    err,passwd = cognitoObj.password_check(password)
    if(err):
        return {'err':err}
    data = {
        'password'  : password,
        'email'     : email,
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.login(data)
    if(err):
        return {'err':err}
    else:
        id_token = result['AuthenticationResult']['IdToken']
        response = make_response({"token": id_token})
        print(id_token)
        response.set_cookie( "token", id_token,secure=False,httponly=False,domain=request.remote_addr)
        response.headers['Authorization'] = id_token
        return response



@app.route('/logistics/login', methods=['POST'])
def login_logistics():
    
    req         = request.get_json()

    try:
        email       = req.get('email','')
    except Exception as e:
        print(e)
        return {'err':"email was not sent."}
    
    try:    
        password    = req.get('password','')
    except Exception as e:
        print(e)
        return {'err':"password was not sent."}

    
    if email == '' or password == '':
        return {'err':"email or password cannot be empty"}

    print(email,password)
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_logistics_org.cognito()
    err,passwd = cognitoObj.password_check(password)
    if(err):
        return {'err':err}
    data = {
        'password'  : password,
        'email'     : email,
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.login(data)
    if(err):
        return {'err':err}
    else:
        id_token = result['AuthenticationResult']['IdToken']
        response = make_response({"token": id_token})
        print(id_token)
        response.set_cookie( "token", id_token ,secure=False ,httponly=False,domain=request.remote_addr)
        response.headers['Authorization'] = id_token
        return response

################### TRX
@app.route('/callurl', methods=['POST','GET'])
def home123():
    req = request.get_json()
    print(req)
    url = req['url']
    headers = {
		'Content-Type' : 'application/json'
        }
    try:
        requestss = requests.get(url,headers= headers)
        try:
            result = json.loads(requestss.content)
            return result
        except Exception as e:
            app.logger.critical(e)
        try:
            result = requestss.content
            return result
        except Exception as e:
            app.logger.critical(e)
    except Exception as e:
        app.logger.critical(e)
    return {"HEY":"HEY"}



@app.route('/trx/admin/user/create', methods=['POST'])
@authorizer_trx
def admin_create_user(claims):
    role = claims['custom:roles']
    print(role)
    if role != '4':
        return {"message" : "Only admin can change role"}
    req = request.get_json()
    req_trx = req.get('trx_users','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_trx_help_center.cognito()
    trx_user = trx_users.trx_user(req_trx)
    ### logic
    ### validating inputs 
    err['trx_user_err'] = trx_user.verify_data_all()
    
    if err['trx_user_err'] == {}:
        del err['trx_user_err']

    if err != {}:
        print("PRINTING ERROR")
        print(err)
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : req_trx.get('email',""),
        "password"  : req_trx.get('password',""),
        "roles"     : req_trx.get('roles',""),
        "status0"   : "0",
        "status1"   : "1",
        }
        err,result = cognitoObj.create_user(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = trx_user.get_data_all(id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            check =  msql.create_trx_user(verified_data)
            #MySQL error check
            if check:
                err,result = cognitoObj.delete_user(cog_data)
                return {"err" : check}
            else:       
                return {"result" : "Success"}
                

@app.route('/trx/role/change', methods=['POST'])
@authorizer_trx
def admin_change_role(claims):
    role = claims['custom:roles']
    if role != '4':
        return {"message" : "Only admin can change role"}
    req         = request.get_json()
    email       = req.get('email')
    roles       = req.get('roles')
    #confirmation_code = req.get('confirmation_code')
    ### class
    cognitoObj = cognito_trx_help_center.cognito()
    data = {
        'email'     : email,
        'roles'     : roles,
        
    } 
    #err,result = cognitoObj.sign_up_owner(data)
    #err,result = cognitoObj.confirm_signup(data)
    err,result = cognitoObj.add_role(data)
    if(err):
        return {'err':err}
    else:
        return {'result' : "Role Changed Successfully"}


@app.route('/trx/logistics/support_tickets', methods=['GET'])
#@authorizer_trx
def trx_get_pending_supp_tickets():#claims
    #role = claims['custom:roles']

    req         = request.args.to_dict()
    print(req)
    
    try:
        s_ticket = req.get('supp_id',None)
    except:
        s_ticket = None

    try:
        op = req.get('status',None)
    except:
        op = None

    op_list = ['completed','assigned','not-assigned']

    if op != None:
        if op  not in op_list:
            return {'err':"Allowed operations are 'completed','assigned' and 'not-assigned'"}

    check = msql.trx_get_supp_ticket(s_ticket,op)

    return check

@app.route('/trx/logistics/support_tickets/services', methods=['GET'])
@authorizer_trx
def trx_find_mechanics_log(claims):#claims
    #role = claims['custom:roles']

    req         = request.args.to_dict()
    
    try:
        s_ticket = req.get('supp_id',None)
    except:
        s_ticket = None

    try:
        t_ticket = req.get('trip_id',None)
    except:
        t_ticket = None

    if s_ticket == None and t_ticket == None:
        return {'err':"Both supp_id and trip_id cannot be empty"}


    check = msql.get_4_prec_hash(s_ticket,t_ticket)
    print(check)

    return check



@app.route('/trx/user/list', methods=['GET'])
@authorizer_trx
def list_users(claims):
    
    role = claims['custom:roles']
    if role != '4':
        return {"message" : "Only admin can list users"}
    err,result =  msql.get_trx_users()
    if(err):
        return err
    else:
        return {"result":result}

#Implement Support Tickets offers chat rooms in Chat Service
@app.route('/trx/support_tickets_offers', methods=['POST'])
@authorizer_trx
def trx_support_tickets_offerss(claims):
    

    try:
        trx_user_id = claims['cognito:username']
        print("user_ID",trx_user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}    
    ### input
    #supp_id = '21'
    
    
    req = request.get_json()
    supp_offers = req.get('support_tickets_offers','')
    supp_id = supp_offers.get('supp_id')
    mechanic_org_id     = supp_offers.get('mechanic_org_id')
    mechanics_user_id   = supp_offers.get('mechanics_user_id')
    
    ### garbage collector
    err = {}

    ### class
   
    supp_offers_obj =  support_tickets_offers.supp_tick_offers(supp_offers)
     
    err =  supp_offers_obj.verify_org_ticket_all()
    
    if(err):
        return {'err' : err}
    
    #print("from route")
    ### Creating record in DB
    data =  supp_offers_obj.get_profile_org_ticket_all(supp_id,mechanic_org_id,mechanics_user_id)
    print(data)
    err,offer_id = msql.trx_create_support_tickets_offers(data,trx_user_id)
    if(err):
        return {"err" : err}

    ## getting mechanic_name
    err2,sev_user_data =  msql.get_sev_users(mechanics_user_id)
    if(err2):
        return {'err':err2}
    print("Printing result")
    mechanic_name = sev_user_data['f_name']     
    route = 'chat'    
    payload = {
            "username" : mechanic_name,
            "room" : offer_id['offer_id']
        }

    chatObj = chat_service.chat()
    result = chatObj.post_call(payload,route)
    
    return result

# Create function to implement chat between TRx help center and mechanics in support ticket offers
@app.route('/trx/chat/support_tickets_offers/mechanics', methods=['POST','GET'])
@authorizer_trx
def chat_between_trx_mechanics(claims):
    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}
    ##################### INPUT
    req = request.get_json()
    offer_id       = req.get('offer_id')

    trx_user_id  = user_id
    
    print("PRINTING OFFER ID")
    
    print(offer_id)
    ### Getiing mechanic ID
    err2,support_tickets_offers_data =  msql.get_support_ticket_offers_chat(offer_id)
    print(support_tickets_offers_data)
    if(err2):
        print(support_tickets_offers_data)
        print("from 1")
        return {'err':err2}

    mechanics_user_id = support_tickets_offers_data['mechanics_user_id']
    print("HEREEEE")
    print(mechanics_user_id)


    ## getting mechanic_name
    err2,sev_user_data =  msql.get_sev_users(mechanics_user_id)
    if(err2):
        return {'err':err2}
    print("Printing result")
    mechanic_name = sev_user_data['f_name']

    err2,trx_user_data =  msql.get_trx_user(trx_user_id)
    if(err2):
        return {'err':err2}
    print("Printing result")
    print(trx_user_data)
    trx_user_name = trx_user_data['f_name']       
    print(trx_user_name)
    route = 'chat'    
    payload = {
            "username" : trx_user_name,
            "room" : offer_id
        }

    chatObj = chat_service.chat()
    result = chatObj.post_call(payload,route)
    
    return result

#Route for Help Center To  Initiate Geo-scan and chat for quotes for the corresponding support offer
@app.route('/trx/logistics/support_tickets_offers/geo_scan', methods=['POST','GET'])
@authorizer_trx
def support_tickets_geo_scan(claims):
    ### from claims take the org_id and id of the owner adding employeee
    #org_id = claims['custom:org_id']
    ### input
    supp_id = '21'
    mechanics_user_id = '28c6dab0-c836-411c-a52d-ea35a3dffafb'
    req = request.get_json()
    
    ### garbage collector
    err = {}

    ### class
    chatObj = chat_service.chat()
    
    route = 'chat'    
    payload = {
            "username" : mechanics_user_id,
            "room" : supp_id
        }

    print(type(payload))
    chatObj = chat_service.chat()
    result = chatObj.post_call(payload,route)
    print("PRINTING RESULT")
    print(type(result))
    print(result)
    return result


@app.route('/trx/services/org', methods=['GET'])
@authorizer_trx
def get_services_orgs_status(claims):
    req = request.args.to_dict()
    #default param
    org_id = ''

    #required inputs
    #org_id = req.get('org_id')
    #op = req.get('op')



    try:
        op = req.get('op','')
    except:
        op = ''
    
    try:
        org_id = req.get('org_id','')
    except:
        org_id = ''

    #get all services orgs pending for approval
    if op == 'pending':
        op = 0
        res = msql.get_services_orgs_status(op,org_id)
        return {'res':res}
    
    elif op == 'approved':
        op = 2
        return {'res':msql.get_services_orgs_status(op,org_id)}

    elif org_id != '':
        op = 1
        print(org_id)
        return {'res':msql.get_services_orgs_status(op,org_id)}

    else:
        return {'err':'incorrect format'}    

@app.route('/trx/logistics/org', methods=['GET'])
@authorizer_trx
def get_log_org(claims):
    req = request.args.to_dict()
    #default param
    org_id = ''

    #required inputs
    #org_id = req.get('org_id')
    #op = req.get('op')


    try:
        org_id = req.get('org_id','')
    except:
        org_id = ''
    

    if org_id != '':
        return {'result':msql.get_log_org(org_id)}
    
    else:
        return {'result':msql.get_log_orgs()}   


@app.route('/trx/logistics/company', methods=['GET'])
@authorizer_trx
def get_log_company(claims):
    req = request.args.to_dict()
    #default param
    owner_id = ''

    #required inputs
    #org_id = req.get('org_id')
    #op = req.get('op')


    try:
        owner_id = req.get('owner_id','')
    except:
        owner_id = ''
    

    if owner_id != '':
        return {'result':msql.get_log_company(owner_id)}
    
    else:
        return {'result':msql.get_log_companies()}


@app.route('/trx/services/company', methods=['GET'])
@authorizer_trx
def get_services_company_status(claims):
    req = request.args.to_dict()
    #default param
    user_id = ''

    #required inputs
    #user_id = req.get('user_id')
    #op = req.get('op')



    try:
        op = req.get('op','')
    except:
        op = ''
    
    try:
        user_id = req.get('owner_id','')
    except:
        user_id = ''

    if user_id != '':
        op = ''

    #get all services orgs pending for approval
    if op == 'pending':
        op = 0
        print(op)
        return {'result':msql.get_services_company_status(op,user_id)}
    
    elif op == 'approved':
        op = 2
        return {'result':msql.get_services_company_status(op,user_id)}

    elif user_id != '':
        op = 1
        return {'result':msql.get_services_company_status(op,user_id)}

    else:
        return {'err':'incorrect format'}




@app.route('/trx/services/company/action', methods=['POST'])
@authorizer_trx
def get_services_company_action(claims):
    req = request.get_json()
    #default param
    user_id = ''

    #required inputs
    #user_id = req.get('user_id')
    #op = req.get('op')



    try:
        op = req.get('op','')
    except:
        return {"err":"Opeartion not specified"}
    
    try:
        user_id = req.get('owner_id','')
    except:
        return {"err":"owner_id not specified"}
    
    if op == "approve":
        op = 0
        return {'res':msql.action_services_company_status(op,user_id)}
    
    elif op == "deny":
        op = 1
        return {'result':msql.action_services_company_status(op,user_id)}

    else:
        return {"err":"Unexpected exit"}




@app.route('/trx/services/org/action', methods=['POST'])
@authorizer_trx
def get_services_org_action(claims):
    req = request.get_json()
    #default param
    org_id = ''

    #required inputs
    #org_id = req.get('org_id')
    #op = req.get('op')



    try:
        op = req.get('op','')
        print(op)
        if op == 'approve' or op == 'deny':
            pass
        else:
            return {"err":"Invalid action specified."}
    except:
        return {"err":"Opeartion not specified"}
    
    try:
        org_id = req.get('org_id','')
    except:
        return {"err":"org_id not specified"}

    if op == "approve":
        op = 0
        return {'result':msql.action_services_org_status(op,org_id)}
    
    elif op == "deny":
        op = 1
        return {'result':msql.action_services_org_status(op,org_id)}

    else:
        return {"err":"Unexpected exit"}                     

##Logistics company, Trx join the support ticket for appropriate roles
@app.route('/trx/add/representative/', methods=['POST'])
@authorizer_trx
def add_rep(claims):
    ## Input
    req             = request.get_json()
    supp_id         = req.get('supp_id')
    rep_id          = req.get('rep_id')
   
    
    err,data =  msql.get_supp_id(supp_id)
    print("Printing Data")
    print(data)
    if(err):
        return {"err":err}

    
    if data['status'] == 1:
        return {"message" : "Support ticket Already assigned to representative"}    
    print("PRINTING DATA")
    print(data)    
    check =  msql.add_rep(supp_id,rep_id)
    if(check):
        return {"meesage": "failed"}
    status = 1
    check = msql.update_supp_ticket_status(supp_id,status)
    if(check):
        print(check)
        return {"err" :check}

    return {"message":"Representative added Successfully"}

@app.route('/trx/mechanic/create', methods=['POST'])
@authorizer_trx
def trx_add_mechanic(claims):
    ### from claims take the org_id and id of the owner adding employeee
    org_id = ""
    ### input
    req = request.get_json()
    print(req)
    if req == None:
        return {'err':"Empty Request"}
    mech = req.get('services_user','')
    print(mech)
    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_services_org.cognito()
    sev_mechanic = services_users.services_users(mech)
    ### logic
    ### validating inputs
    # assuming that org_id coming from authorizer
    #org_id = "8" 
    
    err['services_user_err'] = sev_mechanic.verify_role_7_data_all()
    
    if err['services_user_err'] == {}:
        del err['services_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : mech.get('email',""),
        "password"  : mech.get('password',""),
        "roles"     : "7",
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : org_id
        }
        err,result = cognitoObj.create_user(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = sev_mechanic.get_role_7_data_all(id,org_id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            insert_to = "services_user"
            check =  msql.trx_create_mechanic(verified_data,insert_to)
            #MySQL error check
            if check:
                print("CHECK_1")
                print(check)
                err,result = cognitoObj.delete_user(cog_data)
                return {"message" : check}
            else:
                ### inserting data to logistics_users_profiles with role 7
                insert_to = "services_user_profile_3"
                check =  msql.trx_create_mechanic(verified_data,insert_to)
                if check:
                    print("CHECK_2")
                    print(check)
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"message" : check}
                else:
                    return {"message" : "Record Created"}

####################### SERVICES
############ Registration
#Register solo mechanics #signup #no org_id
@app.route('/services/com/create', methods=['POST','GET'])
def mechanic():
    ### input
    req = request.get_json()
    mech = req.get('services_user','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_services_org.cognito()
    sev_mechanic = services_users.services_users(mech)
    ### logic
    ### validating inputs 
    err['services_user_err'] = sev_mechanic.verify_role_3_7_data_all()
    
    if err['services_user_err'] == {}:
        del err['services_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : mech.get('email',""),
        "password"  : mech.get('password',""),
        "roles"     : "3,7",
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : "none"
        }
        err,result = cognitoObj.sign_up(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = sev_mechanic.get_role_3_7_data_all(id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            insert_to = "services_user"
            check =  msql.reg_mechanic_solo(verified_data,insert_to)
            #MySQL error check
            if check:
                print("CHECK_1")
                print(check)
                err,result = cognitoObj.delete_user(cog_data)
                return {"message" : check}
            else:
                ### inserting data to logistics_users_profiles with role 3
                insert_to = "services_user_profile_3"
                check =  msql.reg_mechanic_solo(verified_data,insert_to)
                if check:
                    print("CHECK_2")
                    print(check)
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"message" : check}
                else:
                    ### inserting data to logistics_users_profiles with role 7
                    insert_to = "services_user_profile_7"
                    check =  msql.reg_mechanic_solo(verified_data,insert_to)
                    if check:
                        print("CHECK_3")
                        print(check)
                        ### settting status in cognito to 1
                        err,result = cognitoObj.update_user(cog_data)
                        return {"message" : check}
                    else:
                        return {"message" : "Success"}

#Register organization with multiple mechanics #signup # put orgid to cognito
@app.route('/services/org/create', methods=['POST','GET'])
def mechanic_mut():
    ### input
    req = request.get_json()
    req_org = req.get('services_org','')
    mech    = req.get('services_user','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_services_org.cognito()
    sev_mechanic = services_users.services_users(mech)  ##service_user class
    ser_org = services_orgs.ser_orgs(req_org) ##serviceorg class
    ### logic
    ### validating inputs
    
    err['services_org_err'] = ser_org.verify_org_data_all()
    print("HERE")
    if err['services_org_err'] == {}:
        del err['services_org_err']



    err['services_user_err'] = sev_mechanic.verify_role_1_data_all()

    if err['services_user_err'] == {}:
        del err['services_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : mech.get('email',""),
        "password"  : mech.get('password',""),
        "roles"     : "1",
        "status0"   : "1",
        "status1"   : "1",
        "org_id"    : "none"
        }
        err,result = cognitoObj.sign_up(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            print("Printing cog_data")
            print(result)
            id =  result['UserAttributes'][0]['Value']
            verified_data = sev_mechanic.get_role_1_data_all(id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### Creating user in services_users with role
            insert_to = "services_user"
            err_db,result =  msql.reg_mechanic_org(verified_data,insert_to,id)
            #MySQL error check
            if(err_db):
                print("FROM CHECK_1")
                print(err)
                err,result = cognitoObj.delete_user(cog_data)
                return {"err" : err_db}
            else:
                ### inserting data to services_orgs with role 1
                insert_to = "services_orgs"
                verified_org_data = ser_org.get_org_data_all()
                err_db,org_id =  msql.reg_mechanic_org(verified_org_data,insert_to,id)
                if(err_db):
                    print("FROM CHECK_2")
                    print(err_db)
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"err" : err_db}
                else:
                    print("From route printing org_id")
                    print(org_id)
                    err,result = cognitoObj.add_org_id(cog_data,str(org_id))
                    ### inserting data to logistics_users_profiles with role 7
                    insert_to = "services_user_profile_1"
                    err_db,result =  msql.reg_mechanic_org(verified_data,insert_to,id)
                    if err_db:
                        print("FROM CHECK_3")
                        print(err_db)
                        ### settting status in cognito to 1
                        err,result = cognitoObj.update_user(cog_data)
                        return {"err" : err_db}
                    else:
                        return {"message" : "Record Created"}    

#MECHANIC- Add other mobile mechanics to the company (if the number of employees > 1) #create user
@app.route('/services/mecahnic/create', methods=['POST','GET'])
@authorizer
def add_mechanic(claims):
    ### from claims take the org_id and id of the owner adding employeee
    org_id = claims['custom:org_id']
    ### input
    req = request.get_json()
    mech = req.get('services_user','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj   = cognito_services_org.cognito()
    sev_mechanic = services_users.services_users(mech)
    ### logic
    ### validating inputs
    # assuming that org_id coming from authorizer
    #org_id = "8" 
    
    err['services_user_err'] = sev_mechanic.verify_role_7_data_all()
    
    if err['services_user_err'] == {}:
        del err['services_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : mech.get('email',""),
        "password"  : mech.get('password',""),
        "roles"     : "7",
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : org_id
        }
        err,result = cognitoObj.create_user(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = sev_mechanic.get_role_7_data_all(id,org_id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            insert_to = "services_user"
            check =  msql.add_mechanic_org(verified_data,insert_to)
            #MySQL error check
            if check:
                print("CHECK_1")
                print(check)
                err,result = cognitoObj.delete_user(cog_data)
                return {"message" : check}
            else:
                ### inserting data to logistics_users_profiles with role 3
                insert_to = "services_user_profile_3"
                check =  msql.add_mechanic_org(verified_data,insert_to)
                if check:
                    print("CHECK_2")
                    print(check)
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"message" : check}
                else:
                    return {"message" : "Record Created"}

@app.route('/services/support_ticket/workapproval', methods=['PUT'])
@authorizer
def work_appr(claims):

    org_id = claims.get('custom:org_id',None)
    print(org_id)

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}

    req = request.form



    #inserting image record in req obj

    try:
        #Holding image object for later use.
        image = request.files['img_record_after']
    except Exception as e:
        image = None
        print('IMG NOT FOUND',e)


    #req = request.get_json()
    print(req,'\n')

    if req == '' or req == {} or req == None:
        return {"err":"Empty record sent"}




    suppObj = support_tickets.supp_tickets(req)



    if org_id != None:
        suppObj.logistics_org_id = org_id #set org_id
        suppObj.img_record_after = image



        err  = suppObj.verify_work_approval_data()
        print(err)
        if err:
            
            return {"err":err}
        

    return {'result':"Image uploaded Successfully"}

@app.route('/services/logistics/support_tickets', methods=['GET'])
#@authorizer_trx
def get_pending_supp_tickets():#claims
    #role = claims['custom:roles']

    req         = request.args.to_dict()
    
    try:
        s_ticket = req.get('supp_id',None)
        op = req.get('status',None)
    except:
        s_ticket = None

    try:
        op = req.get('status',None)
    except:
        op = None

    op_list = ['completed','pending','not-assigned']

    if op != None:
        if op  not in op_list:
            return {'err':"Allowed operations are 'completed','pending' and 'not-assigned'"}

    check = msql.trx_get_supp_ticket(s_ticket,op)

    return check

@app.route('/services/logistics/support_ticket/scan', methods=['GET'])
#@authorizer_trx
def find_log_jobs():#claims
    #role = claims['custom:roles']

    id = '28c6dab0-c836-411c-a52d-ea35a3dffafb'


    check = msql.get_4_prec_hash_services(id)
    print(check)

    return check


#Implement Support Tickets offers chat rooms in Chat Service
@app.route('/services/support_tickets_offers', methods=['POST'])
@authorizer
def support_tickets_offerss(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}    
    ### input
    #supp_id = '21'
    mechanic_org_id = org_id
    mechanics_user_id = user_id

    #Checking Mechanic's availablity
    err = msql.check_services_users_availablity(mechanics_user_id)
    print(err)
    if err != {}:
        return err

    req = request.get_json()
    supp_offers = req.get('support_tickets_offers','')
    supp_id = supp_offers.get('supp_id')
    
    ### garbage collector
    err = {}

    ### class
   
    supp_offers_obj = support_tickets_offers.supp_tick_offers(supp_offers)
     
    err =  supp_offers_obj.verify_org_ticket_all()
    
    if(err):
        return {'err' : err}
    
    print("from route")
    ### Creating record in DB
    data =  supp_offers_obj.get_profile_org_ticket_all(supp_id,mechanic_org_id,mechanics_user_id)
    print(data)
    err,offer_id = msql.create_support_tickets_offers(data)
    if(err):
        return {"err" : err}

    ## getting mechanic_name
    err2,sev_user_data =  msql.get_sev_users(mechanics_user_id)
    if(err2):
        return {'err':err2}
    print("Printing result")
    mechanic_name = sev_user_data['f_name']     
    route = 'chat'    
    payload = {
            "username" : mechanic_name,
            "room" : offer_id['offer_id']
        }

    chatObj = chat_service.chat()
    result = chatObj.post_call(payload,route)
    
    return result

#Update quotes in support_ticket_offers with tag-mark TRx and send it to support_ticket chat    
@app.route('/services/support_tickets_offers/quote', methods=['POST'])
@authorizer
def supp_offers_quote(claims):
    ### input
    req             = request.get_json()
    offer_id         = req.get('offer_id')
    print("printing offer_id")
    print(offer_id)    
    ### garbage collector
    err = {}

    ### class
    req = request.get_json()
    supp_offers = req.get('support_tickets_offers','')

    supp_offers_obj = support_tickets_offers.supp_tick_offers(supp_offers)
     
    err =  supp_offers_obj.verify_quote()
    
    ## checking if the support ticket offer is already accepted 
    err1,support_tickets_offers_data =  msql.get_support_ticket_offers_chat(offer_id)
    if(err1):
        print("from 1")
        return {'err':err1}
    
    
    if support_tickets_offers_data['status'] == 1:
        return {"message" : "Offer is already acccpeted"}

    if(err):
        return {'err' : err}
    
    print("from route")
    quote =  supp_offers_obj.get_quote()
    print("Printing quote",quote)
    check = msql.update_quote(offer_id,quote)
    if(check):
        print(check)
        return {"err" : check}
   
    return {"message" : "Quote Updated"}

@app.route('/services/repairjobs', methods=['GET'])
def s_r_jobs():
    check = msql.get_repair_jobs()
    
    try:
        if check['err']:
            return {'err':check}
    except:
        pass

    return {'result':check}




### Update information for services Organization
@app.route('/services/org/profile/update', methods=['GET'])
@authorizer
def update_servicess_org(claims):
    ### Inputs extracting from token
    org_id = claims['custom:org_id']
    ### input
    req = request.args.to_dict()
    req_org = req.get('services_org','')
    print("PRINTING REQ ORG")
    print(req_org)
    ### garbage collector
    err = {}
    ### class
    key = (req_org.keys())
    ser_org = services_orgs.ser_orgs(req_org)
    ### logic
    ### validating inputs 
    err['services_org_err'] = ser_org.verify_org_data_all()
    
    if err['services_org_err'] == {}:
        del err['services_org_err']
    del_vals = []
    
    if err != {}:
        vals = err['services_org_err']
        for x in req_org.keys():
            for y in vals.keys():
                if x==y:
                    return {"err":err}
                else:
                    del_vals.append(y)
    

    print("printing del_vals")
    
    ### create user in cognito
    verified_data = ser_org.get_org_data_all()
    
    if del_vals != []:    
        del_vals = list(dict.fromkeys(del_vals))
        print(del_vals)
        for x in del_vals:
            if x in verified_data['services_org']:
                del verified_data['services_org'][x]

    print("PRINTING VERFIED DATA")
    print(verified_data)
    ### push data to logistic user db
    check =  msql.update_services_org(verified_data,org_id)
    #MySQL error check
    if check:
        print("CHECK_1")
        print(check)
        return {"err" : check}
    else:
        return {"message" : "Record Updated"}

### Update information for mechanic profile
@app.route('/services/mechanic/profile/update', methods=['GET'])
@authorizer
def update_mechanic(claims):
    ### Inputs extracting from token
    id = claims['sub']
    return id
    ### input
    req = request.args.to_dict()
    req_org = req.get('services_user','')
    print("PRINTING REQ ORG")
    print(req_org)   
    ### garbage collector
    err = {}
    ### class
    key = (req_org.keys())
    ser_users = services_users.services_users(req_org)
    ### logic
    ### validating inputs 
    err['services_users_err'] = ser_users.verify_role_7_data_all()
    
    if err['services_users_err'] == {}:
        del err['services_users_err']
    del_vals = []
    
    if err != {}:
        vals = err['services_users_err']
        for x in req_org.keys():
            for y in vals.keys():
                if x==y:
                    return {"err":err}
                else:
                    del_vals.append(y)
    

    print("printing del_vals")
    
    ### create user in cognito
    verified_data = ser_users.update_role_7_data_all()
    
    if del_vals != []:    
        del_vals = list(dict.fromkeys(del_vals))
        print(del_vals)
        for x in del_vals:
            if x in verified_data['services_user_profile_7']:
                del verified_data['services_user_profile_7'][x]

    print("PRINTING VERFIED DATA")
    print(verified_data['services_user_profile_7'])
    ### push data to logistic user db
    check =  msql.update_mechanic(verified_data,id)
    #MySQL error check
    if check:
        print("CHECK_1")
        print(check)
        return {"err" : check}
    else:
        return {"message" : "Record Updated"}          

### Update information for solo owners services
@app.route('/services/com/profile/update', methods=['GET'])
@authorizer
def update_services_owner(claims):
    ### Inputs extracting from token
    id = claims['sub']
    ### input
    req = request.args.to_dict()
    req_org = req.get('services_user','')
    print("PRINTING REQ ORG")
    print(req_org)
       
    ### garbage collector
    err = {}
    ### class
    key = (req_org.keys())
    ser_users = services_users.services_users(req_org)
    ### logic
    ### validating inputs 
    err['services_users_err'] = ser_users.verify_role_3_7_data_all()
    
    if err['services_users_err'] == {}:
        del err['services_users_err']
    del_vals = []
    
    if err != {}:
        vals = err['services_users_err']
        for x in req_org.keys():
            for y in vals.keys():
                if x==y:
                    return {"err":err}
                else:
                    del_vals.append(y)
    

    print("printing del_vals")
    
    ### create user in cognito
    verified_data = ser_users.update_role_3_data_all()
    
    if del_vals != []:    
        del_vals = list(dict.fromkeys(del_vals))
        print(del_vals)
        for x in del_vals:
            if x in verified_data['services_user_profile_3']:
                del verified_data['services_user_profile_3'][x]

    print("PRINTING VERFIED DATA")
    print(verified_data['services_user_profile_3'])
    ### push data to logistic user db
    check =  msql.update_solo_owner_services(verified_data,id)
    #MySQL error check
    if check:
        print("CHECK_1")
        print(check)
        return {"err" : check}
    else:
        return {"message" : "Record Updated"}        


############################ LOGISTICS

@app.route('/logistics/org/create', methods=['POST','GET'])
def create_org():
    req = request.get_json()
    ### class
    #cognitoObj = cognito_logistics_emp.cognito()
    
    #Required inputs for "logistics_org" sub dictionary     
    #    "org_name"
    #    "country"
    #    "state"
    #    "city"  
    #    "permanent_address"
    #    "zip_code" 
    #   "date_established" 
    #    "contact_num"

    #Required inputs for "logistics_user" sub dictionary
    #    "email"
    #    "f_name"
    #    "l_name"
    #    "permanent_address"
    #    "contact_num"
    #    "state"
    #    "city"
    #   "country"
  

    
    req_org = req.get('logistics_org','')
    req_owner = req.get('logistics_user','')



    if req_org == '' and req_owner == '':
        return {"err":"Both profiles cannot be empty"}


    ## garbage collection
    err = {}




    ### input
    if req_org != '':

        log_org = logistics_orgs.log_orgs(req_org)
        
        err['logistics_org_err'] = log_org.verify_org_data_all()
        print("HERE")
        if err['logistics_org_err'] == {}:
            del err['logistics_org_err']
    


    if req_owner != '' :
        

        log_owner = logistics_users.log_users(req_owner)

        err['logistics_user_err'] = log_owner.verify_role_0_data_all()
        print("HERE")
        if err['logistics_user_err'] == {}:
            del err['logistics_user_err']
    print(log_owner.roles)
    
    if err != {}:
        return {"err":err}
   

    ##cognito
    cognitoObj = cognito_logistics_org.cognito()
    cog_data = {
        "email"     : req_owner.get('email',""),
        "password"  : req_owner.get('password',""),
        "roles"     : log_owner.roles,
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : ""  
        }
    
    err,result = cognitoObj.sign_up(cog_data)
    if(err):
        return err

    print (result,err,result['UserSub'])
    owner_id =  result['UserSub']

    ##cognito



    #Getting and Inserting  org_id and owner_id
    #assuming owner_id for now

    #owner_id = '11-22-33-444424444'
    print(log_org.insert_owner_id(owner_id))
    print(log_owner.insert_user_id(owner_id))
    
    #print("\n",log_owner.get_role_0_data_all(),'\n')
    check =  msql.create_org(log_org.get_org_data_all(),log_owner.get_role_0_data_all())
    print(check)

    #MySQL error check
    if check.get('err',"") != "":
        #adding org_id in cognito and setting status to success
        return {'error':check.get('err',"")}
    
    print(check['org_id'])
    cog_data['org_id'] = check['org_id']
    err,result = cognitoObj.update_user_logstics_status_org_id(cog_data)
    print(err,result)
    return {"message":"record created"}

#.Register driver operated company #signup
@app.route('/logistics/com/create', methods=['POST','GET'])
def driver_company():
    ### input
    req = request.get_json()
    req_owner = req.get('logistics_user','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_logistics_org.cognito()
    log_driver = logistics_users.log_users(req_owner)
    ### logic
    ### validating inputs 
    err['logistics_user_err'] = log_driver.verify_role_2_6_data_all()
    
    if err['logistics_user_err'] == {}:
        del err['logistics_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : req_owner.get('email',""),
        "password"  : req_owner.get('password',""),
        "roles"     : "2,6",
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : "None"  
        }
        err,result = cognitoObj.sign_up(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = log_driver.get_role_2_6_data_all(id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            insert_to = "logistics_user"
            check =  msql.reg_driver_company(verified_data,insert_to)
            #MySQL error check
            if check:
                err,result = cognitoObj.delete_user(cog_data)
                return {"err" : check}
            else:
                ### inserting data to logistics_users_profiles with role 2
                insert_to = "logistics_user_profile_2"
                check =  msql.reg_driver_company(verified_data,insert_to)
                if check:
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"err" : check}
                else:
                    ### inserting data to logistics_users_profiles with role 6
                    insert_to = "logistics_user_profile_6"
                    check =  msql.reg_driver_company(verified_data,insert_to)
                    if check:
                        ### settting status in cognito to 1
                        err,result = cognitoObj.update_user(cog_data)
                        return {"err" : check}
                    else:
                        return {"message" : "Success"}

@app.route('/logistics/driver/create', methods=['POST','GET'])
@authorizer_logistics
def create_driver(claims):
    req = request.get_json()

    #Required inputs for route
    #    "email"
    #    "f_name"
    #    "l_name" 
    #    "permanent_address"
    #    "contact_num"
    #    "state"
    #    "city"
    #    "country"
    #    "dot_num"
    #    "license_number"

    try:
        org_id = claims['custom:org_id']
        
    except:
        return {'err':"User is not owner"}

    

    ### class
    cognitoObj = cognito_logistics_org.cognito()


    if req == '' or req == {} or req == None:
        return {"err":"Drivers record cannot be empty"}
    print(req,'\n')
    driv = req.get('logistics_user','')

    ## garbage collection
    err = {}

    log_user_drv = logistics_users.log_users(driv)

    err['logistics_user_err'] = log_user_drv.verify_role_6_data_all()
    print("HERE")
    if err['logistics_user_err'] == {}:
        del err['logistics_user_err']


    
    if err != {}:
        return {"err":err}


    #assuming org_id
    #org_id = '15'
    #drv_id = 'e97517ac-cb72-4c58-84aa-9e09acef384b'

    cog_data = {
        "email"     : driv.get('email',""),
        "password"  : driv.get('password',""),
        "roles"     : "6",
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : org_id
        }
    err,result = cognitoObj.create_user(cog_data)
    if(err):
        return {"err":err}

    else:
        ### create user in cognito
        err,result = cognitoObj.get_user(cog_data)
        drv_id =  result['UserAttributes'][0]['Value']
        log_user_drv.insert_org_id(org_id)
        log_user_drv.insert_user_id(drv_id)
        data = log_user_drv.get_role_6_data_all(drv_id)
        check  =  msql.add_org_driver(data)
        #MySQL error check
        if check:
            print("CHECK_1")
            print(check)
            err,result = cognitoObj.delete_user(cog_data)
            return {"message" : check}
        else:
           
            return {"user_id" : drv_id}

    #log_user_drv.insert_org_id(org_id)
    #log_user_drv.insert_user_id(drv_id)
    #print(log_user_drv.get_role_6_data_all(drv_id))
    #check  =  msql.add_org_driver(log_user_drv.get_role_6_data_all(drv_id))
    

    #print(check)

    #MySQL error check
    #if check:
    #    return {'err':check}


    #return {"message":"record created"}

@app.route('/logistics/employee/rep/create', methods=['POST'])
@authorizer_logistics
def logistics_create_user(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}
    ### input
    req = request.get_json()
    req_owner = req.get('logistics_user','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_logistics_org.cognito()
    log_driver = logistics_users.log_users(req_owner)
    ### logic
    ### validating inputs 
    ### Declaring role

    err['logistics_user_err'] = log_driver.verify_employee_rep_data_all()
    
    if err['logistics_user_err'] == {}:
        del err['logistics_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : req_owner.get('email',""),
        "password"  : req_owner.get('password',""),
        "roles"     : '6',
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : org_id  
        }
        err,result = cognitoObj.create_user(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = log_driver.emp_data(id,org_id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            insert_to = "logistics_user"
            check =  msql.create_emp(verified_data,insert_to)
            #MySQL error check
            if check:
                err,result = cognitoObj.delete_user(cog_data)
                return {"err" : check}
            else:
                ### inserting data to logistics_users_profiles with role 2
                insert_to = "logistics_user_profile_5"
                check =  msql.create_emp(verified_data,insert_to)
                if check:
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"err" : check}
               
                return {"message" : "Success"}

@app.route('/logistics/support_tickets/services', methods=['GET'])
#@authorizer_trx
def find_mechanics_log():#claims
    #role = claims['custom:roles']

    req         = request.args.to_dict()
    
    try:
        s_ticket = req.get('supp_id',None)
    except:
        s_ticket = None

    try:
        t_ticket = req.get('trip_id',None)
    except:
        t_ticket = None

    if s_ticket == None and t_ticket == None:
        return {'err':"Both supp_id and trip_id cannot be empty"}


    check = msql.get_4_prec_hash(s_ticket,t_ticket)
    print(check)

    return check



#Within the same route for create support ticket, create a chat room as well for that support ticket
@app.route('/logistics/support_ticket', methods=['PUT'])
@authorizer_logistics
def l_supp_ticker(claims):

    org_id = claims.get('custom:org_id',None)
    print(org_id)

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}

    req = request.form



    #inserting image record in req obj

    try:
        #Holding image object for later use.
        image = request.files['img_record_before']
    except Exception as e:
        image = None
        print('IMG NOT FOUND',e)


    #req = request.get_json()
    print(req,'\n')

    if req == '' or req == {} or req == None:
        return {"err":"Empty record sent"}




    suppObj = support_tickets.supp_tickets(req)



    if org_id != None:
        suppObj.logistics_org_id = org_id #set org_id
        suppObj.img_record_before = image



        err  = suppObj.verify_org_ticket_all()
        print(err)
        if err:
            return {"err":err}
        
        
        
        

        check = msql.register_support_event(suppObj.get_profile_org_ticket_all())


        if check.get('err',None):
            return {'err':check}

        #If no errors we can get the supp_id from check dict
        #merging the supp_id with img_record_before key
        suppObj.img_record_before = suppObj.img_record_before + str(check['supp_id']) + '/before'

        print(suppObj.img_record_before)

        s3 = trx_s3_class.s3_file(image,suppObj.img_record_before)
        print(s3.put_img_before())

        print('S# KEY',msql.update_img_before({"supp_id":check['supp_id'],"img_record_before":suppObj.img_record_before}))
        #########################

        print('STARTING FROM HERE')
        rep_id = req.get('logistics_rep_id',None)
        
        supp_id = check['supp_id']

        ## gettimg trip_id
        err,trip_id =  msql.get_trip_id(supp_id)
        if(err):
            return {'err':err}
        trip_id = trip_id['trip_id']
        ## getting driver id
        err1,driver_id =  msql.get_driver_id_from_trip_id(trip_id)
        if(err1):
            return {'err':err1}
        driver_id = driver_id['driver_id']      
        ## getting driver_name
        err2,log_user_data =  msql.get_logistics_users(driver_id)
        if(err2):
            return {'err':err2}
        driver_name = log_user_data['f_name']
        
        err3,log_user_data1 =  msql.get_logistics_users(rep_id)
        if(err3):
            return {'err':err3}
        rep_name = log_user_data1['f_name']
        print("Printing supp_id")

        route = "chat"
		
        payload = {
            "username" : driver_name,
            "room" : supp_id
        }

        print(type(payload))
        chatObj = chat_service.chat()
        result = chatObj.post_call(payload,route)
        # donot change it to {"result" : result}  as we are rendering template
        return result
        
            
    
    else:
        err  = suppObj.verify_com_data_all()

        print(err)
        if err:
            return {"err":err}

    #check = msql.get_repair_jobs()
    
    try:
        if check['err']:
            return {'err':check}
    except:
        pass

    return {'result':check}

##Logistics company, Trx join the support ticket for appropriate roles
@app.route('/logistics/support_tickets', methods=['GET'])
@authorizer_logistics
def suppoooort_tickets(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    check = msql.get_support_tickets(org_id)
    
    try:
        if check['err']:
            return {'err':check}
    except:
        pass

    return {'result':check}




@app.route('/logistics/add/representative/', methods=['POST'])
@authorizer_logistics
def log_add_rep(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}
    ## Input
    req             = request.get_json()
    supp_id         = req.get('supp_id')
    rep_id          = req.get('rep_id')
   
    
    err,data =  msql.get_supp_id(supp_id)
    print("Printing Data")
    print(data)
    if(err):
        return {"err":err}

    
    if data['status'] == 1:
        return {"message" : "Support ticket Already assigned to representative"}    
    print("PRINTING DATA")
    print(data)    
    check =  msql.add_rep(supp_id,rep_id)
    if(check):
        return {"meesage": "failed"}
    status = 1
    check = msql.update_supp_ticket_status(supp_id,status)
    if(check):
        print(check)
        return {"err" :check}

    return {"message":"Representative added Successfully"}

@app.route('/logistics/replace/representative/', methods=['POST'])
@authorizer_logistics
def log_replace_rep(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}
    ## Input
    req             = request.get_json()
    supp_id         = req.get('supp_id')
    rep_id          = req.get('rep_id')
   
    
    err,data =  msql.get_supp_id(supp_id)
    print("Printing Data")
    print(data)
    if(err):
        return {"err":err}

    
    print("PRINTING DATA")
    print(data)    
    check =  msql.add_rep(supp_id,rep_id)
    if(check):
        return {"meesage": "failed"}
    status = 1
    check = msql.update_supp_ticket_status(supp_id,status)
    if(check):
        print(check)
        return {"err" :check}

    return {"message":"Representative replaced Successfully"}


@app.route('/logistics/remove/representative/', methods=['POST'])
@authorizer_logistics
def log_remove_rep(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}
    ## Input
    req             = request.get_json()
    supp_id         = req.get('supp_id')
    rep_id = None
   
    
    err,data =  msql.get_supp_id(supp_id)
    print("Printing Data")
    print(data)
    if(err):
        return {"err":err}

    if data['status'] == 0:
        return {"message" : "Support ticket Not assigned to anyone"}    
    
    print("PRINTING DATA")
    print(data)    
    check =  msql.add_rep(supp_id,rep_id)
    if(check):
        return {"meesage": "Removed Successfully"}
    status = 0
    check = msql.update_supp_ticket_status(supp_id,status)
    if(check):
        print(check)
        return {"err" :check}

    return {"message":"Representative removed Successfully"}    



    

## get support ticket offers by logistics
@app.route('/logistics/support_tickets_offers/', methods=['GET'])
@authorizer_logistics
def get_support_ticket_offers(claims):
    ##Input
    req             = request.get_json()
    supp_id         = req.get('supp_id')

    err,data = msql.get_support_ticket_offers_all(supp_id)
    
    if(err):
        return err
    return {'result':data}




##Create route to accept support_ticket_offers
@app.route('/logistics/support_tickets_offers/accept', methods=['POST'])
@authorizer_logistics
def supp_offers_accept(claims):
    ### from claims take the org_id and id of the owner adding employeee
    #org_id = claims['custom:org_id']
    ### INPUT

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}

    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    try:
        roles = claims['custom:Role']
        print("roles",roles)
    except:
        return {'err':"Error roles is not found in user"}

    if roles != "2,6" and roles != "0":
        return {"Message" : "Invalid previligies to accept offers"}

    req = request.get_json()

    offer_id       = req.get('offer_id')
    status = 1
   
    ## checking if the support ticket offer is already accepted 
    err1,support_tickets_offers_data =  msql.get_support_ticket_offers_chat(offer_id)
    if(err1):
        return {'err':err1}
    
    
    if support_tickets_offers_data['status'] == 1:
        return {"err" : "offer is already acccpeted"}

    ## extracting the support ticket id form the offer_id    
    supp_id = support_tickets_offers_data['supp_id']
    services_user_id = support_tickets_offers_data['mechanics_user_id']

    ## checking if the support ticket offer is already accepted
    print("From Route already accepted")
    print(supp_id) 
    err,data =  msql.get_supp_id(supp_id)
    if(err):
        return {"err":err}
    print(data)
    if data['offer_id'] != None :
        return {"message" : "Offer Already accepted for this support ticket"}

    check = msql.update_supp_ticket_offer_id(offer_id,supp_id)
    if(check):
        ("printing Check")
        print(check)
        return {"err" :check}

    check = msql.update_supp_ticket_offers_status(offer_id,status,services_user_id)
    if(check):
        print(check)
        return {"err" :check}
    
    return {"message" : "Offer Accepted"}

##Create route to accept support_ticket_offers
@app.route('/logistics/support_tickets/complete', methods=['POST'])
@authorizer_logistics
def supp_ticket_complete(claims):
    ### from claims take the org_id and id of the owner adding employeee
    #org_id = claims['custom:org_id']
    ### INPUT

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}

    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    try:
        roles = claims['custom:Role']
        print("roles",roles)
    except:
        return {'err':"Error roles is not found in user"}

    if roles != "2,6" and roles != "0":
        return {"Message" : "Invalid previligies to accept offers"}

    req = request.get_json()

    supp_id       = req.get('supp_id')
    
   
    ## checking if the support ticket offer is already accepted 
    err1,support_tickets_data =  msql.get_support_ticket(supp_id)
    if(err1):
        return {'err':err1}
    
    
    if support_tickets_data['status'] == 0:
        return {"err" : "No offer is accepted for this support ticket"}

    if support_tickets_data['status'] == 2:
        return {"err" : "This ticket is already Completed"}    

    
    if support_tickets_data['offer_id'] == None :
        return {"message" : "No offer  accepted for this support ticket"}

    
    status = 2
    check = msql.update_supp_ticket_status(supp_id,status)
    if(check):
        print(check)
        return {"err" :check}
    
    return {"message" : "Support ticket successfully mark completed"}

#Create a get route to get the approved mechanic job
# get approved support offer for support ticket
@app.route('/logistics/support_tickets_offers', methods=['GET'])
@authorizer_logistics
def get_job(claims):
    ##INPUT
    req = request.get_json()
    supp_id      = req.get('supp_id')
   
    ## checking if the support ticket offer is already accepted 
    err,data =  msql.get_supp_id(supp_id)
    if(err):
        return {"err":err}
    
    if data['offer_id'] == None or data['offer_id'] == '' or data['offer_id'] == {} :
        return {"message" : "No offer accepted for this support ticket"}

    offer_id = data['offer_id']

    err1,support_tickets_offers_data =  msql.get_support_ticket_offers(offer_id)
    if(err1):
        return {'err':err1}

    print(type(data['offer_id']))
    return {"message" : support_tickets_offers_data}

##Logistics company, Trx join the support ticket for appropriate roles
@app.route('/logistics/support_tickets_offers/location', methods=['POST'])
@authorizer_logistics
def support_tickets_offers_location(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    req = request.get_json()
    offer_id       = req.get('offer_id')

    err,result = msql.get_support_ticket_offers_chat(offer_id)
    
    if(err):
        return err
    mech_org_id = result['mechanics_org_id']
    mech_user_id = result['mechanics_user_id']
    supp_id = result['supp_id']

    print(mech_org_id)
    print(mech_user_id)

    route = "logistics/mech_info"
		
    payload = {
        "mechanics_org_id" : mech_org_id,
        "mechanics_user_id" : mech_user_id,
        "supp_id" : supp_id
    }

    print(type(payload))
    locObj = location_service.location()
    result1 = locObj.post_call(payload,route)
    print(result)
    return result1
    #return {'result':result}

@app.route('/logistics/driver/eta', methods=['POST'])
@authorizer_logistics
def logistics_driver_eta(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    req = request.get_json()
    trip_id       = req.get('trip_id')

    err,result = msql.get_tripss(trip_id)
    coor_start = result['coor_start']
    coor_end = result['coor_end']
    
    
    
    route = "driver/trip/eta"
		
    payload = {
        "coor_start" : coor_start,
        "coor_end" : coor_end,
    }

    print(type(payload))
    locObj = location_service.location()
    result1 = locObj.post_call(payload,route)
    print(result)
    return result1

@app.route('/logistics/mechanic/eta', methods=['POST'])
@authorizer_logistics
def logistics_mechanic_eta(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    req = request.get_json()
    offer_id      = req.get('offer_id')

    err,result = msql.get_support_ticket_offers_chat(offer_id)
    coor_start = result['coor_start']
    coor_end   = result['coor_end']
    print(coor_start)
    #if(err):
    #    return err
    
    route = "mechanic/eta"
		
    payload = {
        "coor_start" : coor_start,
        "coor_end" : coor_end,
    }

    print(type(payload))
    locObj = location_service.location()
    result1 = locObj.post_call(payload,route)
    print(result)
    return result1

@app.route('/logistics/mechanic/location', methods=['POST'])
@authorizer_logistics
def mechanic_location(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    req = request.get_json()
    offer_id       = req.get('offer_id')

    err,result = msql.get_support_ticket_offers_chat(offer_id)
    
    if(err):
        return err
    mech_org_id = result['mechanics_org_id']
    mech_user_id = result['mechanics_user_id']
    supp_id = result['supp_id']

    print(mech_org_id)
    print(mech_user_id)

    route = "logistics/mechanic/liveLoc"
		
    payload = {
        "mechanics_org_id" : mech_org_id,
        "mechanics_user_id" : mech_user_id,
        "supp_id" : supp_id
    }

    print(type(payload))
    locObj = location_service.location()
    result1 = locObj.post_call(payload,route)
    print(result)
    return result1
    #return {'result':result}

@app.route('/logistics/driver/location', methods=['POST'])
@authorizer_logistics
def driver_location(claims):
    try:
        org_id = claims['custom:org_id']
        print("org_id",org_id)
    except:
        return {'err':"Error Organization is not found in user"}

    req = request.get_json()
    trip_id       = req.get('trip_id')

    
    
    
    route = "logistics/driver/liveLoc"
		
    payload = {
        "trip_id" : trip_id,
       
    }

    print(type(payload))
    locObj = location_service.location()
    result1 = locObj.post_call(payload,route)
   
    return result1

##############################################################
@app.route('/logistics/repairjobs', methods=['GET'])
def l_r_jobs():

    check = msql.get_repair_jobs()
    
    try:
        if check['err']:
            return {'err':check}
    except:
        pass

    return {'result':check}



@app.route('/home', methods=['POST','GET'])
def home():
    route = "chat"
    payload = {
        "username" : "Muqaddads",
        "room" : "5717"
    }

    print(type(payload))
    chatObj = chat_service.chat()
    result = chatObj.post_call(payload,route)
   
    return {"Result" : result}     
      
    #return rep_name




@app.route('/logistics/profile', methods=['GET'])
@authorizer_logistics
def get_logistics_org(claims):
    print(claims)

    try:
        user_id = claims['sub']
    except:
        return {"err":"User ID not Found"}
    
    try:
        org_id = claims['custom:org_id']
        print(org_id)
    except:
        return {"err":"Organistaion ID not Found"}
    
    try:
        roles = claims['custom:Role']
    except:
        pass

    req = request.args.to_dict()


    org_rec = msql.get_logistics_org(org_id)

    return {'org_profile':org_rec}






@app.route('/logistics/employee', methods=['GET'])
@authorizer_logistics
def get_logistics_org_emp(claims):
    
    req =request.args.to_dict()

    id = ''
    try:
        org_id = claims['custom:org_id']
        print(org_id)
    except:
        return {"err":"Organistaion ID 'org_id' not Found"}

    try:
        id = req.get('id','')
    except:
        id = ''

    #for all employees if id == ''

    emp_all_rec = msql.get_logistics_org_employee(org_id,id)

    return {'emp_profile':emp_all_rec}










@app.route('/logistics/vehicle/create', methods=['POST','GET'])
@authorizer_logistics
def create_vehicle(claims):
    req = request.get_json()
    #Required inputs for route
    #   "vin"
    #   "type"


    ### class
    #cognitoObj = cognito_logistics_emp.cognito()
    err = {}

    if req == '' or req == {} or req == None:
        return {"err":"Vehicles record cannot be empty"}

    org_id = claims.get('custom:org_id',None)
    print(org_id)

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}

    vobj = vehicles.log_vehicles(req)

    err['vehicle_err'] = vobj.validate_vehicle()

    print(err['vehicle_err'])
    if err['vehicle_err'] == {}:
        del err['vehicle_err']


    ## garbage collection
    if err != {}:
        return {"err":err}


    #MySQL part
    #assuming cognito id
    #user_id = 'Geert' #user adding vehicle
    print(vobj.insert_user_id(user_id))
    vobj.org_id = org_id
    check = msql.add_vehicle(vobj.get_vehicle_profile())
    print(check)

    #MySQL error check
    if check:
        return {'err' : check}

    return {"success":"record created"}



@app.route('/logistics/vehicle', methods=['GET'])
@authorizer_logistics
def get_vehicle(claims):
    req = request.args.to_dict()
    
    try:
        org_id = claims['custom:org_id']
    except:
        org_id  = ''

        
    try:
        vehicle_id = req.get('vehicle_id','')
    except:
        vehicle_id = ''


    try:
        user_id = claims['cognito:username']
    except:
        return {'user_id':"user_id cannot be empty"}


    print(vehicle_id)
    emp_all_rec = msql.get_log_vehicles(org_id,user_id,vehicle_id)

    return {'vehicles':emp_all_rec}










@app.route('/logistics/trip/create', methods=['POST','GET','PUT'])
@authorizer_logistics
def create_trip(claims):
    req = request.get_json()


    ### class
    #cognitoObj = cognito_logistics_emp.cognito()
    
    err = {}

    if req == '' or req == {} or req == None:
        return {"err":"Vehicles record cannot be empty"}

    trpobj = driver_trips.drv_trps(req)

    org_id = claims.get('custom:org_id','')
    print(org_id)

    try:
        user_id = claims['cognito:username']
        print("user_ID",user_id)
    except:
        return {'err':"Error in Authorization. User ID not found"}
        
    #assume cognito org_id and user_id
    #org_id = '18'
    #user_id = '16fa8751-5d8c-464c-9664-9544009696df'

    err['trip_err'] = trpobj.verify_create_trip(org_id,user_id)

       
   
    print(err['trip_err'])
    if err['trip_err'] == {}:
        del err['trip_err']

    if err != {}:
        return {"err":err}

    #print(trpobj.create_trip_profile()['logistics_org_id'],type(trpobj.create_trip_profile()['logistics_org_id']))
    
    check = msql.create_trip(trpobj.create_trip_profile())
    print(check)

    if check:
        return check

    return {"message":"trip created"}

  


#DRIVER-Create and register driver account
@app.route('/driver/create', methods=['POST','GET'])
def driver_com():
    ### input
    req = request.get_json()
    req_owner = req.get('logistics_user','')

    
    ### garbage collector
    err = {}
    ### class
    cognitoObj = cognito_logistics_org.cognito()
    log_driver = logistics_users.log_users(req_owner)
    ### logic
    ### validating inputs 
    err['logistics_user_err'] = log_driver.verify_role_6_data_all()
    
    if err['logistics_user_err'] == {}:
        del err['logistics_user_err']

    if err != {}:
        return {"err":err}
     
    else:
        cog_data = {
        "email"     : req_owner.get('email',""),
        "password"  : req_owner.get('password',""),
        "roles"     : "6",
        "status0"   : "0",
        "status1"   : "1",
        "org_id"    : "none"
        }
        err,result = cognitoObj.sign_up(cog_data)
        if(err):
            return {"err":err}
        else:
            ### create user in cognito
            err,result = cognitoObj.get_user(cog_data)
            id =  result['UserAttributes'][0]['Value']
            verified_data = log_driver.get_role_6_data_all(id)
            print("PRINTING VERFIED DATA")
            print(verified_data)
            ### push data to logistic user db
            insert_to = "logistics_user"
            check =  msql.reg_driver_solo(verified_data,insert_to)
            #MySQL error check
            if check:
                err,result = cognitoObj.delete_user(cog_data)
                return {"message" : check}
            else:
                ### inserting data to logistics_users_profiles with role 2
                insert_to = "logistics_user_profile_6"
                check =  msql.reg_driver_solo(verified_data,insert_to)
                if check:
                    ### settting status in cognito to 1
                    err,result = cognitoObj.update_user(cog_data)
                    return {"message" : check}
                else:        
                    return {"message" : "Record Created"}


### Associate Driver                    
@app.route('/logistics/driver/associate', methods=['GET'])
def associate_driver():
    ### from claims take the org_id and id of the owner adding employeee
    
    ### input
    req = request.get_json()

    
    
    ### id of driver  
    id = "60a3b526-7330-49ad-94b9-d376a3e553f5"
    ### org id of the owner from token
    org_id = "1"
    ### garbage collector
    
    ### class
    
    ### logic
    ### checking drivers attributes
    err,log_user_data =  msql.get_logistics_users(id)
    if(err):
        return {"err":err}
    err,log_user_profile_data =  msql.get_logistics_users_profiles(id)
    if(err):     
        return {"err":err}
    print("PRINTING DATA")
    print("printing user data")
    print(log_user_data)
    print("printing log_user")
    print(log_user_profile_data)

   

    if log_user_profile_data['role'] != '6':
        return {"message" : "User in not a driver"}

        

    if log_user_data['org_id'] != None:
        print("Printing org id")
        print(log_user_data['org_id'])
        return {"message" : "driver is already associated with orgnaization"}

    

    if log_user_profile_data['contact_num'] == '' or log_user_profile_data['contact_num'] == {} or log_user_profile_data['contact_num'] == None:
        return {"message" : "driver phone number does not exist"}

    
    
    check =  msql.associate_driver(id,org_id)
    if(check):
        return {'err':check}
    
  
    return {"message" : "Record Created"}

### Update information for Logistics Organization
@app.route('/logistics/org/profile/update', methods=['GET'])
@authorizer
def update_logistics_org(claims):
    ### Inputs extracting from token
    org_id = claims['custom:org_id']
    ### input
    req = request.get_json()
    req_org = req.get('logistics_org','')
    print("PRINTING REQ ORG")
    print(req_org)
    
    
    ### garbage collector
    err = {}
    ### class
    key = (req_org.keys())
    log_org = logistics_orgs.log_orgs(req_org)
    ### logic
    ### validating inputs 
    err['logistics_org_err'] = log_org.verify_org_data_all()
    
    if err['logistics_org_err'] == {}:
        del err['logistics_org_err']
    del_vals = []
    
    if err != {}:
        vals = err['logistics_org_err']
        for x in req_org.keys():
            for y in vals.keys():
                if x==y:
                    return {"err":err}
                else:
                    del_vals.append(y)
    

    print("printing del_vals")
    
    ### create user in cognito
    verified_data = log_org.get_org_data_all()
    
    if del_vals != []:    
        del_vals = list(dict.fromkeys(del_vals))
        print(del_vals)
        for x in del_vals:
            if x in verified_data['logistics_org']:
                del verified_data['logistics_org'][x]

    print("PRINTING VERFIED DATA")
    print(verified_data)
    ### push data to logistic user db
    check =  msql.update_logistics_org(verified_data,org_id)
    #MySQL error check
    if check:
        print("CHECK_1")
        print(check)
        return {"err" : check}
    else:
        return {"message" : "Record Updated"}


 

   

### Update information for driver profile
@app.route('/logistics/driver/update/profile', methods=['POST'])
@authorizer_logistics
def update_driver(claims):
    ### Inputs extracting from token
    id = claims['sub']
    ### input
    req = request.get_json()
    req_org = req.get('logistics_user','')
    print("PRINTING REQ ORG")
    print(req_org)
       
    ### garbage collector
    err = {}
    ### class
    key = (req_org.keys())
    log_users = logistics_users.log_users(req_org)
    ### logic
    ### validating inputs 
    err['logistics_users_err'] = log_users.verify_role_6_data_all()
    
    if err['logistics_users_err'] == {}:
        del err['logistics_users_err']
    del_vals = []
    
    if err != {}:
        vals = err['logistics_users_err']
        for x in req_org.keys():
            for y in vals.keys():
                if x==y:
                    return {"err":err}
                else:
                    del_vals.append(y)
    

    print("printing del_vals")
    
    ### create user in cognito
    verified_data = log_users.update_role_6_data_all()
    
    if del_vals != []:    
        del_vals = list(dict.fromkeys(del_vals))
        print(del_vals)
        for x in del_vals:
            if x in verified_data['logistics_user_profile_6']:
                del verified_data['logistics_user_profile_6'][x]

    print("PRINTING VERFIED DATA")
    print(verified_data['logistics_user_profile_6'])
    ### push data to logistic user db
    check =  msql.update_driver(verified_data,id)
    #MySQL error check
    if check:
        print("CHECK_1")
        print(check)
        return {"err" : check}
    else:
        return {"message" : "Record Updated"}  





### Update information for solo owner logistics
@app.route('/logistics/com/profile/update', methods=['POST'])
@authorizer
def update_logistics_owner(claims):
    ### Inputs extracting from token
    id = claims['sub']
    ### input
    req = request.get_json()
    req_org = req.get('logistics_user','')
    print("PRINTING REQ ORG")
    print(req_org)
       
    ### garbage collector
    err = {}
    ### class
    key = (req_org.keys())
    log_users = logistics_users.log_users(req_org)
    ### logic
    ### validating inputs 
    err['logistics_users_err'] = log_users.verify_role_6_data_all()
    
    if err['logistics_users_err'] == {}:
        del err['logistics_users_err']
    del_vals = []
    
    if err != {}:
        vals = err['logistics_users_err']
        for x in req_org.keys():
            for y in vals.keys():
                if x==y:
                    return {"err":err}
                else:
                    del_vals.append(y)
    

    print("printing del_vals")
    
    ### create user in cognito
    verified_data = log_users.update_role_6_data_all()
    
    if del_vals != []:    
        del_vals = list(dict.fromkeys(del_vals))
        print(del_vals)
        for x in del_vals:
            if x in verified_data['logistics_user_profile_6']:
                del verified_data['logistics_user_profile_6'][x]

    print("PRINTING VERFIED DATA")
    print(verified_data['logistics_user_profile_6'])
    ### push data to logistic user db
    check =  msql.update_driver(verified_data,id)
    #MySQL error check
    if check:
        print("CHECK_1")
        print(check)
        return {"err" : check}
    else:
        return {"message" : "Record Updated"}     


@app.route('/trx/user/list_filter', methods=['GET'])
@authorizer_trx
def get_trx_users_filter_by_role(claims):
    
    roles = request.args.get("roles")
    err,result =  msql.get_trx_users_filter_by_role(roles)
    if(err):
        return err
    else:
        return {"result":result}

@app.route('/logistics/user/list_filter', methods=['GET'])
@authorizer_logistics
def get_logistic_users_filter_by_role(claims):
    user_id = claims['sub']
    org_id = claims['custom:org_id']
    print("id Is : ",user_id,"org_id:",org_id)
    roles = request.args.get("roles")
    print(roles)
    err,result =  msql.get_logistic_users_filter_by_role(roles, org_id)
    if(err):
        return err
    else:
        return {"result":result}

@app.route('/service/user/list_filter', methods=['GET'])
@authorizer
def get_service_users_filter_by_role(claims):
    user_id = claims['sub']
    org_id = claims['custom:org_id']
    print("id Is : ",user_id,"org_id:",org_id)
    roles = request.args.get("roles")
    print(roles)
    err,result =  msql.get_service_users_filter_by_role(roles,org_id)
    if(err):
        return err
    else:
        return {"result":result}

@app.route('/trx/bydriver/trip', methods=['GET'])
@authorizer_trx
def list_trip_by_driver_id(claims):
    
    driver_id = str(request.args.get("driver_id")) 
    print(driver_id) 
    err,result =  msql.get_trip_by_driver_id(driver_id)
    if(err):
        return err
    else:
        return {"result":result}
  

@app.route('/logistics/tickets/mechanic', methods=['GET'])
@authorizer_logistics
def list_support_ticket_for_machenics_logistics(claims):
    
    supp_id = str(request.args.get("supp_id")) 
    print(supp_id) 
    err,result =  msql.list_support_ticket_for_machenics_logistics(supp_id)
    if(err):
        return err
    else:
        return {"result":result}


@app.route('/trx/tickets/mechanic', methods=['GET'])
@authorizer_trx
def list_support_ticket_for_machenics_trx(claims):
 
    supp_id = str(request.args.get("supp_id")) 
    print(supp_id) 
    err,result =  msql.list_support_ticket_for_machenics_trx(supp_id)
    if(err):
        return err
    else:
        return {"result":result}


@app.route('/logistics/vehicle/update', methods=['POST'])
@authorizer_logistics
def update_vehicle(claims):
    user_id = claims['sub']
    org_id = claims['custom:org_id']
    print("id Is : ",user_id,"org_id:",org_id)
    req = request.get_json()

    try:
        vehicle_id = req.get('vehicle_id','')
        vin = req.get('vin','')
        org_id = org_id
        user_id = user_id
        type = req.get('type','')
        status = req.get('status','')
    except Exception as e:
        print(e)
        return {'err':"email was not sent."}
    print({"vehicle_id":vehicle_id, 'vin':vin,"type":type,"status":status, "org_id":org_id, "user_id":user_id})
    err,result =  msql.update_vehicle(vin,type,status,vehicle_id, org_id, user_id)

    if(err):
        return err
    else:
        return {"result":result}
    

# Endpoint for deleting a vehicle
@app.route("/logistics/vehicle/delete", methods=["GET"])
@authorizer_logistics
def delete_vehicle(claims):
    user_id = claims['sub']
    org_id = claims['custom:org_id']
    print("id Is : ",user_id,"org_id:",org_id)
    vehicle_id = request.args.get("vehicle_id")
    print(vehicle_id) 
    err,result =  msql.delete_vehicle1(vehicle_id,user_id, org_id)

    if(err):
        return err
    else:
        return {'msg':'Vehicle Deleted Successfully',"result":result}
    # return {'msg':'Vehicle Deleted Successfully', "vehicles":'vehicle1'}           

@app.route("/trx/user/delete", methods=["GET"])
@authorizer_trx
def delete_trx_user(claims):
    id = request.args.get("id")
    print(id) 
    err,result =  msql.delete_trx_user1(id)
    if(err):
        return err
    else:
        return {'msg':'TRx user Deleted Successfully',"result":result}
    # return {'msg':'Vehicle Deleted Successfully', "vehicles":'vehicle1'}


@app.route("/service/user/delete", methods=["GET"])
@authorizer
def delete_service_user(claims):
    user_id = claims['sub']
    org_id = claims['custom:org_id']
    print(user_id, org_id)
    id = request.args.get("id")
    print(id) 
    err,result =  msql.delete_service_user(id, org_id)
    if(err):
        return err
    else:
        return {'msg':'Service user Deleted Successfully',"result":result}
    # return {'msg':'Vehicle Deleted Successfully', "vehicles":'vehicle1'}


@app.route("/logistics/user/delete", methods=["GET"])
@authorizer_logistics
def delete_logistics_user(claims):
    user_id = claims['sub']
    org_id = claims['custom:org_id']
    print(user_id, org_id)
    id = request.args.get("id")
    print(id) 
    err,result =  msql.delete_logistics_user(id, org_id)
    if(err):
        return err
    else:
        return {'msg':'Logistics user Deleted Successfully',"result":result}
    # return {'msg':'Vehicle Deleted Successfully', "vehicles":'vehicle1'}



region = 'us-east-2'
userpool_id = 'us-east-2_f7JPaMI34'
app_client_id = '7q98kt3cpckaths14pngr9q3a3'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)
# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/





def lambda_handler(event, context):
    with urllib.request.urlopen(keys_url) as f:
        response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']
    
    token = event['token']
    # get the kid from the headers prior to verification
    if(err):
        return err
    else:
        return result




if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 1024,debug = True)



         
