import datetime
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import firestore
from firebase import firebase

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "sistemaalertatemprana-e1f00",
  "private_key_id": "cb611e910c6b8491f85eacab14148372dc6bd125",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDRLjbL4IQcZAZK\nb/YVBi5dhTvZE75GVp1nbXMRnNpPy8hXgwUzMi1XdfTnsU+7ax+pbaaOMGRPoS3O\nerhJpRmpdqtB01DPSizHQt8YF53heA4sSLWeDgn8cCvmbDcOSexfq28khZ/4DIFi\n7407tjk/2KNqfUFnF2Dwlv5QqvKhBgSzAoIX/90xhQOq7uNM20R9fxXD1St3PNSR\nfnIt9Jd+RXpE/1eDdy5q9QzCqvu+UhfpaZ5p9Y5yBcOjQ1TdBqgtPGxZIUf3iVnm\n2niTNCZplbIpoL7d3fnqyq+GQpW8BNi2s4e9lF4fVgg0JjvMLb4AWvnhOJjOQ1D3\nsa2q6WD5AgMBAAECggEAV2ae4KrLqG0mr71+LaSqhMrhib8VFqCkHg3+MVK/aO31\npJMK/iwuA8g2bwSIEwAcd5doKysPDrKCyC5AiAzi3wrFXbikoCgW857+Rju/7PBT\nw68Rq5ukEoTv4tQ+YMsEZ6jixHjMsUDQYv1CnrtxyjqDdUAmrqN3Dq+YTS5QOHTg\nxJNQNIw2Jlxu8wVe2EB2T+AuhG0DshHgz4Vg2AbhdzuEBf01Tr9dpbeoE9VzaUdf\ncOJdR4tLmwq8v7TJG3cWcxIZwS8uczW66OEugMGWz2uE7ura36XikUdnE+pSwLh3\nzhnYTndWSW/TlgaqT5yd+R9eVdaGLsYTg6ncnhuSPQKBgQDwpNFzZ1SVeXVT3Qus\nh4dRuX6fq53iLxsUFBdGHLX1zo+9lGxYPLXi+otqDdGGtn1AeQB45cZbHCWRUGJA\nTbN1e0KQT1EzIRUJQlRmRbF3DIw7L9sjeZziMm0ri1bIp7AFBeepXvWeXHRIQYnX\nXck3u5BOWzKXVzi4N4oOLBvdwwKBgQDeh2iEVASVVldq7UmTcLfCyLpLXVYlTnlv\noLZAM3bN58s/FT/+wzqaFLwc+cYQuEPmPGehaIszibir6TQ4tadNHRcV8UqVQAUj\nHgoXtP4CjK9gMp/UhvWizT3Y/IZ9k4VG9PGKbr2rBw/i4F5xje+5QCH78MeLtpey\nSOgOtbAukwKBgQDfOXSVYZ/DvFRKw/yFQX8UH0bHZJHjc6DhwjVIs29TIhaSXHEY\ndNCgSZszeLgJB5UuTlBS1Ypnj7eFkZRiY/F5pCo95WXEUQbLfPz/ldymOzyF1sGn\nqbMO3IoKX4nUPkD4l96qbUzYZpjzQeBUqEn0agfVt6E5ZA5YTCTDOsVqswKBgFL/\ntmAE5mC8/4YGUzcHB8NDExkhCwyHJIwaKV/w0hMirZAt4Nyo/KaTrUYxc0qxL8Ik\nLZLqZ2ElsReNt8ifGHOOshmhEexxIHlkrucAvu08g/0hZLPkUqISY0sXhSI5b7Bz\nk9PKUjwEOkyo2xEHm65A2Wwa9pKJ3DLHNqal5by5AoGAIQSdwdqHbTQJJhXKmkF6\nktP+1rgOiRd+YWGsfCcofQ0RhZsFtXcbyil54Jw/1l4W67ON2kyEBNxIr+cuZp8y\nDLDrnn4pWqVLSnKIehWTKtqtxhyocPcIMTtf0VksPuNP5d596ihbh1CH01F9Vdl9\ntCCtzHJ6Tjg2FhYzByWykxY=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-5z9jd@sistemaalertatemprana-e1f00.iam.gserviceaccount.com",
  "client_id": "109139081570722535869",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-5z9jd%40sistemaalertatemprana-e1f00.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = firebase.FirebaseApplication('https://sistemaalertatemprana-e1f00-default-rtdb.firebaseio.com/', None)

#firebase_admin.initialize_app(cred,{'databaseURL':'https://sistemaalertatemprana-e1f00-default-rtdb.firebaseio.com/'})



def storeData():
    db = firestore.client().collection("usuarios")
    key = db.document().id

    data = {
        'id': key,
        'nombre': 'Amazon2',
        'apellido': datetime.datetime.now(),
        'telefono': 3443.63,
        'correo': 'Amazon',
        'genero': 'hombre',
        'ocupacion': 'desarrollador',
        'edad':'23'
    }

    db.document(key).set(data)

storeData()
#ref=db.reference('/Noticia')
# ref.push({
     
#       'name': 'Amazon2',
#       'creationDate': str(today),
#       'lastClose': 3443.63,
#       'indices': [ 'NDX', 'OEX', 'S5COND', 'SPX' ]
    
    
# })