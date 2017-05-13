import urllib.request
import json
import dml
import prov.model
import datetime
import uuid


class transformation8(dml.Algorithm):
    contributor = 'bohan_nyx_xh1994_yiran123'
    reads = ['bohan_nyx_xh1994_yiran123.airbnb_rating', 'bohan_nyx_xh1994_yiran123.newairbnb_eliminated_version', 'bohan_nyx_xh1994_yiran123.Airbnb_surrounding_restauranScoreAVG','bohan_nyx_xh1994_yiran123.airbnb_safety']
    writes = ['bohan_nyx_xh1994_yiran123.airbnb_score_system']

    @staticmethod
    def execute(trial = False):
        startTime = datetime.datetime.now()

        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('bohan_nyx_xh1994_yiran123','bohan_nyx_xh1994_yiran123')

        airbnb_rating = repo.bohan_nyx_xh1994_yiran123.airbnb_rating.find()
        airbnb_MBTA_elim = repo.bohan_nyx_xh1994_yiran123.newairbnb_eliminated_version.find()
        airbnb_rest_avg = repo.bohan_nyx_xh1994_yiran123.Airbnb_surrounding_restauranScoreAVG.find()
        airbnb_safety = repo.bohan_nyx_xh1994_yiran123.airbnb_safety.find()

        repo.dropCollection("airbnb_score_system")
        repo.createCollection("airbnb_score_system")

        repo.dropCollection("high_rating_airbnb")
        repo.createCollection("high_rating_airbnb")


        print("start tran8")
        total_review = []
        overall_rating = []
        clean_level = []
        accuracy_level = []
        communication = []
        location = []
        coor=[]
        longitude=[]
        airbnbname = []
        airbnb_rest_score = []
        url = []

        #print(airbnb_rest_avg[0])
        for i in airbnb_rest_avg:
            i_avgscore = float(i['Avg Restaurants Score'])
            airbnb_rest_score.append(i_avgscore)

        '''maxrest = max(airbnb_rest_score)
        minrest = min(airbnb_rest_score)
        for i in range(len(airbnb_rest_score)):
            normalized_restscore = (airbnb_rest_score[i] - minrest)/(maxrest - minrest)
            airbnb_rest_score[i] = normalized_restscore'''


        #print(20202020202020202)

        #print(airbnb_rating[0])
        for i in airbnb_rating:
            i_review = str(i['number_of_reviews'])
            i_orating = str(i['review_scores_rating'])
            i_clean = str(i['review_scores_cleanliness'])
            i_accu = str(i['review_scores_accuracy'])
            i_com = str(i['review_scores_communication'])
            i_location = str(i['review_scores_location'])
            i_longitude=float(i['longitude'])
            i_latitude=float(i['latitude'])
            i_name = str(i['name'])
            i_url = i['listing_url']
            i_weekly_price = i['price']
            airbnbname.append(i_name)
            total_review.append(i_review)
            overall_rating.append(i_orating)
            clean_level.append(i_clean)
            accuracy_level.append(i_accu)
            communication.append(i_com)
            location.append(i_location)
            coor.append((i_longitude,i_latitude))
            longitude.append(i_longitude)
            url.append(i_url)
        
        #print(clean_level)

        #print(total_review)
        #print(overall_rating)
        
        #Rating System
        # print (coor)
        rating_system = []
        new_rate = 0
        for i in range(len(total_review)):
            #print(overall_rating[i])
            if overall_rating[i] == 'None':
                overall_rating[i] = 0
            new_rate = int(overall_rating[i]) * 0.6 
            if int(total_review[i]) > 10:
                new_rate = new_rate + 5
            if str(clean_level[i]) == 'None':
                clean_level[i] = 0
            if accuracy_level[i] == 'None':
                accuracy_level[i] = 0
            if str(communication[i]) == 'None':
                communication[i] = 0
            if str(location[i] == 'None'):
                location[i] = 0
            new_rate = new_rate + (int(clean_level[i]) + int(accuracy_level[i]) + int(communication[i]) + int(location[i]))
            #print(new_rate)
            rating_system.append(float(new_rate))
        
        maxrate = max(rating_system)
        minrate = min(rating_system)
        for i in range(len(rating_system)):
            nomalized_rating = (rating_system[i] - minrate) / (maxrate- minrate)
            rating_system[i] = nomalized_rating
        #Lit of Best Airbnb
        rating2=[]
        #l=len(rating_system)

        relation=[]

        #print(airbnb_MBTA_elim[0])
        for i in airbnb_MBTA_elim:
        
            relation.append((i['MBTA stops num within 1mile']))

        maxtraffic = max(relation)
        mintraffic = min(relation)
        for i in range(len(relation)):
            normalized_traffic = (relation[i] - mintraffic) / (maxtraffic - mintraffic)
            relation[i] = normalized_traffic
           


        safe = [c for c in airbnb_safety]

        crimenum = []
        for i in safe:
            crimenum.append(i['crime number around airbnb'])
        
        maxcrime = max(crimenum)
        safety = []
        for i in range(len(crimenum)):
            safety.append(1 - crimenum[i]/float(maxcrime))
        
        result = []

        for i in range(len(rating_system)):
            #print(i)
            finalscore = (relation[i]+rating_system[i]+airbnb_rest_score[i]+safety[i])/4
            result.append((rating_system[i],coor[i],relation[i], airbnbname[i], finalscore,airbnb_rest_score[i],safety[i],url[i],crimenum[i]))

        

       

        for i in result:
            #print(i[0])

            insertMaterial={'name':i[3] ,'longitude':i[1][0], 'latitude':i[1][1], 'airbnb score': i[0], 'traffic convinence': i[2], 'surrounding restaurant score': i[5],'safety score': i[6],'overall score': i[4],'url': i[7],'crime':i[8] }
            #insertMaterial = { "type": "Feature","geometry": {"type": "Point", "coordinates": [i[1][0], i[1][1]]},"properties": {'name':i[3], 'airbnb score': i[0], 'traffic convinence': i[2], 'surrounding restaurant score': i[5],'safety score': i[6],'overall score': i[4],'url': i[7]}}
            repo['bohan_nyx_xh1994_yiran123.airbnb_score_system'].insert_one(insertMaterial)
       
        '''     
            if (float(i['overall score']) >= 90):
                insertMaterial_90={'name':i[3] ,'longitude':i[1][0], 'latitude':i[1][1], 'airbnb score': i[0], 'traffic convinence': i[2], 'surrounding restaurant score': i[5],'crime_num': i[6],'overall score': i[4]}
                repo['bohan_nyx_xh1994_yiran123.high_rating_airbnb'].insert_one(insertMaterial_90)
        '''
        #print (insertMaterial)

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

#transformation8.execute()
'''
doc = transformation8.provenance()
print(doc.get_provn())
print(json.dumps(json.loads(doc.serialize()), indent=4))
'''