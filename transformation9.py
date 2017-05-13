import urllib.request
import json
import dml
import prov.model
import datetime
import uuid


class transformation9(dml.Algorithm):
    contributor = 'bohan_nyx_xh1994_yiran123'
    reads = ['bohan_nyx_xh1994_yiran123.airbnb_score_system']
    writes = ['bohan_nyx_xh1994_yiran123.finalscore_frequency']



    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        #print(11111111111111111)
        repo = client.repo
        repo.authenticate('bohan_nyx_xh1994_yiran123', 'bohan_nyx_xh1994_yiran123')  
        finalscore = repo.bohan_nyx_xh1994_yiran123.airbnb_score_system.find()
        finalscore = [c for c in finalscore]


        #Foodlocation_name = FoodEI.project(lambda t: (t['businessname'],t['location']))
        #crime_location = crime.project(lambda t: (t[-2]))
        #safety_level = []
        repo.dropCollection("finalscore_frequency")
        repo.createCollection("finalscore_frequency")

        print("start tran9")
        firstfive = [0,0,0,0,0,0,0,0,0,0]
        for i in finalscore:
            #print(i['overall score'])
            if(i['overall score']>0 and i['overall score']<=0.1):
                firstfive[0]+=1
            elif(i['overall score']>0.1 and i['overall score']<=0.2):
                firstfive[1]+=1
            elif(i['overall score']>0.2 and i['overall score']<=0.3):
                firstfive[2]+=1
            elif(i['overall score']>0.3 and i['overall score']<=0.4):
                firstfive[3]+=1
            elif(i['overall score']>0.4 and i['overall score']<=0.5):
                firstfive[4]+=1
            elif(i['overall score']>0.5 and i['overall score']<=0.6):
                firstfive[5]+=1
            elif(i['overall score']>0.6 and i['overall score']<=0.7):
                firstfive[6]+=1
            elif(i['overall score']>0.7 and i['overall score']<=0.8):
                firstfive[7]+=1
            elif(i['overall score']>0.8 and i['overall score']<=0.9):
                firstfive[8]+=1
            elif(i['overall score']>0.9 and i['overall score']<=1.0):
                firstfive[9]+=1

        #for j in range(len(firstfive)):
        insertMaterial1 = {'frequency':firstfive[0], 'range': '0.0 to 0.1'}
        insertMaterial2 = {'frequency':firstfive[1], 'range': '0.1 to 0.2'}
        insertMaterial3 = {'frequency':firstfive[2], 'range': '0.2 to 0.3'}
        insertMaterial4 = {'frequency':firstfive[3], 'range': '0.3 to 0.4'}
        insertMaterial5 = {'frequency':firstfive[4], 'range': '0.4 to 0.5'}
        insertMaterial6 = {'frequency':firstfive[5], 'range': '0.5 to 0.6'}
        insertMaterial7 = {'frequency':firstfive[6], 'range': '0.6 to 0.7'}
        insertMaterial8 = {'frequency':firstfive[7], 'range': '0.7 to 0.8'}
        insertMaterial9 = {'frequency':firstfive[8], 'range': '0.8 to 0.9'}
        insertMaterial10 = {'frequency':firstfive[9], 'range': '0.9 to 1.0'}
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial1)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial2)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial3)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial4)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial5)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial6)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial7)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial8)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial9)
        repo['bohan_nyx_xh1994_yiran123.finalscore_frequency'].insert_one(insertMaterial10)


            

        #repo['bohan_nyx_xh1994_yiran123.Restaurants_safety'].insert_many(safety_level)
        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}


    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime = None, endTime = None):

        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('bohan_nyx_xh1994_yiran123','bohan_nyx_xh1994_yiran123')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format
        doc.add_namespace('dat', 'http://datamechanics.io/data/')
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofboston.gov/resource/')

        this_script = doc.agent('alg:bohan_nyx_xh1994_yiran123#transformation8', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})


        resource_airbnb_rating = doc.entity('dat:bohan_nyx_xh1994_yiran123#airbnb_rating',{'prov:label':'Airbnb Rating', prov.model.PROV_TYPE:'ont:DataSet'})
        resource_newairbnb_eliminated_version = doc.entity('dat:bohan_nyx_xh1994_yiran123#newairbnb_eliminated_version',{'prov:label':'New Airbnb Eliminated Version', prov.model.PROV_TYPE:'ont:DataSet'})
        resource_airbnb_surr_restaurant_score_avg = doc.entity('dat:bohan_nyx_xh1994_yiran123#Airbnb_surrounding_restauranScoreAVG',{'prov:label':'Airbnb Surrounding Restaurant Score Average', prov.model.PROV_TYPE:'ont:DataSet'})

        get_airbnb_score_system = doc.activity('log:uuid' + str(uuid.uuid4()), startTime, endTime)

        doc.wasAssociatedWith(get_airbnb_score_system, this_script)

        doc.usage(get_airbnb_score_system, resource_airbnb_rating, startTime, None,
                  {prov.model.PROV_TYPE: 'ont:Computation'})
        doc.usage(get_airbnb_score_system, resource_newairbnb_eliminated_version, startTime, None,
                  {prov.model.PROV_TYPE: 'ont:Computation'})
        doc.usage(get_airbnb_score_system, resource_airbnb_surr_restaurant_score_avg, startTime, None,
                  {prov.model.PROV_TYPE: 'ont:Computation'})

        airbnb_score_system = doc.entity('dat:bohan_nyx_xh1994_yiran123#airbnb_score_system',
                            {prov.model.PROV_LABEL:'Airbnb Score System',
                             prov.model.PROV_TYPE: 'ont:DataSet'})

        doc.wasAttributedTo(airbnb_score_system, this_script)

        doc.wasGeneratedBy(airbnb_score_system, get_airbnb_score_system, endTime)
        
        doc.wasDerivedFrom(airbnb_score_system, resource_airbnb_rating, get_airbnb_score_system, get_airbnb_score_system, get_airbnb_score_system)
        doc.wasDerivedFrom(airbnb_score_system, resource_newairbnb_eliminated_version, get_airbnb_score_system, get_airbnb_score_system, get_airbnb_score_system)
        doc.wasDerivedFrom(airbnb_score_system, resource_airbnb_surr_restaurant_score_avg, get_airbnb_score_system, get_airbnb_score_system, get_airbnb_score_system)

        repo.logout()

        return doc



#transformation9.execute()    
'''
doc = transformation9.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
'''