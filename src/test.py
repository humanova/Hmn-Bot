import dovizIslem as d
import json

res = d.DovizParse('altin')

for i in range(len(res) - 2):
    print(list(res)[i+2])
    print(res[list(res)[i+2]])