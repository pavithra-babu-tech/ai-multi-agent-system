import requests

def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Calculation error"

def weather(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        res.encoding = 'utf-8'   # 🔥 FIX
        return res.text
    except:
        return "Weather fetch failed"