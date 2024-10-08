import re
from datetime import datetime
import uuid
from pytz import timezone

class supp_tick_offers():

    def __init__(self,req):
        self.supp_id            = None  #NN
        self.offer_id           = None 
        self.mechanic_org_id    = None  #NN
        self.mechanic_user_id   = None     #NN
        self.job_desc           = req.get('job_desc',"")     #NN
        self.coor_start         = None
        self.coor_end           = None
        self.date_created       = None
        self.mechanic_est_time_arrival        = req.get('mechanic_est_time_arrival',"")  #NN
        self.mechanic_est_job_completion_time = req.get('mechanic_est_job_completion_time',"")
        self.sys_job_completion_time          = req.get('sys_job_completion_time',"")
        self.sys_mech_arrival_time            = req.get('sys_mech_arrival_time',"")
        self.quote                            = req.get('quote',"") #NN
        self.status                           = '0'       #NN
        

    def set_date_current(self):

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

    def check_job_descr(self):
        li = []
        
        if len(self.job_desc) > 500:
            li.append('Job description cannot be more than 500 words')

        return li

    def verify_mechanic_est_time_arrival(self):
        li = []

        if self.mechanic_est_time_arrival != "":
            check =  self.check_date_obj(self.mechanic_est_time_arrival)
            if check != "err":
                self.mechanic_est_time_arrival = check
            else:
                li.append('Estimated time should be of format YYYY-MM-DD.')
        else:
            li.append('Estimated time cannot be empty.')

        return li

    def verify_mechanic_est_job_completion_time(self):
        li = []

        if self.mechanic_est_job_completion_time != "":
            check =  self.check_date_obj(self.mechanic_est_job_completion_time)
            if check != "err":
                self.mechanic_est_job_completion_time = check
            else:
                li.append('Estimated time should be of format YYYY-MM-DD.')
        else:
            li.append('Estimated time cannot be empty.')

        return li  

    def verify_sys_job_completion_time(self):
        li = []

        if self.sys_job_completion_time != "":
            check =  self.check_date_obj(self.sys_job_completion_time)
            if check != "err":
                self.sys_job_completion_time = check
            else:
                li.append('Estimated time should be of format YYYY-MM-DD.')
        else:
            li.append('Estimated time cannot be empty.')

        return li

    def verify_sys_mech_arrival_time(self):
        li = []

        if self.sys_mech_arrival_time != "":
            check =  self.check_date_obj(self.sys_mech_arrival_time)
            if check != "err":
                self.sys_mech_arrival_time = check
            else:
                li.append('Estimated time should be of format YYYY-MM-DD.')
        else:
            li.append('Estimated time cannot be empty.')

        return li

    def check_quote(self):
        
        li = []
        
        if len(self.quote) > 100:
            li.append('Job description cannot be more than 100 words')

        return li

    def verify_org_ticket_all(self):
        err_log = {}
        err_log['job_desc']                         = []
        err_log['mechanic_est_time_arrival']        = []
        err_log['mechanic_est_job_completion_time'] = []
        err_log['sys_job_completion_time']          = []
        err_log['sys_mech_arrival_time']            = []
        err_log['quote']                            = []

       
        err_log['job_desc']                         = self.check_job_descr()
        
        err_log['mechanic_est_time_arrival']        = self.verify_mechanic_est_time_arrival()
        
        err_log['mechanic_est_job_completion_time'] = self.verify_mechanic_est_job_completion_time()
                
        err_log['sys_job_completion_time']          = self.verify_sys_job_completion_time()
        
        err_log['sys_mech_arrival_time']            = self.verify_sys_mech_arrival_time()
        
        err_log['quote']                            = self.check_quote()
        




        #check if any error 
        print(err_log)
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)
        print("keys")
        print(keys)
        
        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log

    def verify_quote(self):
        err_log = {}
        
        err_log['quote']  = []
    
        err_log['quote']  = self.check_quote()
    

        #check if any error 
        print(err_log)
        keys= []
        for x in err_log:
            if err_log[x] == []:
                keys.append(x)
        print("keys")
        print(keys)
        
        #deleting empty keys
        for x in keys:
            del err_log[x]

        return err_log

    def get_profile_org_ticket_all(self,supp_id,mechanic_org_id,mechanics_user_id):
        self.date_created = self.set_date_current()
        profile = {
            'supp_id'           : supp_id, 
            'offer_id'          : self.offer_id,
            'mechanic_org_id'   : mechanic_org_id,
            'mechanic_user_id'  : mechanics_user_id,
            'job_desc'          : self.job_desc,
            'coor_start'        : self.coor_start,
            'coor_end'          : self.coor_end,
            'date_created'      : self.date_created,
            'mechanic_est_time_arrival'         : self.mechanic_est_time_arrival,
            'mechanic_est_job_completion_time'  : self.mechanic_est_job_completion_time,
            'sys_job_completion_time'           : self.sys_job_completion_time,
            'sys_mech_arrival_time'             : self.sys_mech_arrival_time,
            'quote'             : self.quote,
            'status'            : self.status,
        }

        return profile


    def get_quote(self):
        self.date_created = self.set_date_current()
        quote = self.quote
        print("Priting from function quote")
        print(quote)

        return quote      

countries = ["USA"]
states = ['Ohio','Texas']

ohio_cities = ['Akron', 'Alliance', 'Stark', 'Amherst', 'Ashland', 'Ashtabula', 'Athens', 'Aurora', 'Avon', 'Avon Lake', 'Barberton', 'Bay Village', 'Beachwood', 'Beavercreek', 'Bedford', 'Bedford Heights', 'Bellbrook', 'Bellefontaine', 'Bellevue', 'Huron', 'Sandusky', 'Belpre', 'Berea', 'Bexley', 'Blue Ash', 'Bowling Green', 'Brecksville', 'Broadview Heights', 'Brooklyn', 'Brook Park', 'Brookville', 'Brunswick', 'Bryan', 'Bucyrus', 'Cambridge', 'Campbell', 'Canal Fulton', 'Canal Winchester', 'Franklin', 'Canfield', 'Canton', 'Celina', 'Centerville', 'Montgomery', 'Chardon', 'Cheviot', 'Chillicothe', 'Cincinnati', 'Circleville', 'Clayton', 'Montgomery', 'Cleveland', 'Cleveland Heights', 'Clyde', 'Columbiana', 'Mahoning', 'Columbus', 'Fairfield', 'Franklin', 'Conneaut', 'Cortland', 'Coshocton', 'Cuyahoga Falls', 'Dayton', 'Deer Park', 'Defiance', 'Delaware', 'Delphos', 'Van Wert', 'Dover', 'Dublin', 'Franklin', 'Union', 'East Cleveland', 'East Liverpool', 'Eastlake', 'Eaton', 'Elyria', 'Englewood', 'Euclid', 'Fairborn', 'Fairfield', 'Fairlawn', 'Fairview Park', 'Findlay', 'Forest Park', 'Fostoria', 'Seneca', 'Wood', 'Franklin', 'Fremont', 'Gahanna', 'Galion', 'Garfield Heights', 'Geneva', 'Germantown', 'Girard', 'Grandview Heights', 'Green', 'Greenville', 'Grove City', 'Groveport', 'Hamilton', 'Harrison', 'Heath', 'Highland Heights', 'Hilliard', 'Hillsboro', 'Hubbard', 'Huber Heights', 'Montgomery', 'Hudson', 'Huron', 'Independence', 'Ironton', 'Jackson', 'Kent', 'Kenton', 'Kettering', 'Montgomery', 'Kirtland', 'Lakewood', 'Lancaster', 'Lebanon', 'Lima', 'Logan', 'London', 'Lorain', 'Louisville', 'Loveland', 'Hamilton', 'Warren', 'Lyndhurst', 'Macedonia', 'Madeira', 'Mansfield', 'Maple Heights', 'Marietta', 'Marion', 'Martins Ferry', 'Marysville', 'Mason', 'Massillon', 'Maumee', 'Mayfield Heights', 'Medina', 'Mentor', 'Mentor-on-the-Lake', 'Miamisburg', 'Middleburg Heights', 'Middletown', 'Milford', 'Monroe', 'Warren', 'Montgomery', 'Moraine', 'Mount Healthy', 'Mount Vernon', 'Munroe Falls', 'Napoleon', 'Nelsonville', 'New Albany', 'Licking', 'New Carlisle', 'New Franklin', 'New Philadelphia', 'Newark', 'Niles', 'North Canton', 'North College Hill', 'North Olmsted', 'North Ridgeville', 'North Royalton', 'Northwood', 'Norton', 'Norwalk', 'Norwood', 'Oakwood', 'Oberlin', 'Olmsted Falls', 'Ontario', 'Oregon', 'Orrville', 'Oxford', 'Painesville', 'Parma', 'Parma Heights', 'Pataskala', 'Pepper Pike', 'Perrysburg', 'Pickerington', 'Franklin', 'Piqua', 'Port Clinton', 'Portsmouth', 'Powell', 'Ravenna', 'Reading', 'Reynoldsburg', 'Franklin', 'Licking', 'Richmond Heights', 'Rittman', 'Riverside', 'Rocky River', 'Rossford', 'Saint Clairsville', 'Saint Marys', 'Salem', 'Sandusky', 'Seven Hills', 'Shaker Heights', 'Sharonville', 'Hamilton', 'Sheffield Lake', 'Shelby', 'Sidney', 'Solon', 'South Euclid', 'Springboro', 'Warren', 'Springdale', 'Springfield', 'Steubenville', 'Stow', 'Streetsboro', 'Strongsville', 'Struthers', 'Sylvania', 'Tallmadge', 'Summit', 'The Village of Indian Hill', 'Tiffin', 'Tipp City', 'Toledo', 'Toronto', 'Trenton', 'Trotwood', 'Troy', 'Twinsburg', 'Uhrichsville', 'Union', 'Montgomery', 'University Heights', 'Upper Arlington', 'Upper Sandusky', 'Urbana', 'Van Wert', 'Vandalia', 'Vermilion', 'Lorain', 'Wadsworth', 'Wapakoneta', 'Warren', 'Warrensville Heights', 'Washington Court House', 'Waterville', 'Wauseon', 'Wellston', 'West Carrollton', 'Westerville', 'Franklin', 'Westlake', 'Whitehall', 'Wickliffe', 'Willard', 'Willoughby', 'Willoughby Hills', 'Willowick', 'Wilmington', 'Wooster', 'Worthington', 'Wyoming', 'Xenia', 'Youngstown', 'Zanesville']
texas_cities = ['Abbott', 'Abernathy', 'Abilene', 'Abram-Perezville', 'Ackerly', 'Addison', 'Adrian', 'Agua Dulce', 'Agua Dulce', 'Airport Road Addition', 'Alamo', 'Alamo Heights', 'Alba', 'Albany', 'Aldine', 'Aledo', 'Alfred-South La Paloma', 'Alice', 'Alice Acres', 'Allen', 'Alma', 'Alpine', 'Alto', 'Alto Bonito', 'Alton', 'Alton North', 'Alvarado', 'Alvin', 'Alvord', 'Amarillo', 'Ames', 'Amherst', 'Anahuac', 'Anderson', 'Anderson Mill', 'Andrews', 'Angleton', 'Angus', 'Anna', 'Annetta', 'Annetta North', 'Annetta South', 'Annona', 'Anson', 'Anthony', 'Anton', 'Appleby', 'Aquilla', 'Aransas Pass', 'Archer City', 'Arcola', 'Argyle', 'Arlington', 'Arp', 'Arroyo Alto', 'Arroyo Colorado Estates', 'Arroyo Gardens-La Tina Ranch', 'Asherton', 'Aspermont', 'Atascocita', 'Athens', 'Atlanta', 'Aubrey', 'Aurora', 'Austin', 'Austwell', 'Avery', 'Avinger', 'Azle', 'Bacliff', 'Bailey', "Bailey's Prairie village", 'Baird', 'Balch Springs', 'Balcones Heights', 'Ballinger', 'Balmorhea', 'Bandera', 'Bangs', 'Bardwell', 'Barrett', 'Barry', 'Barstow', 'Bartlett', 'Barton Creek', 'Bartonville', 'Bastrop', 'Batesville', 'Bausell and Ellis', 'Bay City', 'Bayou Vista', 'Bayside', 'Baytown', 'Bayview', 'Beach City', 'Bear Creek village', 'Beasley', 'Beaumont', 'Beckville', 'Bedford', 'Bee Cave village', 'Beeville', 'Bellaire', 'Bellevue', 'Bellmead', 'Bells', 'Bellville', 'Belton', 'Benavides', 'Benbrook', 'Benjamin', 'Berryville', 'Bertram', 'Beverly Hills', 'Bevil Oaks', 'Bigfoot', 'Big Lake', 'Big Sandy', 'Big Spring', 'Big Wells', 'Bishop', 'Bishop Hills', 'Bixby', 'Blackwell', 'Blanco', 'Blanket', 'Blessing', 'Bloomburg', 'Blooming Grove', 'Bloomington', 'Blossom', 'Blue Berry Hill', 'Blue Mound', 'Blue Ridge', 'Bluetown-Iglesia Antigua', 'Blum', 'Boerne', 'Bogata', 'Boling-Iago', 'Bolivar Peninsula', 'Bonham', 'Bonney village', 'Booker', 'Borger', 'Botines', 'Bovina', 'Bowie', 'Box Canyon-Amistad', 'Boyd', 'Brackettville', 'Brady', 'Brazoria', 'Breckenridge', 'Bremond', 'Brenham', 'Briar', 'Briarcliff village', 'Briaroaks', 'Bridge City', 'Bridgeport', 'Broaddus', 'Bronte', 'Brookshire', 'Brookside Village', 'Browndell', 'Brownfield', 'Brownsboro', 'Brownsville', 'Brownwood', 'Bruceville-Eddy', 'Brundage', 'Bruni', 'Brushy Creek', 'Bryan', 'Bryson', 'Buchanan Dam', 'Buckholts', 'Buda', 'Buffalo', 'Buffalo Gap', 'Buffalo Springs village', 'Bullard', 'Bulverde', 'Buna', 'Bunker Hill Village', 'Burkburnett', 'Burke', 'Burleson', 'Burnet', 'Burton', 'Butterfield', 'Byers', 'Bynum', 'Cactus', 'Caddo Mills', 'Caldwell', 'Callisburg', 'Calvert', 'Cameron', 'Cameron Park', 'Campbell', 'Camp Swift', 'Camp Wood', 'Canadian', 'Caney City', 'Canton', 'Cantu Addition', 'Canutillo', 'Canyon', 'Canyon Lake', 'Carbon', "Carl's Corner", 'Carmine', 'Carrizo Hill', 'Carrizo Springs', 'Carrollton', 'Carthage', 'Castle Hills', 'Castroville', 'Catarina', 'Cedar Hill', 'Cedar Park', 'Celeste', 'Celina', 'Center', 'Centerville', 'Central Gardens', 'Cesar Chavez', 'Chandler', 'Channelview', 'Channing', 'Charlotte', 'Chester', 'Chico', 'Childress', 'Chillicothe', 'China', 'China Grove', 'Chireno', 'Christine', 'Christoval', 'Chula Vista-Orason', 'Chula Vista-River Spur', 'Cibolo', 'Cienegas Terrace', 'Cinco Ranch', 'Circle D-KC Estates', 'Cisco', 'Citrus City', 'Clarendon', 'Clarksville', 'Clarksville City', 'Claude', 'Clear Lake Shores', 'Cleburne', 'Cleveland', 'Clifton', 'Clint', 'Cloverleaf', 'Clute', 'Clyde', 'Coahoma', 'Cockrell Hill', 'Coffee City', 'Coldspring', 'Coleman', 'College Station', 'Colleyville', 'Collinsville', 'Colmesneil', 'Colorado City', 'Columbus', 'Comanche', 'Combes', 'Combine', 'Comfort', 'Commerce', 'Como', 'Concepcion', 'Conroe', 'Converse', 'Cool', 'Coolidge', 'Cooper', 'Coppell', 'Copperas Cove', 'Copper Canyon', 'Corinth', 'Corpus Christi', 'Corral City', 'Corrigan', 'Corsicana', 'Cottonwood', 'Cottonwood Shores', 'Cotulla', 'Cove', 'Covington', 'Coyanosa', 'Coyote Acres', 'Crandall', 'Crane', 'Cranfills Gap', 'Crawford', 'Creedmoor', 'Crockett', 'Crosby', 'Crosbyton', 'Cross Mountain', 'Cross Plains', 'Cross Roads', 'Cross Timber', 'Crowell', 'Crowley', 'Crystal City', 'Cuero', 'Cuevitas', 'Cumby', 'Cumings', 'Cuney', 'Cushing', 'Cut and Shoot', 'Daingerfield', 'Daisetta', 'Dalhart', 'Dallas', 'Dalworthington Gardens', 'Damon', 'Danbury', 'Darrouzett', 'Dawson', 'Dayton', 'Dayton Lakes', 'Dean', 'Decatur', 'Deer Park', 'De Kalb', 'De Leon', 'Dell City', 'Del Mar Heights', 'Del Rio', 'Del Sol-Loma Linda', 'Denison', 'Denton', 'Denver City', 'Deport', 'DeSoto', 'Detroit', 'Devers', 'Devine', 'Deweyville', 'Diboll', 'Dickens', 'Dickinson', 'Dilley', 'Dimmitt', 'Dodd City', 'Dodson', 'Doffing', 'Domino', 'Donna', 'Doolittle', 'Dorchester', 'Double Oak', 'Douglassville', 'Doyle', 'Dripping Springs', 'Driscoll', 'Dublin', 'Dumas', 'Duncanville', 'Eagle Lake', 'Eagle Mountain', 'Eagle Pass', 'Early', 'Earth', 'East Bernard', 'Eastland', 'East Mountain', 'Easton', 'East Tawakoni', 'Ector', 'Edcouch', 'Eden', 'Edgecliff Village', 'Edgewater-Paisano', 'Edgewood', 'Edinburg', 'Edmonson', 'Edna', 'Edom', 'Edroy', 'Eidson Road', 'Elbert', 'El Camino Angosto', 'El Campo', 'El Cenizo', 'Eldorado', 'Electra', 'Elgin', 'El Indio', 'Elkhart', 'El Lago', 'Elm Creek', 'Elmendorf', 'El Paso', 'El Refugio', 'Elsa', 'Emhouse', 'Emory', 'Encantada-Ranchito El Calaboz', 'Enchanted Oaks', 'Encinal', 'Encino', 'Ennis', 'Escobares', 'Estelline', 'Euless', 'Eureka', 'Eustace', 'Evadale', 'Evant', 'Everman', 'Fabens', 'Fairchilds village', 'Fairfield', 'Fair Oaks Ranch', 'Fairview', 'Falcon Heights', 'Falcon Lake Estates', 'Falcon Mesa', 'Falcon Village', 'Falfurrias', 'Falls City', 'Falman-County Acres', 'Farmers Branch', 'Farmersville', 'Farwell', 'Fate', 'Fayetteville', 'Faysville', 'Ferris', 'Fifth Street', 'Flatonia', 'Florence', 'Floresville', 'Flowella', 'Flower Mound', 'Floydada', 'Follett', 'Forest Hill', 'Forney', 'Forsan', 'Fort Bliss', 'Fort Davis', 'Fort Hancock', 'Fort Hood', 'Fort Stockton', 'Fort Worth', 'Four Corners', 'Fowlerton', 'Franklin', 'Frankston', 'Fredericksburg', 'Freeport', 'Freer', 'Fresno', 'Friendswood', 'Friona', 'Frisco', 'Fritch', 'Fronton', 'Frost', 'Fruitvale', 'Fulshear', 'Fulton', 'Gainesville', 'Galena Park', 'Gallatin', 'Galveston', 'Ganado', 'Garceno', 'Gardendale', 'Garden Ridge', 'Garfield', 'Garland', 'Garrett', 'Garrison', 'Gary City', 'Gatesville', 'Georgetown', 'George West', 'Geronimo', 'Gholson', 'Giddings', 'Gilmer', 'Girard', 'Gladewater', 'Glenn Heights', 'Glen Rose', 'Godley', 'Goldsmith', 'Goldthwaite', 'Goliad', 'Golinda', 'Gonzales', 'Goodlow', 'Goodrich', 'Gordon', 'Goree', 'Gorman', 'Graford', 'Graham', 'Granbury', 'Grand Acres', 'Grandfalls', 'Grand Prairie', 'Grand Saline', 'Grandview', 'Granger', 'Granite Shoals', 'Granjeno', 'Grape Creek', 'Grapeland', 'Grapevine', 'Grays Prairie village', 'Greatwood', 'Green Valley Farms', 'Greenville', 'Gregory', 'Grey Forest', 'Groesbeck', 'Groom', 'Groves', 'Groveton', 'Gruver', 'Guerra', 'Gun Barrel City', 'Gunter', 'Gustine', 'Hackberry', 'Hale Center', 'Hallettsville', 'Hallsburg', 'Hallsville', 'Haltom City', 'Hamilton', 'Hamlin', 'Happy', 'Hardin', 'Harker Heights', 'Harlingen', 'Harper', 'Hart', 'Hartley', 'Haskell', 'Haslet', 'Havana', 'Hawk Cove', 'Hawkins', 'Hawley', 'Hays', 'Hearne', 'Heath', 'Hebbronville', 'Hebron', 'Hedley', 'Hedwig Village', 'Heidelberg', 'Helotes', 'Hemphill', 'Hempstead', 'Henderson', 'Henrietta', 'Hereford', 'Hermleigh', 'Hewitt', 'Hickory Creek', 'Hico', 'Hidalgo', 'Higgins', 'Highland Haven', 'Highland Park', 'Highlands', 'Highland Village', 'Hill Country Village', 'Hillcrest village', 'Hillsboro', 'Hilltop', 'Hilshire Village', 'Hitchcock', 'Holiday Lakes', 'Holland', 'Holliday', 'Hollywood Park', 'Homestead Meadows North', 'Homestead Meadows South', 'Hondo', 'Honey Grove', 'Hooks', 'Horizon City', 'Horseshoe Bay', 'Houston', 'Howardwick', 'Howe', 'Hubbard', 'Hudson', 'Hudson Bend', 'Hudson Oaks', 'Hughes Springs', 'Humble', 'Hungerford', 'Hunters Creek Village', 'Huntington', 'Huntsville', 'Hurst', 'Hutchins', 'Hutto', 'Huxley', 'Idalou', 'Impact', 'Imperial', 'Indian Hills', 'Indian Lake', 'Industry', 'Inez', 'Ingleside', 'Ingleside on the Bay', 'Ingram', 'Iowa Colony village', 'Iowa Park', 'Iraan', 'Iredell', 'Irving', 'Italy', 'Itasca', 'Jacinto City', 'Jacksboro', 'Jacksonville', 'Jamaica Beach', 'Jasper', 'Jayton', 'Jefferson', 'Jersey Village', 'Jewett', 'Joaquin', 'Johnson City', 'Jolly', 'Jollyville', 'Jones Creek village', 'Jonestown', 'Josephine', 'Joshua', 'Jourdanton', 'Junction', 'Justin', 'Karnes City', 'Katy', 'Kaufman', 'K-Bar Ranch', 'Keene', 'Keller', 'Kemah', 'Kemp', 'Kempner', 'Kendleton', 'Kenedy', 'Kenefick', 'Kennard', 'Kennedale', 'Kerens', 'Kermit', 'Kerrville', 'Kilgore', 'Killeen', 'Kingsbury', 'Kingsland', 'Kingsville', 'Kirby', 'Kirbyville', 'Kirvin', 'Knippa', 'Knollwood village', 'Knox City', 'Kosse', 'Kountze', 'Kress', 'Krugerville', 'Krum', 'Kyle', 'La Blanca', 'La Casita-Garciasville', 'Lackland AFB', 'LaCoste', 'Lacy-Lakeview', 'Ladonia', 'La Feria', 'La Feria North', 'Lago', 'Lago Vista', 'La Grange', 'La Grulla', 'Laguna Heights', 'Laguna Seca', 'Laguna Vista', 'La Homa', 'La Joya', 'Lake Bridgeport', 'Lake Brownwood', 'Lake City', 'Lake Dallas', 'Lakehills', 'Lake Jackson', 'Lake Kiowa', 'Lakeport', 'Lakeshore Gardens-Hidden Acres', 'Lakeside town (San Patricio County)', 'Lakeside town (Tarrant County)', 'Lakeside City', 'Lake Tanglewood village', 'Lakeview', 'Lake View', 'Lakeway', 'Lakewood Village', 'Lake Worth', 'La Marque', 'Lamesa', 'Lampasas', 'Lancaster', 'La Paloma', 'La Paloma-Lost Creek', 'La Porte', 'La Presa', 'La Pryor', 'La Puerta', 'Laredo', 'Laredo Ranchettes', 'Larga Vista', 'La Rosita', 'Lasana', 'Lasara', 'Las Colonias', 'Las Lomas', 'Las Lomitas', 'Las Palmas-Juarez', 'Las Quintas Fronterizas', 'Latexo', 'Laughlin AFB', 'Laureles', 'La Vernia', 'La Victoria', 'La Villa', 'Lavon', 'La Ward', 'Lawn', 'League City', 'Leakey',
 'Leander', 'Leary', 'Lefors', 'Leona', 'Leonard', 'Leon Valley', 'Leroy', 'Levelland', 'Lewisville', 'Lexington', 'Liberty', 'Liberty City', 'Liberty Hill', 'Lincoln Park', 'Lindale', 'Linden', 'Lindsay', 'Lindsay', 'Lipan', 'Lipscomb', 'Little Elm', 'Littlefield', 'Little River-Academy', 'Live Oak', 'Liverpool', 'Livingston', 'Llano', 'Llano Grande', 'Lockhart', 'Lockney', 'Log Cabin', 'Lolita', 'Loma Linda East', 'Lometa', 'Lone Oak', 'Lone Star', 'Longview', 'Lopeno', 'Lopezville', 'Loraine', 'Lorena', 'Lorenzo', 'Los Alvarez', 'Los Angeles Subdivision', 'Los Ebanos', 'Los Fresnos', 'Los Indios', 'Lost Creek', 'Los Villareales', 'Los Ybanez', 'Lott', 'Louise', 'Lovelady', 'Lowry Crossing', 'Lozano', 'Lubbock', 'Lucas', 'Lueders', 'Lufkin', 'Luling', 'Lumberton', 'Lyford', 'Lyford South', 'Lytle', 'Mabank', 'McAllen', 'McCamey', 'McGregor', 'McKinney', 'McLean', 'McLendon-Chisholm', 'McQueeney', 'Madisonville', 'Magnolia', 'Malakoff', 'Malone', 'Manor', 'Mansfield', 'Manvel', 'Marathon', 'Marble Falls', 'Marfa', 'Marietta', 'Marion', 'Markham', 'Marlin', 'Marquez', 'Marshall', 'Marshall Creek', 'Mart', 'Martindale', 'Mason', 'Matador', 'Mathis', 'Maud', 'Mauriceville', 'Maypearl', 'Meadow', 'Meadowlakes', 'Meadows Place', 'Medina', 'Megargel', 'Melissa', 'Melvin', 'Memphis', 'Menard', 'Mercedes', 'Meridian', 'Merkel', 'Mertens', 'Mertzon', 'Mesquite', 'Mexia', 'Miami', 'Midland', 'Midlothian', 'Midway', 'Midway North', 'Midway South', 'Mila Doce', 'Milam', 'Milano', 'Mildred', 'Miles', 'Milford', "Miller's Cove", 'Millican', 'Millsap', 'Mineola', 'Mineral Wells', 'Mingus', 'Mirando City', 'Mission', 'Mission Bend', 'Missouri City', 'Mobeetie', 'Mobile City', 'Monahans', 'Mont Belvieu', 'Monte Alto', 'Montgomery', 'Moody', 'Moore', 'Moore Station', 'Morales-Sanchez', 'Moran', 'Morgan', 'Morgan Farm Area', "Morgan's Point", "Morgan's Point Resort", 'Morning Glory', 'Morse', 'Morton', 'Moulton', 'Mountain City', 'Mount Calm', 'Mount Enterprise', 'Mount Pleasant', 'Mount Vernon', 'Muenster', 'Muleshoe', 'Mullin', 'Munday', 'Muniz', 'Murchison', 'Murphy', 'Mustang', 'Mustang Ridge', 'Nacogdoches', 'Naples', 'Nash', 'Nassau Bay', 'Natalia', 'Navarro', 'Navasota', 'Nazareth', 'Nederland', 'Needville', 'Nesbitt', 'Nevada', 'Newark', 'New Berlin', 'New Boston', 'New Braunfels', 'Newcastle', 'New Chapel Hill', 'New Deal', 'New Fairview', 'New Falcon', 'New Home', 'New Hope', 'New London', 'New Summerfield', 'New Territory', 'Newton', 'New Waverly', 'Neylandville', 'Niederwald', 'Nixon', 'Nocona', 'Nolanville', 'Nome', 'Noonday', 'Nordheim', 'Normangee', 'Normanna', 'North Alamo', 'North Cleveland', 'Northcliff', 'North Escobares', 'Northlake', 'North Pearsall', 'North Richland Hills', 'North San Pedro', 'Novice', 'Nurillo', 'Oak Grove', 'Oakhurst', 'Oak Leaf', 'Oak Point', 'Oak Ridge town (Cooke County)', 'Oak Ridge town (Kaufman County)', 'Oak Ridge North', 'Oak Trail Shores', 'Oak Valley', 'Oakwood', "O'Brien", 'Odem', 'Odessa', "O'Donnell", 'Oglesby', 'Oilton', 'Old River-Winfree', 'Olivarez', 'Olmito', 'Olmos Park', 'Olney', 'Olton', 'Omaha', 'Onalaska', 'Onion Creek', 'Opdyke West', 'Orange', 'Orange Grove', 'Orchard', 'Ore City', 'Overton', 'Ovilla', 'Owl Ranch-Amargosa', 'Oyster Creek', 'Ozona', 'Paducah', 'Paint Rock', 'Palacios', 'Palestine', 'Palisades village', 'Palmer', 'Palmhurst', 'Palm Valley', 'Palmview', 'Palmview South', 'Pampa', 'Panhandle', 'Panorama Village', 'Pantego', 'Paradise', 'Paris', 'Parker', 'Pasadena', 'Pattison', 'Patton Village', 'Pawnee', 'Payne Springs', 'Pearland', 'Pearsall', 'Pecan Acres', 'Pecan Gap', 'Pecan Grove', 'Pecan Hill', 'Pecan Plantation', 'Pecos', 'Pelican Bay', 'Penelope', 'Penitas', 'Pernitas Point village', 'Perryton', 'Petersburg', 'Petrolia', 'Petronila', 'Pettus', 'Pflugerville', 'Pharr', 'Pilot Point', 'Pine Forest', 'Pinehurst', 'Pinehurst', 'Pine Island', 'Pineland', 'Pinewood Estates', 'Piney Point Village', 'Pittsburg', 'Plains', 'Plainview', 'Plano', 'Pleak village', 'Pleasanton', 'Pleasant Valley', 'Plum Grove', 'Point', 'Point Blank', 'Point Comfort', 'Ponder', 'Port Aransas', 'Port Arthur', 'Porter Heights', 'Port Isabel', 'Portland', 'Port Lavaca', 'Port Mansfield', 'Port Neches', 'Post', 'Post Oak Bend City', 'Poteet', 'Poth', 'Potosi', 'Pottsboro', 'Powell', 'Poynor', 'Prado Verde', 'Prairie View', 'Premont', 'Presidio', 'Primera', 'Princeton', 'Progreso', 'Progreso Lakes', 'Prosper', 'Putnam', 'Pyote', 'Quail', 'Quanah', 'Queen City', 'Quemado', 'Quinlan', 'Quintana', 'Quitaque', 'Quitman', 'Radar Base', 'Ralls', 'Ranchette Estates', 'Ranchitos Las Lomas', 'Rancho Alegre', 'Rancho Banquete', 'Rancho Chico', 'Ranchos Penitas West', 'Rancho Viejo', 'Ranger', 'Rangerville village', 'Rankin', 'Ransom Canyon', 'Ratamosa', 'Ravenna', 'Raymondville', 'Realitos', 'Redford', 'Red Lick', 'Red Oak', 'Redwater', 'Redwood', 'Reese Center', 'Refugio', 'Reid Hope King', 'Reklaw', 'Relampago', 'Rendon', 'Reno city (Lamar County)', 'Reno city (Parker County)', 'Retreat', 'Rhome', 'Rice', 'Richardson', 'Richland', 'Richland Hills', 'Richland Springs', 'Richmond', 'Richwood', 'Riesel', 'Rio Bravo', 'Rio Grande City', 'Rio Hondo', 'Rio Vista', 'Rising Star', 'River Oaks', 'Riverside', 'Roanoke', 'Roaring Springs', 'Robert Lee', 'Robinson', 'Robstown', 'Roby', 'Rochester', 'Rockdale', 'Rockport', 'Rocksprings', 'Rockwall', 'Rocky Mound', 'Rogers', 'Rollingwood', 'Roma', 'Roma Creek', 'Roman Forest', 'Ropesville', 'Roscoe', 'Rosebud', 'Rose City', 'Rose Hill Acres', 'Rosenberg', 'Rosita North', 'Rosita South', 'Ross', 'Rosser village', 'Rotan', 'Round Mountain', 'Round Rock', 'Round Top', 'Rowlett', 'Roxton', 'Royse City', 'Rule', 'Runaway Bay', 'Runge', 'Rusk', 'Sabinal', 'Sachse', 'Sadler', 'Saginaw', 'St. Hedwig', 'St. Jo', 'St. Paul', 'St. Paul', 'Salado', 'Salineno', 'Samnorwood', 'San Angelo', 'San Antonio', 'San Augustine', 'San Benito', 'San Carlos', 'Sanctuary', 'Sanderson', 'Sandia', 'San Diego', 'Sandy Hollow-Escondidas', 'San Elizario', 'San Felipe', 'Sanford', 'Sanger', 'San Ignacio', 'San Isidro', 'San Juan', 'San Leanna village', 'San Leon', 'San Manuel-Linn', 'San Marcos', 'San Patricio', 'San Pedro', 'San Perlita', 'San Saba', 'Sansom Park', 'Santa Anna', 'Santa Clara', 'Santa Cruz', 'Santa Fe', 'Santa Maria', 'Santa Monica', 'Santa Rosa', 'Savoy', 'Scenic Oaks', 'Schertz', 'Schulenburg', 'Scissors', 'Scotland', 'Scottsville', 'Seabrook', 'Seadrift', 'Seagoville', 'Seagraves', 'Sealy', 'Sebastian', 'Seguin', 'Selma', 'Seminole', 'Serenada', 'Seth Ward', 'Seven Oaks', 'Seven Points', 'Seymour', 'Shady Hollow', 'Shady Shores', 'Shallowater', 'Shamrock', 'Shavano Park', 'Sheldon', 'Shenandoah', 'Shepherd', 'Sherman', 'Shiner', 'Shoreacres', 'Sienna Plantation', 'Sierra Blanca', 'Siesta Shores', 'Silsbee', 'Silverton', 'Simonton', 'Sinton', 'Skellytown', 'Skidmore', 'Slaton', 'Smiley', 'Smithville', 'Smyer', 'Snook', 'Snyder', 'Socorro', 'Solis', 'Somerset', 'Somerville', 'Sonora', 'Sour Lake', 'South Alamo', 'South Fork Estates', 'South Houston', 'Southlake', 'Southmayd', 'South Mountain', 'South Padre Island', 'South Point', 'Southside Place', 'South Toledo Bend', 'Spade', 'Sparks', 'Spearman', 'Splendora', 'Spofford', 'Spring', 'Spring Garden-Terra Verde', 'Springlake', 'Springtown', 'Spring Valley', 'Spur', 'Stafford', 'Stagecoach', 'Stamford', 'Stanton', 'Star Harbor', 'Stephenville', 'Sterling City', 'Stinnett', 'Stockdale', 'Stonewall', 'Stowell', 'Stratford', 'Strawn', 'Streetman', 'Study Butte-Terlingua', 'Sudan', 'Sugar Land', 'Sullivan City', 'Sulphur Springs', 'Sundown', 'Sunnyvale', 'Sunray', 'Sunrise Beach Village', 'Sunset', 'Sunset Valley', 'Sun Valley', 'Surfside Beach', 'Sweeny', 'Sweetwater', 'Taft', 'Taft Southwest', 'Tahoka', 'Talco', 'Talty', 'Tatum', 'Taylor', 'Taylor Lake Village', 'Teague', 'Tehuacana', 'Temple', 'Tenaha', 'Terrell', 'Terrell Hills', 'Texarkana', 'Texas City', 'Texhoma', 'Texline', 'The Colony', 'The Hills village', 'The Woodlands', 'Thompsons', 'Thorndale', 'Thornton', 'Thorntonville', 'Thrall', 'Three Rivers', 'Throckmorton', 'Tierra Bonita', 'Tierra Grande', 'Tiki Island village', 'Timbercreek Canyon village', 'Timberwood Park', 'Timpson', 'Tioga', 'Tira', 'Toco', 'Todd Mission', 'Tolar', 'Tomball', 'Tom Bean', 'Tool', 'Tornillo', 'Toyah', 'Tradewinds', 'Trent', 'Trenton', 'Trinidad', 'Trinity', 'Trophy Club', 'Troup', 'Troy', 'Tuleta', 'Tulia', 'Tulsita', 'Turkey', 'Tuscola', 'Tye', 'Tyler', 'Tynan', 'Uhland', 'Uncertain', 'Union Grove', 'Universal City', 'University Park', 'Utopia', 'Uvalde', 'Uvalde Estates', 'Valentine', 'Valley Mills', 'Valley View', 'Val Verde Park', 'Van', 'Van Alstyne', 'Vanderbilt', 'Van Horn', 'Van Vleck', 'Vega', 'Venus', 'Vernon', 'Victoria', 'Vidor', 'Villa del Sol', 'Villa Pancho', 'Villa Verde', 'Vinton village', 'Waco', 'Waelder', 'Wake Village', 'Waller', 'Wallis', 'Walnut Springs', 'Warren City', 'Waskom', 'Watauga', 'Waxahachie', 'Weatherford', 'Webster', 'Weimar', 'Weinert', 'Weir', 'Wellington', 'Wellman', 'Wells', 'Wells Branch', 'Weslaco', 'West', 'Westbrook', 'West Columbia', 'Westdale', 'Westlake', 'West Lake Hills', 'West Livingston', 'Westminster', 'West Odessa', 'Weston', 'West Orange', 'Westover Hills', 'West Pearsall', 'West Sharyland', 'West Tawakoni', 'West University Place', 'Westway', 'Westworth Village', 'Wharton', 'Wheeler', 'White Deer', 'Whiteface', 'Whitehouse', 'White Oak', 'Whitesboro', 'White Settlement', 'Whitewright', 'Whitney', 'Wichita Falls', 'Wickett', 'Wild Peach Village', 'Willamar', 'Willis', 'Willow Park', 'Wills Point', 'Wilmer', 'Wilson', 'Wimberley', 'Windcrest', 'Windemere', 'Windom', 'Windthorst', 'Winfield', 'Wink', 'Winnie', 'Winnsboro', 'Winona', 'Winters', 'Wixon Valley', 'Wolfe City', 'Wolfforth', 'Woodbranch', 'Woodcreek', 'Woodloch', 'Woodsboro', 'Woodson', 'Woodville', 'Woodway', 'Wortham', 'Wyldwood', 'Wylie', 'Yantis', 'Yoakum', 'Yorktown', 'Yznaga', 'Zapata', 'Zapata Ranch', 'Zavalla', 'Zuehl']



country_codes = {
    "USA":'+1'
}