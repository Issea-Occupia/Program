import json
from pathlib import Path

p = Path(r"D:\Program\python\requests\test.json")
text = p.read_text(encoding="utf-8")  
data = json.loads(text)             
dic1 = dict(data)
print(dic1)
