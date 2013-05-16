import operator
import csv

# UPDATE THESE WITH CORRECT PATH
calls = open("/Users/lindsayrgwatt/Desktop/Seattle_Police_Department_911_Incident_Response.csv")
incidents = open("/Users/lindsayrgwatt/Desktop/Seattle_Police_Department_Police_Report_Incident.csv")

summary_codes = {}
codes = {}
cases = set()

# 911 Calls

reader = csv.reader(calls, delimiter=',', quotechar='"')

counter = 0
for line in reader:
    if counter != 0:
        if line[4] in codes:
            codes[line[4]] += 1
        else:
            codes[line[4]] = 1
        
        cases.add(line[2])
        
        if line[6] in summary_codes:
            summary_codes[line[6]] += 1
        else:
            summary_codes[line[6]] = 1
        
    counter += 1


sorted_911_codes = sorted(codes.iteritems(), key=operator.itemgetter(1))
sorted_911_summary_codes = sorted(summary_codes.iteritems(), key=operator.itemgetter(1))

print "///////////////////////////////////"
print "911 Codes"

for case in sorted_911_codes:
    print case[0], case[1]

print ""
print "///////////////////////////////////"
print "911 Summary Codes"

for case in sorted_911_summary_codes:
    print case[0], case[1]

# All police incidents

incident_reader = csv.reader(incidents, delimiter=',', quotechar='"')

offense_types = {}
summarized_offense_types = {}
reported_cases = set()

counter = 0
for line in incident_reader:
    if counter != 0:
        if line[4] in offense_types:
            offense_types[line[4]] += 1
        else:
            offense_types[line[4]] = 1
        
        reported_cases.add(line[1])
        
        if line[6] in summarized_offense_types:
            summarized_offense_types[line[6]] += 1
        else:
            summarized_offense_types[line[6]] = 1
        
    counter += 1


sorted_offense_types = sorted(offense_types.iteritems(), key=operator.itemgetter(1))
sorted_summarized_offense_types = sorted(summarized_offense_types.iteritems(), key=operator.itemgetter(1))

print "///////////////////////////////////"
print "Reported Offense Types"

for case in sorted_offense_types:
    print case[0], case[1]

print ""
print "///////////////////////////////////"
print "Reported Summary Offense Types"

for case in sorted_summarized_offense_types:
    print case[0], case[1]

# Calculate overlap

print ""
print "Number of 911 cases: %d" % len(cases)
print ""
print "Number of reported cases: %d" % len(reported_cases)
print ""
print "Number of overlapping cases: %d" % len(cases.intersection(reported_cases))

# Merge all the summary offenses and print by key name
merged_summary = summary_codes

for key in summarized_offense_types:
    if key in merged_summary:
        merged_summary[key] += summarized_offense_types[key]
    else:
        merged_summary[key] = summarized_offense_types[key]

keys = merged_summary.keys()
keys.sort()

print ""
print "Aggregate offense codes:"
for key in keys:
    print "%s :: %d" % (key, merged_summary[key])
