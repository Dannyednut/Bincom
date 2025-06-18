
from flask import Flask, render_template, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Define database connection parameters
username = 'root'
password = 'root'
host = 'localhost'
database = 'bincomphptest'

# Establish database connection
def get_db_connection():
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

import requests

def get_user_location(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    data = response.json()
    if data['status'] == "success":
        latitude = data['lat']
        longitude = data['lon']
        return latitude, longitude
    else:
        return None,None
    
global wards
global lgas

@app.route("/")
def index():
    try:
        # Create a cursor object to execute queries
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Define query to execute
        party_query = "SELECT partyname FROM party"
        ward_query = "SELECT uniqueid, ward_name FROM ward"
        lga_query = "SELECT lga_id, lga_name FROM lga"

        # Execute query
        # cursor.execute(query, (lga_id,))
        # rows = cursor.fetchall()
        cursor.execute(party_query)
        party = cursor.fetchall()
        cursor.execute(ward_query)
        ward = cursor.fetchall()
        cursor.execute(lga_query)
        lga = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        cnx.close()

        parties = [i[0] for i in party]
    
        wards = {}
        for i in ward:
            wards[i[0]] = i[1]

        lgas = {}
        for i in lga:
            lgas[i[0]] = i[1]


        # Render template with fetched data
        return render_template("Question3.html",  lgas=lgas, wards = wards, parties = parties)
    except mysql.connector.Error as err:
        return f"Error: {err}"
    except Exception as e:
        return f"An error occurred: {e}"

import requests  
@app.route("/submit", methods=['POST'])
def store():
    data = request.form
    try:
        # Create a cursor object to execute queries
        cnx = get_db_connection()
        cursor = cnx.cursor()
        # Define query to execute
        party_query = "SELECT partyname FROM party"
        cursor.execute(party_query)
        party = cursor.fetchall()
        parties = [i[0] for i in party]

        polling_unit_query = """
            INSERT INTO polling_unit(
            polling_unit_id, 
            ward_id, lga_id, 
            uniquewardid,   
            polling_unit_number, 
            polling_unit_name, 
            polling_unit_description, 
            lat,
            `long`, 
            entered_by_user, 
            user_ip_address,
            date_entered
        )VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
        """

        score_query = """
            INSERT INTO announced_pu_results(
            polling_unit_uniqueid,
            party_abbreviation,
            party_score,
            entered_by_user,
            date_entered,
            user_ip_address
        )VALUES(%s, %s, %s, %s, %s, %s)
        """
        simp = """
            INSERT INTO states(
            state_id,
            state_name 
            )VALUES(%s, %s)
        """
        lat, long = get_user_location(request.remote_addr)
        #Execute query
        cursor.execute(polling_unit_query, (
            data['polling_unit_id'],
            data['ward'],
            data['lga'],
            data['uniquewardid'],
            f"DT{data['lga']}0{data['ward']}00{data['polling_unit_id']}",
            data['polling_unit_name'],
            data['polling_unit_description'],
            lat,
            long,
            data['entered_by_user'],
            request.remote_addr,
            "0000-00-00 00:00:00"
        ))

        def last_id():
            cursor.execute("SELECT LAST_INSERT_ID()")
            last_insert = cursor.fetchall()
            return last_insert[0][0]

        for i in parties:
            cursor.execute(score_query, (
                last_id(),
                i,
                data[i],
                data['entered_by_user'],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                request.remote_addr
            ))
        cnx.commit()
        
        return "Database updated successfully"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    except Exception as e:
        return f"An error occurred: {e}"
   
if __name__ == "__main__":
    app.run()


