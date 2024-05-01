import json
import subprocess
from datetime import datetime

from shellpython.helpers import Dir


def clean_stderr(s: str):
    if s is None:
        return ""
    s = s.split("\n")
    o = []
    for l in s:
        if "direnv" in l:
            continue
        o.append(l)

    if len(o) == 0:
        return ""
    return "\n".join(o)


def parse_date(dte: str) -> datetime:
    return datetime.strptime(dte, '%Y-%m-%dT%H:%M:%SZ')


def get_prs() -> str:
    cmd = 'gh pr list --author="@me" --json="number,title"'
    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90, shell=True)
    ret.stderr = clean_stderr(ret.stderr)
    if ret.returncode != 0 or ret.stderr != "":
        raise RuntimeError(ret.stderr)
    return ret.stdout


def process_single_pr(num: int, title: str):
    shouldPost = should_post_for_single_pr(num)
    if shouldPost:
        print(f'Posting comment for PR #{num} - {title}')
        cmd = f'gh pr comment {num} --body "publish all"'
        ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90, shell=True)
        ret.stderr = clean_stderr(ret.stderr)
        if ret.returncode != 0 or ret.stderr != "":
            raise RuntimeError(ret.stderr)
        print(ret.stdout)


def should_post_for_single_pr(num: int) -> bool:
    cmd = f'gh pr view {num} --json "commits,comments"'
    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90, shell=True)
    ret.stderr = clean_stderr(ret.stderr)
    if ret.returncode != 0 or ret.stderr != "":
        raise RuntimeError(ret.stderr)
    ret = json.loads(ret.stdout)

    # 1. get date of latest commit
    commits = ret["commits"]
    latestCommit = commits[len(commits) - 1]
    latestCommitDate = parse_date(latestCommit["authoredDate"])

    # 1. get date of latest comment
    comments = ret["comments"]
    if len(comments) == 0:
        return True

    latestCommentDate = None
    i = len(comments) - 1
    while i >= 0:
        comm = comments[i]
        if comm["body"] == "publish all":
            latestCommentDate = parse_date(comm["createdAt"])
            break
        i -= 1

    if latestCommentDate is None:
        return True

    return latestCommentDate < latestCommitDate


def main():
    from os.path import expanduser
    home = expanduser("~")
    with Dir(f"{home}/code/src/github.com/integralads/pb-platform"):
        prs = get_prs()
        prs_json = json.loads(prs)
        for p in prs_json:
            process_single_pr(p["number"], p["title"])


if __name__ == '__main__':
    main()
