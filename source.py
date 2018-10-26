import os
import csv
import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET


# DEFINE TWO LISTS TO STORE VALUES
list_of_tags = []
list_of_counts = []


# FIND FILE PATH OF DATASET.
file_name = "stackoverflow_tags.xml"
full_file = os.path.abspath(file_name)

# SET UP AN ELEMENT TREE AND FIGURE OUT THE ROOT OF THE XML FILE.
tree = ET.parse(full_file)
root = tree.getroot()                           # ROOT = 'tags'

# LOOP THROUGH DATASET AND APPEND TAG NAMES AND HOW MANY TIMES EACH TAG HAS BEEN USED TO RESPECTIVE LISTS.
for child in root:
    list_of_tags.append(child.attrib['TagName'])
    list_of_counts.append(child.attrib['Count'])

# MAKE LIST LOWERCASE
lower_list_of_tags = [x.lower() for x in list_of_tags]

# MAKE DICTIONARY FROM THE TWO LISTS.
data_dict = dict(zip(lower_list_of_tags, list_of_counts))

# OPEN UP CSV FILE CONTAINING ALL PROGRAMMING LANGUAGES LISTED ON WIKIPEDIA TO USE FOR CROSS REFERENCING
# IN ORDER TO ELIMINATE TAGS THAT ARE NOT FOR PROGRAMMING LANGUAGES. STORE LANGUAGE NAMES IN A LIST AND
# THEN CONVERT LIST TO A SET FOR OPTIMIZATION PURPOSES.
with open('languages.csv') as my_csv_file:
    reader = csv.reader(my_csv_file, delimiter=',')
    
    language_list = []

    for row in reader:
        language_list.append(row[0])
   
    lower_language_list = [x.lower() for x in language_list]
    language_set = set(lower_language_list)

# COMPARE DATA_DICT WITH LANGUAGE_SET TO FIND COMMON VALUES. REMOVE UNSHARED VALUES.
final_dict = {k: int(v) for (k,v) in data_dict.items() if k in language_set}

# SORT FINAL DICTIONARY BY VALUE. UNCOMMENT PRINT LINES TO SHOW ALL OF THE PROGRAMMING LANGUAGE TAGS AND THEIR NUMBER OF USES ON STACK OVERFLOW.
dict_sorted_by_value = sorted(final_dict.items(), key=lambda kv: kv[1])
#print('DICT_SORTED_BY_VALUE:')
#print(dict_sorted_by_value)

chart_labels = []
chart_sizes = []

for key, value in dict_sorted_by_value:
	chart_labels.append(key)
	chart_sizes.append(value)

# SET UP PIE CHART
labels = chart_labels[-10:]
sizes = chart_sizes[-10:]
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
