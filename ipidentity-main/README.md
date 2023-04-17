# ipidentity

# Overview

This is a program to evaluate the capabilities of a person to write software.
The applicant shall write a program in either
- Python if possible
- Java


There are two Bonus requirements, which should be completed, but where it is not dramatic if this is not possible.

After finishing the task please zip your result and send it to the human resource responsible person. 
Please don't fork the repository.

If you have any question regarding the requirements make a sensible assumption and document this assumption.

---

The dataset contains 4 text files that represents which IP-addresses are assigned to a customer for a specific period of time. 

## Field description

### customers

| name | description           |
| -----| ----------------------|
| id   | unique ID of customer |
| name | Name of customer      |


### ip-ranges 

| name     | description                               |
| ---------|-------------------------------------------|
| id       | unique id of ip-range                     |
| start_ip | first ip address of the assigned ip range |
| end_ip   | las ip address of the assigned ip range   |

Any IP address between start_ip and end_ip (including start/end) is included in the ip-range


### ip-assignments

| name       | description                             |
| -----------| --------------------------------------- |
| id         | unique id of the ip address assignment  |
| start_date | start date of the ip address assignment |
| end_date   | end date of the ip address assignment   |


### customer2ipassignment

| name             | description                     |
| ---------------- | --------------------------------|
| customer_id      | id of the customer              |
| ip_assignment_id | id of the ip address assignment |



## Requirements

- use a decent Python3 version (>= 3.7) (if you write it in java java>java 11)
- use only modules included in the Python/java standard library, no external depencies allowed

### Tasks

1) Write a function that finds customers that have the given ip address assigned at a specific date. 
    - If no date is given, all assignments should be returned

    Assigned means, that the given IP address is part of an ip-range

2) Write a function that finds the IP of customer at a specific date.
    - If no date is given, show all ip assignments.
    - It should be possible to pass either the customer-id or customer name as parameters
    - customer name may contain only a part of the name, all customers with matching name should be returned


### Bonus Tasks

3) make this functions available as a CLI tool (command line interface)

```
usage: findme.py [-h] [-i] [-c] [-d]

Find IP address assignment

options:
  -h, --help       show this help message and exit
  -i, --ipaddress  ip address
  -c, --customer   customer name or customer ID
  -d, --date   
```

4) make the CLI tool installable with pip (python only)








