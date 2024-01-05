import mlflow
# from mlflow.tracking import MlflowClient

from flask import Flask, request, jsonify

app = Flask(__name__)

RUN_ID = '9b4fcc81e5ba4ca698265705f41bc162'
# MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
# mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
logged_model = f"s3://mlfow-aws-bucket-remote/2/{RUN_ID}/artifacts/model"
# logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)


def prepare_features(ride):
    features = {}
    features['PU_DO'] = "%s_%s" % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    preds = model.predict(features)
    return preds


@app.route("/")
def index():
    return "Hello World"


@app.route("/predict", methods=['POST'])
def predict_endpoint():
    try:

        ride = request.get_json()
        features = prepare_features(ride)
        pred = predict(features)

        result = {
            "duration": pred.tolist(),
            "model_version": RUN_ID
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"{e}"})


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=9696, debug=True)
    pass
