class ProjectAbstract(object):
    cvs_repo_url = None
    cvs_repo_branch = None
    location = None
    static_location = None

    def __init__(self, cvs_repo_url, cvs_repo_branch=u'master', location=u'/app/', media_location=u'/app/media/',
                 static_location=u'/app/static'):
        self.cvs_repo_url = cvs_repo_url
        self.cvs_repo_branch = cvs_repo_branch
        self.location = location
        self.media_location = media_location
        self.static_location = static_location