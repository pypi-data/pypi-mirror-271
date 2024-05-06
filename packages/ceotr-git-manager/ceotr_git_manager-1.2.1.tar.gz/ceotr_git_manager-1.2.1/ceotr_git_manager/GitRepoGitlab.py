from ceotr_git_manager.GitRepoRemoteBase import GitRepoRemoteBase
from ceotr_git_manager.GitRepo import GitException
from ceotr_git_manager.GitUser import GitUser
from ceotr_git_manager.GitFile import GitFile

import requests


class GitRepoGitlab(GitRepoRemoteBase):
    def __init__(self, git_user: GitUser, repo_path, branch: str,
                 gitlab_base_url="https://gitlab.oceantrack.org/api/v4/"):
        super().__init__(git_user, repo_path, branch)
        self.repo_path = self.repo_path.replace("/", "%2F")
        self.gitlab_base_url = gitlab_base_url

    def _gitlab_request(self, path: str, additional_params=None) -> requests.Response:
        if additional_params is None:
            additional_params = []
        if not self.git_user.access_token:
            raise ValueError("The GitUser must have an access token")

        url = f"{self.gitlab_base_url}{path.lstrip('/')}?ref={self.branch}"
        for param in additional_params:
            url += f"&{param}"
        headers = {
            "PRIVATE-TOKEN": self.git_user.access_token
        }
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            raise GitException(f"Got status code: {res.status_code} when accessing: {url}")
        return res

    def get_file_contents(self, file_path="", git_file: GitFile = None) -> str:
        if git_file:
            file_path = git_file.file_relative_path
        file_path = file_path.replace("/", "%2F")
        url = f"projects/{self.repo_path}/repository/files/{file_path}/raw"
        res = self._gitlab_request(url)
        return res.content.decode()

    def _find_files(self, url, path: str):
        ret = []
        file_res = self._gitlab_request(url, additional_params=[f"path={path.replace('/', '%2F')}"])
        for file in file_res.json():
            print(file["name"])
            if file["type"] == "blob":
                ret.append(file)
            elif file["type"] == "tree":
                ret.extend(self._find_files(url, file["path"]))
        return ret

    def find_files(self, file_name: str) -> list[GitFile]:
        matched_paths = []
        url = f"projects/{self.repo_path}/repository/tree"
        all_files = self._find_files(url, "/")
        for file in all_files:
            if file["name"] == file_name:
                git_file = GitFile(self.repo_path, file_relative_path=file["path"])
                matched_paths.append(git_file)
        return matched_paths

    def get_file_tree(self):
        pass
