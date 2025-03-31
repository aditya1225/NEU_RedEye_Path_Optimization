import os
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory
from Controller.controller import startup

app = Flask(__name__)

@app.route('/generate_maps', methods=['POST'])
def generate_maps():
    num_vans = int(request.form['num_vans'])
    num_students = int(request.form['num_students'])
    maps = startup(number_of_locations=num_students, number_of_vans=num_vans)
    return redirect('/')

@app.route('/Route_maps/<path:filename>')
def send_map(filename):
    return send_from_directory('Route_maps', filename)

@app.route('/')
def hello_world():
    map_files = os.listdir(os.path.join('Route_maps'))
    return render_template('maps_display.html', map_files=map_files)

if __name__ == '__main__':
    app.run()
