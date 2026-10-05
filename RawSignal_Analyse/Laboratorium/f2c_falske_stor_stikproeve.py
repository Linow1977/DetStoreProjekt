# Flere falske celler end i f2, så andelen af falske, der slipper igennem, bliver stabil.
import numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("f2", "f2b_oos_procentgraenser.py"); f2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(f2)
saml = {}
antal = 0
for _ in range(40):
    i, o, s = f2.measure(0, 2_000_000)
    k = i >= 4.0
    antal += k.sum()
    for navn, v in f2.rules(i[k], o[k], s[k]).items():
        saml[navn] = saml.get(navn, 0) + v.sum()
print("falske valgt (IS-t >= 4):", antal, "af 80 mio.")
for navn, v in saml.items():
    print(f"{navn:>10}: falske igennem {v / antal:6.1%}")
