# ## Create SDG Data Packages by Goal

# -----------------------
# Import python libraries
# -----------------------

# https://docs.python.org/3/library/copy.html
# Shallow and deep copy operations
import copy

# https://docs.python.org/3/library/getpass.html
# Portable password input
# Used to prompt for user input. When using this script internally, you may
# remove this and simply hard code in your username and password
import getpass

# https://docs.python.org/3/library/json.html
# JSON encoder and decoder
import json

# https://docs.python.org/3/library/os.html
# Miscellaneous operating system interfaces
import os

# https://docs.python.org/3/library/re.html
# Regular expression operations
# import re

# https://docs.python.org/3/library/sys.html
# System-specific parameters and functions
import sys

# https://docs.python.org/3/library/time.html
# Time access and conversions
# import time

# https://docs.python.org/3/library/traceback.html
# Print or retrieve a stack traceback
import traceback

# https://docs.python.org/3/library/urllib.html
# URL handling modules
# import urllib

# https://docs.python.org/3/library/urllib.request.html
# Extensible library for opening URLs
import urllib.request as request

# https://docs.python.org/3/library/urllib.request.html
# Extensible library for opening URLs
import urllib.request as urlopen

# https://docs.python.org/3/library/datetime.html#datetime-objects
# A datetime object is a single object containing all the information from a
# date object and a time object
# from datetime import datetime

# http://docs.python-requests.org/en/master/
# HTTP for Humans
import requests

# http://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html
# Public API for display tools in IPython.
# Optional component to help debug within the Python Notebook
from IPython.display import display

# https://docs.python.org/3/library/pathlib.html
# Object-oriented filesystem paths
from pathlib import Path


from io import StringIO

import csv

#-----------------------------

#-----------------------------


###############################################################################

# ### Get information on all SDG Goals
# Get details for the list of 17 SDG Goals from the SDG API
def get_goal_information():
    url = "https://unstats.un.org/SDGAPI/v1/sdg/Goal/List?includechildren=true"
    req = request.Request(url)
    response = urlopen.urlopen(req)
    response_bytes = response.read()
    goals_json_data = json.loads(response_bytes.decode("UTF-8"))
    return goals_json_data


def get_goal_dimensions(goal_code):
    url_dimensions = "https://unstats.un.org/SDGAPI/v1/sdg/Series/"+goal_code+"/Dimensions"
    req = request.Request(url_dimensions)
    response = urlopen.urlopen(req)
    response_bytes = response.read()
    goal_dimensions_json_data = json.loads(response_bytes.decode("UTF-8"))
    return goal_dimensions_json_data


def get_geography():
    url_geography = "https://unstats.un.org/SDGAPI/v1/sdg/GeoArea/Tree"
    req = request.Request(url_geography)
    response = urlopen.urlopen(req)
    response_bytes = response.read()
    geography_json_data = json.loads(response_bytes.decode("UTF-8"))
    return geography_json_data

def process_data_package(goal_code=None):
    
    try:
    
        for goal in get_goal_information():
            
        
            if goal_code is not None and int(goal["code"]) not in goal_code:
                # Skip the code below, and continue with the next goal
                continue
            
            
            print("\nStarted Goal ", goal["code"], "\n" )
            
            #--------------------------------------
            # Create data file for the current goal
            #--------------------------------------
            
            payload = {'goal':str(goal["code"])}

            data_file = os.path.join(path, goal["code"],  "data.csv")
            
            r = requests.post(url, data=payload, headers = headers)
            r.encoding = "UTF-8"
            
            resp = r.text.replace('\0', '')
            resp = resp.replace('\r\n', '\n')
            resp = resp.replace('\u010d','c')
            resp = resp.replace('\u0219','s')
            resp = resp.replace('\u0103','a')
            resp = resp.replace('\u0130','I')
            resp = resp.replace('\x9c','oe')
            resp = resp.replace('\u0151','o') 
            
#            if '\0' in resp:
#                print ("you have null bytes in your input csv")
#            else:
#                print ("you do not have null bytes in your input csv")
#                
#            
#            
#            if '\u010d' in resp:
#                print ("you have LATIN SMALL LETTER C WITH CARON in your input csv")
#            else:
#                print ("you do not have LATIN SMALL LETTER C WITH CARON in your input csv")
#                
           # reader = csv.reader(StringIO(resp), csv.excel)
              
            csv_file = open(data_file , "w")
            csv_file.write(resp)
            csv_file.close()  
            
            data_columns = resp.split('\n')[0].split(',')
            
            
            xData = ""
            count = 0
            for i in data_columns:
                count = count + 1
                if count == 1:
                    xData = xData + "{ \"name\": \"" + i + "\", \"type\": \"string\" }"
                else:
                    xData = xData + ", { \"name\": \"" + i + "\", \"type\": \"string\" }"
                
            
            
            #--------------------------------------------------
            # Create dimensionvalues file for the current goal
            #--------------------------------------------------
            
            dimensionvalues_file = os.path.join(path, goal["code"],  "dimensionvalues.csv")
            
            
            csv_columns = []
            
            dimensions = dict()
            
            csv_file = open(dimensionvalues_file, "w") 
            
            csv_file.write('Dimension, Value, Description\n')
            
            for dimension in get_goal_dimensions(goal["code"]):
               # print("\n\nProcessing dimension", dimension["id"] )
                
                for code in dimension["codes"]:
                    dimensions["Dimension"] = "\"" + dimension["id"].replace("\"", "\"\"") + "\"" 
                    dimensions["Value"] = "\"" + code["code"].replace("\"", "\"\"") + "\""
                    dimensions["Description"] = "\"" + code["description"].replace("\"", "\"\"") + "\""
                    
                    row = dimensions["Dimension"] + "," + dimensions["Value"] + "," + dimensions["Description"] + "\n"
                    csv_file.write(row)
                    
                 #   print(dimensions)
                    
            csv_file.close()  
            
            
            dimensionvalues_columns = 'Dimension,Value,Description'.split(',')
            
            
            xDimensions = ""
            count = 0
            for i in dimensionvalues_columns:
                count = count + 1
                if count == 1:
                    xDimensions = xDimensions + "{ \"name\": \"" + i + "\", \"type\": \"string\" }"
                else:
                    xDimensions = xDimensions + ", { \"name\": \"" + i + "\", \"type\": \"string\" }"

            #--------------------------------------------------
            # Create geography file for the current goal
            #--------------------------------------------------
            
            geography_file = os.path.join(path, goal["code"],  "geography.csv")
            
            
            csv_columns = []
            
            areas = dict()
            
            csv_file = open(geography_file, "w") 
            
            csv_file.write('Lineage, ParentGeoAreaName, ParentGeoAreaCode, GeoAreaName, GeoAreacode, Type\n')
            

            
            for area in get_geography():
                
                if area["geoAreaCode"] == 922:
                    # Skip the code below
                    continue
                
                areas["Lineage"] = "\"" + area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ")" + "\"" 
                areas["ParentGeoAreaName"] = ""
                areas["ParentGeoAreaCode"] = ""
                areas["GeoAreaName"] = "\"" + area["geoAreaName"] + "\"" 
                areas["GeoAreaCode"] = "\"" + str(area["geoAreaCode"]) + "\""
                areas["Type"] = "\"" + area["type"]  + "\""
                
                row = areas["Lineage"] + "," + \
                      areas["ParentGeoAreaName"] + "," + \
                      areas["ParentGeoAreaCode"] + "," + \
                      areas["GeoAreaName"]+ "," + \
                      areas["GeoAreaCode"]+ "," + \
                      areas["Type"] + "\n"
                      
                csv_file.write(row)
                
                # print(area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ")")
                
                if area["geoAreaCode"] != 1:
                    # Skip the code below
                    continue
                
                if area["children"]  is None :
                    # Skip the code below
                    continue
                
                for area2 in area["children"]:
                
                    if area2["geoAreaCode"]  in [62, 419] :
                        # Skip the code below
                        continue
                    
                    areas["Lineage"] = "\"" + area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ")" + "\"" 
                    areas["ParentGeoAreaName"] = "\"" + area["geoAreaName"] + "\"" 
                    areas["ParentGeoAreaCode"] = "\"" + str(area["geoAreaCode"]) + "\""
                    areas["GeoAreaName"] = "\"" + area2["geoAreaName"] + "\"" 
                    areas["GeoAreaCode"] = "\"" + str(area2["geoAreaCode"]) + "\""
                    areas["Type"] = "\"" + area2["type"]  + "\""
                    
                    row = areas["Lineage"] + "," + \
                          areas["ParentGeoAreaName"] + "," + \
                          areas["ParentGeoAreaCode"] + "," + \
                          areas["GeoAreaName"]+ "," + \
                          areas["GeoAreaCode"]+ "," + \
                          areas["Type"] + "\n"
                          
                    csv_file.write(row)
                    
                    # print(area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ")")
                    
                    if area2["children"]  is None :
                        # Skip the code below
                        continue
                    
                    for area3 in area2["children"]:
                        
                        areas["Lineage"] = "\"" + area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ") -- " + area3["geoAreaName"] + " (" + str(area3["geoAreaCode"]) + ")" + "\"" 
                        areas["ParentGeoAreaName"] = "\"" + area2["geoAreaName"] + "\"" 
                        areas["ParentGeoAreaCode"] = "\"" + str(area2["geoAreaCode"]) + "\""
                        areas["GeoAreaName"] = "\"" + area3["geoAreaName"] + "\"" 
                        areas["GeoAreaCode"] = "\"" + str(area3["geoAreaCode"]) + "\""
                        areas["Type"] = "\"" + area3["type"]  + "\""
                        
                        row = areas["Lineage"] + "," + \
                              areas["ParentGeoAreaName"] + "," + \
                              areas["ParentGeoAreaCode"] + "," + \
                              areas["GeoAreaName"]+ "," + \
                              areas["GeoAreaCode"]+ "," + \
                              areas["Type"] + "\n"
                              
                        csv_file.write(row)
                        
                        # print(area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ") -- " + area3["geoAreaName"] + " (" + str(area3["geoAreaCode"]) + ")")
                    
                        if area3["children"]  is None :
                            # Skip the code below
                            continue
                        
                        for area4 in area3["children"]:
                        
                            areas["Lineage"] = "\"" + area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ") -- " + area3["geoAreaName"] + " (" + str(area3["geoAreaCode"]) + ") -- " + area4["geoAreaName"] + " (" + str(area4["geoAreaCode"]) + ")" + "\"" 
                            areas["ParentGeoAreaName"] = "\"" + area3["geoAreaName"] + "\"" 
                            areas["ParentGeoAreaCode"] = "\"" + str(area3["geoAreaCode"]) + "\""
                            areas["GeoAreaName"] = "\"" + area4["geoAreaName"] + "\"" 
                            areas["GeoAreaCode"] = "\"" + str(area4["geoAreaCode"]) + "\""
                            areas["Type"] = "\"" + area4["type"]  + "\""
                            
                            row = areas["Lineage"] + "," + \
                                  areas["ParentGeoAreaName"] + "," + \
                                  areas["ParentGeoAreaCode"] + "," + \
                                  areas["GeoAreaName"]+ "," + \
                                  areas["GeoAreaCode"]+ "," + \
                                  areas["Type"] + "\n"
                                  
                            csv_file.write(row)
                            
                            # print(area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ") -- " + area3["geoAreaName"] + " (" + str(area3["geoAreaCode"]) + ") -- " + area4["geoAreaName"] + " (" + str(area4["geoAreaCode"]) + ")")
                    
                            if area4["children"]  is None :
                                # Skip the code below
                                continue
                            
                            for area5 in area4["children"]:
                        
                                areas["Lineage"] = "\"" + area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ") -- " + area3["geoAreaName"] + " (" + str(area3["geoAreaCode"]) + ") -- " + area4["geoAreaName"] + " (" + str(area4["geoAreaCode"]) + ") -- " + area5["geoAreaName"] + " (" + str(area5["geoAreaCode"]) + ")" + "\"" 
                                areas["ParentGeoAreaName"] = "\"" + area4["geoAreaName"] + "\"" 
                                areas["ParentGeoAreaCode"] = "\"" + str(area4["geoAreaCode"]) + "\""
                                areas["GeoAreaName"] = "\"" + area5["geoAreaName"] + "\"" 
                                areas["GeoAreaCode"] = "\"" + str(area5["geoAreaCode"]) + "\""
                                areas["Type"] = "\"" + area5["type"]  + "\""
                                
                                row = areas["Lineage"] + "," + \
                                      areas["ParentGeoAreaName"] + "," + \
                                      areas["ParentGeoAreaCode"] + "," + \
                                      areas["GeoAreaName"]+ "," + \
                                      areas["GeoAreaCode"]+ "," + \
                                      areas["Type"] + "\n"
                                      
                                csv_file.write(row)
                                
                                # print(area["geoAreaName"] + " (" + str(area["geoAreaCode"]) + ") -- " + area2["geoAreaName"] + " (" + str(area2["geoAreaCode"]) + ") -- " + area3["geoAreaName"] + " (" + str(area3["geoAreaCode"]) + ") -- " + area4["geoAreaName"] + " (" + str(area4["geoAreaCode"]) + ") -- " + area5["geoAreaName"] + " (" + str(area5["geoAreaCode"]) + ")")
                
                    
            csv_file.close() 
            
            
            geography_columns = 'Lineage,ParentGeoAreaName,ParentGeoAreaCode,GeoAreaName,GeoAreacode,Type'.split(',')
            
            xGeography = ""
            count = 0
            for i in geography_columns:
                count = count + 1
                if count == 1:
                    xGeography = xGeography + "{ \"name\": \"" + i + "\", \"type\": \"string\" }"
                else:
                    xGeography = xGeography + ", { \"name\": \"" + i + "\", \"type\": \"string\" }"
                    
            #---------------------------------
            # json datapackage
            #---------------------------------
            
            json_datapackage = """ {{
                    "name": "Goal {xGoal}",
                    "title": "{xGoalTitle}",
                    "description": "{xGoalDescription}",
                    "homepage": "https://unstats.un.org/sdgs",
                    "resources": [{{
                            "name": "data",
                            "path": "data.csv",
                            "format": "csv",
                            "mediatype": "text/csv",
                            "schema": {{ "fields": [{xData}] }}
                            }}, {{
                            "name": "dimensionvalues",
                            "path": "dimensionvalues.csv",
                            "format": "csv",
                            "mediatype": "text/csv",
                            "schema": {{ "fields": [{xDimensions}] }}
                            }}, {{
                            "name": "geography",
                            "path": "geography.csv",
                            "format": "csv",
                            "mediatype": "text/csv",
                            "schema": {{ "fields": [{xGeography}] }}
                            }}
                        ],
                    "sources": [{{
                        "title": "United Nations Statistics Division",
                        "path": "https://unstats.un.org"
                        }}]
            }}""".format(xGoal = goal["code"],
                         xGoalTitle = goal["title"],
                         xGoalDescription = goal["description"],
                         xData = xData,
                         xDimensions = xDimensions,
                         xGeography = xGeography
                        )
             
                
                
            #print(json_datapackage)
            

            data_file = os.path.join(path, goal["code"],  "datapackage.json")
            
            json_file = open(data_file , "w")
            json_file.write(json_datapackage)
            json_file.close()  
            
            print("Finished Goal ", goal["code"], "\n" )



    except:
        
        traceback.print_exc()
        
    return

  
def main():
     # Set up the global information and variables
    global path
    global url
    global headers
    
    global dimensions
    
    path = "C:\\Users\\L.GonzalezMorales\\Documents\\GitHub\\SDG-DataPackages\\DataPackages\\Goal"
    os.chdir(path)

    url = 'https://unstats.un.org/SDGAPI/v1/sdg/Goal/DataCSV'
    headers = {'Content-Type':'application/x-www-form-urlencoded', 
               'Accept':'application/octet-stream'}
     
    process_data_package(goal_code=[17])
    #process_data_package()
    
    dimensions = dict()

    return

#set the primary starting point
if __name__ == "__main__":
    main()      
