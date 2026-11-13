"""Generate self-contained GitHub README assets from cached public GitHub data."""
from pathlib import Path
import html, json, base64, textwrap
from datetime import date, timedelta, datetime, timezone
P=Path(__file__).resolve().parents[1]
A=P/'assets'
escape=html.escape
F='#edf3fa'; M='#9299a2'; G='#31b84c'; B='#151c24'
font={}
rows={
'A':'01110/10001/10001/11111/10001/10001/10001','B':'11110/10001/10001/11110/10001/10001/11110','C':'01111/10000/10000/10000/10000/10000/01111','D':'11110/10001/10001/10001/10001/10001/11110','E':'11111/10000/10000/11110/10000/10000/11111','F':'11111/10000/10000/11110/10000/10000/10000','G':'01111/10000/10000/10111/10001/10001/01110','H':'10001/10001/10001/11111/10001/10001/10001','I':'111/010/010/010/010/010/111','J':'00111/00010/00010/00010/10010/10010/01100','K':'10001/10010/10100/11000/10100/10010/10001','L':'10000/10000/10000/10000/10000/10000/11111','M':'10001/11011/10101/10101/10001/10001/10001','N':'10001/11001/10101/10011/10001/10001/10001','O':'01110/10001/10001/10001/10001/10001/10001/01110','P':'11110/10001/10001/11110/10000/10000/10000','Q':'01110/10001/10001/10001/10101/10010/01101','R':'11110/10001/10001/11110/10100/10010/10001','S':'01111/10000/10000/01110/00001/00001/11110','T':'11111/00100/00100/00100/00100/00100/00100','U':'10001/10001/10001/10001/10001/10001/01110','V':'10001/10001/10001/10001/10001/01010/00100','W':'10001/10001/10001/10101/10101/11011/10001','X':'10001/10001/01010/00100/01010/10001/10001','Y':'10001/10001/01010/00100/00100/00100/00100','Z':'11111/00001/00010/00100/01000/10000/11111','0':'01110/10001/10011/10101/11001/10001/01110','1':'010/110/010/010/010/010/111','2':'01110/10001/00001/00110/01000/10000/11111','3':'11110/00001/00001/01110/00001/00001/11110','4':'00010/00110/01010/10010/11111/00010/00010','5':'11111/10000/10000/11110/00001/00001/11110','6':'01110/10000/10000/11110/10001/10001/01110','7':'11111/00001/00010/00100/01000/01000/01000','8':'01110/10001/10001/01110/10001/10001/01110','9':'01110/10001/10001/01111/00001/00001/01110','>':'100/010/001/000/001/010/100','*':'00000/00100/10101/01110/10101/00100/00000'}
def r(x,y,w,h,c,rx=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}"/>'
def pix(t,x,y,s=3,c=G):
 out=''
 for ch in t.upper():
  if ch==' ': x+=s*4;continue
  a=rows.get(ch,rows['*']).split('/')
  for j,row in enumerate(a):
   for i,b in enumerate(row):
    if b=='1':out+=r(x+i*s,y+j*s,s,s,c)
  x+=(len(a[0])+1)*s
 return out

def txt(t,x,y,size=16,c=F,weight=400,mono=False):return f'<text x="{x}" y="{y}" fill="{c}" font-family="{("monospace" if mono else "Arial, sans-serif")}" font-size="{size}" font-weight="{weight}">{html.escape(t)}</text>'
def card(w,h):return f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{B}" stroke="#29313c"/>'
def save(name,w,h,body,title):
 (A/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{html.escape(title)}</title>{body}</svg>')
def streaks(days,today):
 counts={date.fromisoformat(d['date']):d['contributionCount'] for d in days if date.fromisoformat(d['date'])<=today}
 run=best=0;last=None
 for day,count in sorted(counts.items()):
  run=(run+1 if last==day-timedelta(days=1) else 1) if count else 0
  best=max(best,run);last=day
 cursor=today if counts.get(today,0) else today-timedelta(days=1)
 current=0
 while counts.get(cursor,0):current+=1;cursor-=timedelta(days=1)
 return current,best

def room(commits,languages):
 # Independently drawn geometry in an 880 x 448 pixel-art scene.
 css='''<style>.stars{animation:twinkle 3s ease-in-out infinite}.steam{animation:steam 3s ease-out infinite}.cat{transform-box:fill-box;transform-origin:bottom;animation:breathe 4s ease-in-out infinite}.tail{transform-box:fill-box;transform-origin:right;animation:tail 3s ease-in-out infinite}.plant{transform-box:fill-box;transform-origin:bottom;animation:sway 5s ease-in-out infinite}.sleep{animation:sleep 3s linear infinite}.terminal{animation:terminal 20s linear infinite}@keyframes twinkle{50%{opacity:.25}}@keyframes steam{to{transform:translateY(-12px);opacity:0}}@keyframes breathe{50%{transform:scaleY(1.04)}}@keyframes tail{50%{transform:rotate(12deg)}}@keyframes sway{50%{transform:rotate(2deg)}}@keyframes sleep{0%{opacity:0}30%{opacity:1}100%{transform:translate(4px,-16px);opacity:0}}@keyframes terminal{to{transform:translateY(-192px)}}@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'''
 b=css+'<defs><clipPath id="rounded"><rect width="880" height="448" rx="12"/></clipPath><clipPath id="monitor"><rect x="338" y="120" width="224" height="128"/></clipPath></defs><g clip-path="url(#rounded)">'+r(0,0,880,448,'#1c2130')
 for x in range(0,880,64):b+=r(x,0,32,352,'#202635')
 b+=r(0,352,880,8,'#62422e')+r(0,360,880,88,'#3b2c24')
 for row in range(3):
  for col in range(5):b+=r(col*184-row*12,380+row*24,174,4,'#32261f')
 b+=r(32,48,208,168,'#10161e')+r(40,56,192,152,'#0d1a3b')
 for i,(x,y) in enumerate([(66,80),(162,72),(202,112),(82,160),(186,168)]):b+=f'<g class="stars" style="animation-delay:-{i*.6}s">'+r(x,y,4,4,'#eff5ff')+'</g>'
 b+='<path d="M176 80v24h24v-8h-16V80Z" fill="#faf3d9"/>'+r(132,56,8,152,'#10161e')+r(40,128,192,8,'#10161e')+r(24,216,224,12,'#704e35')
 b+=r(320,40,220,52,'#10161e')+r(324,44,212,44,'#f5e9d1')+pix('TOMMY WU',336,52,4,'#302719')
 b+='<circle cx="768" cy="64" r="28" fill="#0d151e"/><circle cx="768" cy="64" r="24" fill="#f5e9d1"/><path d="M768 64l6 17m-6-17 2 12" stroke="#332a20" stroke-width="4"/>'
 for y in [176,248]:b+=r(680,y,176,12,'#704e35')+r(680,y+8,176,4,'#533a2a')
 for i,lang in enumerate(languages[:5]):
  x=684+i*22;h=[40,40,48,40,44][i];col=['#3178bc','#adb2cb','#347aa6','#795618','#3c7896'][i]
  b+=f'<g><title>{escape(lang)}</title>'+r(x,176-h,18,h,col)+r(x,180-h,18,4,'#23374a')+'</g>'
 b+=r(296,148,8,116,'#50545a')+'<path d="M280 156H328L356 264H248Z" fill="#ddd3b0" opacity=".09"/>'+r(280,136,52,20,'#f4cf62')
 b+=r(328,112,240,144,'#404653')+r(336,120,224,128,'#0c1720')
 lines=(commits or ['Building useful software.'])[:7]
 lines=(['$ git log --oneline']+lines)
 while len(lines)<8:lines.append('')
 lines=lines[:8]
 b+='<g clip-path="url(#monitor)"><g class="terminal">'
 for i,line in enumerate(lines*2):b+=txt(line[:41],344,132+i*24,10,'#77db8c',mono=True)
 b+='</g></g>'+r(416,256,64,8,'#404653')+r(404,264,88,5,'#404653')
 b+='<g class="steam"><path d="M568 232q-5-6 0-12" fill="none" stroke="#adb2bc" opacity=".5" stroke-width="3"/></g>'+r(552,232,24,32,'#dfd8c8')+r(576,240,8,12,'#dfd8c8')
 b+=r(264,264,368,16,'#704e35')+r(264,280,368,8,'#533a2a')+r(280,288,12,64,'#704e35')+r(604,288,12,64,'#704e35')
 b+=r(440,296,72,12,'#303840')+r(496,240,12,56,'#303840')+r(468,308,12,52,'#303840')
 b+='<g class="plant">'+r(164,248,8,64,'#29a445')+r(144,264,24,12,'#29a445')+r(172,256,28,12,'#29a445')+r(136,284,28,12,'#29a445')+r(176,280,24,12,'#29a445')+'</g>'+r(144,312,48,48,'#9e5e3a')+r(140,312,56,8,'#77492f')
 b+='<g class="cat">'+r(704,336,64,24,'#e8a353')+r(752,324,24,20,'#e8a353')+r(752,320,8,8,'#c78337')+r(768,320,8,8,'#c78337')+r(712,344,40,4,'#c78337')+'</g><g class="tail"><path d="M708 347l-28 6" stroke="#c78337" stroke-width="8"/></g><g class="sleep">'+pix('Z',792,272,3,'#78818d')+'</g></g>'
 return '<svg xmlns="http://www.w3.org/2000/svg" width="880" height="448" viewBox="0 0 880 448" role="img"><title>Tommy Wu’s animated engineering studio</title>'+b+'</svg>'

def build():
 profile=json.loads((P/'data/profile.json').read_text());repos=json.loads((P/'data/repos.json').read_text())
 user=json.loads((P/'data/github.json').read_text())['data']['user'];c=user['contributionsCollection'];calendar=c['contributionCalendar']
 projects=user['pinnedItems']['nodes'];days=[d for w in calendar['weeks'] for d in w['contributionDays']]
 today=date.fromisoformat(json.loads((P/'data/meta.json').read_text())['date'])
 current,best=streaks(days,today)
 languages=list(dict.fromkeys(r['language'] for r in repos if r.get('language')))
 commits=json.loads((P/'data/commits.json').read_text())
 (A/'room.svg').write_text(room(commits,languages))
 avatar=base64.b64encode((A/'avatar.jpg').read_bytes()).decode()
 body=card(880,260)+pix('> ABOUT',36,32,2)
 body+=txt('Tommy Wu',36,94,32,weight=700)
 body+=txt('Computer Engineering at TMU',36,128,18)
 body+=txt('Founder of paddleiq.pro',36,154,18)
 body+=txt('Hardware, embedded systems and useful software.',36,190,16,M)
 body+='<path d="M36 210H580" stroke="#29313c"/>'
 body+=txt('Toronto · Python · VHDL · TypeScript',36,234,13,M,mono=True)
 body+=r(700,64,144,144,F)+r(703,67,138,138,'#090d12')+f'<image xlink:href="data:image/jpeg;base64,{avatar}" x="707" y="71" width="130" height="130"/>'
 save('about.svg',880,260,body,'Tommy Wu — Computer Engineering at TMU; founder of paddleiq.pro')
 body=card(880,96)
 for x,n,label in [(28,str(c['totalCommitContributions']),'COMMITS'),(241,str(c['totalPullRequestContributions']),'PULL REQS'),(455,str(calendar['totalContributions']),'CONTRIBUTIONS'),(669,str(best)+'D','BEST STREAK')]:body+=pix(n,x,14,4,F)+pix(label,x,51,2,M)
 body+=txt('GitHub activity over the past 12 months',28,84,10,M)
 save('stats.svg',880,96,body,'Verified GitHub statistics over the past 12 months')
 save('projects-heading.svg',880,42,pix('> PROJECTS',0,9,3)+'<path d="M196 20H880" stroke="#29313c" stroke-dasharray="6 6"/>','Projects')
 creatures=['001000100/011000110/111111111/001101100/011101110/001000100/011101110/110010011/100000001','101111101/011010110/110111011/010000010/000111000/001111100/011111110/101111101/011010110','001111100/110000011/100000001/101101101/011111110/001111100/001001100/101111101/011111110','001111100/011010110/110111011/101111101/011111110/001101100/111101111/101101101/101101101']
 for i,p in enumerate(projects):
  lang=p.get('primaryLanguage') or {'name':'Code','color':'#678'};color=lang.get('color') or '#678'
  body=card(434,180)+r(14,36,101,101,color,8)+r(14,36,101,101,'#00000088',8)
  for yy,row in enumerate(creatures[i%4].split('/')):
   for xx,b in enumerate(row):
    if b=='1':body+=r(22+xx*9,44+yy*9,9,9,color)
  name=p['name'];title_size=min(16,278/(len(name)*.62))
  body+=txt(name,133,44,title_size,weight=700,mono=True)
  lines=textwrap.wrap(p.get('description') or 'View project on GitHub.',width=34)
  if len(lines)>4:lines=lines[:4];lines[-1]=lines[-1][:30]+'…'
  for j,line in enumerate(lines):body+=txt(line,133,70+j*18,12.5,M)
  body+=txt('View project →',133,165,12,G)+txt(lang['name'],412-len(lang['name'])*7.5,165,12,M,mono=True)
  save(f'project-{i+1}.svg',434,180,body,name+': '+(p.get('description') or ''))
 body=card(880,263)+pix('> ACTIVITY',36,34,2)
 for col,week in enumerate(calendar['weeks'][-26:]):
  for row,d in enumerate(week['contributionDays']):
   n=d['contributionCount'];color=['#1c252e','#0e4429','#006d32','#26a641','#39d353'][0 if n==0 else 1 if n<5 else 2 if n<10 else 3 if n<20 else 4]
   body+=f'<g><title>{d["date"]}: {n} contributions</title>'+r(36+col*16,82+row*16,13,13,color)+'</g>'
 for y,label,value in [(86,'CURRENT STREAK',f'{current} days'),(142,'BEST STREAK',f'{best} days'),(198,'PAST 12 MONTHS',str(calendar['totalContributions']))]:body+=txt(label,520,y,12,M,mono=True)+txt(value,520,y+26,24,weight=700)
 body+=txt('Last 26 weeks · updated '+today.isoformat(),36,231,11,M)
 save('activity.svg',880,263,body,f"GitHub activity: {calendar['totalContributions']} contributions in the past 12 months")
 intro='Computer Engineering @ TMU · Founder @ paddleiq.pro'
 md='<img src="assets/room.svg" width="100%" alt="Tommy Wu — animated pixel studio" />\n\n'+intro+'\n\n[GitHub](https://github.com/TommyWu1) · [Portfolio](https://tommywu.dev/)\n\n'
 for name in ['about','stats','projects-heading']:md+=f'<img src="assets/{name}.svg" width="100%" alt="{name.replace("-"," ")}" />\n\n'
 for i,p in enumerate(projects):
  md+=f'<a href="{html.escape(p["url"],quote=True)}"><img src="assets/project-{i+1}.svg" width="49%" alt="{html.escape(p["name"]+": "+(p.get("description") or ""),quote=True)}" /></a>\n'
  if i%2:md+='\n'
 md+='\n<img src="assets/activity.svg" width="100%" alt="GitHub contribution calendar and streak statistics" />\n\n<details>\n<summary>Project links and descriptions</summary>\n\n'
 for p in projects:md+=f'- [{p["name"]}]({p["url"]}) — {p.get("description") or "View repository."}\n'
 md+='\n</details>\n\n<sub>GitHub data updated '+today.isoformat()+'. Room shows a stylized night scene; terminal displays recent public commits.</sub>\n'
 (P/'README.md').write_text(md)
 content='<img src="assets/room.svg" alt="Animated pixel studio"><p>'+intro+'</p><p><a href="https://github.com/TommyWu1">GitHub</a> · <a href="https://tommywu.dev/">Portfolio</a></p>'
 for name in ['about','stats','projects-heading']:content+=f'<img class="section" src="assets/{name}.svg" alt="{name}">'
 content+='<div class="grid">'+''.join(f'<a href="{p["url"]}"><img src="assets/project-{i+1}.svg" alt="{escape(p["name"])}"></a>' for i,p in enumerate(projects))+'</div><img class="activity" src="assets/activity.svg" alt="Activity"><footer>GitHub data updated '+today.isoformat()+'. Independent animated profile.</footer>'
 (P/'preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tommy Wu — Engineering</title><style>*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#bec6ce;font:17px Arial,sans-serif}main{max-width:1000px;margin:auto;padding:54px 40px}img{display:block;width:100%;height:auto}p{line-height:1.6;margin:24px 0}a{color:#58a6ff;text-decoration:none}a:focus-visible{outline:2px solid #58a6ff;outline-offset:4px}.section{margin:20px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px 6px}.activity{margin-top:30px}footer{margin-top:32px;font-size:12px}@media(max-width:550px){main{padding:24px 12px}.grid{grid-template-columns:1fr}}</style><main>'+content+'</main></html>')
if __name__=='__main__':build()
