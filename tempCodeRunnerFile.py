@app.route('/pushups', methods=['GET'])
def pushups():
    return render_template('pushups.html')

@app.route('/community', methods=['GET'])
def pushups():
    return render_template('community.html')

@app.route('/videos', methods=['GET'])
def pushups():
    return render_template('videos.html')

@app.route('/workout', methods=['GET'])
def pushups():
    return render_template('workout.html')