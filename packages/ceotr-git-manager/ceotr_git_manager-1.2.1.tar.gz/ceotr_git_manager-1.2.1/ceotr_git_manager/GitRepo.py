import shutil
import os
import subprocess
import logging
import datetime
from .GitUser import GitUser
from .GitFile import GitFile
from typing import List

logger = logging.getLogger(__name__)


class GitException(Exception):
    """Raised when there is a git issue"""
    pass


class GitRepo:
    def __init__(self,
                 url,
                 repo_dir,
                 user: GitUser = None,
                 branch="master",
                 pull_replace_remote=True,
                 pull_replace_local=False,
                 overwrite=False):
        """
            Params:
                overwrite=False: only used when using this class with the "with" keyword
        """

        self.url = url
        self.repo_dir = repo_dir
        self.user: GitUser = user
        self.base_url = url
        self.branch = branch
        self.currently_committed = False
        self.pull_replace_local = pull_replace_local
        self.pull_replace_remote = pull_replace_remote
        self.overwrite = overwrite

        self.entered = False

        if pull_replace_local == pull_replace_remote:
            raise ValueError("pull_replace_local AND pull_replace_remote cannot be set to the same value")

    @classmethod
    def from_dict(cls, config):
        """
            Shortcut to use a config dictionary-like object
                Params:
                    git_user: The gituser
                    config: url: str
                            repo_dir: str
                            branch: str
                            pull_replace_remote: str
                            pull_replace_local: str
                            overwrite: bool

        """
        return cls(**config)

    # private

    def _repo_exists(self):
        return os.path.exists(self.repo_dir)

    def _inject_credentials(self) -> str:
        return f'{self.url[:8]}{self.user.username}:{self.user.access_token}@{self.url[8:]}'

    def _run_git_cmd(self, cmd, exception_msg="") -> str:
        if type(cmd) is str:
            cmd = [cmd]
        cmd_start = ["git", "--git-dir", os.path.join(self.repo_dir, ".git"), "--work-tree", self.repo_dir]
        cmd_start.extend(cmd)
        run = subprocess.run(cmd_start, capture_output=True)
        if run.returncode != 0:
            if exception_msg == "":
                exception_msg = " ".join(cmd_start)
            logging.error(
                f"Got an error from a git command, info: \nreturn code: {run.returncode} \nstd_out: {run.stdout.decode()}")
            raise GitException(
                f"Code: {run.returncode}. Something went wrong when trying to execute git command: {exception_msg}\n{run.stdout.decode()}\n{run.stderr.decode()}")
        return run.stdout.decode()

    def _get_changed_contents(self):
        changed_files = [os.path.join(self.repo_dir, file) for file in self.get_file_changes(["M"])]
        changed_files_contents = []
        for file in changed_files:
            with open(file, "r") as f:
                changed_files_contents.append(f.read())
        return changed_files_contents, changed_files

    def _write_changed_contents(self, changed_files, changed_files_contents):
        for index, file in enumerate(changed_files):
            with open(file, "w") as f:
                f.write(changed_files_contents[index])

    def _update_repo(self):
        try:
            self._run_git_cmd("pull", exception_msg="pull")
        except GitException as e:
            if "Your local changes to the following files would be overwritten by merge" in str(e):
                print()
                if self.pull_replace_local:
                    self._stage_files()
                    self._run_git_cmd(["stash"])
                elif self.pull_replace_remote:
                    changed_files_contents, changed_files = self._get_changed_contents()
                    self._stage_files()
                    self._run_git_cmd(["stash"])
                    self._run_git_cmd(["pull"])
                    self._write_changed_contents(changed_files, changed_files_contents)
            else:
                logger.error("Looks like you committed changes before re-pulling, why?")
                raise e

    def _first_pull(self):
        repo_with_credentials = self._inject_credentials()
        cmd = f"git clone --branch {self.branch} {repo_with_credentials} {self.repo_dir}"
        subprocess.call(cmd, shell=True)

    def _push(self) -> bool:
        self._run_git_cmd(["push"])
        return True

    # if files is empty it will stage all
    def _stage_files(self, files=None):
        if files is None:
            files = []
        if type(files) is str:
            files = [files]
        args = ["-A"]
        if files:
            args = files
        cmd = ["add"]
        cmd.extend(args)
        self._run_git_cmd(cmd)

    def _commit(self, message="", allow_push_fix=False):
        if not message:
            current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            message = f"ceotr auto-commit: {current_date_str}"
        if len(message) > 50:
            logger.warning("git commit message too long, please keep it under 50 characters")
        commit_std = self._run_git_cmd(["commit", "-m", message[:50]], exception_msg="commit")
        if "nothing to commit" in commit_std:
            logger.warning("Nothing to commit, working tree clean")
            return False
        elif "nothing added to commit but untracked files" in commit_std:
            logger.warning("untracked files found, try adding them first")
        else:
            return True

    def _pull(self):
        msg = self._update_repo()
        print(msg)

    def _find_files(self, filename_to_search, many=True, case_sensitive=True):
        matched_files = []
        for root, dirs, files in os.walk(self.repo_dir):
            for filename in files:
                if (not case_sensitive and filename.lower() == filename_to_search.lower()) or \
                        filename == filename_to_search:
                    file_path = os.path.join(root, filename)
                    git_file = GitFile(self.repo_dir, file_path.split(self.repo_dir)[1])
                    if not many:
                        return git_file
                    matched_files.append(git_file)

    def _add_file(self, file_path, replace, git_relative_filename="", git_relative_dirname=""):
        if (git_relative_filename == "" and git_relative_dirname == "") or \
                (git_relative_filename != "" and git_relative_dirname != ""):
            raise ValueError("Cannot set a relative filename and dirname!")
        if git_relative_dirname:
            git_relative_path = os.path.join(git_relative_dirname, file_path.split("/")[-1])
        else:
            git_relative_path = git_relative_filename

        full_path = os.path.join(self.repo_dir, git_relative_path)
        if os.path.exists(full_path) and not replace:
            raise FileExistsError("File exists, and replace is set to false")
        try:
            shutil.copyfile(file_path, full_path)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(full_path))
            shutil.copyfile(file_path, full_path)
        return GitFile(self.repo_dir, git_relative_path)

    def __enter__(self):
        self.entered = True
        self.init(self.overwrite)
        return self

    def __exit__(self, *args):
        self.save_and_upload()

    # public

    def init(self, overwrite: bool) -> None:
        """
            Create or update the repo.
                Params:
                    overwrite: overwrite the current repo with a fresh clone.
        """
        if overwrite and self._repo_exists():
            try:
                print("Removing")
                shutil.rmtree(self.repo_dir)
            except:
                print("WARN: Could not delete repo when trying to init")
        if not self._repo_exists():
            os.makedirs(self.repo_dir, exist_ok=True)

        else:
            current_branch = self._run_git_cmd(["branch", "--show-current"])
            if current_branch != self.branch:
                self.change_branch(self.branch)
            self._update_repo()
            return

        self._first_pull()
        self._run_git_cmd(["config", "--local", "user.name", self.user.username])
        self._run_git_cmd(["config", "--local", "user.email", self.user.email])

    def change_branch(self, branch: str) -> None:
        """
            Change the branch.
                Params:
                    branch: the name of the branch to checkout to, needs to exist.
        """

        try:
            self._run_git_cmd(["checkout", branch], exception_msg="changing branch")
        except Exception as e:
            if "did not match any file(s)" in str(e):
                raise GitException(f"Error: Cannot checkout to '{branch}'. Branch does not exist")
        self._update_repo()

    def get_file_changes(self, filter=[], clean_output=True) -> List[
        str]:  # DOESN'T WORK IF THE DIR HAS SPACES NEED FIX
        """
            Get untracked file changes on the repo:
                Params:
                    clean_output: True - only return the file names. False - Return the character code with the file name
                    filter[]: A list of characters representing the files state
                Returns:
                    A list of filenames for untracked changes

                Character codes from the git manual:
                            X          Y     Meaning
                -------------------------------------------------
                    [AMD]   not updated
                M        [ MTD]  updated in index
                T        [ MTD]  type changed in index
                A        [ MTD]  added to index
                D                deleted from index
                R        [ MTD]  renamed in index
                C        [ MTD]  copied in index
                [MTARC]          index and work tree matches
                [ MTARC]    M    work tree changed since index
                [ MTARC]    T    type changed in work tree since index
                [ MTARC]    D    deleted in work tree
                        R    renamed in work tree
                        C    copied in work tree
                -------------------------------------------------
                D           D    unmerged, both deleted
                A           U    unmerged, added by us
                U           D    unmerged, deleted by them
                U           A    unmerged, added by them
                D           U    unmerged, deleted by us
                A           A    unmerged, both added
                U           U    unmerged, both modified
                -------------------------------------------------
                ?           ?    untracked
                !           !    ignored
                -------------------------------------------------

            Please use in a list, ex:   ["A", "D"]
                                        ["A"]
        """
        status = self._run_git_cmd(["status", "--porcelain", "--untracked-files=all"])
        files: list = status.split("\n")[:-1]  # empty line at the end, last index is blank
        if files:
            if filter:
                files = [file for file in files if True in [True for substr in filter if substr in file]]
            if clean_output:
                files = [file.split(" ")[-1] for file in files]

        return files

    def save_and_upload(self, files: list = [], commit_message="") -> None:
        """
            Stage, commit, and push changed files to the remote git repo.
                Params:
                    files: optional, a list of filenames to stage, if there are any filenames in this list,
                            it will only stage those files to be commited and pushed.
                    commit_message: optional, the commit message.
        """
        self._update_repo()
        if self.get_file_changes():
            self._stage_files(files=files)
            self._commit(commit_message)
            self._push()
        else:
            logger.info("No changed files")

    def get_file(self, git_relative_path: str) -> GitFile:
        return GitFile(self.repo_dir, git_relative_path)

    def find_file(self, filename, case_sensitive=True) -> GitFile:
        """
            Find a file in the repo with a specific filename
                Params:
                    filename: The filename to look for
                    case_sensitive = True: Case sensitive search
        """
        return self._find_files(filename, many=False, case_sensitive=case_sensitive)

    def find_all_files(self, filename, case_sensitive=True) -> List[GitFile]:
        """
            Find all files in the repo with a specific filename
                Params:
                    filename: The filename to look for
                    case_sensitive = True: Case sensitive search
        """
        return self._find_files(filename, many=True, case_sensitive=case_sensitive)

    def add_file(self, file_path: str, git_relative_filename="", git_relative_dirname="", replace=True):
        """
            Add a file to the git repo. \n
            **NOTE** this will be slow if adding multiple files and not using this class with the "with" keyword or use 'add_many_files()'
                Params:
                    file_path: The full filename and path to add to the git repo
                    git_relative_filename: the relative filename related to the git repo
                    git_relative_dirname: the dir to add the file in, this will keep the original filename
                    replace=True: If a file with the same name exists, replace it or not
                Returns:
                    GitFile of the added file
        """
        git_file = self._add_file(file_path,
                                  replace,
                                  git_relative_dirname=git_relative_dirname,
                                  git_relative_filename=git_relative_filename)
        if not self.entered:
            self.save_and_upload(commit_message=f"added file: {git_file.file_relative_path}")
        return git_file

    def add_many_files(self, file_paths: List[str], git_relative_dirname="", replace=True):
        """
            Add multiple files to the git repo.
                Params:
                    file_path: The full filename and path to add to the git repo
                    git_relative_dirname: the dir to add the files into, this will keep the original filename
                    replace=True: If a file with the same name exists, replace it or not
                Returns:
                    GitFile of the added file
        """
        git_files = []
        for file in file_paths:
            git_file = self._add_file(file, replace, git_relative_dirname=git_relative_dirname)
            git_files.append(git_file)
        if not self.entered:
            self.save_and_upload(commit_message=f"added files to: {git_relative_dirname}")
        return git_files
