import fitz
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent/'references'
out.mkdir(exist_ok=True)
books={'planner':'Course Policy and Lecture Plan for CRE II (CL24303)- MO2026.pdf',
       'fogler':'Fogler 5th Edn(full).pdf','levenspiel':'Levenspiel(full).pdf',
       'smith':'Smith-J.M-Chemical-Engineering-Kinetics.pdf',
       'carberry':'James J. Carberry - Chemical and Catalytic Reaction Engineering (2001, Dover Publications)..pdf',
       'fogler_short':'Fogler.pdf','levenspiel_short':'Levenspiel (1).pdf'}
for key,name in books.items():
    doc=fitz.open(root/name)
    texts=[p.get_text() for p in doc]
    (out/f'{key}.txt').write_text('\n'.join(f'\n=== PDF PAGE {i+1} ===\n{t}' for i,t in enumerate(texts)),encoding='utf-8')
    print(key,len(doc),'pages,',sum(map(len,texts)),'text characters')
    for term in ['Weisz','Mears','Effective Diffusivity','Knudsen','Porous Catalysts','Solid Catalyzed','18.1']:
        hits=[i+1 for i,t in enumerate(texts) if term.lower() in t.lower()]
        if hits: print(' ',term,':',hits[:55])
    if key=='planner': print('\n'.join(texts))
