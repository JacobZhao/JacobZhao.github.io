"""Render the static pages. Requires Python 3 only: python build.py."""
from pathlib import Path
from html import escape
from collections import defaultdict
import json

ROOT = Path(__file__).resolve().parent
PUBLICATIONS = json.loads((ROOT / 'data/publications.json').read_text())
SCHOLAR = 'https://scholar.google.com/citations?user=62711IsAAAAJ&hl=en'
SITE = 'https://jacobzhao.github.io/'
LABELS = {'journal': 'Journal article', 'conference': 'Conference / workshop', 'preprint': 'Preprint', 'book': 'Book / chapter / correction'}

def icon(name):
    paths = {
        'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
        'scholar': '<path d="m2 8 10-5 10 5-10 5Z M6 10v7c4 3 8 3 12 0v-7 M22 8v9"/>',
        'code': '<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
        'id': '<circle cx="12" cy="12" r="9"/><path d="M8 10v7m0-10v1m4 2h2a3 3 0 0 1 0 7h-2Z"/>',
        'link': '<path d="M14 3h7v7m0-7L10 14m0-10H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-5"/>'
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'

def profile():
    links = [('mail', 'Email', 'mailto:zhao.dafang@ist.osaka-u.ac.jp'), ('scholar','Google Scholar',SCHOLAR), ('code','GitHub','https://github.com/JacobZhao'), ('id','ORCID','https://orcid.org/0000-0001-8107-4260'), ('link','researchmap','https://researchmap.jp/zhaodafang?lang=en')]
    return '''<aside class="profile" aria-label="Dafang Zhao's profile">
      <img class="portrait" src="assets/portrait.jpg" alt="Dafang Zhao" width="160" height="160">
      <h2 class="profile-name">Dafang Zhao</h2>
      <p class="profile-role">Specially Appointed<br>Assistant Professor</p>
      <p class="profile-institution">The University of Osaka<span>Graduate School of Information<br>Science and Technology</span></p>
      <ul class="profile-links"><li class="location">''' + icon('pin') + 'Osaka, Japan</li>' + ''.join(f'<li>{icon(i)}<a href="{escape(url)}">{title}</a></li>' for i,title,url in links) + '''</ul>
      <p class="sidebar-note">AI for energy · Smart buildings<br>Optimization · Cyber-physical systems</p>
    </aside>'''

def pub(p):
    authors = escape(p['authors']).replace('Dafang Zhao','<strong>Dafang Zhao</strong>').replace('D Zhao','<strong>D. Zhao</strong>')
    link_label = 'Preprint' if p['type'] == 'preprint' else ('Paper' if p['url'] != p['scholar'] else 'Details')
    links = f'<a href="{escape(p["url"])}">{link_label} ↗</a>'
    if p.get('preprint'): links += f'<a href="{escape(p["preprint"])}">Preprint ↗</a>'
    return f'''<li class="publication" data-type="{p['type']}" data-year="{p['year']}">
      <div class="pub-kicker"><span class="year">{p['year']}</span><span>{LABELS[p['type']]}</span></div>
      <h3><a href="{escape(p['url'])}">{escape(p['title'])}</a></h3>
      <p class="authors">{authors}</p><p class="venue">{escape(p['venue'])}</p>
      <div class="pub-links">{links}</div></li>'''

def wrap(content, page='home'):
    title = 'Dafang Zhao | AI for Energy' if page == 'home' else 'Publications | Dafang Zhao'
    canonical = SITE + ('' if page == 'home' else 'publications.html')
    schema = {'@context':'https://schema.org','@type':'Person','name':'Dafang Zhao','url':SITE,'image':SITE+'assets/portrait.jpg','jobTitle':'Specially Appointed Assistant Professor','affiliation':{'@type':'Organization','name':'The University of Osaka'},'sameAs':[SCHOLAR,'https://github.com/JacobZhao','https://orcid.org/0000-0001-8107-4260','https://researchmap.jp/zhaodafang?lang=en']}
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Dafang Zhao, Specially Appointed Assistant Professor at The University of Osaka. Research in AI for energy, HVAC control, battery scheduling, and optimization.">
<meta name="theme-color" content="#14777b"><meta property="og:type" content="website"><meta property="og:title" content="{title}">
<meta property="og:description" content="AI, optimization, and intelligent energy systems. Research, publications, and academic background."><meta property="og:url" content="{canonical}">
<link rel="canonical" href="{canonical}"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{json.dumps(schema)}</script><script src="assets/main.js" defer></script>
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="masthead"><div class="masthead-inner"><a class="brand" href="index.html">Dafang Zhao<span>Personal website</span></a>
<nav class="main-nav" aria-label="Main navigation"><a href="index.html" {'aria-current="page"' if page=='home' else ''}>About</a><a href="index.html#research">Research</a><a href="publications.html" {'aria-current="page"' if page=='publications' else ''}>Publications</a><a href="index.html#contact">Contact</a></nav></div></header>
<div class="page-layout">{profile()}<main class="content" id="main">{content}</main></div>
<footer class="footer"><div class="footer-inner"><span>© 2026 Dafang Zhao · The University of Osaka</span><span>Updated October 2026 · <a href="https://github.com/JacobZhao/JacobZhao.github.io">Website source</a></span></div></footer>
</body></html>'''

def home():
    preprints = [p for p in PUBLICATIONS if p['type']=='preprint']
    selected = [p for p in PUBLICATIONS if p.get('selected')]
    content = '''<p class="eyebrow">AI · Optimization · Energy</p><h1>About me</h1>
    <p class="intro">I am a <strong>Specially Appointed Assistant Professor</strong> at <a href="https://www.osaka-u.ac.jp/en">The University of Osaka</a>, working in the <a href="https://www-ise2.ist.osaka-u.ac.jp/en/">Information Systems Synthesis Laboratory</a>.</p>
    <p>My research connects artificial intelligence, mathematical optimization, and real-world energy systems. I develop data-driven models and control methods that make buildings and distributed energy resources more efficient, flexible, and responsive to people's needs.</p>
    <p>My work spans HVAC energy management, demand-side flexibility, battery scheduling, and renewable energy integration, with an emphasis on interpretable models and experimental validation. I am also exploring how physically constrained agentic AI can support energy scheduling.</p>
    <p>I received my Ph.D. in Information Science from Osaka University in 2022 and my master's degree from Nara Institute of Science and Technology (NAIST).</p>
    <section class="section" id="research" aria-labelledby="research-title"><div class="section-heading"><h2 id="research-title">Research interests</h2></div>
    <div class="research-list">
      <article class="research-item"><h3>Smart buildings &amp; HVAC</h3><p>Data-driven thermal modeling, model predictive control, and comfort-aware operation in real buildings.</p></article>
      <article class="research-item"><h3>Demand-side flexibility</h3><p>Coordinating flexible loads through reinforcement learning, optimization, and hierarchical aggregation.</p></article>
      <article class="research-item"><h3>Storage &amp; renewable energy</h3><p>Degradation-aware battery scheduling, PV integration, and energy management across multiple timescales.</p></article>
      <article class="research-item"><h3>AI for energy systems</h3><p>Symbolic regression, forecasting, physics-informed models, and agentic AI with physical constraints.</p></article>
    </div></section>
    <section class="section" id="preprints" aria-labelledby="preprints-title"><div class="section-heading"><h2 id="preprints-title">Preprints</h2></div><p class="preprint-note">Recent work shared before peer-reviewed publication.</p><ul class="pub-list">'''
    content += ''.join(pub(p) for p in preprints)
    content += '''</ul></section><section class="section" id="publications" aria-labelledby="publications-title"><div class="section-heading"><h2 id="publications-title">Selected publications</h2><a href="publications.html">Full list ↗</a></div><ul class="pub-list">'''
    content += ''.join(pub(p) for p in selected)
    content += '''</ul><a class="all-link" href="publications.html">Browse all publications <span aria-hidden="true">→</span></a></section>
    <section class="section" id="background" aria-labelledby="background-title"><div class="section-heading"><h2 id="background-title">Academic background</h2></div>
    <div class="timeline"><div class="timeline-time">2022 – present</div><div><strong>Specially Appointed Assistant Professor</strong><p>The University of Osaka<br>Graduate School of Information Science and Technology</p></div></div>
    <div class="timeline"><div class="timeline-time">2022</div><div><strong>Ph.D. in Information Science</strong><p>Osaka University</p><a href="https://hdl.handle.net/11094/89577">Doctoral thesis ↗</a></div></div>
    <div class="timeline"><div class="timeline-time">Master's degree</div><div><strong>Nara Institute of Science and Technology</strong><p>NAIST, Japan</p></div></div></section>
    <section class="contact-box" id="contact" aria-labelledby="contact-title"><h2 id="contact-title">Get in touch</h2><p>For research discussions and collaboration in intelligent energy systems, please contact me by email.</p><a href="mailto:zhao.dafang@ist.osaka-u.ac.jp">zhao.dafang@ist.osaka-u.ac.jp ↗</a></section>'''
    (ROOT/'index.html').write_text(wrap(content), encoding='utf-8')

def publications():
    years = sorted({p['year'] for p in PUBLICATIONS}, reverse=True)
    content = f'''<a class="back-link" href="index.html">← Back to homepage</a><p class="eyebrow">Research output</p><h1>Publications</h1><p class="page-intro">Journal articles, conference papers, preprints, and books.<br>See my <a href="{escape(SCHOLAR)}">Google Scholar profile ↗</a> for citation information and the latest updates.</p>
    <div class="publication-tools js-only"><label class="search-label" for="publication-search">Search publications</label><input class="search-input" type="search" id="publication-search" placeholder="Search by title, author, or venue…" autocomplete="off">
    <div class="filter-row"><div class="type-filter" role="group" aria-label="Publication type">'''
    for k,v in [('all','All'),('journal','Journals'),('conference','Conferences'),('preprint','Preprints'),('book','Books & chapters')]:
        content += f'<button type="button" class="filter-button" data-filter="{k}" aria-pressed="{str(k=="all").lower()}">{v}</button>'
    content += '</div><select class="year-select" id="publication-year" aria-label="Publication year"><option value="all">All years</option>' + ''.join(f'<option value="{y}">{y}</option>' for y in years) + '</select></div></div>'
    content += f'<p class="results-status js-only" id="results-status" role="status" aria-live="polite">Showing {len(PUBLICATIONS)} entries</p>'
    for year in years:
        content += f'<section class="year-group" aria-labelledby="year-{year}"><h2 class="year-heading" id="year-{year}">{year}</h2><ul class="pub-list">' + ''.join(pub(p) for p in PUBLICATIONS if p['year']==year) + '</ul></section>'
    content += '''<div class="empty-state" id="empty-state" hidden><p>No publications match these filters.</p><button class="reset-button" type="button" id="reset-filters">Clear filters</button></div><p class="small-print section">Publication records checked against Google Scholar and the laboratory publication list in October 2026. Preprints are labeled separately; some author lists are abbreviated.</p>'''
    (ROOT/'publications.html').write_text(wrap(content,'publications'), encoding='utf-8')

if __name__ == '__main__':
    home(); publications()
    print(f'Built index.html and publications.html from {len(PUBLICATIONS)} records.')
