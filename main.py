import logging

from flask import Flask
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize
import requests

app = Flask(__name__)


@app.route('/ols')
def ols():
    return_str = 'ok'
    resp = requests.get('https://valid-decoder-258800.appspot.com/censobyedo?entidad=30')
   
    if resp.status_code != 200:
    # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))
    #for todo_item in resp.json():
    #    print('{} {}'.format(todo_item['actividad_economica'], todo_item['ue']))
        #return_str += '{} {}'.format(todo_item['cve_ent'], todo_item['entidad'])
    data=json_normalize(resp.json())
    df = data[['idmunicipio', 'UE', 'H001A']]
    print (df)
 
    import statsmodels.formula.api as smf
    #print (df)
    df.to_csv('mydata.csv')

    mydata = pd.read_csv("mydata.csv")
    lm= smf.ols(formula= "UE~H001A", data=mydata).fit()
   
    print (lm.params)
    print(lm.summary())
    return_str += str(lm.rsquared) + ' , ' + str(lm.rsquared_adj)

    return return_str

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0', port=8080, debug=True)
