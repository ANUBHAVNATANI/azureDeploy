# LNMHacks 4.0
# Anubhav Natani

from flask import Flask, request, jsonify,render_template
import os
import traceback
#My library
from azure_utils import get_face_id,face_compare
from azure_database import get_database,post_matched_images

# API definition
app = Flask(__name__)

# Webpage to be made for this route
@app.route("/")
def home():
    return render_template('home.html')


@app.route("/checkImagesV2",methods=["GET","POST"])
def checkImages():
    try:
        #Api of checking for the android cliet
        faceId = request.args.get('faceId')
        database = get_database('perm')
        a,name = database[0],database[1] 
        #take face ids from the original database
        #results array
        score = []
        boolArr = []
        for i in a:
            try:
                v = face_compare(i,faceId)
                score.append(v['confidence'])
                boolArr.append(v['isIdentical'])
            except:
                pass
        extract_max = score.index(max(score))
        if(boolArr[extract_max]==True):
            #call database route to store the array
            r = post_matched_images(a[extract_max],faceId,name[extract_max])
            if(len(r.json())==1):
                #error handling 
                return jsonify({"Feedback": "Error"}) 

        #passing this as a api response to the client
        return jsonify({"Feedback":"ThankYou"})
    except:
        return jsonify({"Feedback": "Error"})

@app.route("/getId",methods=["GET","POST"])
def getId():
    try:
        dbItemId = request.args.get('dbItemId')
        #generating the face id
        faceId = get_face_id(dbItemId)
        #get the temp database images using the database route
        a = get_database("temp")
        #results array
        score = []
        boolArr = []
        try:
            for i in a:
                try:
                    v = face_compare(i,faceId)
                    score.append(v['confidence'])
                    boolArr.append(v['isIdentical'])
                except:
                    pass
            extract_max = score.index(max(score))
            if(boolArr[extract_max]==True):
                #call database route to store the array
                return jsonify({"face_id":faceId,"matched_id":a[extract_max]})
            else:
                #else do not call the database route
                return jsonify({"face_id":faceId,"matched_id":""})
        except:
            return jsonify({"face_id":faceId,"matched_id":""})
    except:
        return jsonify({'Feedback': "error"})


#App running code
if __name__ == '__main__':
    app.run(debug=True)
    


