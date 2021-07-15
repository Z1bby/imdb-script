import pyrebase
import urllib

firebaseConfig = {
  "apiKey": "AIzaSyCDzSPlKXr-DZyXPX_DuiXBg74XDyKsghc",
  "authDomain": "moviesdb-816e7.firebaseapp.com",
  "databaseURL": "https://moviesdb-816e7-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "moviesdb-816e7",
  "storageBucket": "moviesdb-816e7.appspot.com",
  "messagingSenderId": "146539970908",
  "appId": "1:146539970908:web:b08e0f834df99053960199",
  "measurementId": "G-CJ0SXXNXY1"
  }

firebase = pyrebase.initialize_app(firebaseConfig)

# Authentication
auth = firebase.auth()
def firebase_login():
  print("Logging in")
  email = input("Enter your email: ")
  password=input("Enter your password: ")
  auth.sign_in_with_email_and_password(email, password)
  print("Succesfully signed in!")

def firebase_signup():
  print("Creating account")
  email = input("Enter your email: ")
  password=input("Enter your password: ")
  auth.create_user_with_email_and_password(email, password)
  print("Succesfully signed up!")

# Storage
storage=firebase.storage()
def firebase_upload_file():
  print("Uploading file")
  filename=input("Local file name: ")
  cloudfilename=input("New cloud file name: ")
  storage.child(cloudfilename).put(filename)

def firebase_download_file():
  print("Downloading file")
  cloudfilename=input("Cloud file name: ")
  storage.child(cloudfilename).download("", "downloaded.txt")
  downloaded = open("downloaded.txt", "r")

  print("Downloaded to downloaded.txt")
  print(downloaded.readlines())

  downloaded.close()

def firebase_read_file_online():
  print("Reading file")
  cloudfilename=input("Cloud file name: ")
  url = storage.child(cloudfilename).get_url(None)
  f = urllib.request.urlopen(url).read()
  print(f)

# Database
db = firebase.database()

# adding new movies
def firebase_push(id, data):
  print("Pushing to database")
  db.child("movies").child(id).set(data)

# editing existing movies
def firebase_update(id, data):
  print("Pushing to database")
  db.child("movies").child(id).update(data)
  movies = db.child("movies").get()
  print(movies)

# returns all movies or an empty dictionary
def firebase_get():
  movies = {}
  # Gdy baza jest pusta
  if not db.child("movies").shallow().get().val():
    print("Firebase is empty")
    return movies
  
  # adding all movies to the dictionary
  firebase_movies = db.child("movies").get()
  for movie in firebase_movies.each():
    movies[int(movie.key())] = movie.val() # necessary casting from string to int
  return movies

def firebase_delete(key):
  db.child("movies").child(key).remove()
