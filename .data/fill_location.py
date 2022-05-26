import csv
from accounts.models import Location
with open('E:/projet/frontend/backend/data/wilaya.csv', 'r', encoding="latin1") as wilaya_file:
    reader = csv.reader(wilaya_file)
    next(reader, None)  # to jump a line
    for row in reader:
        Location.objects.create(state_name=row[0], state_number=row[1])
        """ 
        This code do an insert SQL statement behind the scenes 
        An alternative code -->
            a = Location.objects.create(state_number=i[0], state_name=i[1])
            a.save() 
        """
