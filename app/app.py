from flask import Flask, jsonify, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
app = Flask(__name__)

@app.route("/health")
def  health_check():
	return jsonify({"status": "ok"})

analyzer = SentimentIntensityAnalyzer()

@app.route("/analyze", methods=["POST"])
def analyze():
	data=request.get_json()
	text=data["text"]
	scores=analyzer.polarity_scores(text)
	if scores["compound"] >= 0.05 :
		return jsonify({"text": text,
				"sentiment": "positive",
				"score": scores["compound"]})
	elif scores["compound"] <= -0.05 :
		return  jsonify({"text": text,
                                "sentiment": "negative",
                                "score": scores["compound"]})
	else:
		return  jsonify({"text": text,
                                "sentiment": "neutral",
                                "score": scores["compound"]})

if __name__ == "__main__" :
	app.run(host="0.0.0.0", debug=True)
