from flask import Flask, request, jsonify
from Stitchr.stitchr import stitch_from_parts

app = Flask(__name__)

@app.route("/stitch", methods=["POST"])
def stitch():
    data = request.get_json()
    v = data.get("v")
    j = data.get("j")
    cdr3 = data.get("cdr3")

    try:
        result = stitch_from_parts(v, j, cdr3)
        return jsonify({"sequence": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()