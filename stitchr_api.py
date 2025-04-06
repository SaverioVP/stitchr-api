import os
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
        env = os.environ.copy()
        env["STITCHR_DATA"] = os.path.join(os.path.dirname(__file__), "Data")

        command = f'export STITCHR_DATA="{os.path.join(os.path.dirname(__file__), "Data")}" && stitchr -v "{v}" -j "{j}" -cdr3 "{cdr3}"'

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,  # important!
            executable="/bin/bash",
            cwd=os.path.dirname(__file__)
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 400

        return jsonify({"sequence": result.stdout.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
