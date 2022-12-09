import json
import requests



class   chat():
    def __init__(self):
        
        # Setiing up class Variables

        self.id = 'api.trxapp.io/chat'

    
    
    
    def post_call(self,payload,route):
       

        if self.id == "":
            return {"Message":"Cannot reach EC2"}

        url = "http://{}/{}".format(self.id,route)
        print(url)
        headers = {
		'Content-Type' : 'application/json'
        }
        try:
            payload = json.dumps(payload)
            print("From Function")
        
        
            request = requests.post(url,data=payload,headers= headers)
            try:
                result = json.loads(request.content)
                return result
            except Exception as e:
                print("ffrom exception")
                result = request.content
                return result
        except Exception as e:
            print(e)
            return e
    def post_call_2(self,payload):
       

        if self.id == "":
            return {"Message":"Cannot reach EC2"}

        url = "http://{}".format(self.id)
        print(url)
        headers = {
		'Content-Type' : 'application/json'
        }
        try:
            payload = json.dumps(payload)
            print("From Function")
        
        
            request = requests.post(url,data=payload,headers= headers)
            try:
                result = json.loads(request.content)
                return result
            except Exception as e:
                result = request.content
                return result
        except Exception as e:
            print(e)
            return e,url               
        
    def get_call(self,route):
        if self.id == "":
            return {"Message":"Cannot reach EC2"}

        url = "http://{}/{}".format(self.id,route)
        headers = {
		'Content-Type' : 'application/json'
        }
        try:
            request = requests.get(url)
            result = json.loads(request.content)
            return result
        #
        except:
            return {"Message":"Unexpected Error"} 