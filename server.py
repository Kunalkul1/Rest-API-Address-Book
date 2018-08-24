import requests
import json
from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify

port_no = 9200

#Create the connection
es = Elasticsearch([{'host': '127.0.0.1', 'port': port_no}])
app = Flask(__name__)
index = "address-book"
doc_type = "contact"
es.indices.create(index=index, ignore=400)

#Testing if default route works
@app.route('/')
def test_default():
    res = requests.get('http://127.0.0.1:9200/')
    return res.content

#Method for handling get all query with page size and page numbers
@app.route('/contact', methods=['GET'])
def get_all_contacts():
    #Input validation and bound checking
    if 'pageSize' in request.args:
        pagesize = int(request.args['pageSize'])
        if pagesize < 1:
            return "ERROR: PageSize is less than 1!\n", 400
    else:
        pagesize = 20

    if 'page' in request.args:
        page = int(request.args['page'])
        if page < 1:
            return "ERROR: Page number less than 1!\n", 400
    else:
        page = 1

    #Default field in query is name. If another field is specified, it will map the query to that field.
    if 'query' in request.args:
        query_string = request.args['query']
        query = {"query": {"query_string":{ "default_field" : "name",
            "query" : query_string}}}
    else:
        #Return all by default
        query = {"query": {"match_all": {} }}
    
    #Search and collect all matches into result list
    res = es.search(index=index, doc_type=doc_type, body=query)
    result = []
    count = int(res ['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s" % (doc['_source']))
        result.append(doc)

    #Paging logic
    if page > 1:
        if count > pagesize*(page-1):
            if count < pagesize*page:
                return jsonify(result[pagesize*(page-1):count])
            else:
                return jsonify(result[pagesize*(page-1):pagesize*page])
        else:
            return "ERROR: Page does not exist, since there are not enough results!\n", 400
    else:
        if count > pagesize:
            return jsonify(result[0:pagesize])
        else:
            return jsonify(result[0:count])


#Method for GET, PUT and DELETE requests
@app.route('/contact/<name>', methods=['GET', 'PUT', 'DELETE'])
def do_something_to_contact(name):
    user_id = []
    result = []

    #Query all matches and store in res
    res = es.search(index=index, doc_type=doc_type, body={"query": {"match": {"name":name}}})

    #If no hits, return ERROR message
    if res["hits"]["total"] == 0:
        return "ERROR: No matches\n", 400

    #Otherwise collect all matching ID's
    for doc in res['hits']['hits']:
        user_id.append(doc['_id'])

    #Handle GET request
    if request.method == 'GET':
        for doc in res['hits']['hits']:
            result.append(doc)
        return jsonify(result)

    #Handle PUT request
    elif request.method == 'PUT':
        if request.get_json().get("number") is None:
            return "ERROR: number field missing from JSON!", 400
        else:
            number = request.get_json().get("number")
        for i in user_id:
            res = es.update(index=index, refresh=True, doc_type=doc_type, id=i, body={"doc": {"name": name, "number": number }})
            result.append(res)
        return jsonify(result)

    #Handle Delete request
    elif request.method == 'DELETE':
        #Iterate and delete every matching entry
        for i in user_id:
            res = es.delete(index=index, doc_type=doc_type, id=i, refresh=True)
            result.append(res)
        return jsonify(result)


#Method for POST request to create new contact
@app.route('/contact', methods=['POST'])
def create_contact():
    #Check if name is present in request body
    if request.get_json().get("name") is None:
        return "ERROR: Name field missing in request!\n", 400
    else:
        name = request.get_json().get("name")

    #Check if number is present in request body
    if request.get_json().get("number") is None:
        return "ERROR: number field missing in request!\n", 400
    else:
        number = request.get_json().get("number")
    
    #Check bounds for phone number
    if int(number) > 999999999999999:
        return "ERROR: (Phone number cannot be of more than 15 digits!)\n", 400
    elif int(number) < 0:
        return "ERROR: (Phone number cannot be of less than 0 digits!)\n", 400
    else:
        #Check if name has only alphabets
        if name.isalpha() is False:
            return "ERROR: Name can only have alphabets!\n", 400
        else:
            res = es.search(index=index, doc_type=doc_type, body={"query": {"match": {"name":name}}})
            
            #Return error message if duplicates are present
            if res['hits']['total'] is not 0:
                print(res)
                return "ERROR: Name already exists in database \n", 400

            #Else create new contact
            res = jsonify(es.index(index=index, refresh=True, doc_type=doc_type, body={"name": name, "number": number}))
    
    return res


#404 error handler
@app.errorhandler(404)
def page_not_found(e):
    res = "ERROR: The function you requested does not exist. Try a different route or method!\n"
    return res, 400

#Main
if __name__ == '__main__':
    app.run()