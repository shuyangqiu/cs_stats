import pandas as pd
from flask import Flask, request
from pyper import *

r = R(use_pandas=True)
r.assign("path", "winrates.rds")
r('model <- readRDS(path)')

app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    kdr = float(request.form['kdr'])
    hs = float(request.form['hs'])
    adr = float(request.form['adr'])
    rounds = int(request.form['rounds'])

    # Create dataframe
    df = pd.DataFrame({'kill_death_ratio': [kdr],
                        'hs': [hs],
                        'adr': [adr],
                        'rounds': [rounds]}) 
    
    # Get prediction
    r.assign('data', df)
    r('result <- predict(model, newdata = data, type = "response")')
    
    return f'{{{r.get("result")}}}' # Return model prediction