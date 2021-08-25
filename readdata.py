
import json
import datetime
import pandas as pd

delta_lon =  118.1324 - 118.1319

lon = -118.13247

max_lon = -118.131692
min_lon = -118.132749

#min_lon = lon - delta_lon
#max_lon = lon + delta_lon

min_lat = 34.151284
max_lat = 34.161954

def read_data():

    count = 0
    killed = 0
    injured = 0
    
    lat = []
    lon = []
    injury = []
    death  = []
    date_arr = []


    with open('Traffic_Collisions.geojson', 'r') as infile: 
        data = json.loads(infile.read())

    for crash in data['features']:
    #print(crash['properties'].keys())

        info = crash['properties']
        lon_c, lat_c  = crash['geometry']['coordinates']

        #if ('LAKE' in info['Street']): 
        #    print(info['Street'])
        #    count += 1
        #    print(lon, lat)

        if lon_c > min_lon and lon_c < max_lon:
            if lat_c < max_lat and lat_c > min_lat:
                count += 1
                #print(info['Street'])
                #print(info['CrossSt'])
        
                #print(info['Date'])
            
                date = datetime.datetime.strptime(info['Date'], '%m/%d/%Y')
                #print(date)
                
                killed += int(info['NoKilled'])
                injured += int(info['NoInjured'])
                
                lat.append(lat_c)
                lon.append(lon_c)
                injury.append(int(info['NoInjured']))
                death.append(int(info['NoKilled']))
                date_arr.append(date)
                
    #print(count, injured, killed)


    lake_data =  pd.DataFrame({
        'lat': lat,
        'lon': lon,
        'date'   : date_arr,
        'injury' : injury,
        'death' : death
    })

    return(lake_data)


