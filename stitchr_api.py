import os
os.environ["STITCHR_DATA"] = "Data"
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/stitch", methods=["POST"])
def stitch():
    data = request.get_json()
    v = data.get("v")
    j = data.get("j")
    cdr3 = data.get("cdr3")

    try:
        result = subprocess.run(
            ["stitchr", "-v", v, "-j", j, "-cdr3", cdr3],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 400

        return jsonify({"sequence": result.stdout.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
