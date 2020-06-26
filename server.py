import sys
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from HighScore import HighScore

high_scores = []
app = Flask(__name__)
cors = CORS(app, resources={r"/high-scores": {"origins": "https://minesweeper.ethanoz.com"}})
cors = CORS(app, resources={r"/save-high-score": {"origins": "https://minesweeper.ethanoz.com"}})

# Retrieve all High Scores
@app.route('/high-scores')
def get_high_scores():
  my_scores = jsonify_high_scores()
  app.logger.debug(my_scores)
  
  return jsonify(my_scores)

# Save a High Score
@app.route('/save-high-score', methods=['POST'])
def save_high_score():
  try:
    name = request.json['name']
    time = request.json['time']
    score = request.json['score']
    new_high_score = HighScore(name, score, time)
    high_scores.append(new_high_score)
    
    return jsonify({
      'code': 200,
      'message': 'success'
    })
  except:
    error = sys.exc_info()[0]
    app.logger.error('error => %s', error)
    return jsonify({
      'code': 400,
      'message': 'Error, unable to process request'
    })


def jsonify_high_scores():

  scores_to_return = []

  for s in high_scores:
    scores_to_return.append(s.to_json())

  return scores_to_return
  
  
  # return list(map(lambda score: score.to_json, high_scores))
