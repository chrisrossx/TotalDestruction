from pygame import Vector2    

def validate_txt_point( text):
    parts = text.split(",")
    if len(parts) != 2:
        return None 
    text_x, text_y = parts[0].strip(), parts[1].strip()
    if len(text_x) < 1 or len(text_y) < 1:
        return None 
    try:
        float_x = float(text_x)
        float_y = float(text_y)
    except ValueError:
        return None 
    return Vector2(float_x, float_y)
