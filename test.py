from flask import Flask, request, jsonify

app = Flask(__name__)

FULL_NAME = "john_doe"      
DOB_DDMMYYYY = "17091999"   
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"


def is_numeric_str(s: str) -> bool:
    return s.isdigit()


def is_alpha_str(s: str) -> bool:
    return s.isalpha()


def alternating_caps_reverse(s: str) -> str:
    """
    Reverse the string and apply alternating caps starting with UPPER at index 0.
    Example: "abcDe" -> reverse "eD c b a" -> "EdCbA"
    """
    rev = s[::-1]
    return "".join(ch.upper() if i % 2 == 0 else ch.lower() for i, ch in enumerate(rev))


@app.route("/", methods=["GET"])
def root():
    
    return jsonify(
        {
            "message": "BFHL API is running. Send a POST to /bfhl.",
            "try": {"method": "POST", "path": "/bfhl", "body_example": {"data": ["a", "1", "334", "4", "R", "$"]}},
        }
    ), 200


@app.route("/bfhl", methods=["GET"])
def bfhl_get():
    
    return jsonify({"status": "ok", "hint": "Send a POST with JSON {\"data\": [...] } to this same endpoint."}), 200


@app.route("/bfhl", methods=["POST"])
def bfhl_post():
    try:
        payload = request.get_json(silent=True)
        if not payload or "data" not in payload or not isinstance(payload["data"], list):
            return jsonify({"is_success": False, "error": "Body must be JSON with a 'data' list."}), 400

        input_items = payload["data"]

        
        even_numbers = []
        odd_numbers = []
        alphabets = []
        special_characters = []
        total_sum = 0

       
        letters_linear = []

        for item in input_items:
            s = str(item)  
            if is_numeric_str(s):
                n = int(s)
                (even_numbers if n % 2 == 0 else odd_numbers).append(s)  
                total_sum += n
            elif is_alpha_str(s):
                alphabets.append(s.upper())
                letters_linear.extend(list(s))  
            else:
                special_characters.append(s)

        concat_string = alternating_caps_reverse("".join(letters_linear))

        response = {
            "is_success": True,
            "user_id": f"{FULL_NAME.lower()}_{DOB_DDMMYYYY}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,               
            "special_characters": special_characters,
            "sum": str(total_sum),                
            "concat_string": concat_string,
        }
        return jsonify(response), 200

    except Exception as exc:
        return jsonify({"is_success": False, "error": str(exc)}), 500


if __name__ == "__main__":
    
    app.run(host="127.0.0.1", port=5000, debug=True)

