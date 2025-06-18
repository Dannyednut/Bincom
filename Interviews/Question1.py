from flask import Flask, render_template
import mysql.connector


app = Flask(__name__)

# Define database connection parameters
username = 'root'
password = 'root'
host = 'localhost'
database = 'bincomphptest'

@app.route("/")
def index():
    # Establish database connection
    cnx = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

    # Create a cursor object to execute queries
    cursor = cnx.cursor()

    # Define query to execute
    query = "SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid=8"
    pu = "SELECT * FROM polling_unit WHERE uniqueid=8"

    # Execute query
    cursor.execute(query)

    # Fetch all rows from query result
    rows = cursor.fetchall()
    cursor.execute(pu)
    pu_name = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    cnx.close()


    # Render template with fetched data
    return render_template("Question1.html", poll_title = pu_name[0][6][:13], totol_votes = 100, results=rows)

if __name__ == "__main__":
    app.run()
