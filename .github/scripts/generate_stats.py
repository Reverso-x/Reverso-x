import os,json,urllib.request
from collections import Counter
from html import escape
from pathlib import Path
USER='Reverso-x'
def get(url):
 r=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'github-stats'})
 t=os.getenv('GITHUB_TOKEN')
 if t:r.add_header('Authorization','Bearer '+t)
 with urllib.request.urlopen(r,timeout=20) as x:return json.load(x)
t=Counter(); page=1
while True:
 repos=get(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}&type=owner')
 if not repos:break
 for repo in repos:
  if repo.get('fork') or repo.get('archived'):continue
  try:
   for lang,n in get(repo['languages_url']).items():t[lang]+=n
  except Exception:pass
 if len(repos)<100:break
 page+=1
langs=t.most_common(8) or [('Nenhuma linguagem ainda',1)]
total=sum(v for _,v in langs)
colors={'Python':'#3776AB','SQL':'#00758F','C#':'#68217A','JavaScript':'#F7DF1E','TypeScript':'#3178C6','HTML':'#E34F26','CSS':'#1572B6','Java':'#B07219','C++':'#F34B7D','C':'#555555','PHP':'#4F5D95','Shell':'#89E051','PowerShell':'#012456','Go':'#00ADD8','Rust':'#DEA584'}
rows=[];y=86
for lang,n in langs:
 p=n/total*100; w=max(8,350*p/100); c=colors.get(lang,'#58A6FF')
 rows.append(f'<text x="28" y="{y}" fill="#E6EDF3" font-family="Arial" font-size="14">{escape(lang)}</text><rect x="125" y="{y-14}" width="350" height="16" rx="8" fill="#21262D"/><rect x="125" y="{y-14}" width="{w:.1f}" height="16" rx="8" fill="{c}"/><text x="490" y="{y}" text-anchor="end" fill="#8B949E" font-family="Arial" font-size="13">{p:.1f}%</text>');y+=38
h=y+15
svg=f'''<svg width="560" height="{h}" viewBox="0 0 560 {h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" rx="14" fill="#0D1117"/><text x="28" y="38" fill="#58A6FF" font-family="Arial" font-size="20" font-weight="700">Linguagens dos meus projetos</text><text x="28" y="61" fill="#8B949E" font-family="Arial" font-size="12">Atualizado automaticamente pelo GitHub Actions</text>{''.join(rows)}</svg>'''
Path('stats.svg').write_text(svg,encoding='utf-8')
