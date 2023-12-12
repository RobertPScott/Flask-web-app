from flask import Flask, render_template
app = Flask(__name__)

DOGS = [
  {
    'id':1,
    'name':'Max',
    'age':2,
    'location':'Brooklyn, NY',
    'sex' : 'M',
    'image': 'Max.jpg'
  },
  {
    'id':2,
    'name':'Scout',
    'age':1,
    'location':'Denver, CO',
    'sex' : 'F',
    'image': 'Scout.jpg'
  },
  {
    'id':3,
    'name':'Rex',
    'age':5,
    'location':'Charlotte, NC',
    'sex' : 'M',
    'image': 'Rex.jpg'
  },
  {
    'id':4,
    'name':'Melvin',
    'age':2,
    'location':'Colorado Springs, CO',
    'sex' : 'M',
    'image': 'Melvin.jpg'
  }
]

@app.route('/')
def hello_world():
    return render_template('home.html', dogs = DOGS)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)