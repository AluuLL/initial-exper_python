from flask import Flask,request
#import TaskThread
import database as database
import statics as statics
import datetime
import statics as statics
import system_manage as system_manage
import accurate_search as accurate_search
#app = Flask(__name__,static_url_path='',root_path='/disk/linda/IgenomeCloudGemini/WordReport')
app = Flask(__name__,static_url_path='')

@app.route("/test",methods=["POST","GET"])
def test():
    return 'hello world'

@app.route("/report_init",methods=["POST","GET"])
def report_init():
    if request.method == 'POST':
        data=dict(request.form.lists())
        print(data)
        report_id = int(data['report_id'][0])

        status = database.report_init(report_id)
        return status

@app.route("/report_interact",methods=["POST","GET"])
def report_interact():
    if request.method == 'POST':
        data=dict(request.form.lists())
        status = database.checkpoint_interact(data)
        return status


@app.route("/generate_word",methods=["POST","GET"])
def generate_word():
    if request.method == 'POST':
        data=dict(request.form.lists())
        report_id = int(data['report_id'][0])
        begin = datetime.datetime.now()
        status = database.toword(report_id)
        end = datetime.datetime.now()
        print(end-begin)
        return status

@app.route("/label_search",methods=["POST","GET"])
def label_search():
    if request.method == 'POST':
        data = request.values.get("labelData")
        data=eval(data)
        status = statics.label_result(data)
        return status

@app.route("/usage_statistics",methods=["POST","GET"])
def usage_statistics():
    if request.method == 'POST':
        status = system_manage.system_result()
        return status

@app.route("/accurate",methods=["POST","GET"])
def accurate():
    if request.method == 'POST':
        data = request.values.get("accurate")
        data=eval(data)
        status = accurate_search.accurate_result(data)
        return status
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8686)