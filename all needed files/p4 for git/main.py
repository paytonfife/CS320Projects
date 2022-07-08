import pandas as pd
from flask import Flask, request, jsonify, Response
import re
import time
import matplotlib
from matplotlib import pyplot as plt
from io import StringIO, BytesIO

# project: p4
# submitter: pjfife
# partner: none
# hours: 8

matplotlib.use('Agg')

app = Flask(__name__)
df = pd.read_csv("main.csv")
df_pd = df.to_html()
df_dict = df.to_dict(orient = 'index')

froma = 0
fromb = 0

home_visits = 0

@app.route('/')
def home():
    global home_visits
    global froma
    global fromb
    if home_visits < 10:
        if home_visits % 2 == 0:
            with open("index.html") as f:
                html = f.read()
        else:
            with open("indexB.html") as f:
                html = f.read()
    else:
        if froma >= fromb:
            with open("index.html") as f:
                html = f.read()
        else:        
            with open("indexB.html") as f:
                html = f.read()
    home_visits += 1
    return html

@app.route("/dashboard_1.svg")
def svg1():
    color = ""
    try:
        color = str(request.args["color"])
    except:
        pass
    fig, ax = matplotlib.pyplot.subplots(figsize = (6, 4))
    if color == "red":
        pd.Series(df['Budget']).plot.line(ax=ax, c = "red")
    else:
        pd.Series(df['Budget']).plot.line(ax=ax)
    ax.set_ylabel("Budget ($10 millions)")
    f = StringIO()
    matplotlib.pyplot.tight_layout()
    fig.savefig(f, format = "svg")
    matplotlib.pyplot.close()
    png = f.getvalue()
    hdr = {"Content-Type": "image/svg+xml"}
    return Response(png, headers=hdr)
    

@app.route("/dashboard_2.svg")
def svg2():
    fig, ax = plt.subplots(figsize = (6, 5))
    df["Distributor"].value_counts().plot.bar(ax=ax)
    ax.set_ylabel("Number of Movies Released")
    f = StringIO()
    plt.tight_layout()
    fig.savefig(f, format = "svg")
    matplotlib.pyplot.close()
    png = f.getvalue()
    hdr = {"Content-Type": "image/svg+xml"}
    return Response(png, headers=hdr)
    
@app.route('/browse.html')
def browse():
    with open("browse.html") as f:
        html = f.read()
    return html + df_pd

clients_d = {}

@app.route('/browse.json')
def browse_json():
    global last_visit
    
    ip = request.remote_addr
    if ip in clients_d:
        if time.time() - clients_d[ip] > 3:
            clients_d[ip] = time.time()
            return jsonify(df_dict)
        else:
            html = "nah"
            return Response(html, status = 429, headers = {"Retry-After": 3})
    else:
        clients_d[ip] = time.time()
        return jsonify(df_dict)

        
@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"\w+@\w+\.{1}\w{3}", email): # 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        with open("emails.txt", "r") as f:
            num_subscribed = len(f.readlines())
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify("ERROR: invalid email format") # 3

@app.route('/donate.html')
def donate():
    global froma
    global fromb
    try: #from B
        vers = request.args["from"]
    except: # from A
        vers = "A"
    if vers == "A":
        froma += 1
    if vers == "B":
        fromb += 1
    with open("donate.html") as f:
        html = f.read()
    return html

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.