"""forsoeg6.py -- F11: K1's dybt-regel (længde-parametre omregnes til samme minutter på nabo-barstørrelsen).
Hvor stor en del af 25x25-gitteret kan overhovedet dybt-testes, fordi den omregnede værdi ligger
inden for nabo-gitterets værdier? Rent regnestykke; gitrene er OPDIGTEDE (de rigtige står i filter_case)."""
NABO = {5: [10], 10: [5, 15], 15: [10, 25], 20: [10, 30], 25: [15, 40], 30: [20, 45], 35: [20, 55],
        40: [25, 60], 45: [30], 50: [30], 55: [35], 60: [40]}          # K1's tabel (tavlen / afsnit H)
for navn, gitter in (("1..25 skridt 1", list(range(1, 26))), ("5..29 skridt 1", list(range(5, 30))),
                     ("2..50 skridt 2", list(range(2, 51, 2))), ("5..125 skridt 5", list(range(5, 126, 5)))):
    lo, hi = min(gitter), max(gitter)
    tot = ok_en = ok_alle = 0
    for b, naboer in NABO.items():
        for n1 in gitter:
            for n2 in gitter:
                tot += 1
                inde = [all(lo <= v * b / nb <= hi for v in (n1, n2)) for nb in naboer]
                ok_alle += all(inde); ok_en += any(inde)
    print(f"Gitter {navn:16s}: begge parametre = længde -> kan dybt-testes mod ALLE naboer: {ok_alle/tot:5.1%}, "
          f"mod mindst én nabo: {ok_en/tot:5.1%}")
