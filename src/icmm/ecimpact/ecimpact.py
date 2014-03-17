import json
import random

from icmm import icmm
from icmm import tools

__author__ = 'mscholl'
__date__ = '$13.03.2014 09:39:15$'

def economic_impact_calulation(worldstate):
    # TODO: economic impact calc
    template = {}
    template['HumanHealth'] = {}
    template['HumanHealth']['PhysicalInjuries'] = random.randint(0, 10000000)
    template['HumanHealth']['PsycologicalInjuries'] = random.randint(0, 10000000)
    template['HumanHealth']['Fatalities'] = random.randint(0, 10000000)

    template['Buildings'] = {}
    template['Buildings']['Residential'] = random.randint(0, 10000000)
    template['Buildings']['Commercial'] = random.randint(0, 10000000)
    template['Buildings']['SchoolAndPublicOffice'] = random.randint(0, 10000000)
    template['Buildings']['Hospital'] = random.randint(0, 10000000)
    template['Buildings']['IndustrialPlant'] = random.randint(0, 10000000)
    template['Buildings']['MilitaryBuilding'] = random.randint(0, 10000000)
    template['Buildings']['ProtectiveStructure'] = random.randint(0, 10000000)
    template['Buildings']['CulturalHeritage'] = random.randint(0, 10000000)

    template['Lifelines'] = {}
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

    template['Nature'] = {}
    template['Nature']['Forest'] = random.randint(0, 10000000)
    template['Nature']['Water'] = random.randint(0, 10000000)
    template['Nature']['Air'] = random.randint(0, 10000000)

    template['Agriculture'] = {}
    template['Agriculture']['Crop'] = random.randint(0, 10000000)
    template['Agriculture']['Livestock'] = random.randint(0, 10000000)
    template['Agriculture']['Fields'] = random.randint(0, 10000000)
    template['Agriculture']['AgriculturalMachines'] = random.randint(0, 10000000)
    template['Agriculture']['AgriculturalBuildings'] = random.randint(0, 10000000)

    template['RescueAndEmergencyOperation'] = {}
    template['RescueAndEmergencyOperation']['PersonnelResources'] = random.randint(0, 10000000)
    template['RescueAndEmergencyOperation']['Vehicles'] = random.randint(0, 10000000)
    template['RescueAndEmergencyOperation']['OtherResources'] = random.randint(0, 10000000)

    return template
    
def create_dataitem(economic_impact_data, helper):
    dataitem = {}
    dataitem['id'] = helper.get_next_id('dataitems')
    dataitem['$self'] = helper.create_ref('dataitems', dataitem['id'])
    dataitem['name'] = 'Economic Impact Calculation'
    dataitem['description'] = 'This is the Economic Impact Calculation dataitem'
    now = tools.current_time_millis();
    dataitem['lastmodified'] = now
    dataitem['temporalcoveragefrom'] = now
    dataitem['temporalcoverageto'] = now
    dataitem['datadescriptor'] = {}
    dataitem['datadescriptor']['$ref'] = '/CRISMA.datadescriptors/25'
    dataitem['actualaccessinfocontenttype'] = 'application/json'
    dataitem['actualaccessinfo'] = json.dumps(economic_impact_data)
    
    return dataitem

def ec_impact_workflow():
    # TODO: receive the worldstate id from pub sub event
    worldstate_id = 56
    # create helper so that the url and the domain does not have to be repeated over and over
    helper = icmm.ICMMHelper('http://crisma.cismet.de/economic-impact/icmm_api', 'CRISMA')
    # receive the worldstate from icmm
    worldstate = helper.get_worldstate(worldstate_id)
    # do impact calculations with worldstate data
    economic_impact_data = economic_impact_calulation(worldstate)
    # create a new dataitem from the economic impact data
    dataitem = create_dataitem(economic_impact_data, helper)
    
    ## quick fix for older versions of the data model, not needed anymore in the future
    if isinstance(worldstate['iccdata'], dict):
        indicators = worldstate['iccdata']
        worldstate['iccdata'] = []
        worldstate['iccdata'].append(indicators)
    
    # set the dataitem in the worldstate
    worldstate['iccdata'].append(dataitem)
    
    print json.dumps(worldstate)
    
    # save the changed worldstate
    result = helper.put_worldstate(worldstate)
    
    if result.status_code >= 200 and result.status_code < 300:
        print 'updated worldstate successfully'
    else:
        print "update worldstate failed, code '" + str(result.status_code) + "'"