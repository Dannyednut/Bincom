
from flask import Flask, render_template
import mysql.connector

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

@app.route("/")
def index():
    return get_results(lga_id=1)

@app.route("/<int:lga_id>")
def get_results(lga_id):
    try:
        # Create a cursor object to execute queries
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Define query to execute
        query = """
            SELECT announced_pu_results.party_abbreviation, announced_pu_results.party_score,
                   polling_unit.polling_unit_name, ward.ward_name, lga.lga_name
            FROM (((announced_pu_results
            INNER JOIN polling_unit ON announced_pu_results.polling_unit_uniqueid = polling_unit.uniqueid)
            INNER JOIN ward ON polling_unit.ward_id = ward.ward_id)
            INNER JOIN lga ON ward.lga_id = lga.lga_id)
            WHERE lga.lga_id = %s;
        """
        party = "SELECT partyname FROM party"
        lga_query = "SELECT lga_id, lga_name FROM lga"

        # Execute query
        cursor.execute(query, (lga_id,))
        rows = cursor.fetchall()
        cursor.execute(party)
        party_names = cursor.fetchall()
        cursor.execute(lga_query)
        lga = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        cnx.close()

        parties = [i[0] for i in party_names]
        d = {}
        for i in parties:
            d[i] = [m[1] if m[0].strip() == i.strip() else 0 for m in rows]
        for i in d:
            d[i] = sum(d[i])
        
        total = sum(d.values())

        lgas = {}
        for i in lga:
            lgas[i[0]] = i[1]


        # Render template with fetched data
        return render_template("Question2.html", poll_title=parties, lgas=lgas, results=d, total=total)
    except mysql.connector.Error as err:
        return f"Error: {err}"
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run()


