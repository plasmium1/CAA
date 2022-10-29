import pandas as pd
from urllib.request import urlopen
import json

curr_page = 0
allpages = []
while True:
    API_URL=(
        f"https://api.data.gov/ed/collegescorecard/v1/schools.json?fields=id,school.name,"
        f"school.state,"
        f"school.city,"
        f"school.zip,"
        f"school.school_url,"
        f"school.price_calculator_url,"
        f"location.lat,"
        f"location.lon,"
        f"school.ownership,"
        f"2020.admissions.admission_rate.overall,"
        f"2019.admissions.admission_rate.overall,"
        f"2020.admissions.sat_scores.average.overall,"
        f"2019.admissions.sat_scores.average.overall,"
        f"2020.admissions.sat_scores.75th_percentile.math,"
        f"2020.admissions.sat_scores.75th_percentile.critical_reading,"
        f"2019.admissions.sat_scores.75th_percentile.math,"
        f"2019.admissions.sat_scores.75th_percentile.critical_reading,"
        f"2020.cost.attendance.academic_year,"
        f"2019.cost.attendance.academic_year,"
        f"2020.student.size,"
        f"2019.student.size,"
        f"latest.programs.cip_4_digit.earnings.highest.3_yr.overall_median_earnings,"
        f"latest.programs.cip_4_digit.title,latest.programs.cip_4_digit.code,"
        f"latest.programs.cip_4_digit.credential.title,"
        f"latest.programs.cip_4_digit.credential.level,"
        f"latest.earnings.10_yrs_after_entry.median,"
        f"latest.cost.avg_net_price.public,"
        f"latest.cost.avg_net_price.private,"
        f"latest.completion.consumer_rate"
        f"&api_key=cAjOlRW1SJa2uqaeJwYYgzjVVzGzFLX1eFEtCIvB&_per_page=100&_page={curr_page}&latest.programs.cip_4_digit.credential.level=3&school.main_campus=1"
    )
    myURL = urlopen(API_URL)
    json_data=json.loads(myURL.read())
    if json_data['results']:
        allpages.append(pd.json_normalize(json_data, 'results'))
    else:
        break
    curr_page += 1
df = pd.concat(allpages,ignore_index=True)
df.rename({
    '2020.admissions.admission_rate.overall':'Latest Admission Rate',
    '2019.admissions.admission_rate.overall':'2019 Admission Rate',
    '2020.admissions.sat_scores.average.overall':'Latest SAT Average',
    '2019.admissions.sat_scores.average.overall':'2019 SAT Average',
    '2020.admissions.sat_scores.midpoint.math':'Latest SAT Math',
    '2020.admissions.sat_scores.midpoint.critical_reading':'Latest SAT Reading',
    '2019.admissions.sat_scores.midpoint.math':'2019 SAT Math',
    '2019.admissions.sat_scores.midpoint.critical_reading':'2019 SAT Reading',
    '2020.admissions.act_scores.midpoint.cumulative':'Latest ACT',
    '2019.admissions.act_scores.midpoint.cumulative':'2019 ACT',
    '2020.cost.attendance.academic_year':'Latest Total Cost',
    '2019.cost.attendance.academic_year':'2019 Total Cost',
    '2020.student.size':'Latest Student Size',
    '2019.student.size':'2019 Student Size',
    'latest.completion.consumer_rate':'Graduation Rate',
    'latest.earnings.10_yrs_after_entry.median':'Median Earnings',
    'location.lat':'Latitude',
    'location.lon':'Longitude',
    'school.name':'Name',
    'school.state':'State',
    'school.city':'City',
    'school.zip':'Zip',
    'school.school_url':'URL',
    'school.price_calculator_url':'Price Calculator',
    'school.ownership':'Type'
    }, axis='columns', inplace=True)
df = df.set_index("id")
df['Type'] = df['Type'].map({1:'Public', 2:'Private NonProfit', 3:'Private ForProfit'})
df['Average Cost'] = df['latest.cost.avg_net_price.public'].combine_first(df['latest.cost.avg_net_price.private'])
df.drop(columns=['latest.cost.avg_net_price.public','latest.cost.avg_net_price.private'], inplace=True)
df.to_csv('~/CAA/dash/data/colleges.csv')