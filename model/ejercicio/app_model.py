from flask import Flask, request, jsonify
import os
import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import mean_squared_error
import sqlite3
from sklearn.linear_model import LinearRegression




dir_path = os.path.dirname(os.path.realpath(__file__))

os.path.join(dir_path,"data","advertising_data.db")

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. Endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/v1/predict', methods=['GET'])
def predict():
    conn = sqlite3.connect(os.path.join(dir_path,"data","advertising_data.db"))#('./data/advertising_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM advertising_data')
    advertising = cursor.fetchall()
    conn.close()    
    
    model = pickle.load(open(os.path.join(dir_path,"data","advertising_model"),'rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newpaper = request.args.get('newpaper', None)

    if tv is None or radio is None or newpaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[int(tv),int(radio),int(newpaper)]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

@app.route('/predict', methods=['GET'])
def predict_list():
    model = pickle.load(open(os.path.join(dir_path,"data","advertising_model"),'rb'))#('./data/advertising_model','rb'))
    data = request.get_json()
    
    input_values = data['data'][0]
    tv, radio, newpaper = map(int, input_values)

    prediction = model.predict([[tv, radio, newpaper]])
    return jsonify({'prediction': round(prediction[0], 2)})






@app.route('/v1/ingest_data', methods=['POST'])
def ingest_data():
    data = request.get_json()

    connection = sqlite3.connect(os.path.join(dir_path,"data","advertising_data.db"))#('./data/advertising_data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO advertising_data (TV, radio, newpaper, sales) VALUES (?, ?, ?, ?)', (data['TV'], data['radio'], data['newpaper'], data['sales']))

    connection.commit()
    connection.close()

    return "Nuevo Registro agregado"


@app.route('/v2/ingest', methods=['POST'])
def add_data():
    data = request.get_json().get('data', [])
    
    for row in data:
        tv, radio, newpaper, sales = row
        query = "INSERT INTO Advertising (tv, radio, newpaper, sales) VALUES (?, ?, ?, ?)"
        connection = sqlite3.connect(os.path.join(dir_path,"data","advertising_data.db"))#('./data/advertising_data.db')
        cursor = connection.cursor()
        cursor.execute(query, (tv, radio, newpaper, sales))
        connection.commit()
        connection.close()

    return jsonify({'message': 'Datos ingestados correctamente'})

@app.route('/ingest', methods=['POST'])
def ingest_datas():
    
    data = request.get_json()
    

    for row in data.get('data', []):
        tv, radio, newpaper, sales = row
        query = "INSERT INTO advertising_data (TV, radio, newpaper, sales) VALUES (?, ?, ?, ?)"
        connection = sqlite3.connect(os.path.join(dir_path,"data","advertising_data.db"))#('./data/advertising_data.db')
        cursor = connection.cursor()
        cursor.execute(query, (tv, radio, newpaper, sales))

        connection.commit()
        connection.close()   
    return jsonify({'message': 'Datos ingresados correctamente'})


@app.route('/retrain', methods=['POST'])
def retrain():
    query = "SELECT * FROM advertising_data;"
    conn = sqlite3.connect(os.path.join(dir_path,"data","advertising_data.db"))#('./data/advertising_data.db')
    crsr = conn.cursor()
    crsr.execute(query)
    ans = crsr.fetchall()
    conn.close()
    names = [description[0] for description in crsr.description]
    df=pd.DataFrame(ans,columns=names)
    X=df.drop(columns=['sales'])
    y=df['sales']
    model= LinearRegression()
    model.fit(X,y)
    filename = 'new_model'
    pickle.dump(model, open(filename, 'wb'))
    return jsonify({'message': 'Modelo reentrenado correctamente.'})









    
    # connection = sqlite3.connect('./data/advertising_data.db')
    # query = "SELECT * FROM advertising_database"
    # df = pd.read_sql_query(query, connection)
    # connection.close()

    
    # X = df[['TV', 'radio', 'newpaper']]
    # y = df['sales']

    
    # model = LinearRegression()
    # model.fit(X, y)

    # with open('data/advertising_model', 'wb') as file:
    #     pickle.dump(model, file)

    # return jsonify({'message': 'Modelo reentrenado correctamente.'})

app.run(host='0.0.0.0',port=5000)