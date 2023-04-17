import csv
import datetime
import ipaddress

class customers:
    id = list()
    name = list()
    def __init__(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0: continue
                self.id.append(row[0])
                self.name.append(row[1])
class customer2IP:
    customer_id = list()
    ip_assignment_id = list()
    def __init__(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0: continue
                self.customer_id.append(row[0])
                self.ip_assignment_id.append(row[1])    
class ipAssignments:
    id = list()
    ip_range_id = list()
    start_date= list()
    end_date = list()
    def __init__(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0: continue
                self.id.append(row[0]) 
                self.ip_range_id.append(row[1]) 
                l = row[2].split('-')
                self.start_date.append(datetime.datetime(int(l[0]),int(l[1]),int(l[2])))
                li2 = row[3].split('-')
                self.end_date.append(datetime.datetime(int(li2[0]),int(li2[1]),int(li2[2])))
class ipRange:
    id = list()
    start_ip = list()
    end_ip = list()
    def __init__(self, path):
        with open(path, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for i, row in enumerate(reader):
                if i == 0: continue
                self.id.append(row[0]) 
                self.start_ip.append(ipaddress.ip_address(row[1]))
                self.end_ip.append(ipaddress.ip_address(row[2]))
# TASK 1 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def getCustomerID(input_assignmentID):
    global customer2ipCSV
    customerIdIndex = customer2ipCSV.ip_assignment_id.index(input_assignmentID)
    return customer2ipCSV.customer_id[customerIdIndex]
def isIPPartOfRange(input_ipadress, input_rangeID):
    global ipRangeCSV
    try:
        idIndex = ipRangeCSV.id.index(str(input_rangeID))
    except ValueError:
        return False
    if input_ipadress >= ipRangeCSV.start_ip[idIndex] and input_ipadress <= ipRangeCSV.end_ip[idIndex]:
        return True
    return False  
def searchIPRange(input_ipadress):
    for f_id, f_start, f_end in zip(ipRangeCSV.id, ipRangeCSV.start_ip, ipRangeCSV.end_ip):
        if input_ipadress >= f_start and input_ipadress <= f_end:
            return f_id
    return -1
def getAssignmentID(input_ipadress,input_date):
    global ipAssignmentsCSV
    for f_id_assignment, f_ip_range_id, f_startDate, f_endDate in zip(ipAssignmentsCSV.id, ipAssignmentsCSV.ip_range_id , ipAssignmentsCSV.start_date, ipAssignmentsCSV.end_date):
        if input_date >= f_startDate and input_date <= f_endDate:
            if isIPPartOfRange(input_ipadress, f_ip_range_id):
                return getCustomerID(f_id_assignment)   
    return '-1'
def printName(input_customerid):
    for f_id, f_name in zip(customerCSV.id, customerCSV.name):
        if f_id == input_customerid:
            print(f_name)
def iterateAdressAssignmentsWithRangeID(input_range_id):
    global ipAssignmentsCSV
    for f_id_assign, f_id_range in zip(ipAssignmentsCSV.id,ipAssignmentsCSV.ip_range_id):
        if f_id_range == input_range_id:
            customerid = getCustomerID(f_id_assign)
            printName(customerid)
def findCustomer(input_ipadress, input_date): # Main Call
    if input_date != None:
        customerid = getAssignmentID(input_ipadress,input_date)
        if customerid == '-1': 
            print("Nothing found")
            return
        printName(customerid)
    else:
        ip_range_id = searchIPRange(input_ipadress)
        if ip_range_id != -1:
            iterateAdressAssignmentsWithRangeID(ip_range_id)
        else: print("IP not found")

# TASK 2 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def printIPRange(input_rangeID):
    global ipRangeCSV
    try:
        index = ipRangeCSV.id.index(input_rangeID)
    except ValueError:
        print("No IP Range found")
        return 
    print(str(ipRangeCSV.start_ip[index]) + "-" + str(ipRangeCSV.end_ip[index]))
def AssignIDtoRangeID(input_assignID, input_date, input_CustomerID):
    for f_assign_id, f_range_id, f_startDate, f_endDate in zip(ipAssignmentsCSV.id, ipAssignmentsCSV.ip_range_id, ipAssignmentsCSV.start_date, ipAssignmentsCSV.end_date):
        if input_assignID == f_assign_id:
            if input_date is None or (input_date >= f_startDate and input_date <= f_endDate):
                print("IP Range for " + customerCSV.name[customerCSV.id.index(input_CustomerID)] + ": ")
                printIPRange(f_range_id)        
def searchAssignID(input_CustomerID,input_date):
    global customerCSV
    for f_customer_id, f_asign_id in zip(customer2ipCSV.customer_id, customer2ipCSV.ip_assignment_id):
        if input_CustomerID == f_customer_id:
            AssignIDtoRangeID(f_asign_id, input_date, input_CustomerID)
def findIP(input_customer, input_date): # Main Call
    global customerCSV
    for f_name, f_customerid in zip(customerCSV.name, customerCSV.id):
        if input_customer in f_name or input_customer == f_customerid:
            searchAssignID(f_customerid,input_date)

# THE CSV FILES STORED AS OBJECTS
customerCSV = customers("dataset/customer.csv")
customer2ipCSV = customer2IP("dataset/customer2ipassignment.csv")
ipAssignmentsCSV = ipAssignments("dataset/ip-assignments.csv")
ipRangeCSV = ipRange("dataset/ip-ranges.csv")

# USING THE PROGRAMM
# TASK 1
searchIP = ipaddress.ip_address("10.160.189.177")
searchDate = datetime.datetime(2020, 4, 1)
print("Searching Customer who used the IP: " + str(searchIP) + " at the date " + str(searchDate))
findCustomer(searchIP, searchDate)

searchIP = ipaddress.ip_address("10.231.183.135")
searchDate = None
print("Searching Customer who used the IP: " + str(searchIP) + " at the date " + str(searchDate))
findCustomer(searchIP, searchDate)

searchIP = ipaddress.ip_address("1.1.1.1")
searchDate = None
print("Searching Customer who used the IP: " + str(searchIP) + " at the date " + str(searchDate))
findCustomer(searchIP, searchDate)

searchIP = ipaddress.ip_address("192.168.150.255")
searchDate = datetime.datetime(2020,11,30)
print("Searching Customer who used the IP: " + str(searchIP) + " at the date " + str(searchDate))
findCustomer(searchIP, searchDate)
# TASK 2
findIP("Fiebig", datetime.datetime(2022, 4, 1))
findIP("Ha", None)
findIP("Christoph GmbH & Co. OHG", None)
