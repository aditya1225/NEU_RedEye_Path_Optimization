import os
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session
from Controller.controller import startup

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/generate_maps', methods=['POST'])
def generate_maps():
    num_vans = int(request.form['num_vans'])
    num_students = int(request.form['num_students'])
    route_maps_path = os.path.join('Route_maps')
    for filename in os.listdir(route_maps_path):
        file_path = os.path.join(route_maps_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    # Call the startup function and get metrics
    metrics = startup(number_of_locations=num_students, number_of_vans=num_vans)
    session['metrics'] = metrics  # Store metrics in session
    return redirect('/')

@app.route('/Route_maps/<path:filename>')
def send_map(filename):
    return send_from_directory('Route_maps', filename)

@app.route('/')
def hello_world():
    map_files = os.listdir(os.path.join('Route_maps'))
    metrics = session.get('metrics', {})
    return render_template('maps_display.html', map_files=map_files, metrics=metrics)

if __name__ == '__main__':
    app.run()
