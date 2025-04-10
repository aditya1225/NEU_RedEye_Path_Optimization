import os
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session
from Controller.controller import startup

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/generate_maps', methods=['POST'])
def generate_maps():
    num_vans = int(request.form['num_vans'])
    num_students = int(request.form['num_students'])
    clean_directory()
    metrics, cumulative_metrics, distance_sorted, time_sorted = startup(number_of_locations=num_students, number_of_vans=num_vans)
    session['metrics'] = metrics
    session['cumulative_metrics'] = cumulative_metrics
    session['distance_sorted'] = distance_sorted
    session['time_sorted'] = time_sorted
    return redirect('/show-maps')

def clean_directory():
    route_maps_path = os.path.join('Route_maps')
    for filename in os.listdir(route_maps_path):
        file_path = os.path.join(route_maps_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

@app.route('/Route_maps/<path:filename>')
def send_map(filename):
    return send_from_directory('Route_maps', filename)

@app.route('/show-maps')
def show_maps():
    map_files = os.listdir(os.path.join('Route_maps'))
    sorted_map_files = sorted(map_files, key=lambda x: int(x.split('-')[1].split('_')[0]))
    metrics = session.get('metrics', {})
    cumulative_metrics = session.get('cumulative_metrics', {})
    distance_sorted = session.get('distance_sorted', {})
    time_sorted = session.get('time_sorted', {})
    return render_template('maps_display.html', map_files=sorted_map_files, metrics=metrics, cumulative_metrics=cumulative_metrics, distance_sorted=distance_sorted, time_sorted=time_sorted)

@app.route('/')
def hello_world():
    clean_directory()
    map_files = os.listdir(os.path.join('Route_maps'))
    metrics = {}
    cumulative_metrics = {}
    distance_sorted = {}
    time_sorted = {}
    return render_template('maps_display.html', map_files=map_files, metrics=metrics, cumulative_metrics=cumulative_metrics, distance_sorted=distance_sorted, time_sorted=time_sorted)

if __name__ == '__main__':
    app.run()