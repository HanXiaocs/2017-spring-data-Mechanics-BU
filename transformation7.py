import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
from geopy.distance import vincenty

from math import radians, sqrt, sin, cos, atan2





def geodistance(lat1, lon1, lat2, lon2):
        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlon = lon1 - lon2

        EARTH_R = 6372.8

        y = sqrt(
            (cos(lat2) * sin(dlon)) ** 2
            + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
            )
        x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
        c = atan2(y, x)
        return EARTH_R * c



class transformation7(dml.Algorithm):
    contributor = 'bohan_nyx_xh1994_yiran123'
    reads = ['bohan_nyx_xh1994_yiran123.airbnb_rating', 'bohan_nyx_xh1994_yiran123.crime_boston']
    writes = ['bohan_nyx_xh1994_yiran123.airbnb_safety']




    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('bohan_nyx_xh1994_yiran123', 'bohan_nyx_xh1994_yiran123')  
        airbnb = repo.bohan_nyx_xh1994_yiran123.airbnb_rating.find()
        crime = repo.bohan_nyx_xh1994_yiran123.crime_boston.find()
        crimes = [c for c in crime]
        # print(crime[0]['location'])
        # print(FoodEI[0])

        #Foodlocation_name = FoodEI.project(lambda t: (t['businessname'],t['location']))
        #crime_location = crime.project(lambda t: (t[-2]))
        #safety_level = []
        repo.dropCollection("airbnb_safety")
        repo.createCollection("airbnb_safety")
        setdis = []
        #counter = 0
        #jcounter=0

        print("start tran7")
        for i in airbnb:
            #print(i['name'])
            #jcounter+=1
            crime_num = 0
            #print(i['location'])
            #print('i',jcounter)
            #print(len(crimes))
            for j in crimes:
                
                distance = geodistance(i['longitude'],i['latitude'],j['location']['coordinates'][0],j['location']['coordinates'][1])
               # print(distance)
                if distance<=0.5:
                    crime_num+=1
            
            insertMaterial = {'longitude':i['longitude'], 'latitude':i['latitude'], 'crime number around airbnb':crime_num}
            #insertMaterial = {'Businessname':i['businessname'], 'location':None, 'crime incidents number within amile':crime_incident_within_amile}
  
            repo['bohan_nyx_xh1994_yiran123.airbnb_safety'].insert_one(insertMaterial)

        #repo['bohan_nyx_xh1994_yiran123.Restaurants_safety'].insert_many(safety_level)
        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('bohan_nyx_xh1994_yiran123', 'bohan_nyx_xh1994_yiran123')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')
        doc.add_namespace('airbnbr','http://datamechanics.io/?prefix=bohan_xh1994/')

        this_script = doc.agent('alg:bohan_nyx_xh1994_yiran123#transformation1', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        resource_food_estab_licenses = doc.entity('dat:bohan_nyx_xh1994_yiran123#Active_Food_Establishment_Licenses', {prov.model.PROV_LABEL:'Food Establishment Licenses', prov.model.PROV_TYPE:'ont:DataSet'})
        resource_crime_boston = doc.entity('dat:bohan_nyx_xh1994_yiran123#crime_boston', {prov.model.PROV_LABEL:'Crime Boston', prov.model.PROV_TYPE:'ont:DataSet'})

        get_restaurant_safe = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(get_restaurant_safe, this_script)
        
        doc.usage(get_restaurant_safe, resource_food_estab_licenses, startTime, None, 
                  {prov.model.PROV_TYPE:'ont:Computation'})
        doc.usage(get_restaurant_safe, resource_crime_boston, startTime, None, 
                  {prov.model.PROV_TYPE:'ont:Computation'})
        
        restaurant_safe = doc.entity('dat:bohan_nyx_xh1994_yiran123#Restaurants_safety',
                                    {prov.model.PROV_LABEL:'Restaurant Safety',
                                     prov.model.PROV_TYPE:'ont:DataSet'})

        #lost = doc.entity('dat:alice_bob#lost', {prov.model.PROV_LABEL:'Animals Lost', prov.model.PROV_TYPE:'ont:DataSet'})
        doc.wasAttributedTo(restaurant_safe, this_script)
        doc.wasGeneratedBy(restaurant_safe, get_restaurant_safe, endTime)
        doc.wasDerivedFrom(restaurant_safe, resource_food_estab_licenses, get_restaurant_safe, get_restaurant_safe, get_restaurant_safe)
        doc.wasDerivedFrom(restaurant_safe, resource_crime_boston, get_restaurant_safe, get_restaurant_safe, get_restaurant_safe)


        repo.logout()
                  
        return doc



 
'''
doc = transformation7.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
'''