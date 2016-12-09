#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Pierre Haessig — December 2016
""" A script to download Airquality data from http://www.airbreizh.asso.fr/,
(data that is used by the Flash applet)

"""

import requests
import re
from itertools import groupby

city_names = {
    1: 'Rennes',
    2: 'Brest',
    4: 'Lorient ou Vannes',
    5: 'Vannes ou Lorient',
    6: 'St Brieuc',
    8: 'St Malo',
    9: 'Fougères',
}

def get_airdata(day='today'):
    '''download the raw air data string for `day`
    
    Parameter `day`: 'hier', 'today' or 'demain'
    
    Returns raw string response from the POST request
    '''
    if not day in ['hier', 'today', 'demain']:
        raise ValueError("`day` should be 'hier', 'today', or 'demain', but is {!r} instead.".format(day))
    
    r = requests.post("http://www.airbreizh.asso.fr/index.php?id=36", data={'q': day})
    if r.status_code == 200:
        airdat = r.text
    else:
        raise IOError('Erreur de connexion à Airbreizh: {} {}'.format(r.status_code, r.reason))
    return airdat

def decode_elem(elem):
    '''decode an item of the Airbreizh data response
     
    Each eleme is either of the style 
     * "PM10=8" → detected by RE pattern 1
     * or "2[PM10]=6" → detected by RE pattern 2
    
    Returns:
     * for example 1:  (0, 'PM10', 8)
     * for example 2:  (2, 'PM10', 6)
    '''
    pat1 = r'^(\w+)=(\d)$'
    pat2 = r'^(\d)\[(\w+)\]=(\d)$'
    m1 = re.match(pat1, elem)
    m2 = re.match(pat2, elem)
    
    if m1 is None and m2 is None:
        raise ValueError('Element {!r} doesn\'t match any decoding pattern'.format(elem))
    if m1 is not None and m2 is not None:
        raise ValueError('Element {!r} matches both decoding patterns (should never happen)'.format(elem))
    
    if m1:
        return (0, m1.group(1), int(m1.group(2)))
    if m2:
        return (int(m2.group(1)), m2.group(2), int(m2.group(3)))


def parse_airdat(airdat):
    '''parse the raw airdat string
    
    returns a nice dict of dict:
    {city => {polluant => value }}
    '''
    airdat = airdat.split('&')
    assert airdat[0] == 'done=1'
    assert airdat[-2].startswith('laDate=')
    date = airdat[-2][7:]
    
    assert airdat[-1].startswith('sortie=')
    airdat = airdat[1:-2]
    
    airdat = map(decode_elem, airdat)

    groups = []
    for i, group in groupby(airdat, lambda e: e[0]):
        gp_dict = dict([(code, val) for j,code,val in group])
        groups.append(gp_dict)
    
    cities = {}
    for gp_dict in groups:
        city_idx = gp_dict['city']
        # gp_dict.pop('city')
        if city_idx in city_names:
            city = city_names[city_idx]
        else:
            # unknown city index
            city = 'City {:d}'.format(city_idx)
        
        cities[city] = gp_dict
    return cities, date


def print_cities(cities):
    '''pretty table print of air pollution in cities'''
    print('              City: Ind| SO2 NO2 O3 PM10')
    for city in sorted(cities):
        data = cities[city]
        print('{:>18}:  {Val} | {SO2} {NO2} {O3} {PM10}'.format(city, **data))


if __name__ == '__main__':
    # minimalist command line interface:
    import sys
    if len(sys.argv)>1:
        day = sys.argv[1]
    else:
        day = 'today'
        
    airdat = get_airdata(day)
    cities, date = parse_airdat(airdat)

    print('Air quality for {} ({})'.format(day, date))
    print_cities(cities)

