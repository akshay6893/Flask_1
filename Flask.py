from flask import Flask, escape, request,render_template
from Flask101 import Input
import pandas as pd

app = Flask(__name__)

@app.route("/")                                    # ,methods = ['GET']
def home():
    return render_template('index.html') 


@app.route('/json',methods=["POST"])
def json():
    if request.method == "POST":    
        json_data = request.get_json()       
        # data_file = "netaporter_gb_similar.json" 
        url2 = 'https://greendeck-datasets-2.s3.amazonaws.com/netaporter_gb_similar.json'
        data = pd.read_json(url2,lines=True,orient='columns')
        # ff = Input.convert(data,json_data).get_results()          
        return render_template('result.html',message = data )


if __name__=='__main__':
    app.debug=True
    app.run()
