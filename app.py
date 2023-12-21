#Imports:
import os
from flask import Flask,request, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import DB_Requests_creation_insertion as plzHireMe
# at the start of the project i used DB_Requests_creation_insertion file as a source file of all sql commands used

load_dotenv()# this function load .env file variable in ur flask app

#setting a flask app
app = Flask(__name__)

#mysql configuration for connection setup
app.config['MYSQL_HOST']= os.getenv('MYSQL_HOST')
app.config['MYSQL_USER']= os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD']=os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB']= os.getenv('MYSQL_DB')

mysql =MySQL(app)




@app.route('/')
def hello_world():
    return 'Hello World!'

#insert functions :

@app.post('/api/user/insert')
def insert_user():
    try:
        data = request.get_json() #extract json data from the request
        user_id = data.get("user_id")
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        address = data.get("address")
        phone_number = data.get("phone_number")
        email = data.get("email")
        cur = mysql.connection.cursor()
        cur.execute(plzHireMe.create_user_table)  # we execute commands with cursor we create a new table user if it doenst exist
        cur.execute(plzHireMe.insert_user, (user_id, firstname, lastname, address, phone_number, email))
        mysql.connection.commit() # commit the request
        cur.close()
        return jsonify({'message': f'user with id : {user_id} inserted successfully'})
        #to convert the python dictionarry into a json formatted response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.post('/api/meter/insert')
def insert_meter():
    try:
        data = request.get_json()
        meter_id = data.get("meter_id")
        meter_location = data.get("meter_location")
        user_id = data.get("user_id")
        cur = mysql.connection.cursor()
        cur.execute(plzHireMe.create_meter_table)  # we execute commands with cursor
        cur.execute(plzHireMe.insert_meter, (meter_id, meter_location, user_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'meter with id : {meter_id} owned by the user with the id :{user_id} inserted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.post('/api/bill/insert')
def insert_bill():
    try:

        data = request.get_json()

        meter_id = data.get("meter_id")

        bill_id = data.get("bill_id")
        user_id = data.get("user_id")
        bill_date=data.get("bill_date")
        due_date = data.get("due_date")
        total_amount=data.get("total_amount")
        payment_status=data.get("payment_status")
        cur = mysql.connection.cursor()
        cur.execute(plzHireMe.create_bill_table)  # we execute commands with cursor
        cur.execute(plzHireMe.insert_bill, (bill_id,bill_date,due_date,total_amount,payment_status,user_id,meter_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'bill with id : {bill_id} of the meter with id :{meter_id} owned by the user with the id :{user_id} inserted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.post('/api/electricity_reading/insert')
def insert_electricity_reading():
    try:

        data = request.get_json()

        meter_id = data.get("meter_id")
        reading_id = data.get("reading_id")
        reading_date=data.get("reading_date")
        reading_value = data.get("reading_value")

        cur = mysql.connection.cursor()
        cur.execute(plzHireMe.create_electricity_table)  # we execute commands with cursor
        cur.execute(plzHireMe.insert_electricity_reading, (reading_id ,reading_date,reading_value, meter_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'electricity reading with id : {reading_id} of the meter with id :{meter_id} inserted successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#select functions :

#we pass the value in the api endpoint :
@app.get('/api/user/<int:user_id>')
def select_user_with_id(user_id):
 #starting from here we stoped using DB_Requests_creation_insertion file for sql requests
    query = f"SELECT * FROM electricity_bill_management_system_db.user WHERE user_id={user_id} "

    try: #connection
        cur = mysql.connection.cursor()

        cur.execute(query)  # we execute commands with cursor
        fetchdata = cur.fetchall() #it retrieves all the rows of the result set of the last executed query.
        cur.close()
        user = [
            {'user_id': user[0], 'firstname': user[1], 'lastname': user[2], 'address': user[3], 'phone_number': user[4],
             'email': user[5]} for user in fetchdata]
        return jsonify({"user": user})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

#select all of users or with parameters
@app.get('/api/user/')
def get_user_table_records():
    try:
        # Extract parameters from the URL
        firstname=request.args.get('firstname')
        address = request.args.get('address')
        user_id=request.args.get('user_id')
        lastname = request.args.get('lastname')
        phone_number = request.args.get('phone_number')
        email=request.args.get('email')
        query =("select * from electricity_bill_management_system_db.user")

        if lastname is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.user WHERE lastname={lastname}"
        elif phone_number is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.user WHERE phone_number={phone_number}"

        elif firstname is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.user WHERE firstname={firstname}"
        elif address is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.user WHERE address={address}"
        elif email is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.user WHERE email={email}"
        elif user_id is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.user WHERE user_id={user_id}"

        cur = mysql.connection.cursor()

        cur.execute(query)  # we execute commands with cursor
        fetchdata = cur.fetchall()
        cur.close()
        user = [
           {'user_id': user[0], 'firstname': user[1], 'lastname': user[2], 'address': user[3], 'phone_number': user[4],
         'email': user[5]} for user in fetchdata]
        return jsonify({"user": user})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.get('/api/meter/')
def get_meter_table_records():
    try:
        meter_id = request.args.get('meter_id')
        meter_location = request.args.get('meter_location')
        user_id = request.args.get('user_id')

        query = ("select * from electricity_bill_management_system_db.meter")
# return the record based on the json format parameter ur passing on
        if meter_id is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.meter WHERE meter_id={meter_id}"
        elif meter_location is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.meter WHERE meter_location={meter_location}"


        elif user_id is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.meter WHERE user_id={user_id}"

        cur = mysql.connection.cursor()

        cur.execute(query)  # we execute commands with cursor
        fetchdata = cur.fetchall()
        cur.close()
        meter = [{'meter_id': meter[0], 'meter_location': meter[1], 'user_id': meter[2]} for meter in fetchdata]
        return jsonify({"meter": meter})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.get('/api/bill/')
def get_bill_table_records():
    try:
        bill_id = request.args.get('bill_id')
        bill_date = request.args.get('bill_date')
        due_date = request.args.get('due_date')
        total_amount = request.args.get('total_amount')
        payment_status = request.args.get('payment_status')

        query = ("select * from electricity_bill_management_system_db.bill")

        if bill_id is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.bill WHERE bill_id={bill_id}"
        elif bill_date is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.bill WHERE bill_date={bill_date}"


        elif due_date is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.bill WHERE due_date={due_date}"
        elif total_amount is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.bill WHERE total_amount={total_amount}"
        elif payment_status is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.bill WHERE payment_status={payment_status}"

        cur = mysql.connection.cursor()

        cur.execute(query)
        fetchdata = cur.fetchall()
        cur.close()
        bill = [{'bill_id': bill[0], 'bill_date': bill[1], 'due_date': bill[2], 'total_amount': bill[3],
                 'payment_status': bill[4], 'meter_id': bill[5], 'user_id': bill[6]} for bill in fetchdata]
        return jsonify({"bill": bill})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.get('/api/electricity_reading/')
def get_electricity_reading_table_records():
    try:
        meter_id = request.args.get('meter_id')
        reading_date = request.args.get('reading_date')
        reading_value = request.args.get('reading_value')
        reading_id = request.args.get('reading_id')

        query = ("select * from electricity_bill_management_system_db.electricity_reading")

        if meter_id is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.electricity_reading WHERE meter_id={meter_id}"
        elif reading_date is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.electricity_reading WHERE reading_date={reading_date}"


        elif reading_value is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.electricity_reading WHERE reading_value={reading_value}"


        elif reading_id is not None:
            query = f"SELECT * FROM  electricity_bill_management_system_db.electricity_reading WHERE reading_id={reading_id}"

        cur = mysql.connection.cursor()

        cur.execute(query)  # we execute commands with cursor
        fetchdata = cur.fetchall()
        cur.close()
        reading = [
            {'reading_id': reading[0], 'reading_date': reading[1], 'reading_value': reading[2], 'meter_id': reading[3]}
            for reading in fetchdata]
        return jsonify({"electricity_reading": reading})


    except Exception as e:
        return jsonify({'error': str(e)}), 500


#partial update of a record  :

@app.patch('/api/user/user_id=<int:user_id>')
def update_user_table_record(user_id):
    try:
        data = request.get_json()
        new_user_id = data.get("user_id")
        firstname = data.get("firstname")
        lastname = data.get("lastname")
        address = data.get("address")
        phone_number = data.get("phone_number")
        email = data.get("email")
#update based on a parameter
        if lastname is not None:
            query = f"UPDATE electricity_bill_management_system_db.user set lastname='{lastname}' where user_id={user_id}"
        elif phone_number is not None:
            query = f"UPDATE electricity_bill_management_system_db.user set phone_number={phone_number} where user_id={user_id}"

        elif firstname is not None:
            query = f"UPDATE electricity_bill_management_system_db.user set firstname='{firstname}' where user_id={user_id}"
        elif address is not None:
            query = f"UPDATE electricity_bill_management_system_db.user set address='{address}' where user_id={user_id}"
        elif email is not None:
            query = f"UPDATE electricity_bill_management_system_db.user set email='{email}' where user_id={user_id}"
        elif new_user_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.user set user_id={new_user_id} where user_id={user_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'user with id : {user_id} updated successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.patch('/api/meter/meter_id=<int:meter_id>')
def update_meter_table_record(meter_id):
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        new_meter_id = data.get("meter_id")
        meter_location = data.get("meter_location")


        if meter_location is not None:
            query = f"UPDATE electricity_bill_management_system_db.meter set meter_location='{meter_location}' where meter_id={meter_id}"

        elif user_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.meter set user_id='{user_id}' where meter_id={meter_id}"
        elif new_meter_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.meter set meter_id={new_meter_id} where meter_id={meter_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'meter with id : {meter_id} updated successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.patch('/api/bill/bill_id=<int:bill_id>')
def update_bill_table_record(bill_id):
    try:
        data = request.get_json()

        meter_id = data.get("meter_id")

        new_bill_id = data.get("bill_id")
        user_id = data.get("user_id")
        bill_date = data.get("bill_date")
        due_date = data.get("due_date")
        total_amount = data.get("total_amount")
        payment_status = data.get("payment_status")


        if new_bill_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set bill_id='{new_bill_id}' where bill_id={bill_id}"

        elif user_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set user_id='{user_id}' where bill_id={bill_id}"
        elif meter_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set meter_id={meter_id} where bill_id={bill_id}"
        elif bill_date is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set bill_date={bill_date} where bill_id={bill_id}"
        elif due_date is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set due_date={due_date} where bill_id={bill_id}"
        elif total_amount is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set total_amount={total_amount} where bill_id={bill_id}"
        elif payment_status is not None:
            query = f"UPDATE electricity_bill_management_system_db.bill set payment_status={payment_status} where bill_id={bill_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'bill with id : {bill_id} updated successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.patch('/api/electricity_reading/reading_id=<int:reading_id>')
def update_electricity_reading_table_record(reading_id):
    try:
        data = request.get_json()
        new_reading_id = data.get("reading_id")
        meter_id = data.get("meter_id")
        reading_date = data.get("reading_date")
        reading_value = data.get("reading_value")


        if meter_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.electricity_reading set meter_id='{meter_id}' where reading_id={reading_id}"

        elif reading_date is not None:
            query = f"UPDATE electricity_bill_management_system_db.electricity_reading set reading_date='{reading_date}' where reading_id={reading_id}"
        elif reading_value is not None:
            query = f"UPDATE electricity_bill_management_system_db.electricity_reading set reading_value={reading_value} where reading_id={reading_id}"

        elif new_reading_id is not None:
            query = f"UPDATE electricity_bill_management_system_db.electricity_reading set reading_id={new_reading_id} where reading_id={reading_id}"


        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'reading with id : {reading_id} updated successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500


#delete of a record :
@app.delete('/api/user/user_id=<int:user_id>')
def delete_user_table_record(user_id):
    try:


        query=f"delete from user where user_id={user_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'user with id : {user_id} deleted successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.delete('/api/meter/meter_id=<int:meter_id>')
def delete_meter_table_record(meter_id):
    try:


        query=f"delete from meter where meter_id={meter_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'meter with id : {meter_id} deleted successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.delete('/api/bill/bill_id=<int:bill_id>')
def delete_bill_table_record(bill_id):
    try:


        query=f"delete from bill where bill_id={bill_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'bill with id : {bill_id} deleted successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.delete('/api/electricity_reading/reading_id=<int:reading_id>')
def delete_reading_table_record(reading_id):
    try:


        query=f"delete from electricity_reading where reading_id={reading_id}"
        cur = mysql.connection.cursor()

        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f'reading with id : {reading_id} deleted successfully'})


    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run()












