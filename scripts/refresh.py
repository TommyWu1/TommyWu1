"""Refresh public profile data using GitHub CLI and its existing authentication.
Requires Python 3.10+ and gh. GITHUB_TOKEN is supplied by Actions, never saved.
Network failures leave the previous generated assets in place.
"""
from pathlib import Path
from datetime import datetime, timezone
import subprocess, json, tempfile, shutil, os
from generate import build, P

def api(endpoint,query=None):
 args=['gh','api',endpoint]
 if query:args+=['-f','query='+query]
 return json.loads(subprocess.check_output(args,text=True))

def refresh():
 profile=api('users/TommyWu1')
 repos=[];page=1
 while True:
  batch=api(f'users/TommyWu1/repos?per_page=100&sort=pushed&page={page}')
  repos.extend(r for r in batch if not r.get('private'))
  if len(batch)<100:break
  page+=1
 query='query { user(login:"TommyWu1") { contributionsCollection { totalCommitContributions totalPullRequestContributions contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } pinnedItems(first:4,types:REPOSITORY) { nodes { ... on Repository { nameWithOwner name description url stargazerCount primaryLanguage { name color } } } } } }'
 github=api('graphql',query)
 if github.get('errors'):raise RuntimeError('GitHub contribution query failed')
 projects=list(github['data']['user']['pinnedItems']['nodes'])
 overrides_path=P/'data/project-overrides.json'
 overrides=json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
 for i,project in enumerate(projects):
  override=overrides.get(project['nameWithOwner'])
  if not override:continue
  owner,name=override['repository'].split('/')
  query='query { repository(owner:'+json.dumps(owner)+',name:'+json.dumps(name)+') { isPrivate nameWithOwner name description url stargazerCount primaryLanguage { name color } } }'
  result=api('graphql',query)
  replacement=result.get('data',{}).get('repository')
  if result.get('errors') or not replacement or replacement.get('isPrivate'):
   raise RuntimeError('Showcase repository must be publicly accessible')
  projects[i]=dict(replacement,name=override.get('title') or replacement['name'],description=override.get('description') or replacement.get('description'))
 commits=[]
 for repo in [r for r in repos if not r['fork'] and r['name'].lower()!='tommywu1'][:2]:
  for commit in api(f'repos/{repo["full_name"]}/commits?per_page=3'):
   commits.append(repo['name']+': '+commit['commit']['message'].splitlines()[0])
 # Keep only public fields needed for rendering.
 profile={k:profile.get(k) for k in ['name','bio','blog','location','public_repos','followers']}
 repos=[{k:r.get(k) for k in ['name','full_name','language','stargazers_count','fork']} for r in repos]
 payload={'projects.json':projects,'profile.json':profile,'repos.json':repos,'github.json':github,'commits.json':commits,'meta.json':{'date':datetime.now(timezone.utc).date().isoformat()}}
 # Validate all API responses before committing cache files.
 with tempfile.TemporaryDirectory() as temp:
  for name,value in payload.items():Path(temp,name).write_text(json.dumps(value,indent=2)+'\n')
  for name in payload:shutil.copyfile(Path(temp,name),P/'data'/name)
 build()
if __name__=='__main__':refresh()
