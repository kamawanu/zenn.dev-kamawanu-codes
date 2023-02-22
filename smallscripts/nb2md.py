#from google.colab import drive
#drive.mount('/content/drive')

import glob
import sys
import os.path
import json

def mdquote(q:str,ol:list):
    print(f"```{q}")
    print("".join(ol))
    print("```")
    print("")

for fn in sys.argv[1:] or glob.glob(f"*.ipynb"):
    rawnbbook = json.load(open(fn))
    bn = os.path.basename(fn)
    ##print(pno)
    assert rawnbbook["nbformat"]==4
    assert rawnbbook["metadata"]["kernelspec"]["name"] == "python3"
    ##print()
    sys.stdout = open(f"{bn}.md","w")
    for cell1 in rawnbbook["cells"]:
        mdquote("python",cell1["source"])
        for outputpartial in cell1["outputs"]:
            if outputpartial["output_type"] == "stream":
                print(">"+(">".join(outputpartial["text"])))
            elif outputpartial["output_type"] == "execute_result":
                for tt,vv in outputpartial["data"].items():
                    print(">"+(">".join(vv)))
            elif outputpartial["output_type"] == "error":
                print(">"+outputpartial["traceback"][-1])
            else:
                print(outputpartial)
            print("----")
