### utils.py
import ast

def parse_params_from_text(text):
    lines = text.strip().split("\n")
    result = {}
    for line in lines:
        if ":" not in line:
            raise ValueError(f"Dòng thiếu dấu ':' → {line}")
        key, val = map(str.strip, line.split(":", 1))
        try:
            val = ast.literal_eval(val)
        except:
            val = val  # để nguyên chuỗi nếu không ép được
        result[key] = val
    return result
