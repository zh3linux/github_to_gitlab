import commands
member = {
    'zh3linux@gmail.com' : 'zh3linux_new',
}

for git_name, ks_name in member.iteritems():
    cmd = '''
git filter-branch -f --env-filter '
if test "$GIT_AUTHOR_EMAIL" = "%s"
then
    GIT_AUTHOR_NAME="%s"
    GIT_AUTHOR_EMAIL="%s@xxx.com"
fi
export GIT_AUTHOR_NAME
export GIT_AUTHOR_EMAIL
'
''' %(git_name, ks_name, ks_name)
    print cmd
    #res = commands.getoutput(cmd)
