from datetime import datetime, timedelta
import random
import os
import shutil
import subprocess

source = 'git@github.com'

def roundTime(dt=None, roundTo=60):
   if dt == None:
      dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0, rounding-seconds, -dt.microsecond)


def fake_commit(user,repo,days):

    beginning = """#!/usr/bin/env bash
                    REPO={0}
                    git init $REPO
                    cd $REPO
                    touch README.md
                    git add README.md
                """.format(repo)
    ending = """
            git remote add origin {0}:{1}/$REPO.git
            git pull origin master
            git push origin master -f
            """.format(source,user)
    lines = []
    lines.append(beginning)
    
    commitdate = datetime.today()

    for i in range(days):
        rnd = random.randint(1, 2)
        commitdate = roundTime(
            datetime.today() - timedelta(days=i), roundTo=60*60)
        for j in range(rnd):
            template = '''GIT_AUTHOR_DATE={0} GIT_COMMITTER_DATE={1} git commit --allow-empty -m "new commit" > /dev/null\n'''.format(commitdate.isoformat(), commitdate.isoformat())
            lines.append(template)

    lines.append(ending)
    with open('commits.sh', 'w') as f:
        for line in lines:
            f.write(line)
    os.chmod('commits.sh', 0o755)

def main():
    username = "wixzi"
    repo = "commits-history"
    days = int(input('Enter number of days to go back in time: '))
    
    fake_commit(username, repo, days)
    subprocess.call(['./commits.sh'])

if __name__ == '__main__':
    main()