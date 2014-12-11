import os
import gitlab
from pygithub3 import Github

# export git_user='xxx'
# export git_pwd='xxx'
# export gl_token='xxx'
# export gl_url='xxx'

MEMBERS = {
    11111 : 111,  # github_userid : gitlab_userid
}

class MoveGitHub():
    def __init__(self, git_user, git_pwd, gl_url, token):
        self.gh = Github(login=git_user, password=git_pwd)
        self.git = gitlab.Gitlab(gl_url, token=token)
        self.project = 'zh3linux'
        self.repo = 'github_to_gitlab'
        self.gl_project = 'zh3linux/github_to_gitlab'
        self.gl_project_id = self.get_gitlab_id(self.gl_project)

        self.gl_issues = self.get_gitlab_issue()

    def get_gitlab_id(self, project_name):
        projects = self.git.getprojects()
        for p in projects:
            if p['path_with_namespace'] == project_name:
                return p['id']

    def get_gitlab_issue(self):
        gitlab_issues = {}
        for i in range(1, 5):
            for item in self.git.getprojectissues(self.gl_project_id, i, 100):
                gitlab_issues[item['iid']] = item
        return gitlab_issues

    def get_git_issues(self):
        issues = {}
        issues_close = self.gh.issues.list_by_repo(self.project, self.repo, state='close').all()
        for issue in issues_close:
            issues[issue.number] = issue
        issues_open = self.gh.issues.list_by_repo(self.project, self.repo, state='open').all()
        for issue in issues_close:
            issues[issue.number] = issue
        return issues

    def create_issues(self, issues):
        size = 97 #len(issues)
        print 'size:', size
        gl_size = len(self.gl_issues)
        if gl_size < size:
            for i in range(size - gl_size):
                print 'project', self.gl_project_id
                print self.git.createissue(self.gl_project_id, 'test')

    def get_milestones(self):
        gh_milestones = self.gh.issues.milestones.list(self.project, self.repo, state='close').all()
        b = self.gh.issues.milestones.list(self.project, self.repo).all()
        gh_milestones.extend(b)

        gl_milestones_list = self.git.getmilestones(self.gl_project_id)
        gl_milestones = {}
        for item in gl_milestones_list:
            gl_milestones[item['title']] = item
        return gh_milestones, gl_milestones


    def for_issues(self, issues):
        self.create_issues(issues)
        gh_milestones, gl_milestones = self.get_milestones()
        n = 0
        for id, issue in issues.iteritems():
            n += 1
            if id > 0:
                print issue.number
                #print issue.title
                #print issue.__dict__
                #print issue.assignee.id if issue.assignee else ''
                #print issue.__dict__.keys()

                #print self.gl_issues
                iss = self.gl_issues.get(int(issue.number))
                #print iss
                if iss:
                    assignee_id = issue.assignee.id if issue.assignee else ''
                    assignee_id = MEMBERS.get(assignee_id)
                    state_event = 'close' if issue.state == 'closed' else ''
                    milestone_tile = issue.milestone.title if issue.milestone else ''
                    gl_milestones_id = gl_milestones.get(milestone_tile, {}).get('id', '')
                    print 'gl_project_id', self.gl_project_id
                    print 'issid', iss.get('id')
                    print 'issue.title', issue.title
                    print 'assignee_id', assignee_id
                    print 'state_event', state_event
                    print 'gl_milestones_id', gl_milestones_id

                    print self.git.editissue(self.gl_project_id, iss.get('id'), title=issue.title,  description=issue.body, assignee_id=assignee_id, state_event=state_event)
                    print self.git.editissue(self.gl_project_id, iss.get('id'), milestone_id=gl_milestones_id)
                    comments = self.gh.issues.comments.list(issue.number, self.project, self.repo).all()
                    if comments:
                        if len(comments) > len(self.git.getissuewallnotes(self.gl_project_id, iss.get('id'))):
                            for comment in comments:
                                print self.git.createissuewallnote(self.gl_project_id, iss.get('id'), comment.body)


    def run(self):
        self.for_issues(self.get_git_issues())

if __name__ == '__main__':
    git_user = os.getenv('git_user')
    git_pwd = os.getenv('git_pwd')
    token = os.getenv('gl_token')
    gl_url = os.getenv('gl_url')
   
    mvgit = MoveGitHub(git_user, git_pwd, gl_url, token)
    mvgit.run()
