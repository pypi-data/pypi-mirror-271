class GitFile:
    def __init__(self, repo_path: str, file_relative_path: str):
        self.file_relative_path = file_relative_path
        self.repo_path = repo_path

    def get_file_name(self):
        return self.file_relative_path.split("/")[-1]
    
    def get_contents(self):
        raise NotImplementedError
    