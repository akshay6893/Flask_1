from flask import Flask, escape, request,render_template
from Flask101 import Input

app = Flask(__name__)

@app.route("/")                                    # ,methods = ['GET']
def home():
    return render_template('index.html') 


@app.route('/json',methods=["POST"])
def json():
    if request.method == "POST":    
        json_data = request.get_json()       
        data_file = "netaporter_gb_similar.json" 
        ff = Input.convert(data_file,json_data).get_results()          
        return render_template('result.html',message = ff )


if __name__=='__main__':
    app.debug=True
    app.run()
