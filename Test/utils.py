### utils.py
import ast

def parse_params_from_text(text):
    lines = text.strip().split("\n")
    result = {}
    for line in lines:
        if ":" not in line:
            raise ValueError(f"Missing separator symbol ':' → {line}")
        key, val = map(str.strip, line.split(":", 1))
        try:
            val = ast.literal_eval(val)
        except:
            val = val 
        result[key] = val
    return result
