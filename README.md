# Rest-API-Address-Book
This is a RESTful API for an address book with an Elasticsearch data store. It is developed using Python & the Flask framework.
## Functionality
The endpoints in the API are as follows:
1. GET /contact?pageSize={}&page={}&query={}  
This endpoint provides a listing of all contacts. If the pageSize parameter is specified, only those number of results are shown. By default, the field in the query parameter is "name". If a different field is specified, it is mapped to that field. For e.g. query=number:2 will set the number field of the entry to 2.  
2. POST /contact  
3. GET /contact/{name}  
4. PUT /contact/{name}  
5. DELETE /contact/{name}  


