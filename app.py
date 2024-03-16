from flask import Flask, request, jsonify, make_response
import pandas as pd
import package.search as search
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

search.prepareSearchData()

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/name', methods=['GET'])
def SearchByName():
    argList = request.args.to_dict(flat=False)
    query_term = argList['query'][0]
    result = search.searchByName(query_term)
    # check whether if result is a dataframe
    if isinstance(result, pd.DataFrame):
        resultTranpose = result.T
        jsonResult = resultTranpose.to_json()
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200
    else:
        jsonResult = {'similar': list(result)}
        print(jsonResult)
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 404


@app.route('/ingredient', methods=['GET'])
def SearchByIngredient():
    argList = request.args.to_dict(flat=False)
    query_term = argList['query'][0]
    result = search.searchByIngredient(query_term)
    # check whether if result is a dataframe
    if isinstance(result, pd.DataFrame):
        resultTranpose = result.T
        jsonResult = resultTranpose.to_json()
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200
    else:
        jsonResult = {'similar': result}
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 404


@app.route('/process', methods=['GET'])
def SearchByCookingProcess():
    argList = request.args.to_dict(flat=False)
    query_term = argList['query'][0]
    result = search.searchByCookingProcess(query_term)
    # check whether if result is a dataframe
    if isinstance(result, pd.DataFrame):
        resultTranpose = result.T
        jsonResult = resultTranpose.to_json()
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200
    else:
        jsonResult = {'similar': result}
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 404


@app.route('/find', methods=['GET'])
def FindByID():
    argList = request.args.to_dict(flat=False)
    query_term = argList['id'][0]

    result = search.findById(query_term)

    # check whether if result is a dataframe
    if isinstance(result, pd.DataFrame):
        resultTranpose = result.T
        jsonResult = resultTranpose.to_json()
        response = make_response(jsonResult)

        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 200
    else:
        jsonResult = {'Error': 'Dish id not found'}
        response = make_response(jsonResult)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response, 404


if __name__ == '__main__':
    app.run(port=6969, debug=True)