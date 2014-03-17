import json
import random

__author__ = 'mscholl'
__date__ = '$13.03.2014 09:39:15$'

def economic_impact_calulation(worldstate):
    # TODO: economic impact calc
    with open('impact_result_template.json') as template_fh:
        json_data = template_fh.read()
        template = json.loads(json_data)
        
        template['HumanHealth']['PhysicalInjuries'] = random.randint(0, 10000000)
        template['HumanHealth']['PsycologicalInjuries'] = random.randint(0, 10000000)
        template['HumanHealth']['Fatalities'] = random.randint(0, 10000000)
        
        template['Buildings']['Residential'] = random.randint(0, 10000000)
        template['Buildings']['Commercial'] = random.randint(0, 10000000)
        template['Buildings']['SchoolAndPublicOffice'] = random.randint(0, 10000000)
        template['Buildings']['Hospital'] = random.randint(0, 10000000)
        template['Buildings']['IndustrialPlant'] = random.randint(0, 10000000)
        template['Buildings']['MilitaryBuilding'] = random.randint(0, 10000000)
        template['Buildings']['ProtectiveStructure'] = random.randint(0, 10000000)
        template['Buildings']['CulturalHeritage'] = random.randint(0, 10000000)

        template['Lifelines']['PowerSupplySystem'] = random.randint(0, 10000000)
        template['Lifelines']['WaterSupplyNetwork'] = random.randint(0, 10000000)
        template['Lifelines']['UrbanDrainage'] = random.randint(0, 10000000)
        template['Lifelines']['Road'] = random.randint(0, 10000000)
        template['Lifelines']['Railway'] = random.randint(0, 10000000)
        template['Lifelines']['RailwayStation'] = random.randint(0, 10000000)
        template['Lifelines']['TelephoneLine'] = random.randint(0, 10000000)
        template['Lifelines']['MobilePhoneMast'] = random.randint(0, 10000000)
        template['Lifelines']['NaturalGasNetwork'] = random.randint(0, 10000000)
        template['Lifelines']['DistrictHeatingAndCoolingNetwork'] = random.randint(0, 10000000)
        template['Lifelines']['OilProductStorage'] = random.randint(0, 10000000)
        template['Lifelines']['FuelStation'] = random.randint(0, 10000000)
        template['Lifelines']['Airport'] = random.randint(0, 10000000)
        template['Lifelines']['Harbour'] = random.randint(0, 10000000)
        
        template['Nature']['Forest'] = random.randint(0, 10000000)
        template['Nature']['Water'] = random.randint(0, 10000000)
        template['Nature']['Air'] = random.randint(0, 10000000)
        
        template['Agriculture']['Crop'] = random.randint(0, 10000000)
        template['Agriculture']['Livestock'] = random.randint(0, 10000000)
        template['Agriculture']['Fields'] = random.randint(0, 10000000)
        template['Agriculture']['AgriculturalMachines'] = random.randint(0, 10000000)
        template['Agriculture']['AgriculturalBuildings'] = random.randint(0, 10000000)
        
        template['RescueAndEmergencyOperation']['PersonnelResources'] = random.randint(0, 10000000)
        template['RescueAndEmergencyOperation']['Vehicles'] = random.randint(0, 10000000)
        template['RescueAndEmergencyOperation']['OtherResources'] = random.randint(0, 10000000)
        
        return template
    
def create_dataitem(economic_impact_data):
    dataitem = {}
    dataitem['$self'] = 1
    dataitem['id'] = 1
    dataitem['name'] = 'Economic Impact Calculation'
    dataitem['description'] = 'This is the Economic Impact Calculation dataitem'
    dataitem['lastmodified'] = current_time_millis()
    dataitem['temporalcoveragefrom'] = current_time_millis()
    dataitem['temporalcoverageto'] = current_time_millis()
    dataitem['datadescriptor'] = {}
    dataitem['datadescriptor']['$ref'] = '/CRISMA.datadescriptors/25'
    dataitem['actualaccessinfocontenttype'] = 'application/json'
    dataitem['actualaccessinfo'] = json.dumps(economic_impact_data)
    
    return dataitem

if __name__ == '__main__':
    print current_time_millis();
    # TODO: receive the worldstate id from pub sub event
    worldstate_id = 56
    worldstate = get_worldstate(worldstate_id)
    # do impact calculations with worldstate data
    economic_impact_data = economic_impact_calulation(worldstate)
    # create a new dataitem from the economic impact data
    dataitem = create_dataitem(economic_impact_data)
    
    old = worldstate['iccdata']
    worldstate['iccdata'] = []
    worldstate['iccdata'].append(old)
    
    # set the dataitem in the worldstate
    worldstate['iccdata'].append(dataitem)
    
    # save the changed worldstate
    status_code = put_worldstate(worldstate)
    
    if status_code >= 200 and status_code < 300:
        print 'updated worldstate successfully'
    else:
        print "update worldstate failed, code '" + status_code + "'"