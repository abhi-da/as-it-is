from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import json



app = Flask(__name__)

# Function to query the database
def query_db(query, args=(), one=False):
    conn = sqlite3.connect('sports_fest.db')
    conn.row_factory = sqlite3.Row  # Ensures the results are returned as a dictionary
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()  # Fetch all rows
    conn.close()  # No need for commit for SELECT queries
    return (rv[0] if rv else None) if one else rv

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')


# Route to fetch all fixtures
@app.route('/fixtures')
def fixtures():
    # Fetch all fixtures
    all_fixtures = query_db('SELECT * FROM fixtures')

    # Check if there are any fixtures
    if not all_fixtures:
        return render_template('fixtures.html', fixtures=None)

    return render_template('fixtures.html', fixtures=all_fixtures)


@app.route('/announcements')
def announcements():
    # Fetch all announcements
    all_announcements = query_db('SELECT * FROM announcements')

    # Check if there are any announcements
    if not all_announcements:
        return render_template('announcements.html', announcements=None)

    return render_template('announcements.html', announcements=all_announcements)

@app.route('/schedule')
def schedule():
    # Connect to the SQLite database
    conn = sqlite3.connect('sports_fest.db')
    cursor = conn.cursor()

    # Query the schedule table
    cursor.execute('SELECT id, sports, team_a, team_b, match_type, date, time, venue, result FROM schedule')
    schedule_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Format the data into a list of dictionaries
    schedule_data = [
        {
            'id': row[0],
            'sports': row[1],
            'team_a': row[2],
            'team_b': row[3],
            'match_type': row[4],
            'date': row[5],
            'time': row[6],
            'venue': row[7],
            'result': row[8]
        }
        for row in schedule_data
    ]

    # Pass the formatted data to the template
    return render_template('schedule.html', schedule=schedule_data)



# Route to fetch all results
@app.route('/results')
def results():
    # Fetch all results
    all_results = query_db('SELECT * FROM results')

    # Check if there are any results
    if not all_results:
        return render_template('results.html', results=None)

    return render_template('results.html', results=all_results)

@app.route('/team-information')
def team():
    return render_template('team_information.html')


@app.route('/<team_name>.html')
def team_page(team_name):
    players = query_db(f'SELECT * FROM {team_name}')
    player_names = [player[0] for player in players]
    return render_template(f'{team_name}.html', players=player_names)

@app.route('/rule')
def rule():
    return render_template('rule.html')

@app.route('/<category>')
def category_page(category):
    return f"This is the {category} page."

@app.route('/sports/<sport_name>')
def sports_page(sport_name):
    return render_template(f'sports/{sport_name}.html')



@app.route('/medal-tally')
def medal_tally():
    # Fetch data from 'medal' table
    medal = query_db('SELECT team, gold, silver FROM medal ORDER BY gold DESC, silver DESC')

    # Check if there are any results
    if not medal:
        return render_template('medal.html', medal=None)

    return render_template('medal.html', medal=medal)



# Team Sports Fixtures
@app.route('/cricket_fixtures')
def cricket_fixtures():
    return render_template('cricket_fixtures.html')  # You'll need to create this page

@app.route('/dodgeball_fixtures')
def dodgeball_fixtures():
    return render_template('dodgeball_fixtures.html')  # You'll need to create this page

@app.route('/futsal_fixtures')
def futsal_fixtures():
    return render_template('futsal_fixtures.html')  # You'll need to create this page

@app.route('/volleyball_fixtures')
def volleyball_fixtures():
    return render_template('volleyball_fixtures.html')  # You'll need to create this page

@app.route('/basketball_fixtures')
def basketball_fixtures():
    return render_template('basketball_fixtures.html')  # You'll need to create this page

# Individual Sports Fixtures
@app.route('/badminton_fixtures')
def badminton_fixtures():
    return render_template('badminton_fixtures.html')  # You'll need to create this page

@app.route('/lawn_tennis_fixtures')
def lawn_tennis_fixtures():
    return render_template('lawn_tennis_fixtures.html')  # You'll need to create this page

@app.route('/table_tennis_fixtures')
def table_tennis_fixtures():
    return render_template('table_tennis_fixtures.html')  # You'll need to create this page

@app.route('/carrom_fixtures')
def carrom_fixtures():
    return render_template('carrom_fixtures.html')  # You'll need to create this page

@app.route('/chess_fixtures')
def chess_fixtures():
    return render_template('chess_fixtures.html')  # You'll need to create this page
    

@app.route('/tow_fixtures')
def tow_fixtures():
    return render_template('tow_fixtures.html')  # You'll need to create this page






# Path to the JSON file where the registrations will be saved
REGISTRATION_FILE = 'static/data/misc.json'


# Helper function to load data from the JSON file
def load_registrations():
    if os.path.exists(REGISTRATION_FILE):
        with open(REGISTRATION_FILE, 'r') as file:
            return json.load(file)
    return []


# Helper function to save data to the JSON file
def save_registrations(data):
    with open(REGISTRATION_FILE, 'w') as file:
        json.dump(data, file, indent=4)


# Route for the 'misc' page to display the registration form
@app.route('/misc')
def misc():
    registrations = load_registrations()  # Load saved registrations
    return render_template('misc.html', registrations=registrations)


# Route to handle the form submission and save registration data
@app.route('/submit', methods=['POST'])
def submit_registration():
    # Get data from the form
    name = request.form['name']
    batch = request.form['batch']
    team_name = request.form['team-name']
    individual_sport = request.form['individual-sport']

    # Prepare the new registration entry
    new_entry = {
        'name': name,
        'batch': batch,
        'teamName': team_name,
        'individualSport': individual_sport
    }

    # Load existing registrations and add the new one
    registrations = load_registrations()
    registrations.append(new_entry)

    # Save the updated list back to the JSON file
    save_registrations(registrations)

    return jsonify({'status': 'success'})





# Main entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8585, debug=True)
