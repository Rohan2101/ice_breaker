from dotenv import load_dotenv
from flask import Flask,render_template,request,jsonify
from ice_breaker import ice_break_with


load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

def process():
    name = request.form['name']
    summary, profile_pic_url = ice_break_with(name=name)
    summary={"summary":summary}
    return jsonify(
        {
            "summary_and_facts": summary,
            "profile_url": profile_pic_url,
        }
    )
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8070,debug=True)



