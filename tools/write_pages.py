"""Author static portfolio pages from the supplied, source-grounded content."""
from pathlib import Path
from html import escape as esc
from PIL import Image
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
MISSING='[CẦN BỔ SUNG]'
NAME='Thakorn Tangphadungrutch'
DESCRIPTION='Explore Thakorn Tangphadungrutch’s work in rescue drones, smart safety systems, AI research, engineering education, entrepreneurship, and community impact.'
PROJECTS=json.loads((ROOT/'content/projects.json').read_text())
NAV=[('Home','/'),('About','/about/'),('Projects','/projects/'),('Initiatives & Impact','/initiatives-impact/'),('Recognition','/recognition/'),('Experience','/experience/'),('Drone Simulator','/drone-simulator/'),('Contact','/contact/')]

def photo(name,alt,eager=False,contain=False,wide=False):
 w,h=Image.open(OUT/'assets'/f'{name}.webp').size
 sw,sh=Image.open(OUT/'assets'/f'{name}-small.webp').size
 loading='eager' if eager else 'lazy'
 priority='fetchpriority="high"' if eager else ''
 cls='contain' if contain else ''
 sizes='(max-width:650px) 94vw, (max-width:1352px) 92vw, 1240px' if wide else '(max-width:650px) 94vw, 55vw'
 srcset=f'/assets/{name}-small.webp {sw}w, /assets/{name}.webp {w}w' if sw<w else f'/assets/{name}.webp {w}w'
 return f'<img class="{cls}" src="/assets/{name}.webp" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt,quote=True)}" width="{w}" height="{h}" loading="{loading}" decoding="async" {priority}>'

def arrow(): return '<span aria-hidden="true">↗</span>'
def link(text,href,cls='text-link',external=False,download=False):
 attrs=(' target="_blank" rel="noopener noreferrer"' if external else '')+(' download' if download else '')
 return f'<a class="{cls}" href="{href}"{attrs}>{text}{arrow()}</a>'
def missing(label): return f'<div class="missing-item"><span>{label}</span><span class="missing">{MISSING}</span></div>'
def tags(items): return '<div class="skill-tags">'+''.join(f'<span>{esc(t)}</span>' for t in items)+'</div>'
def is_initiative(p): return p['category'] in ('Entrepreneurship','Community Impact')
def collection(p): return '/initiatives-impact/' if is_initiative(p) else '/projects/'
def url(p): return collection(p)+p['slug']+'/'

def gallery(items,extra_class=''):
 figures=''
 for name,alt,caption in items:
  with Image.open(OUT/'assets'/f'{name}.webp') as source: portrait=source.height>source.width
  frame_class=' class="gallery-portrait"' if portrait else ''
  figures+=f'<figure{frame_class}><a class="gallery-photo" href="/assets/{name}.webp" target="_blank" rel="noopener" aria-label="{esc("Open full image: "+alt,quote=True)}">{photo(name,alt)}<span class="gallery-expand" aria-hidden="true">↗</span></a><figcaption>{esc(caption)}</figcaption></figure>'
 return f'<div class="media-gallery gallery-count-{len(items)} {extra_class}">{figures}</div>'

def system_diagram(p):
 d=p.get('diagram')
 if not d: return ''
 return f'<section class="container system-diagram" id="system-diagram">{heading("Inside the prototype",d["title"])}<figure><a class="diagram-image" href="/assets/{d["image"]}.png" target="_blank" rel="noopener" aria-label="Open the full-size {esc(p["title"],quote=True)} diagram">{photo(d["image"],d["alt"],contain=True,wide=True)}</a><figcaption><p>{esc(d["caption"])}</p>{link("View full-size diagram","/assets/"+d["image"]+".png",external=True)}</figcaption></figure></section>'

def research_notes(p):
 r=p.get('research_results')
 if not r: return ''
 columns=''.join(f'<th scope="col">{esc(c)}</th>' for c in r['columns'])
 rows=''.join('<tr><th scope="row">'+esc(row[0])+'</th>'+''.join(f'<td>{esc(cell)}</td>' for cell in row[1:])+'</tr>' for row in r['rows'])
 return f'''<section class="engineering-notes research-notes" id="research-results"><p class="eyebrow">Research in detail</p><h2>{esc(r['title'])}</h2><p class="technical-intro">{esc(r['intro'])}</p><div class="comparison-scroll" role="region" aria-label="{esc(r['title'],quote=True)}" tabindex="0"><table class="comparison-table"><thead><tr>{columns}</tr></thead><tbody>{rows}</tbody></table></div><p class="technical-source">{esc(r['source_note'])}</p></section>'''

def engineering_notes(p):
 t=p.get('technical')
 if not t: return research_notes(p)
 subsystems=''.join(f'<article><h4>{esc(title)}</h4><p>{esc(body)}</p></article>' for title,body in t['subsystems'])
 workflow=''.join(f'<li><h4>{esc(title)}</h4><p>{esc(body)}</p></li>' for title,body in t['workflow'])
 figures=''
 for name,alt,caption in t['figures']:
  original=next(OUT/'assets'/f'{name}.{ext}' for ext in ('png','jpeg','jpg') if (OUT/'assets'/f'{name}.{ext}').exists())
  original_url='/assets/'+original.name
  figures+=f'<figure><a href="{original_url}" target="_blank" rel="noopener" aria-label="{esc("Open original figure: "+alt,quote=True)}">{photo(name,alt,contain=True)}</a><figcaption>{esc(caption)}</figcaption>{link("Open original figure",original_url,external=True)}</figure>'
 e=t['evaluation']
 columns=''.join(f'<th scope="col">{esc(c)}</th>' for c in e['columns'])
 rows=''.join('<tr><th scope="row">'+esc(row[0])+'</th>'+''.join(f'<td>{esc(cell)}</td>' for cell in row[1:])+'</tr>' for row in e['rows'])
 return f'''<section class="engineering-notes" id="engineering-notes"><p class="eyebrow">Engineering in detail</p><h2>{esc(t['title'])}</h2><p class="technical-intro">{esc(t['intro'])}</p><div class="subsystem-grid">{subsystems}</div><h3>{esc(t['workflow_title'])}</h3><ol class="technical-workflow">{workflow}</ol><div class="report-figures">{figures}</div><section class="evaluation-section"><h3>{esc(e['title'])}</h3><p>{esc(e['intro'])}</p><div class="comparison-scroll" role="region" aria-label="{esc(e['title'],quote=True)}" tabindex="0"><table class="comparison-table"><thead><tr>{columns}</tr></thead><tbody>{rows}</tbody></table></div></section><section class="technical-next"><h3>{esc(t['followup_title'])}</h3><p>{esc(t['followup'])}</p></section><p class="technical-source">{esc(t['source_note'])}</p></section>'''

def photo_stories(p):
 return ''.join(f'<section class="activity-photo-story" id="{s["id"]}"><p class="eyebrow">{esc(s.get("eyebrow","Leadership in practice"))}</p><h3>{esc(s["title"])}</h3><p>{esc(s["intro"])}</p>{gallery(s["images"],s.get("gallery_class","preserve-frame"))}</section>' for s in p.get('photo_stories',[]))

def further_details(p):
 details=p.get('details',[])
 if not details: return ''
 items=''.join(f'<article><h4>{esc(title)}</h4><p>{esc(text)}</p></article>' for title,text in details)
 return f'<section class="details-to-add resume-details"><h3>Further details</h3><div class="resume-detail-grid">{items}</div></section>'

def write_page(path,title,body,active,description=DESCRIPTION):
 nav=''
 for label,target in NAV:
  current='aria-current="page"' if label==active else ''
  nav+=f'<a href="{target}" {current}>{label}</a>'
 footer_nav=''.join(f'<a href="{target}">{label}</a>' for label,target in NAV[1:])
 about_styles='<link rel="stylesheet" href="/assets/about-gallery.css">' if path=='/about/' else ''
 wro_styles='<link rel="stylesheet" href="/assets/wro-gallery.css">' if path in ('/projects/','/projects/wro-2026-project/','/recognition/') else ''
 experience_styles='<link rel="stylesheet" href="/assets/experience.css">' if path=='/experience/' else ''
 simulator_assets='<link rel="stylesheet" href="/assets/drone-simulator.css"><script type="module" src="/assets/drone-simulator.js"></script>' if path=='/drone-simulator/' else ''
 html=f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | {NAME}</title><meta name="description" content="{esc(description,quote=True)}"><meta name="theme-color" content="#0c293b">
<link rel="icon" type="image/png" href="/assets/thakorn-mark.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/portfolio.css"><link rel="stylesheet" href="/assets/initiatives.css?v=leadership-4"><link rel="stylesheet" href="/assets/resume-details.css?v=1">{about_styles}{wro_styles}{experience_styles}<link rel="stylesheet" href="/assets/refinements.css">{simulator_assets}<script src="/assets/site.js?v=3" defer></script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner"><a class="identity" href="/" aria-label="{NAME}, home"><span class="brand-mark"><img src="/assets/thakorn-mark.png" width="94" height="94" alt=""></span><span class="brand-name">THAKORN<span>TANGPHADUNGRUTCH</span></span></a><button type="button" class="menu-toggle" aria-label="Open navigation" aria-controls="main-nav" aria-expanded="false"><span></span><span></span></button><nav id="main-nav" class="main-nav" aria-label="Main navigation">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="container footer-top"><div><p class="footer-name">{NAME}<span>Lê Đức Trí</span></p><p>Engineering. Research. Community.</p></div><nav aria-label="Footer navigation">{footer_nav}</nav></div><div class="container footer-bottom"><span>© 2026 {NAME}</span><span>Brentwood School · Class of 2027</span><a href="#main">Back to top ↑</a></div></footer>
</body></html>'''
 target=OUT/path.strip('/')/'index.html' if path!='/' else OUT/'index.html'
 target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(html,encoding='utf-8')

def heading(kicker,title,description='',right=''):
 desc=f'<p>{description}</p>' if description else ''
 return f'<div class="section-heading"><div><p class="eyebrow">{kicker}</p><h2>{title}</h2>{desc}</div>{right}</div>'

def card(p):
 if p.get('image'): visual=photo(p['image'],p['alt'],contain=p.get('contain',False))
 else:
  text='Optimization<br>& design.' if p['slug'].startswith('gas') else 'Science.<br>History.<br>Ethics.'
  visual=f'<div class="typographic-cover"><span>{p["status"].upper()}</span><strong>{text}</strong><span>Project image: {MISSING}</span></div>'
 action='View initiative' if is_initiative(p) else 'View project'
 return f'''<article class="project-card"><a class="card-image" href="{url(p)}" aria-label="Explore {esc(p['title'],quote=True)}">{visual}<span class="image-action" aria-hidden="true">↗</span></a><div class="card-info"><p class="eyebrow">{p['category']}</p><h3><a href="{url(p)}">{p['title']}</a></h3><p>{p['summary']}</p><div class="card-bottom"><span>{p['date']}</span>{link(action,url(p))}</div></div></article>'''

def detail(p):
 if p.get('image'):
  cls='diagram-figure' if p.get('contain') else ''
  if p.get('preserve_frame'): cls+=' preserve-frame'
  with Image.open(OUT/'assets'/f'{p["image"]}.webp') as source:
   if source.height>source.width and not p.get('preserve_frame'): cls+=' portrait-figure'
  visual=f'<figure class="detail-figure {cls}">{photo(p["image"],p["alt"],eager=True,contain=p.get("contain",False),wide=True)}<figcaption>{p["caption"]}</figcaption></figure>'
 else: visual=f'<div class="detail-text-cover"><p class="eyebrow">{p["category"]}</p><p>{p.get("formal_title",p["title"])}</p><span>Project image: <span class="missing">{MISSING}</span></span></div>'
 metrics=''.join(f'<div><strong>{esc(v)}</strong><span>{label}</span></div>' for v,label in p['metrics'])
 metrics=f'<div class="detail-metrics">{metrics}</div>' if metrics else ''
 steps=''.join(f'<section class="project-step"><span class="step-number">{i:02}</span><div><h3>{title}</h3><p>{text}</p></div></section>' for i,(title,text) in enumerate(p['process'],1))
 evidence=''.join(link(t,u,'document-link',external=True) for t,u in p['evidence'])
 evidence=f'<div class="evidence"><p class="eyebrow">Project materials</p>{evidence}</div>' if evidence else ''
 note=f'<div class="project-note"><h3>Current scope</h3><p>{p["note"]}</p></div>' if p.get('note') else ''
 formal=f'<div class="formal-title"><span class="eyebrow">Research title</span><p>{p["formal_title"]}</p></div>' if p.get('formal_title') else ''
 images=([p['secondary']] if p.get('secondary') else [])+p.get('gallery',[])
 secondary='<section class="project-gallery"><h3>In pictures</h3>'+gallery(images)+'</section>' if images else ''
 mentor=f'<div><dt>Research mentor</dt><dd>{p["mentor"]}</dd></div>' if p.get('mentor') else ''
 storytitle='Learning through research.' if p['category']=='Research' else 'From an idea to something useful.'
 parent_label='Initiatives & Impact' if is_initiative(p) else 'All projects'
 active='Initiatives & Impact' if is_initiative(p) else 'Projects'
 jump=link('Explore the engineering','#engineering-notes','diagram-jump') if p.get('technical') else ''
 jump+=link('View the poster’s experiments','#research-results','diagram-jump') if p.get('research_results') else ''
 jump+=link('View the system diagram','#system-diagram','diagram-jump') if p.get('diagram') else ''
 if any(s['id']=='field-testing' for s in p.get('photo_stories',[])):
  jump+=link('View field-testing photos','#field-testing','diagram-jump')
 if p['slug']=='rescue-drone-engineering':
  jump+=link('Try the Rescue Mission','/drone-simulator/','diagram-jump')
 if p['slug']=='safeflow-vietnam' and p.get('photo_stories'):
  jump+=''.join(link(f'Explore {story["title"].split(" · ")[0]}',f'#{story["id"]}','diagram-jump') for story in p['photo_stories'])
 continuation='Explore more initiatives' if is_initiative(p) else 'Explore more engineering & research'
 body=f'''<section class="container detail-header">{link(parent_label,collection(p),'back-link')}<p class="eyebrow">{p['category']} / {p['status']}</p><h1>{p['title']}</h1><p class="detail-deck">{p['summary']}</p><div class="project-byline"><span>{p['role']}</span><span>{p['date']}</span></div>{jump}</section>
<div class="container">{visual}</div><div class="container detail-layout"><aside class="project-sidebar"><p class="eyebrow">At a glance</p><dl><div><dt>Role</dt><dd>{p['role']}</dd></div><div><dt>Timeline</dt><dd>{p['date']}</dd></div><div><dt>Focus</dt><dd>{p['category']}</dd></div>{mentor}</dl>{tags(p['skills'])}{evidence}</aside><article class="project-story"><p class="eyebrow">The initiative</p><h2>{storytitle}</h2><p class="story-lead">{p['overview']}</p>{formal}{metrics}{steps}{note}{engineering_notes(p)}{photo_stories(p)}{secondary}{further_details(p)}</article></div>{system_diagram(p)}<section class="container next-section"><p class="eyebrow">Continue exploring</p>{link(continuation,collection(p),'large-link')}</section>'''
 if not is_initiative(p): body=body.replace('<p class="eyebrow">The initiative</p>','<p class="eyebrow">The project</p>')
 write_page(url(p),p['title'],body,active,p['summary'])

P={p['slug']:p for p in PROJECTS}
home=f'''
<section class="container home-hero"><div class="hero-copy"><p class="eyebrow">Student engineer · Researcher · Builder</p><h1>From prototype<br>to <em>public impact.</em></h1><p class="hero-name">{NAME} <span>/ Lê Đức Trí</span></p><p class="hero-intro">I build, test, and communicate engineering ideas for safer communities and more accessible learning.</p><div class="hero-actions">{link('Explore my work','/projects/','button')}{link('About me','/about/')}</div><div class="hero-school"><span class="small-line"></span><span>Brentwood School, United Kingdom<br>Class of 2027</span></div></div><figure class="hero-portrait">{photo('portrait','Thakorn beside his AI, Finance, and the Vietnam Stock Market research poster at SVIIF.',eager=True)}<figcaption><p>Making ideas<br>understandable.</p><span>Silicon Valley International Invention Festival</span></figcaption></figure></section>
<section class="proof-band"><div class="container proof-grid"><a href="/projects/rescue-drone-engineering/"><strong>60<span> flights</span></strong><p>Laboratory tests on the rescue-drone prototype</p></a><a href="/initiatives-impact/droneverse/"><strong>500<span> people</span></strong><p>Reached through the DRONEVERSE exhibition</p></a><a href="/initiatives-impact/stem-gears/"><strong>VND 100m</strong><p>STEM GEARS revenue, fully donated to community initiatives</p></a></div></section>
<section class="container section">{heading('01 / Selected work','Engineering with a purpose.','Building, testing, and learning across disciplines.',link('All projects','/projects/'))}<div class="featured-grid">{card(P['rescue-drone-engineering'])}{card(P['smart-life-jacket'])}{card(P['ai-vietnam-stock-market'])}</div><div class="diagram-previews"><div class="diagram-preview-heading"><p class="eyebrow">Inside the prototypes</p><h3>See how the systems work.</h3></div><div class="diagram-preview-grid"><a href="/projects/rescue-drone-engineering/#system-diagram">{photo('rescue-drone-operation','Rescue drone architecture and flight-test diagram.',contain=True)}<span>Rescue drone · Flight, control, and testing {arrow()}</span></a><a href="/projects/smart-life-jacket/#system-diagram">{photo('smartvest-operation','SmartVest-SAR tracking, radio communication, and power diagram.',contain=True)}<span>SmartVest-SAR · Tracking, communication, and power {arrow()}</span></a></div></div></section>
<section class="impact-section"><div class="container impact-grid"><figure>{photo('phyx-small-group-learning','A volunteer guiding students during classroom work in the PhyX program at Làng May Mắn.')}<figcaption>Physics Behind Engineering · Làng May Mắn</figcaption></figure><div><p class="eyebrow">02 / Initiatives & Impact</p><h2>Knowledge grows<br>when it is <em>shared.</em></h2><p>Through STEM GEARS, SafeFlow Vietnam, Creativism Club, and PhyX Club, I connect educational products, student leadership, water safety, and hands-on STEM learning.</p><div class="impact-facts"><span><strong>2 months</strong>Teaching at Làng May Mắn</span><span><strong>30 students</strong>Learning through the PhyX program</span></div>{link('Explore Initiatives & Impact','/initiatives-impact/','button button-light')}</div></div></section>
<section class="container home-recognition">{heading('03 / Recognition','Milestones in learning.',right=link('All recognition','/recognition/'))}<div class="recognition-preview"><a href="/recognition/#wro"><span class="award-year">2026</span><h3>First Place</h3><p>World Robot Olympiad<br>Vietnam National Round · RoboSports</p>{arrow()}</a><a href="/recognition/#sviif"><span class="award-year">2025</span><h3>Gold Medal</h3><p>Silicon Valley International<br>Invention Festival</p>{arrow()}</a></div></section>'''
write_page('/','Engineering for people',home,'Home')

principles=[('Build to learn','Use prototypes to expose assumptions and improve decisions.'),('Test with evidence','Measure performance and revise from real results.'),('Explain accessibly','Make technical ideas understandable to a broader audience.'),('Connect with people','Start from a real need and connect technology with the people it can serve.')]
principle_html=''.join(f'<article><span class="step-number">{i:02}</span><h3>{t}</h3><p>{d}</p></article>' for i,(t,d) in enumerate(principles,1))
about=f'''
<section class="container page-hero about-hero"><div><p class="eyebrow">About / {NAME}</p><h1>Curiosity, built<br>into <em>practice.</em></h1><p class="page-deck">I am a student engineer, researcher, and community builder exploring how robotics, artificial intelligence, and mechanical design can address real-world challenges.</p></div><figure>{photo('drone-prototype','Thakorn holding the rescue-drone prototype during development.',eager=True)}<figcaption>Learning by building and testing.</figcaption></figure></section>
<section class="container about-story"><div class="section-side"><p class="eyebrow">The longer story</p><h2>Theory. Practice.<br>People.</h2></div><div class="prose"><p>I am a secondary student at Brentwood School in the United Kingdom, having previously studied at the British International School Ho Chi Minh City. I am most engaged when I can move between theory and practice: understanding how a system works, building a prototype, testing it under real constraints, and explaining the result clearly to others.</p><p>That approach has shaped my work across robotics, artificial intelligence, and mechanical design. For a rescue-drone project, I completed 60 laboratory flights and three outdoor field trials. I later developed a smart life-jacket prototype connecting location tracking and drift-direction prediction with the goal of drone-supported rescue. In research, I led a team studying AI applications in Vietnam’s stock market and collaborated on deep-learning-based optimization of a small gas turbine compressor.</p><p>I also care about how technical knowledge is shared. I founded STEM GEARS, developing ten 3D-printed cutaway aircraft-engine models and STEM kits for younger learners. The venture sold 60 products and generated VND 100 million in revenue, all donated to Creativism Club and SafeFlow Vietnam. Through DRONEVERSE, SafeFlow, and PhyX, I have helped make engineering, water safety, and STEM learning more accessible.</p><p>Across these experiences, I have learned to value iteration, evidence, teamwork, and responsibility. A strong project should be tested honestly, communicated accessibly, and connected to a meaningful need.</p>{link('Download résumé','/documents/Thakorn-Tangphadungrutch-Resume.pdf',download=True)}</div></section>
<section class="principles-section"><div class="container">{heading('How I work','Four principles I return to.')}<div class="principles-grid">{principle_html}</div></div></section>
<section class="container section about-in-pictures">{heading('Beyond the desk','Building. Explaining. Connecting.')} {gallery([('stem-model-maker','Thakorn holding a cutaway aircraft-engine model.','Making mechanical systems visible through STEM GEARS.'),('creativism-darahoa-stem-demo','Volunteers sharing a tabletop STEM demonstration with children at Darahoa.','Making room for shared discovery through Creativism’s Darahoa program.'),('safeflow-waterside-testing','A volunteer testing a model boat as a child watches at the water’s edge.','Connecting model-building with observation through SafeFlow Vietnam.')],'gallery-three preserve-frame')}{link('Explore Initiatives & Impact','/initiatives-impact/')}</section>
<section class="container section" id="skills">{heading('Skills & interests','A toolkit for making ideas real.')}<div class="skills-grid"><div><h3>Programming & data</h3><p>Python, pandas, NumPy, scikit-learn, Matplotlib, Seaborn.</p><p>Feature engineering, Decision Trees, backtesting, portfolio optimization, and Value-at-Risk.</p>{link('AI research','/projects/ai-vietnam-stock-market/')}</div><div><h3>Engineering</h3><p>Drone prototyping, flight testing, systems integration, 3D modeling and printing, and embedded systems.</p>{link('Engineering projects','/projects/#engineering')}</div><div><h3>Beyond the workshop</h3><p><strong>Languages</strong><br>Thai, English, Vietnamese</p><p><strong>Sports</strong><br>Football, tennis</p></div></div></section>
<section class="container education-section">{heading('Education','Learning across two settings.')}<div class="education-row"><span>Class of 2027</span><div><h3>Brentwood School</h3><p>Secondary student · United Kingdom</p></div></div><div class="education-row"><span>Previous school</span><div><h3>British International School Ho Chi Minh City</h3><p>Ho Chi Minh City, Vietnam</p></div></div><div class="about-missing">{missing('Personal origin story')}{missing('Intended university field and long-term goal')}</div></section>'''
write_page('/about/','About',about,'About')

categories=[('Engineering','engineering','Systems for the real world.'),('Research','research','Questions worth investigating.')]
category_links=''.join(f'<a href="#{a}">{c}</a>' for c,a,t in categories)
projects=f'<section class="container page-hero"><p class="eyebrow">Engineering & research</p><h1>Ideas, tested<br><em>in the world.</em></h1><p class="page-deck">Rescue systems, robotics, mechanical design, and independent research. Each project connects a question with a process of building, testing, and learning.</p><nav class="category-nav" aria-label="Project categories">{category_links}</nav></section>'
for i,(category,anchor,title) in enumerate(categories,1):
 cards=''.join(card(p) for p in PROJECTS if p['category']==category)
 projects+=f'<section class="container project-category" id="{anchor}">{heading(f"0{i} / {category}",title)}<div class="project-grid">{cards}</div></section>'
projects+=f'<section class="container collection-bridge"><div><p class="eyebrow">Leadership beyond the prototype</p><h2>Initiatives & Impact</h2><p>Explore the clubs, community programs, and educational venture that bring this work to people.</p></div>{link("Explore initiatives","/initiatives-impact/","button")}</section>'
write_page('/projects/','Projects',projects,'Projects')

initiative_groups=[('Student clubs','clubs','Ideas grow through shared learning.',['droneverse','physics-behind-engineering']),('Community programs','community-impact','Engineering meets community.',['safeflow-vietnam']),('Entrepreneurship','entrepreneurship','A venture with a community purpose.',['stem-gears'])]
initiative_links=''.join(f'<a href="#{anchor}">{label}</a>' for label,anchor,title,slugs in initiative_groups)
initiatives=f'''<section class="container page-hero initiatives-hero"><div><p class="eyebrow">Initiatives & Impact</p><h1>Build ideas.<br><em>Bring people in.</em></h1><p class="page-deck">Student clubs, community programs, and an educational venture: spaces where I turn technical curiosity into shared learning and practical support.</p><nav class="category-nav" aria-label="Initiative categories">{initiative_links}</nav></div><figure class="leadership-hero">{photo('safeflow-waterside-testing','A volunteer lowering a model boat into the water while a child watches beside him at Suoi Tuong.',eager=True,contain=True)}<figcaption>Testing a model together at the water’s edge · SafeFlow Vietnam, Suối Tượng.</figcaption></figure></section>
<section class="proof-band initiative-proof"><div class="container proof-grid"><a href="/initiatives-impact/stem-gears/"><strong>60<span> products</span></strong><p>STEM GEARS models sold, generating VND 100m donated in full</p></a><a href="/initiatives-impact/droneverse/"><strong>500<span> people</span></strong><p>Reached through the DRONEVERSE exhibition</p></a><a href="/initiatives-impact/safeflow-vietnam/"><strong>~200<span> people</span></strong><p>Students and residents served through two SafeFlow field programs</p></a></div></section>'''
initiatives+=f'<section class="container leadership-section" id="leadership-in-practice">{heading("Leadership in practice","Teach. Build. Test together.","Moments of shared learning from Creativism, PhyX, and SafeFlow Vietnam.")}{gallery([("creativism-darahoa-stem-demo","Volunteers demonstrating a tabletop STEM activity to children at Darahoa.","Creativism · Sharing a STEM demonstration at Darahoa."),("phyx-small-group-learning","A volunteer guiding students working at classroom desks.","PhyX · Supporting classroom participation at Làng May Mắn."),("safeflow-model-building","A volunteer and a child assembling a small boat model together.","SafeFlow Vietnam · Building a model together at Suối Tượng.")],"gallery-three preserve-frame")}<div class="leadership-links">{link("Darahoa program","/initiatives-impact/droneverse/#darahoa")}{link("PhyX teaching","/initiatives-impact/physics-behind-engineering/#lang-may-man")}{link("Suối Tượng field program","/initiatives-impact/safeflow-vietnam/#suoi-tuong")}</div></section>'
for i,(label,anchor,title,slugs) in enumerate(initiative_groups,1):
 cards=''.join(card(P[slug]) for slug in slugs)
 layout='initiative-pair' if len(slugs)>1 else 'initiative-feature'
 initiatives+=f'<section class="container initiative-category {layout}" id="{anchor}">{heading(f"0{i} / {label}",title)}<div class="initiative-grid">{cards}</div></section>'
initiatives+=f'<section class="container collection-bridge"><div><p class="eyebrow">Behind the ideas</p><h2>Engineering & research</h2><p>Explore the systems, experiments, and technical questions that connect with these initiatives.</p></div>{link("Explore projects","/projects/","button")}</section>'
write_page('/initiatives-impact/','Initiatives & Impact',initiatives,'Initiatives & Impact','Explore Thakorn’s leadership in Creativism Club, PhyX Club, SafeFlow Vietnam, and STEM GEARS, connecting STEM education with community impact.')
for p in PROJECTS: detail(p)

recognition=f'''
<section class="container page-hero"><p class="eyebrow">Recognition</p><h1>Milestones.<br><em>More to learn.</em></h1><p class="page-deck">Selected distinctions in robotics, invention, physics, and mathematics.</p></section>
<section class="container awards-featured"><article id="wro" class="award-feature"><figure>{photo(P['wro-2026-project']['image'],P['wro-2026-project']['alt'],eager=True)}</figure><div class="award-feature-copy"><p class="eyebrow">2026 / Robotics</p><h2>First Place</h2><p class="award-name">World Robot Olympiad<br>Vietnam National Round</p><p><strong>RoboSports · Double Tennis</strong><br>Team KE GATE · Robot Assembly Lead</p><p>Advanced to the International Round in Puerto Rico, scheduled for December 2026.</p><span class="status-label">International round upcoming</span>{link('Project details','/projects/wro-2026-project/')}</div></article><article id="sviif" class="award-feature"><figure>{photo('sviif-award','Thakorn with his SVIIF award certificate and medal.')}</figure><div class="award-feature-copy"><p class="eyebrow">2025 / Invention & research</p><h2>Gold Medal</h2><p class="award-name">Silicon Valley International<br>Invention Festival</p><p>AI, Finance, and the Vietnam Stock Market · Team Leader</p>{link('Explore the research','/projects/ai-vietnam-stock-market/')}</div></article></section>
<section class="container recognition-gallery">{heading('Learning alongside others','The people around each milestone.')}{gallery([('wro-collaboration','Students reviewing a laptop beside a robotics competition field.','Working through the robotics challenge together.'),('sviif-delegation','A group of SVIIF participants posing with Vietnamese flags.','With fellow participants at the Silicon Valley International Invention Festival.')])}</section>
<section class="container section">{heading('Academic distinctions','Physics. Mathematics. Scholarship.')}<div class="award-list"><article><span class="award-date">Year: {MISSING}</span><h3>Silver Award</h3><p>British Physics Olympiad<br>Intermediate Competition</p></article><article><span class="award-date">2024</span><h3>Gold Award</h3><p>Intermediate Mathematical Challenge</p></article><article><span class="award-date">2025</span><h3>Year 11 Physics Award</h3><p>Brentwood School</p></article><article><span class="award-date">2024</span><h3>Year 10 Academic Award</h3><p>Brentwood School</p></article></div><div class="recognition-missing">{missing('Official result links and additional certificates')}</div></section>'''
write_page('/recognition/','Recognition',recognition,'Recognition')

EXPERIENCES=[
 ('MENTORING','Dates: '+MISSING,'Brentwood School','Mathematics Mentor','I mentored students in Years 7–10 in algebra, geometry, numerical reasoning, and academic problem-solving through structured peer tutoring.',['Peer tutoring','Mathematics','Communication'],'Mentoring hours and number of students'),
 ('INTERNSHIP','Jun – Jul 2025','Saigon Hi-Tech Park','Technology Intern','I completed a two-month internship with exposure to applied research, prototyping workflows, and the development of technology-based solutions.',['Applied technology','Prototyping'],'Department, main assignment, and project output'),
 ('TRAINING','27 Jun – 27 Sep 2025','Ho Chi Minh City University of Technology and Education','AI & Embedded Systems Training','I completed a three-month, project-based training program organized by the Faculty of Electrical and Electronics Engineering at HCMUTE, connecting foundations in programming and AI with practical work in embedded systems and computer vision.',['Python','Microcontrollers','OpenCV','TensorFlow'],''),
 ('ENRICHMENT','Apr – Aug 2024','The Duke of Edinburgh’s Award','Silver-Level Participant','I completed the volunteering, physical activity, skills-development, and expedition components of the Silver level.',['Volunteering','Expedition','Personal development'],'Expedition detail or personal reflection')]
experience_rows=''
for cat,date,org,title,text,skills,gap in EXPERIENCES:
 pictures=gallery([('internship-visit','Students observing a production process during an internship visit.','Observing production processes during the Saigon Hi-Tech Park internship.')]) if cat=='INTERNSHIP' else ''
 details=''
 anchor=''
 if cat=='TRAINING':
  anchor=' id="hcmute"'
  curriculum=[
   ('Programming & algorithmic design','Computational problem-solving, algorithm design, and data structures using Python.'),
   ('Embedded systems & computer vision','Microcontroller programming, sensor interfacing, and computer-vision pipelines with OpenCV.'),
   ('AI foundations','Linear algebra and calculus for AI, alongside the fundamentals of machine learning and neural networks.'),
   ('Real-time AI','Deploying pre-trained models for real-time inference using TensorFlow.'),
  ]
  curriculum_items=''.join(f'<div><dt>{esc(label)}</dt><dd>{esc(body)}</dd></div>' for label,body in curriculum)
  campus_images=[
   ('hcmute-campus-vehicle','Two people reviewing a laptop and radio-control setup on a yellow autonomous vehicle at HCMUTE.','Supporting operation and testing of the autonomous vehicle project.'),
   ('hcmute-drone-electronics','Hands-on work on a drone’s onboard electronics at a laboratory workbench.','Working on drone electronics in the laboratory.'),
   ('hcmute-vehicle-controls','A closer view of two people examining the laptop, controller, and wiring on the autonomous vehicle.','Reviewing the autonomous vehicle’s controls and wiring during testing.'),
  ]
  certificate_url='/documents/HCMUTE-AI-Embedded-Systems-Certificate.pdf'
  details=f'''<section class="training-section" aria-labelledby="hcmute-curriculum"><h3 id="hcmute-curriculum">What I studied</h3><dl class="training-curriculum">{curriculum_items}</dl></section><section class="training-section" aria-labelledby="hcmute-practice"><h3 id="hcmute-practice">Campus and laboratory work</h3>{gallery(campus_images,'hcmute-gallery preserve-frame')}</section><section class="training-certificate" aria-labelledby="hcmute-certificate"><a class="certificate-preview" href="{certificate_url}" target="_blank" rel="noopener" aria-label="Open HCMUTE training completion certificate PDF">{photo('hcmute-certificate','HCMUTE certificate confirming Le Duc Tri’s completion of the AI and Embedded Systems training program, 27 June to 27 September 2025.',contain=True)}</a><div><p class="eyebrow">Program completed</p><h3 id="hcmute-certificate">Performance Evaluation &amp; Project Completion Certificate</h3><p>Issued by the Faculty of Electrical and Electronics Engineering, HCMUTE, and signed by Assoc. Prof. Dr. Lê Mỹ Hà, Acting Dean.</p>{link('View certificate · PDF',certificate_url,external=True)}</div></section>'''
  details+=f'<section class="training-section" aria-labelledby="hcmute-outcome"><h3 id="hcmute-outcome">Applied project work</h3><p>I supported the operation and testing of an autonomous vehicle project and completed my own rescue-drone prototype, applying the program’s training in embedded systems and computer vision.</p>{link("Explore my rescue-drone project","/projects/rescue-drone-engineering/")}</section>'
 experience_rows+=f'<article{anchor}><div class="experience-when"><span>{cat}</span><p>{date}</p></div><div><p class="eyebrow">{org}</p><h2>{title}</h2><p>{text}</p>{tags(skills)}{pictures}{details}{missing(gap) if gap else ""}</div></article>'
experience=f'<section class="container page-hero experience-hero"><div><p class="eyebrow">Experience</p><h1>Learn deeply.<br><em>Share generously.</em></h1><p class="page-deck">Mentoring, applied technology, and learning beyond the classroom.</p></div><figure>{photo("internship","Thakorn and other students examining a technology demonstration during the SHTP internship.",eager=True)}<figcaption>Exploring applied technology at Saigon Hi-Tech Park.</figcaption></figure></section><section class="container experience-list">{experience_rows}</section><section class="container next-section"><p class="eyebrow">Learning in action</p>{link("See how this connects to my projects","/projects/","large-link")}</section>'
write_page('/experience/','Experience',experience,'Experience')

contact=f'''<section class="container page-hero contact-hero"><p class="eyebrow">Contact</p><h1>A conversation<br>can start <em>an idea.</em></h1><p class="page-deck">Interested in engineering, research, education, or student-led collaboration? I would be glad to share more about my projects and learning process.</p></section>
<section class="container contact-grid"><div class="contact-primary"><p class="eyebrow">Get in touch</p><h2>Public email</h2><p class="contact-email"><a href="mailto:thakorntang7@gmail.com">thakorntang7@gmail.com</a></p><div class="contact-resource"><p class="eyebrow">A closer look</p><h3>Résumé</h3><p>Education, projects, leadership, and selected recognition in one document.</p>{link('Download résumé · PDF','/documents/Thakorn-Tangphadungrutch-Resume.pdf','button',download=True)}</div></div><div class="contact-links"><h2>Community initiatives</h2><p>Project pages included in my résumé.</p>{link('SafeFlow Vietnam','https://www.facebook.com/SafeFlowVietnam','external-row',external=True)}{link('Creativism Club','https://www.facebook.com/Creativism20/','external-row',external=True)}</div></section>'''
write_page('/contact/','Contact',contact,'Contact')

simulator=(ROOT/'content/drone-simulator.html').read_text(encoding='utf-8')
write_page('/drone-simulator/','Drone Simulator',simulator,'Drone Simulator','Try a 75-second rescue-drone mission: search for swimmers, navigate around obstacles, and release flotation rings in an educational 2D game.')

not_found=f'<section class="container page-hero"><p class="eyebrow">404 / Page not found</p><h1>Let’s get<br><em>back on track.</em></h1><p class="page-deck">This page could not be found.</p>{link("Return home","/","button")}</section>'
write_page('/404/','Page not found',not_found,'')
(OUT/'404.html').write_text((OUT/'404/index.html').read_text(),encoding='utf-8')
def redirect(old_path,new_path,title):
 old=OUT/old_path.strip('/');old.mkdir(parents=True,exist_ok=True)
 (old/'index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={new_path}"><link rel="canonical" href="{new_path}"><title>{esc(title)}</title></head><body><main><h1>{esc(title)}</h1><a href="{new_path}">Continue to {esc(title)}</a></main></body></html>',encoding='utf-8')
for p in PROJECTS:
 if is_initiative(p): redirect('/projects/'+p['slug']+'/',url(p),p['title'])
redirect('/projects/3d-cutaway-engine-venture/','/initiatives-impact/stem-gears/','STEM GEARS')
print('Authored eight main pages, six technical project stories, four initiative stories, and fallback routes.')
