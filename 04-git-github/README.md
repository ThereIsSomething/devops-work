# Session 5: Git and GitHub

**Nitish Kumar Bhambu — 24BCS10589**

`git commit -m` commits what is staged. `git commit -a -m` first stages changes and deletions to tracked files; it still does not add an untracked file. The first exercise tests all three cases in a temporary repository.

The second exercise creates three commits on main, three on a feature branch, identifies one commit with git log/show and cherry-picks only that change onto main. Cherry-pick creates a new commit applying the selected change; it does not merge the whole branch. The selected .gitignore change has no dependency on the other feature commits, which makes it a clean example.

These temporary lab repositories keep the practice history separate from the submission repository. Commands and actual before/after logs are below.

```bash
python3 scripts/run_basics.py 5
```

## Execution evidence

<!-- EVIDENCE -->

### current-run.txt

[Complete transcript](outputs/current-run.txt)

````text
Captured 2026-10-07T13:01:03.439850+00:00
$ bash 04-git-github/scripts/task1-commit-a.sh /tmp/nitish-git-lab-2zv6f5q5
############ SETUP: one tracked file, committed ############
$ git log --oneline
9c1ce63 Initial commit: add tracked.txt

$ cat tracked.txt
version 1

##################################################################
#  EXPERIMENT A:  git commit -m   (WITHOUT -a)                    #
##################################################################

--- modify the tracked file, and create a NEW untracked file ---

$ git status --short
 M tracked.txt
?? untracked.txt
  M = modified but NOT staged   ?? = untracked

$ git commit -m 'try to commit without staging'
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   tracked.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	untracked.txt

no changes added to commit (use "git add" and/or "git commit -a")

>>>> NOTHING WAS COMMITTED. 'git commit -m' only commits what is in the
>>>> STAGING AREA (the index). We never ran 'git add', so the index is empty.

$ git log --oneline
9c1ce63 Initial commit: add tracked.txt

--- the correct 2-step way with plain 'git commit -m' ---
$ git add tracked.txt
$ git status --short
M  tracked.txt
?? untracked.txt
  M in the LEFT column = staged

$ git commit -m 'commit -m: staged change only'
[main 3ca6fb9] commit -m: staged change only
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git status --short
?? untracked.txt
>>>> untracked.txt is STILL not committed. Correct: it was never added.

##################################################################
#  EXPERIMENT B:  git commit -a -m                                #
##################################################################

--- modify the tracked file again (untracked.txt still lying around) ---

$ git status --short
 M tracked.txt
?? untracked.txt

$ git commit -a -m 'commit -a -m: auto-stage tracked files'

[Excerpt: 198 intermediate lines omitted; complete transcript linked above.]

$ git log --oneline --graph --decorate --all
* 2448f8a (HEAD -> main) F2: add .gitignore  <-- THIS is the one we will cherry-pick
| * 4234a1e (feature) F3: rewrite app.py to use utils.greet()
| * 881a9ea F2: add .gitignore  <-- THIS is the one we will cherry-pick
| * f6eb3ed F1: add utils.py with greet()
|/
* 82ebc9f C3: document setup in README
* fc503c2 C2: add app.py
* 341681a C1: add README

--- proof the file is tracked on main, not just sitting on disk ---
$ git ls-files
.gitignore
README.md
app.py

$ git log --oneline main -- .gitignore
2448f8a F2: add .gitignore  <-- THIS is the one we will cherry-pick

--- the cherry-picked commit has a NEW hash (different commit object) ---
original on feature : 881a9ea
copy on main        : 2448f8a

$ git show --stat HEAD
commit 2448f8a53357fd646a3dfd91d5ceefa83bc0e96a
Author: Nitish Kumar Bhambu <support@symbiotes.in>
Date:   Wed Oct 7 18:31:03 2026 +0530

    F2: add .gitignore  <-- THIS is the one we will cherry-pick

 .gitignore | 3 +++
 1 file changed, 3 insertions(+)

--- but the CONTENT (the tree/patch) is identical ---
$ diff <(git show 881a9ea -- .gitignore) <(git show HEAD -- .gitignore)
IDENTICAL patch — same change, new commit.

--- F1 and F3 were NOT brought over: only the one commit was picked ---
$ ls
README.md
app.py
$ git log --oneline main
2448f8a F2: add .gitignore  <-- THIS is the one we will cherry-pick
82ebc9f C3: document setup in README
fc503c2 C2: add app.py
341681a C1: add README
>> utils.py (F1) and the app.py rewrite (F3) are still only on 'feature'.

##################################################################
#  BONUS: what a cherry-pick CONFLICT looks like                  #
##################################################################
--- cherry-pick F3, which rewrites app.py and needs utils.py ---
$ git cherry-pick 4234a1e
[main 7fa5f12] F3: rewrite app.py to use utils.greet()
 Date: Wed Oct 7 18:31:03 2026 +0530
 1 file changed, 3 insertions(+), 1 deletion(-)

>> It applied cleanly, BUT the code is now BROKEN on main:
$ cat app.py
from utils import greet

print(greet("DevOps"))
$ ls utils.py
ls: cannot access 'utils.py': No such file or directory
utils.py does NOT exist on main!

>> This is the real lesson: cherry-pick copies ONE commit, not its
>> dependencies. app.py imports utils.greet, but F1 (which created
>> utils.py) was never picked. Git cannot know that.

$ git reset --hard HEAD~1   # undo it
HEAD is now at 2448f8a F2: add .gitignore  <-- THIS is the one we will cherry-pick

$ git log --oneline main   (final state)
2448f8a F2: add .gitignore  <-- THIS is the one we will cherry-pick
82ebc9f C3: document setup in README
fc503c2 C2: add app.py
341681a C1: add README
[exit 0]
LAB EXECUTION FINISHED
````
