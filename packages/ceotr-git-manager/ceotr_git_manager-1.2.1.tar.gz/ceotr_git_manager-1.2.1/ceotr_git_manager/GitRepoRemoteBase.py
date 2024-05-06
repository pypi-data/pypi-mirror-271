from .GitUser import GitUser
from ceotr_git_manager.GitFile import GitFile


class GitRepoRemoteBase:
    def __init__(self, git_user: GitUser, repo_path: str, branch: str):
        """
        Tools for interacting with a remote repository using the service's API
            Params:
                git_user: The gituser to authenticate, needs to have an access token
                repo_path: The path of the repo, including the project(s)
                            Ex: '/ceotr/practice_lab/meta-json-example'
        """
        self.repo_path = repo_path
        self.git_user = git_user
        self.branch = branch

    def get_file_tree(self):
        raise NotImplementedError

    def get_file_contents(self, file_path="", git_file: GitFile = None) -> str:
        """
        Get a files contents matching an exact path within the repo
            Params:
                file_path: the exact file path within the repo of the file to get
                git_file: a GitFile to use as a lookup
            Returns:
                The file contents as a string of the requested file
        """
        raise NotImplementedError

    def find_files(self, file_name: str) -> list[GitFile]:
        """
        Get all files matching a name.
        This can take a while for repos with lots of subdirectories
            Params:
                file_name: the file name to match
            Returns:
                A list of GitFiles matching the file_name
        """
        raise NotImplementedError
