"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    times = {'200': 34, '300': 32, '400': 32, '600': 30, '1000': 28}
    above200 = 200 / times['200']
    above300 = above200 + 100 / times['300']
    above400 = above300 + 100 / times['400']
    above600 = above400 + 200 / times['600']
    above1000 = above600 + 400 / times['1000']
    over = {'200': above200, '300': above300, '400': above400, '600': above600, '1000': above1000}
    if control_dist_km >= brevet_dist_km:
       hours = over[str(brevet_dist_km)]
    else:  
      if control_dist_km < 200:
         hours = control_dist_km / times['200']
      elif control_dist_km >= 200 and control_dist_km < 300:
         hours = above200 + (control_dist_km - 200) / times['300']
      elif control_dist_km >= 300 and control_dist_km < 400:
         hours = above300 + (control_dist_km - 300) / times['400']       
      elif control_dist_km >= 400 and control_dist_km < 600:
         hours = above400 + (control_dist_km - 400) / times['600'] 
      else:
         hours = above600 + (control_dist_km - 600) / times['1000']
    minutes = round(hours * 60)
    return brevet_start_time.shift(minutes=minutes)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  A date object (arrow)
    Returns:
       A date object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    times = {'200': [15, 13.5], '300': [15, 20], '400': [15, 27], '600': [15, 40], '1000': [11.428, 75]}
    if control_dist_km >= brevet_dist_km:
       hours = times[str(brevet_dist_km)][1]
    else:
      above200 = 200 / times['200'][0]  
      above300 = above200 + 100 / times['300'][0]
      above400 = above300 + 100 / times['400'][0]
      above600 = above400 + 200 / times['600'][0]
      if control_dist_km < 200:
         hours = control_dist_km / times['200'][0]
      elif control_dist_km >= 200 and control_dist_km < 300:
         hours = above200 + (control_dist_km - 200) / times['300'][0]
      elif control_dist_km >= 300 and control_dist_km < 400:
         hours = above300 + (control_dist_km - 300) / times['400'][0]
      elif control_dist_km >= 400 and control_dist_km < 600:
         hours = above400 + (control_dist_km - 400) / times['600'][0]
      else:
         hours = above600 + (control_dist_km - 600) / times['1000'][0]
      if control_dist_km < 60:
         hours = hours + (60 - control_dist_km)/60
    minutes = round(hours*60)
    return brevet_start_time.shift(minutes = minutes)



t = arrow.get('2020-01-01T00:00:00')
a = str(open_time(599, 600, arrow.get('2020-01-01T00:00:00')))
b = "2020-01-01T04:00:00+00:00".strip()
print(a)