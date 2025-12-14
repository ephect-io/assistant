import json
import re
from pathlib import Path
from tqdm import tqdm

EPHECT_SRC = Path("../ephect-framework/Ephect")
OUT = Path("../data/train.jsonl")
OUT.parent.mkdir(exist_ok=True)

def extract_php_blocks(text):
    return re.findall(r'<\?php[\s\S]*', text)

def infer_instruction(code):
    if 'Component' in code:
        return 'Write an Ephect component'
    if 'Event' in code:
        return 'Write an Ephect domain event'
    if 'Command' in code:
        return 'Write an Ephect command handler'
    return 'Write an Ephect PHP component'

with OUT.open("w") as f:
    for php in tqdm(EPHECT_SRC.rglob("*.php")):
        code = php.read_text(errors="ignore")
        blocks = extract_php_blocks(code)
        for block in blocks:
            item = {
                "instruction": infer_instruction(block),
                "input": f"Based on Ephect source: {php.name}",
                "output": block.strip()
            }
            f.write(json.dumps(item) + "\n")
