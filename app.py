import numpy as np
from flask import Flask, request, jsonify, make_response
import pandas as pd
import package.search as search
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

from elasticsearch import Elasticsearch, helpers

ELASTIC_PASSWORD = "cw1us2Kq73BYmp8+Xl1u"

app.client = Elasticsearch(
    "https://localhost:9200",
    ca_certs="/Users/supachokjirarojkul/http_ca.crt",
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

search.prepareSearchData()

def get_search_query(query: str):
    return {
        "function_score": {
            "query": {
                "dis_max": {
                    "queries": [
                        {"match": {"Name": query}},
                        {"match": {"RecipeIngredientParts": query}},
                        {"match": {"RecipeInstructions": query}},
                        {"match": {"Keywords": query}},
                    ],
                    "tie_breaker": 0.3,
                }
            },
            "functions": [
                {
                    "script_score": {
                        "script": {
                            "source": "(doc['AggregatedRating'].value * doc['ReviewCount'].value + 4.632013709922984 * 100) / (doc['AggregatedRating'].value + 100)"
                        },
                    },
                    "weight": 1,
                },
                {
                    "script_score": {
                        "script": {"source": "_score"},
                    },
                    "weight": 1,
                },
            ],
            "score_mode": "multiply",
        }
    }

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/search", methods=["GET"])
def search():
    response_object = {"status": "success"}
    argList = request.args.to_dict(flat=False)
    query = argList["query"][0]
    results = app.client.search(
        index="recipes",
        size=10,
        query=get_search_query(query),
    )
    total_hit = results["hits"]["total"]["value"]
    if len(results["hits"]["hits"]) > 0:
        results_df = pd.DataFrame(
            [
                [hit["_score"], *hit["_source"].values()]
                for hit in results["hits"]["hits"]
            ],
            columns=["score"] + list(results["hits"]["hits"][0]["_source"].keys()),
        )
    else:
        results_df = pd.DataFrame()
    response_object["total_hit"] = total_hit
    response_object["results"] = results_df.to_dict("records")
    return make_response(response_object, 200)


@app.route("/suggest", methods=["GET"])
def suggest():
    response_object = {"status": "success"}
    argList = request.args.to_dict(flat=False)
    query = argList["query"][0]
    query_dictionary = {
        "suggest": {
            "text": query,
            "suggest-1": {"term": {"field": "all_texts"}},
            "suggest-2": {"term": {"field": "Name"}},
            "suggest-3": {"term": {"field": "Description"}},
            "suggest-4": {"term": {"field": "RecipeInstructions"}},
        }
    }
    res = app.client.search(index="recipes", body=query_dictionary)

    p = []
    for term in np.array(list(res["suggest"].values())).T:
        result = {}
        result["text"] = term[0]["text"]
        options = [v["options"] for v in term]
        result["candidates"] = {}
        for option in options:
            candidates = {}
            if len(option) > 0:
                candidates["text"] = option[0]["text"]
                for candidate in option:
                    # print(candidate)
                    if candidate["text"] not in result["candidates"]:
                        result["candidates"][candidate["text"]] = {
                            "score": candidate["score"],
                            "freq": candidate["freq"],
                        }
                    else:
                        result["candidates"][candidate["text"]]["score"] = (
                            result["candidates"][candidate["text"]]["score"]
                            * result["candidates"][candidate["text"]]["freq"]
                            + candidate["score"] * candidate["freq"]
                        ) / (
                            result["candidates"][candidate["text"]]["freq"]
                            + candidate["freq"]
                        )
                        result["candidates"][candidate["text"]]["freq"] = (
                            result["candidates"][candidate["text"]]["freq"]
                            + candidate["freq"]
                        )
        p += [result["candidates"]]
    out = [""] * len(query.split())
    for i, pp in enumerate(p):
        if pp:
            df = pd.DataFrame.from_dict(pp, orient="index")
            R = (df["score"] * df["freq"]).sum() / df["freq"].sum()
            W = df["freq"].mean()
            df["bayes_score"] = (df["score"] * df["freq"] + W * R) / (df["freq"] + W)
            out[i] = df.sort_values("bayes_score", ascending=False).head(1).index[0]
        else:
            out[i] = query.split()[i]
    response_object["suggest"] = " ".join(out)
    return make_response(response_object, 200)



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


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:4206"
    response.headers["Access-Control-Allow-Headers"] = (
        "Origin, X-Requested-With, Content-Type, Accept"
    )
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


if __name__ == '__main__':
    app.run(port=6969, debug=True)