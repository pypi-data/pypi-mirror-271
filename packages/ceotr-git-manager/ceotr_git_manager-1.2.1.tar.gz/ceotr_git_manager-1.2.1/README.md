# ceotr_git_manager

This library contains tools to manage files controlled by a remote git repository

## Current Functionality

* Clone a remote repo to a specific location
* Check which files have been changed
* Commit and push all or select file changes
* Specify to keep remote or local changes
* Authenticates with git tokens

## Planned Functionality

* Authenticate with ssh keys
* Add tests

There should be no problems with merge conflicts if you only use the public functions. There is more control if you use
private functions, but you'll have to do the error handling your self.

## Reference

[GitLab Repository files API](https://docs.gitlab.com/ee/api/repository_files.html)

## Unit Test

On the project's root folder, run:

```shell
pytest
```