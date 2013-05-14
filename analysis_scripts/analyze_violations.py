import operator
import csv

violations = open("/Users/lindsayrgwatt/Desktop/Code_Violation_Cases.csv")

case_type = {}
case_group = {}

violations_reader = csv.reader(violations, delimiter=',', quotechar='"')

counter = 0
for line in violations_reader:
    if counter != 0:
        if line[1] in case_type:
            case_type[line[1]] += 1
        else:
            case_type[line[1]] = 1
        
        if line[4] in case_group:
            case_group[line[4]] += 1
        else:
            case_group[line[4]] = 1
        
    counter += 1


sorted_case_type = sorted(case_type.iteritems(), key=operator.itemgetter(1))

print "///////////////////////////////////"
print "Case Type"

for case in sorted_case_type:
    print case[0], case[1]

print ""
print "///////////////////////////////////"
print "Case Group"

sorted_case_group = sorted(case_group.iteritems(), key=operator.itemgetter(1))

for case in sorted_case_group:
    print case[0], case[1]
