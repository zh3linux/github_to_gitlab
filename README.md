github_to_gitlab
================

Move Github to Gitlab

## Tutorial

### mv code
```shell
git clone --bare git://github.com/username/project.git
cd project.git
git push --mirror git@xxx.com/username/newproject.git
```

### change username
```shell
git filter-branch  -f --env-filter '
if test "$GIT_AUTHOR_EMAIL" = "old@email"
then
    GIT_AUTHOR_NAME="newname"
    GIT_AUTHOR_EMAIL="newname@gmail.com"
fi
export GIT_AUTHOR_NAME
export GIT_AUTHOR_EMAIL
'

git push origin master --force
```
### mv issue
```shell
pip install pyapi-gitlab
pip install pygithub3
```

```shell
export git_user='xxx'
export git_pwd='xxx'
export gl_token='xxx'
export gl_url='xxx'
```

vim mv_git.py

```
MEMBERS = {
    11111 : 111,  # github_userid : gitlab_userid
}
```

```
    self.project = 'zh3linux'
    self.repo = 'github_to_gitlab'
    self.gl_project = 'zh3linux/github_to_gitlab'
```

python mv_git.py
