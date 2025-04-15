from flask import Flask, request, jsonify
from Stitchr import stitchr as st
from Stitchr import stitchrfunctions as fxn

app = Flask(__name__)

# specify details about the locus to be stitched according to https://jamieheather.github.io/stitchr/importing.html
CHAIN = "TRB"
SPECIES = "HUMAN"

tcr_dat, functionality, partial = fxn.get_ref_data(CHAIN, st.gene_types, SPECIES)
codons = fxn.get_optimal_codons('', SPECIES)
j_res, low_conf_js = fxn.get_j_motifs(SPECIES)
c_res = fxn.get_c_motifs(SPECIES)

@app.route("/stitch", methods=["POST"])
def stitch_endpoint():
    data = request.get_json()
    v = data.get("v")
    j = data.get("j")
    cdr3 = data.get("cdr3")
    l = data.get("l", v)  # use provided l, otherwise default to V gene

    try:
        tcr_bits = {
            "v": v,
            "j": j,
            "cdr3": cdr3,
            "l": l,  # allow leader override
            "c": "TRBC1*01",
            "mode": "",
            "skip_c_checks": False,
            "species": SPECIES,
            "seamless": False,
            "5_prime_seq": "",
            "3_prime_seq": "",
            "name": "TCR"
        }

        result = st.stitch(
            tcr_bits,
            tcr_dat,
            functionality,
            partial,
            codons,
            3,
            "",
            c_res,
            j_res,
            low_conf_js
        )

        return jsonify({"sequence": result["stitched_nt"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()
