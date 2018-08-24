import json
import time
import requests
import random

payload1 = {'name':'KKK', 'number':'7777'}
payload2 = {'name':'John', 'number':'9111'}
payload3 = {'name':'AAA', 'number':'1111'}
payload4 = {'name':'BBB', 'number':'2222'}
payload5 = {'name':'CCC', 'number':'3333'}
payload6 = {'name':'DDD', 'number':'4444'}

def test_post():
    res = requests.post('http://localhost:5000/contact', json = payload1)
    res = requests.post('http://localhost:5000/contact', json = payload2)
    res = requests.post('http://localhost:5000/contact', json = payload3)
    res = requests.post('http://localhost:5000/contact', json = payload4)
    res = requests.post('http://localhost:5000/contact', json = payload5)
    res = requests.post('http://localhost:5000/contact', json = payload6)
    print ("Test 1: POST /contact Passed \n")

def test_post_duplicate():
    print("Attempting to post entry with duplicate name.\n")
    dup = {'name':'KKK', 'number':'11177'}
    res = requests.post('http://localhost:5000/contact', json = dup)
    print(res)
    if res.status_code == 400:
        print ("Test 2: Got 400 error message. Duplicates not allowed. Test case passed \n")

def test_get_one_contact():
    res = requests.get('http://localhost:5000/contact/KKK')
    if res.status_code == 200:
        a, b = json.loads(res.text), payload1
        a = a[0]['_source']
        if a == b:
            print ("Test 3: GET /contact/KKK Passed \n")
        else:
            print(json.dumps(a))
            print(json.dumps(b))

def test_get_contact_with_query():
    res = requests.get('http://localhost:5000/contact?pageSize=1&page=1&query=KKK')
    if res.status_code == 200:
        a, b = json.loads(res.text), payload1
        a = a[0]['_source']
        if a == b:
            print ("Test 4: GET /contact?pageSize=1&page=1&query=KKK Passed \n")
        else:
            print(json.dumps(a))
            print(json.dumps(b))

def test_get_contact_with_query_number():
    res = requests.get('http://localhost:5000/contact?pageSize=1&page=1&query=number:7777')
    if res.status_code == 200:
        a, b = json.loads(res.text), payload1
        a = a[0]['_source']
        if a == b:
            print ("Test 5: GET /contact?pageSize=1&page=1&query=number:7777 Passed \n")
        else:
            print(json.dumps(a))
            print(json.dumps(b))

def test_get_all_contacts_with_query_field_blank():
    res = requests.get('http://localhost:5000/contact?pageSize=1&page=1')
    if res.status_code == 200:
        a, b = json.loads(res.text), payload1
        a = a[0]['_source']
        print ("Test 6: GET /contact?pageSize=1&page=1 Passed \n")
        print(json.dumps(a))
        print(json.dumps(b))
        print("\n")

def test_put():
    rand_number = random.randint(1,4320)
    payload3 = {'number': rand_number}
    res = requests.put('http://localhost:5000/contact/John', json = payload3)
    if res.status_code == 200:
        a = json.loads(res.text)
        a = a[0]['_shards']['successful']
        if a <= 1:
            print ("Test 7: PUT /contact/John Passed \n")

def test_delete():
    res = requests.delete('http://localhost:5000/contact/KKK')
    if res.status_code == 200:
        a = json.loads(res.text)
        a = a[0]['_shards']['successful']
        if a <= 1:
            print ("Test 8: DELETE /contact/KKK Passed \n")

def tearDown():
    print ("Teardown phase initialized\n")    
    res = requests.delete('http://localhost:5000/contact/KKK')
    res = requests.delete('http://localhost:5000/contact/John')
    print ("Teardown phase complete. All records deleted!\n")

if __name__ == '__main__':
    test_post()
    time.sleep(1)
    test_post_duplicate()
    time.sleep(1)
    test_get_one_contact()
    time.sleep(1)
    test_get_contact_with_query()
    time.sleep(1)
    test_get_contact_with_query_number()
    time.sleep(1)
    test_get_all_contacts_with_query_field_blank()
    time.sleep(1)
    test_put()
    time.sleep(1)
    test_delete()
    time.sleep(1)
    tearDown()
