#!/usr/bin/env python3
"""Automated job-pipeline run: discover -> filter (today/yesterday) -> score -> dedup-insert.
Run-relative dates: today/yesterday computed from the machine clock (Asia/Kolkata) at runtime.
Writes to jobs.db with INSERT OR IGNORE (unique indexes enforce no-duplicate rule).
Prints a short summary to stdout (this is what gets sent to Telegram).
Covers: jobs.rubyonrails.org, HireRubyDevs India page, LinkedIn India past-24h search.
Skips: Ruby on Remote (Cloudflare-blocked headless).
Detail pages are fetched for every in-window job so scoring uses the full
description; rows are never overwritten (OR IGNORE), so enriched rows are safe.
Contact research + message drafting stay manual (require verification).
"""
import json, re, sqlite3, html as ihtml
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

BASE = '/Users/utsavmehrotra/Desktop/Ktech/job-agent'
IST = timezone(timedelta(hours=5, minutes=30))
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}

TODAY = datetime.now(IST).date()
YEST = TODAY - timedelta(days=1)

USER_TECH = ['ruby', 'rails', 'rest api', 'postgresql', 'redis', 'microservices', 'react', 'java', 'spring boot', 'aws']
EXP_HAVE = 4
LI_DETAIL_CAP = 15

def fetch(url, timeout=30, tries=3):
    last = None
    for i in range(tries):
        try:
            req = Request(url, headers=UA)
            with urlopen(req, timeout=timeout) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:
            last = e
            if i < tries - 1:
                import time as _t
                _t.sleep(2 * (i + 1))
    raise last

def textify(page):
    t = re.sub(r'<script.*?</script>', ' ', page, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = ihtml.unescape(re.sub(r'<[^>]+>', ' ', t))
    return re.sub(r'\s+', ' ', t).strip()

def canon_url(u):
    return (u or '').strip().lower().split('#')[0].split('?')[0].rstrip('/')

def in_window(label):
    l = (label or '').lower()
    if re.search(r'\d+\s*(hour|minute|second)', l) or 'today' in l or 'just now' in l:
        return TODAY
    m = re.search(r'(\d+)\s*day', l)
    if m:
        dt = TODAY - timedelta(days=int(m.group(1)))
        return dt if dt >= YEST else None
    if 'yesterday' in l:
        return YEST
    return None

def score_job(title, desc, location, salary):
    t, d, loc = title.lower(), desc.lower(), (location or '').lower()
    if re.search(r'\bjunior\b|\bentry.?level\b|\bintern\b|\btrainee\b', t):
        return 0, 'LOW PRIORITY', ['Rejected: junior/intern'], []
    if not (any(k in t or k in d for k in ('ruby', 'rails')) or re.search(r'\bror\b', t) or re.search(r'\bror\b', d)):
        return 0, 'LOW PRIORITY', ['Rejected: non-Ruby'], []
    s, reasons, gaps = 0, [], []
    senior = any(k in t for k in ('senior', 'lead', 'staff', 'principal', 'architect', 'manager'))
    has_rails = any(k in t or k in d for k in ('rails', 'ruby on rails')) or bool(re.search(r'\bror\b', t) or re.search(r'\bror\b', d))
    if senior and has_rails:
        s += 30; reasons.append('Senior Ruby/Rails role')
    elif has_rails and ('engineer' in t or 'developer' in t):
        s += 25; reasons.append('Ruby/Rails engineer role')
    elif has_rails:
        s += 20; reasons.append('Mid-level Ruby/Rails role')
    else:
        s += 10; reasons.append('Ruby role, Rails secondary')
    overlap = [x for x in USER_TECH if re.search(r'\b' + re.escape(x) + r'\b', d) or re.search(r'\b' + re.escape(x) + r'\b', t)]
    if len(overlap) >= 7: s += 20
    elif len(overlap) >= 5: s += 15
    elif len(overlap) >= 3: s += 10
    elif len(overlap) >= 1: s += 5
    reasons.append(f"Tech overlap ({len(overlap)}): {', '.join(overlap) or 'none'}")
    if 'remote' in loc and ('india' in loc or 'worldwide' in loc):
        s += 20; reasons.append('Remote incl. India')
    elif 'remote' in loc and any(x in loc for x in ('united states', 'americas', 'europe')):
        s += 5; reasons.append('International remote')
    elif 'remote' in loc:
        s += 15; reasons.append('Remote')
    elif any(x in loc for x in ('bengaluru', 'bangalore', 'delhi', 'ncr', 'gurugram', 'noida', 'pune', 'hyderabad', 'chennai', 'mumbai', 'india')):
        s += 20; reasons.append('India location')
    else:
        reasons.append('Location may not align')
    if salary:
        nums = [int(n.replace(',', '')) for n in re.findall(r'[\d,]+', salary.replace('k', '000').replace('K', '000'))]
        for n in nums:
            annual = n if n >= 100000 else n * 1000 if n >= 100 else 0
            if annual >= 160000: s += 15; reasons.append('Comp exceeds target'); break
            elif annual >= 120000: s += 10; reasons.append('Comp meets target'); break
            elif annual >= 80000: s += 5; reasons.append('Comp close to target'); break
    else:
        s += 5; reasons.append('Comp unknown')
    # skill: total gap deduction max -30 (-10 minor / -20 significant / -30 major)
    gap_hit = 0
    for pat, pen, name in [(r'\bkubernetes\b|\bk8s\b', 10, 'Kubernetes production experience'),
                           (r'\bgolang\b', 5, 'Go experience'),
                           (r'\bmachine learning\b', 10, 'AI/ML experience')]:
        if re.search(pat, d) or re.search(pat, t):
            gap_hit += pen; gaps.append(name)
    exp_reqs = [int(e) for e in re.findall(r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)', d)]
    over = [e for e in exp_reqs if e > EXP_HAVE]
    if over:
        worst = max(over)
        gaps.append(f"Requires {worst}+ yrs (have {EXP_HAVE}+)")
        gap_hit += 30 if worst >= EXP_HAVE + 6 else 20 if worst > EXP_HAVE + 2 else 10
    s -= min(gap_hit, 30)
    s = max(1, min(100, s))
    rec = 'HIGH PRIORITY' if s >= 90 else 'GOOD MATCH' if s >= 75 else 'POSSIBLE MATCH' if s >= 60 else 'LOW PRIORITY'
    return s, rec, reasons, gaps

def collect_ror():
    page = fetch('https://jobs.rubyonrails.org')
    chunks = re.split(r'<a id="job_', page)[1:]
    jobs = []
    for ch in chunks:
        href = re.search(r'href="(/jobs/[^"]+)"', ch)
        title = re.search(r'<span class="text-lg leading-none">(.*?)</span>', ch, re.S)
        comp = re.search(r'at\s+([^<]+)</span>', ch)
        lis = re.findall(r'<li class="truncate">(.*?)</li>', ch, re.S)
        meta = ' | '.join(' '.join(textify(x).split()) for x in lis)
        ago = re.search(r'((?:about )?\d+ \w+ ago|today|yesterday)', ch + page, re.I)
        pub = in_window(ago.group(1)) if ago else None
        if not href or not title or pub is None:
            continue
        t = ' '.join(title.group(1).split())
        c = comp.group(1).strip() if comp else ''
        if t.lower() in ('test',) or len(t) < 4:
            continue
        loc = re.search(r'(Remote[^|$]*|Hybrid[^|$]*|[A-Z][a-z]+(?:, [A-Z][a-z]+)+)', meta)
        sal = re.search(r'([$£€][\d,.\-kK ]+|USD [\d,\- ]+)', meta)
        url = 'https://jobs.rubyonrails.org' + href.group(1)
        try:
            det = fetch(url)
            pm = re.search(r'<div class="prose.*?</div>\s*(?:<[^>]+>\s*)*Published', det, re.S)
            desc = textify(pm.group(0)).rsplit('Published', 1)[0][:6000] if pm else ''
        except Exception:
            desc = ''
        jobs.append({'title': t, 'company': c, 'location': loc.group(1).strip() if loc else '',
                     'salary': sal.group(1).strip() if sal else None, 'description': desc,
                     'url': url, 'source': 'jobs.rubyonrails.org', 'posted_at': pub.isoformat()})
    return jobs

def collect_hrd_india():
    page = fetch('https://hirerubydevs.com/ruby-on-rails-jobs-in-india')
    lis = re.split(r'<li class="group py-5">', page)[1:]
    jobs = []
    for blk in lis:
        m = re.search(r'href="(/jobs/[a-z0-9-]+)">(.*?)</a>', blk, re.S)
        comp = re.search(r'<span class="text-zinc-300">(.*?)</span>\s*·\s*(.*?)\s*·\s*((?:about )?\d+ \w+ ago|today|yesterday)', blk, re.S)
        if not m or not comp:
            continue
        pub = in_window(comp.group(3))
        if pub is None:
            continue
        t = ' '.join(textify(m.group(2)).split())
        if len(t) < 4 or t.lower() == 'test':
            continue
        url = 'https://hirerubydevs.com' + m.group(1)
        try:
            det = textify(fetch(url))
            m2 = re.search(r'About the role\s*(.*?)\s*(?:Similar jobs|Browse all)', det, re.S)
            desc = (m2.group(1) if m2 else det)[:6000]
        except Exception:
            desc = ''
        jobs.append({'title': t, 'company': comp.group(1).strip(), 'location': comp.group(2).strip(),
                     'salary': None, 'description': desc, 'url': url,
                     'source': 'HireRubyDevs', 'posted_at': pub.isoformat()})
    return jobs

def collect_linkedin():
    page = fetch('https://www.linkedin.com/jobs/search/?keywords=ruby%20on%20rails&location=India&f_TPR=r86400')
    items = re.findall(r'\{"@type":"ListItem".*?"url":"([^"]+)","name":"([^"]+)","disambiguatingDescription":"([^"]*)","description":"([^"]*)"',
                       page, re.S)
    if not items:
        raise RuntimeError('no ListItem data (likely rate-limited); retry next run')
    jobs = []
    for url, name, company, loc in items[:LI_DETAIL_CAP]:
        desc = ''
        try:
            det = fetch(url)
            m = re.search(r'"description":"(.{500,8000}?)"', det, re.S)
            if m:
                desc = ihtml.unescape(re.sub(r'<[^>]+>', ' ', m.group(1).replace('\\n', ' ')))[:4000]
        except Exception:
            pass
        jobs.append({'title': ihtml.unescape(name), 'company': ihtml.unescape(company),
                     'location': ihtml.unescape(loc), 'salary': None, 'description': desc,
                     'url': url, 'source': 'LinkedIn', 'posted_at': TODAY.isoformat()})
    return jobs, len(items)

def main():
    all_jobs, li_total = [], 0
    for fn, name in ((collect_ror, 'rubyonrails.org'), (collect_hrd_india, 'HireRubyDevs')):
        try:
            got = fn()
            all_jobs.extend(got)
            print(f'{name}: {len(got)} in-window')
        except Exception as e:
            print(f'{name}: FETCH FAILED ({e})')
    try:
        got, li_total = collect_linkedin()
        all_jobs.extend(got)
        print(f'LinkedIn: {len(got)} enriched of {li_total} in-window (cap {LI_DETAIL_CAP})')
    except Exception as e:
        print(f'LinkedIn: FETCH FAILED ({e})')
    conn = sqlite3.connect(f'{BASE}/jobs.db')
    cur = conn.cursor()
    try: cur.execute('ALTER TABLE jobs ADD COLUMN posted_at TEXT')
    except Exception: pass
    inserted, skipped, qual = 0, 0, []
    for j in all_jobs:
        if not j['url']:
            skipped += 1
            continue
        s, rec, reasons, gaps = score_job(j['title'], j['description'], j['location'], j['salary'])
        if s == 0:
            skipped += 1
            continue
        status = 'pending' if s >= 75 else 'not_qualified'
        cur.execute('''INSERT OR IGNORE INTO jobs (job_url, source, company, title, location, salary, description,
          score, recommendation, matching_reasons, potential_gaps, evaluated_at, referral_research_status, posted_at)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
          (canon_url(j['url']), j['source'], j['company'], j['title'], j['location'], j['salary'],
           j['description'], s, rec, json.dumps(reasons), json.dumps(gaps),
           datetime.now(IST).isoformat(), status, j['posted_at']))
        if cur.rowcount == 0:
            skipped += 1
            # automation never rescores existing rows: fill an empty
            # description only, leave score/recommendation untouched
            row = cur.execute('SELECT id, description FROM jobs WHERE job_url=?',
                              (canon_url(j['url']),)).fetchone()
            if row and not (row[1] or '').strip() and j['description']:
                cur.execute('UPDATE jobs SET description=? WHERE id=?', (j['description'], row[0]))
        else:
            inserted += 1
            if s >= 75:
                qual.append(f"{j['title']} @ {j['company']} ({s})")
    conn.commit()
    total = cur.execute('SELECT count(*) FROM jobs').fetchone()[0]
    conn.close()
    print(f'run={TODAY} window={YEST}..{TODAY} found={len(all_jobs)} new={inserted} dupes/rejected={skipped} db_total={total}')
    if qual:
        print('QUALIFIED (75+):')
        for q in qual: print(' -', q)
    else:
        print('No new 75+ matches. Contact research needed only if pending rows exist.')

if __name__ == '__main__':
    main()
