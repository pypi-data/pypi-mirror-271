import sys
sys.path.append("C:\\Users\\nouro\\Documents\\pytabtex")
from src.pytabtex.Table import Table, Header
import json

# Load the test examples
with open("tests/tables.json", "r") as f:
    test_examples = json.load(f)

###### Table 1 ######
caption = """The prediction accuracy of GPT-3.5-turbo and GPT-4 on different hyper-parameters. “Base” is our\
baseline (5 MTS, Random Selection, the CSV database format, 5-shot), while the rest are by changing one of the\
hyper-parameters"""
table = Table(test_examples["table 1"]["columns"], test_examples["table 1"]["body"], caption=caption)
#print(table.output)

###### Table 2 ######
caption = "Recall@1K of various prompts on BEIR using Flan-UL2"
highlight = {"max": 0}
table = Table(test_examples["table 2"]["columns"], test_examples["table 2"]["body"], caption=caption,
        highlight=highlight)
print(table.output)