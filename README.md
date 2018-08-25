# Rest-API-Address-Book
This is a RESTful API for an address book with an Elasticsearch back end. It is developed using Python3 & the Flask framework on Windows 10.

## Setup
ElasticSearch needs to be installed on the system. To do so, [follow this link]( https://www.elastic.co/guide/en/elasticsearch/reference/5.1/windows.html). Java8 and Python3 also need to be installed on the system.  

For setting the host/port of ElasticSearch manually, you can edit the host/port_no variable in server.py.  

***Before starting the server, ElasticSearch needs to be running on the system.***

**Run the following commands to activate the Virtual Environment and start the server:**  
```
cd Rest-API-Address-Book
.\env\Scripts\activate
python server.py
```

**In another Powershell Window, run the following commands to run the test cases:**  
```
cd Rest-API-Address-Book
.\env\Scripts\activate
python test.py
```

## Functionality
The endpoints in the API are as follows:
**1. GET /contact?pageSize={}&page={}&query={}**  
This endpoint provides a listing of all contacts. If the pageSize parameter is specified, only those number of results are shown. By default, the field in the query parameter is "name". If a different field is specified, it is mapped to that field. For e.g. query=number:2 will set the number field of the entry to 2.  
**2. POST /contact**  
This endpoint creates the contact. The name is checked for uniqueness and a new contact is only created if the name is unique.
**3. GET /contact/{name}**  
This endpoint returns the contact by a unique name.  
**4. PUT /contact/{name}**  
This endpoint updates the contact by a unique name (and returns an error if not found).  
**5. DELETE /contact/{name}**  
This endpoint deletes the contact by a unique name (and returns an error if not found).  

## Data Model Design
* A contact consists of 2 attributes: name and number. Name is a string, which can consist only of alphabets. The maximum length of the number attribute can be 15 digits, taking into consideration the [Telephonic numbering plan](https://en.wikipedia.org/wiki/Telephone_numbering_plan). If the bounds of the name or number attribute are violated, an appropriate error message is returned. 
* The name attribute of the contact is unique. If a POST request consisting of a duplicate name is submitted, an appropriate error message is returned.

## Unit Tests
The file test.py contains unit tests. Different test cases have been considered while writing this file.
