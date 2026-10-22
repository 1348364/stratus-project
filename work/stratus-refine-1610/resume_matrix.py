from pathlib import Path
w=Path('work/stratus-refine-1610')
original=(w/'qa-request-consumed.txt').read_text()
rest=original[original.index('CMD weather clear'):]
q='CAM 4062 94 4135 0 0\nWAIT 4\nSHOT s1610-cave-lamp-water\n'+rest
(w/'qa-request.txt').write_text(q)
print(q)
