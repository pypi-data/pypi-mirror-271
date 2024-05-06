# gitlab-projects-settings

<!-- markdownlint-disable no-inline-html -->

[![Build](https://gitlab.com/AdrianDC/gitlab-projects-settings/badges/main/pipeline.svg)](https://gitlab.com/AdrianDC/gitlab-projects-settings/-/commits/main/)

Configure GitLab groups and projects settings automatically

---

## Purpose

This tool can automatically configure and update the GitLab settings  
of groups, subgroups and projects, using multiple available options.

Repetitive tasks can be performed accross multiple projects at once,  
for example protecting tags and branches, or setting a new avatar recursively.

The following step is required before using the tool:

- The GitLab user tokens must be created with an `api` scope (a short expiration date is recommended)

---

## Usage

<!-- prettier-ignore-start -->
<!-- readme-help-start -->

```yaml
usage: gitlab-projects-settings [-h] [--version] [-t TOKEN] [--dry-run] [--exclude-group] [--exclude-subgroups]
                                [--exclude-projects] [--reset-features] [--reset-members] [--set-avatar FILE]
                                [--set-description TEXT] [--update-description] [--run-housekeeping]
                                [--archive-project | --unarchive-project] [--delete-group] [--delete-project]
                                [--protect-branches] [--protect-tags LEVEL]
                                [gitlab] [path]

gitlab-projects-settings: Configure GitLab groups and projects settings automatically

internal arguments:
  -h, --help              # Show this help message
  --version               # Show the current version

credentials arguments:
  -t TOKEN                # GitLab API token (default: GITLAB_TOKEN environment)

common settings arguments:
  --dry-run               # Enable dry run mode to check without saving
  --exclude-group         # Exclude parent group settings
  --exclude-subgroups     # Exclude children subgroups settings
  --exclude-projects      # Exclude children projects settings

general settings arguments:
  --reset-features        # Reset features of GitLab projects based on usage
  --reset-members         # Reset members of GitLab projects and groups
  --set-avatar FILE       # Set avatar of GitLab projects and groups
  --set-description TEXT  # Set description of GitLab projects and groups
  --update-description    # Update description of GitLab projects and groups automatically

advanced settings arguments:
  --run-housekeeping      # Run housekeeping of project or projects GitLab in groups
  --archive-project       # Archive project or projects in GitLab groups
  --unarchive-project     # Unarchive project or projects in GitLab groups
  --delete-group          # Delete group or groups in GitLab groups
  --delete-project        # Delete project or projects in GitLab groups

repository settings arguments:
  --protect-branches      # Protect branches with default master/main, develop and staging
  --protect-tags LEVEL    # Protect tags at level [no-one,admins,maintainers,developers]

positional arguments:
  gitlab                  # GitLab URL (default: https://gitlab.com)
  path                    # GitLab group, user namespace or project path
```

<!-- readme-help-stop -->
<!-- prettier-ignore-end -->

---

## Dependencies

- [colored](https://pypi.org/project/colored/): Terminal colors and styles
- [python-gitlab](https://pypi.org/project/python-gitlab/): A python wrapper for the GitLab API
- [setuptools](https://pypi.org/project/setuptools/): Build and manage Python packages

---

## References

- [git-chglog](https://github.com/git-chglog/git-chglog): CHANGELOG generator
- [gitlab-release](https://pypi.org/project/gitlab-release/): Utility for publishing on GitLab
- [gitlabci-local](https://pypi.org/project/gitlabci-local/): Launch .gitlab-ci.yml jobs locally
- [mypy](https://pypi.org/project/mypy/): Optional static typing for Python
- [PyPI](https://pypi.org/): The Python Package Index
- [twine](https://pypi.org/project/twine/): Utility for publishing on PyPI
