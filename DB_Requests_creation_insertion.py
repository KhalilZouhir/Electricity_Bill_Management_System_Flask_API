#table creation :

create_user_table=("create table if not exists user(user_id int primary key ,"
                   "firstname varchar(20),lastname varchar(20), "
                   "address text,phone_number int,email text)")

create_meter_table=("create table if not exists meter(meter_id int primary key ,"
                   " meter_location text,user_id int , FOREIGN KEY (user_id) REFERENCES user(user_id))")

create_bill_table=("create table if not exists bill(bill_id int primary key ,"
                   " bill_date date,due_date date , total_amount float ,payment_status boolean ,user_id int ,meter_id int , "
                   "FOREIGN KEY (user_id) REFERENCES user(user_id),"
                   "FOREIGN KEY (meter_id) REFERENCES meter(meter_id))")

create_electricity_table=("create table if not exists electricity_reading(reading_id int primary key ,"
                   " reading_date date,reading_value int , meter_id int ,FOREIGN KEY (meter_id) REFERENCES meter(meter_id))")


#inserting table user :
insert_user=("insert into electricity_bill_management_system_db.user(user_id,firstname,lastname,address,phone_number,email) values (%s,%s,%s,%s,%s,%s)")

#inserting table meter :
insert_meter=("insert into electricity_bill_management_system_db.meter(meter_id,meter_location,user_id) values (%s,%s,%s)")

#inserting table bill :
insert_bill=("insert into electricity_bill_management_system_db.bill(bill_id,bill_date,due_date,total_amount,payment_status,user_id,meter_id) values (%s,%s,%s,%s,%s,%s,%s)")

#inserting table electricity_reading :
insert_electricity_reading=("insert into electricity_bill_management_system_db.electricity_reading(reading_id ,reading_date,reading_value, meter_id)  values (%s,%s,%s,%s)")

#selecting all table user :
select_all_user =("select * from user")
#selecting all table meter :
select_all_meter=("select * from meter")
#selecting all table bill :
select_all_bill =("select * from bill")

#selecting all table electricity_reading :
select_all_electricity_reading =("select * from electricity_reading")



