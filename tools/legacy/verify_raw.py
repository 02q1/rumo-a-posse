"""Confere se enunciado e alternativas extraídos aparecem, na mesma ordem, no texto bruto (-raw) do PDF.
Retorna lista de números de questão que falharam."""
import subprocess, re, sys, json, unicodedata
def norm(s):
    s = re.sub(r'-\s*\n\s*', '', s); s = s.replace('- -', '-')
    s = unicodedata.normalize('NFKC', s)
    s = re.sub(r'\b([nN])[oº°]?\s*(?=\d)', r'\1', s); s = re.sub(r'(\d)\s?[oºª°](?=[\s,.;:)]|$)', r'\1', s)
    return re.sub(r'[^0-9a-záéíóúâêôãõçàü]', '', s.lower())
def check(pdf, qs):
    raw = norm(re.sub(r'(?m)^[ \t]*[oaº][ \t]*\n', '', subprocess.run(['pdftotext', '-raw', pdf, '-'], capture_output=True, text=True).stdout))
    bad = []
    for q in qs:
        parts = [q['stem']] + [q['opts'][k] for k in 'ABCDE' if k in q['opts']]
        ok = all(norm(p) in raw for p in parts if norm(p))
        if not ok: bad.append(q['n'])
    return bad
if __name__ == '__main__':
    print(check(sys.argv[1], json.load(open(sys.argv[2]))))
