import boto3
import urllib.parse
from urllib.parse import urlencode
import jwt
import requests
import json
import traceback
import logging
import botocore
######## For token validation
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
########
class   cognito():
    def __init__(self):
        # Setiing up class Variables
        self.region = "us-east-2"
        self.userpool_id = "us-east-2_cDL9M7MEt"
        self.app_client_id = '4npctkncia31lbimkoa4hejph2'
        self.keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(self.region,self.userpool_id)
        self.url_get_tokens = 'https://trucking-organization.auth.us-east-2.amazoncognito.com/oauth2/token'
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.code ="71212147-5fcf-48f0-9130-035ef458f1f2"
        
    def validate_token(self,token):
        ######################
        try:
            context = None
            event = {'token': token}
            with urllib.request.urlopen(self.keys_url) as f:
                response = f.read()
            keys = json.loads(response.decode('utf-8'))['keys']
            #######################
            token = event['token']
            # get the kid from the headers prior to verification
            headers = jwt.get_unverified_headers(token)
            kid = headers['kid']
            # search for the kid in the downloaded public keys
            key_index = -1
            for i in range(len(keys)):
                if kid == keys[i]['kid']:
                    key_index = i
                    break
            if key_index == -1:
                print('Public key not found in jwks.json')
                return {"message":"Public key not found in jwks.json"},{}
            # construct the public key
            public_key = jwk.construct(keys[key_index])
            # get the last two sections of the token,
            # message and signature (encoded in base64)
            message, encoded_signature = str(token).rsplit('.', 1)
            # decode the signature
            decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
            # verify the signature
            if not public_key.verify(message.encode("utf8"), decoded_signature):
                print('Signature verification failed')
                return {"message":"Signature verification failed"},{}
            print('Signature successfully verified')
            # since we passed the verification, we can now safely
            # use the unverified claims
            claims = jwt.get_unverified_claims(token)
            # additionally we can verify the token expiration
            if time.time() > claims['exp']:
                print('Token is expired')
                return {"message":"Token Expired"},{}
            # and the Audience  (use claims['client_id'] if verifying an access token)
            if claims['aud'] != self.app_client_id:
                print('Token was not issued for this audience')
                return {"Token was not issued for this audience"},{}
            # now we can use the claims
            print(claims)
            return {},claims
        except:
            return {"Message": "Invalid Token"},{}     

    

    def get_client(self):
        try:
            client = boto3.client('cognito-idp',
                region_name= self.region,
                aws_access_key_id='AKIAUJBUUPBZ6BRJIPFB',
                aws_secret_access_key= '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')
            print("Printing Client")    
            print(client)
            return {},client
        except:
            print("from except")
            return {"Message" : "Client Error"},{}

    def sign_up(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:
            print("PRINTIND DATA FOR COG")  
            print(data)
            response = client.sign_up(
                ClientId=   self.app_client_id,
                Username=   data['email'],
                Password=   data['password'],
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': data['email']
                    },
                    {
                        'Name': 'custom:Role',
                        'Value': data['roles']
                    },
                    {
                        'Name': 'custom:Status',
                        'Value': data['status0']
                    },
                    {
                        'Name': 'custom:org_id',
                        'Value': data['org_id']
                    },
                ] 
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "UnexpectedLambdaException","UserLambdaValidationException",
                            "NotAuthorizedException","InvalidPasswordException",
                            "InvalidLambdaResponseException","UserLambdaValidationException",
                            "InvalidLambdaResponseException","UsernameExistsException",
                            "InvalidSmsRoleAccessPolicyException","InvalidSmsRoleTrustRelationshipException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UnsupportedUserStateException","InternalErrorException",
                            "CodeDeliveryFailureException"
                            ]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}          
    def confirm_signup(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:
            response = client.confirm_sign_up(
                ClientId        = self.app_client_id,
                Username        = data['email'],
                ConfirmationCode= data['confirmation_code']
                )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "UnexpectedLambdaException","UserLambdaValidationException",
                            "NotAuthorizedException","InvalidPasswordException",
                            "InvalidLambdaResponseException","UserLambdaValidationException",
                            "InvalidLambdaResponseException","UsernameExistsException",
                            "InvalidSmsRoleAccessPolicyException","InvalidSmsRoleTrustRelationshipException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UnsupportedUserStateException","InternalErrorException",
                            "CodeDeliveryFailureException","CodeMismatchException",
                            "ExpiredCodeException"
                            ]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}

    def login(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.initiate_auth(
                ClientId        =   self.app_client_id,
                AuthFlow        =   'USER_PASSWORD_AUTH',
                AuthParameters  ={
                    'USERNAME': data['email'],
                    'PASSWORD': data['password']
                }
            )

            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "InvalidParameterException","GroupExistsException",
                            "ResourceNotFoundException","TooManyRequestsException",
                            "LimitExceededException","NotAuthorizedException",
                            "InternalErrorException","UnexpectedLambdaException",
                            "InvalidUserPoolConfigurationException","UserLambdaValidationException",
                            "InvalidLambdaResponseException","PasswordResetRequiredException",
                            "UserNotFoundException","UserNotConfirmedException",
                            "InternalErrorException","InvalidSmsRoleAccessPolicyException",
                            "InvalidSmsRoleTrustRelationshipException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}


    ### ORG
    def create_organization(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.create_group(
                GroupName=data['org_name'],
                UserPoolId=self.userpool_id,
                Description=data['des_of_org'],
                #RoleArn='123444444444444444444444444444444444',
                #Precedence=123
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "InvalidParameterException","GroupExistsException",
                            "ResourceNotFoundException","TooManyRequestsException",
                            "LimitExceededException","NotAuthorizedException",
                            "InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}

    def update_organization(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.update_group(
                GroupName='Aspire',
                UserPoolId=self.userpool_id,
                Description=data['des_of_org'],
            )
            return {},response
        
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "InternalErrorException","NotAuthorizedException",
                            "InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}
    ## USER
    def create_user(self,data):
        print(data)
        err,client = self.get_client()
        if(err):
            return err,{}
        try:    
            response = client.admin_create_user(
                UserPoolId=self.userpool_id,
                Username=data['email'],
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': data['email']
                    },
                    {
                        'Name': 'custom:Role',
                        'Value': data['roles']
                    },
                    {
                        'Name': 'custom:Status',
                        'Value': data['status0']
                    },
                    {
                        'Name': 'custom:org_id',
                        'Value': data['org_id']
                    },
                    #{
                    #    "Name": "email_verified",
                    #    "Value": "True"
                    #},
                ],
                TemporaryPassword=data['password'],
                #DesiredDeliveryMediums=[
                #    'EMAIL',
                #]
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "UserNotFoundException","UsernameExistsException",
                            "InvalidPasswordException","CodeDeliveryFailureException",
                            "UnexpectedLambdaException","UserLambdaValidationException",
                            "InvalidLambdaResponseException","PreconditionNotMetException",
                            "InvalidSmsRoleAccessPolicyException","InvalidSmsRoleTrustRelationshipException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UnsupportedUserStateException","InternalErrorException"
                            ]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}

    def delete_user(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.admin_delete_user(
                UserPoolId=self.userpool_id,
                Username=data['email'],
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UserNotFoundException","InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}

    def add_user_to_group(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.admin_add_user_to_group(
                UserPoolId = self.userpool_id,
                Username = data['email'],
                GroupName= 'Aspire'
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UserNotFoundException","InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}
    def list_users_in_org(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.list_users_in_group(
                UserPoolId = self.userpool_id,
                GroupName= 'Aspire',
                
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UserNotFoundException","InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}
    def add_role(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.admin_update_user_attributes(
                UserPoolId=self.userpool_id,
                Username= data['email'],
                UserAttributes=[
                    {
                        'Name': 'custom:Role',
                        'Value': '[Approver,Representative]'
                    },
                ]
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UserNotFoundException","InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}
    ###########
    def list_users(self):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.list_users(
                        UserPoolId=self.userpool_id,
                        AttributesToGet=[
                        'email','sub'
                        ] 
                        )
            return {},response
        except:
            return {"Message":"cognito error"},{}     

    def get_user(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:    
            response = client.admin_get_user(
                UserPoolId=self.userpool_id,
                Username= data['email']
            )
            return {},response
        
        except:
            return {"Message":"cognito error"},{} 
     

    def update_user(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.admin_update_user_attributes(
                UserPoolId=self.userpool_id,
                Username= data['email'],
                UserAttributes=[
                    {
                        'Name': 'custom:Status',
                        'Value': data['status1']
                    },
                ]
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UserNotFoundException","InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}

    def update_user_logstics_status_org_id(self,data):
        err,client = self.get_client()
        if(err):
            return err,{}
        try:     
            response = client.admin_update_user_attributes(
                UserPoolId=self.userpool_id,
                Username= data['email'],
                UserAttributes=[
                    {
                        'Name': 'custom:Status',
                        'Value': data['status1']
                    },
                    {
                        'Name': 'custom:org_id',
                        'Value': str(data['org_id'])
                    }
                ]
            )
            return {},response
        except botocore.exceptions.ClientError as e:
            print("here")
            exceptions = [  "ResourceNotFoundException","InvalidParameterException",
                            "TooManyRequestsException","NotAuthorizedException",
                            "UserNotFoundException","InternalErrorException"]
            for ex in exceptions:                
                if e.response['Error']['Code'] == ex:
                    print("HURRY")
                
                    return {"message" : ex},{}



    def get_tokens(self,code):
            # To get payload of user tokens from Azure(Including Id token, refresh token)
            payload = {
                "grant_type": "authorization_code",
                "client_id": "6o9saovjrs3g6b692kg3squ2if",
                "code": code,
                "client_secret": "2ucj7l5r3c7q740l4t6r6i2c5njec2osatk1on8s7j1mhur3n70",
                "redirect_uri" : "https://jwt.ms",
                }
            # Converting payload from python dict to xencoded url    
            payload_Authentication_code=urlencode(payload)
            request = requests.post(self.url_get_tokens, data=payload_Authentication_code, headers=self.headers)
            # Converting the json response from Azure into Python dict
            result = request.content
            try:
                result = json.loads(request.content)
                id_token = result['id_token']
                return id_token 
            except:
                return result    

    def refresh_token(self,refreshtoken):
            # payload to refresh the token
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refreshtoken,
                "valid_for": "60",
                "client_secret": "0k~F.1W~w2.fpWYFO.5A8L4F5~w0A_r~mh",
                }
            # Encoding the payload in XencodedURL     
            payload_refresh_token=urlencode(payload)
            request = requests.post(self.url, data=payload_refresh_token, headers=self.headers)
            # Converting the json response from Azure into Python dict
            result = json.loads(request.content)
            return result

    def password_check(self,passwd):
      
        SpecialSym =['$', '@', '#', '%']
        val = True
        
        if len(passwd) < 6:
            return {'error' : 'length should be at least 6'},{}
            
            
        if len(passwd) > 20:
            return {'error' :'length should be not be greater than 8'},{}
            
            
        if not any(char.isdigit() for char in passwd):
            return {'error' :'Password should have at least one numeral'},{}
            
        if not any(char.isupper() for char in passwd):
            return {'error' :'Password should have at least one uppercase letter'},{}
            
            
        if not any(char.islower() for char in passwd):
            return {'error' :'Password should have at least one lowercase letter'},{}
            
            
        if not any(char in SpecialSym for char in passwd):
            return {'error' :'Password should have at least one of the symbols $@#'},{}
            
        else:
            return {},passwd




#cobj = cognito()
#cobj.delete_user({"email":'ammar@dataconnecxion.com'})
#cobj.delete_user({"email":'ammar@minervarg.com'})
#cobj.delete_user({"email":'gg.lionkhan@gmail.com'})
#cobj.delete_user({"email":'khanammar50@hotmail.com'})
