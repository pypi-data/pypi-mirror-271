#!/usr/bin/env python3

# Standard libraries
from time import sleep
from typing import List

# Modules libraries
from gitlab import Gitlab
from gitlab.exceptions import GitlabGetError, GitlabListError
from gitlab.v4.objects import Group, Namespace, Project, User

# GitLabFeature class
class GitLabFeature:

    # Members
    __dry_run: bool = False
    __gitlab: Gitlab

    # Constructor
    def __init__(self, url: str, token: str, dry_run: bool = False) -> None:
        self.__dry_run = dry_run
        self.__gitlab = Gitlab(url, private_token=token)
        self.__gitlab.auth()

    # Group
    def group(self, criteria: str) -> Group:
        return self.__gitlab.groups.get(criteria)

    # Group delete
    def group_delete(self, criteria: str) -> None:

        # Delete group
        if not self.__dry_run:
            group = self.group(criteria)
            group.delete()
            sleep(10)

    # Group reset members
    def group_reset_members(self, criteria: str) -> None:

        # Remove group members
        group = self.group(criteria)
        for member in group.members.list(get_all=True):
            if not self.__dry_run:
                group.members.delete(member.id)

        # Save group
        if not self.__dry_run:
            group.save()

    # Group set avatar
    def group_set_avatar(self, criteria: str, file: str) -> None:

        # Set group avatar
        if not self.__dry_run:
            group = self.group(criteria)
            with open(file, 'rb') as avatar:
                group.avatar = avatar

                # Save group
                group.save()

    # Group set description
    def group_set_description(self, criteria: str, description: str) -> None:

        # Set group description
        if not self.__dry_run:
            group = self.group(criteria)
            group.description = description

            # Save group
            group.save()

    # Namespace
    def namespace(self, criteria: str) -> Namespace:
        return self.__gitlab.namespaces.get(criteria)

    # Project
    def project(self, criteria: str) -> Project:
        return self.__gitlab.projects.get(criteria)

    # Project delete
    def project_delete(self, criteria: str) -> None:

        # Delete project
        project = self.project(criteria)
        if not self.__dry_run:
            project.delete()
            sleep(5)

    # Project protect branches
    def project_protect_branches(self, criteria: str) -> List[str]:

        # Validate project feature
        result: List[str] = []
        project = self.project(criteria)
        try:
            assert project.branches.list(get_all=True)
        except (AssertionError, GitlabListError):
            return result

        # Acquire project, branches and protected branches
        branches = [branch.name for branch in project.branches.list(get_all=True)]
        protectedbranches = [
            protectedbranch.name
            for protectedbranch in project.protectedbranches.list(get_all=True)
        ]

        # Protect main/master
        for branch in ['main', 'master']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 40,
                        'push_access_level': 40,
                        'allow_force_push': False
                    })
                result += [branch]

        # Protect develop
        for branch in ['develop']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 40,
                        'push_access_level': 40,
                        'allow_force_push': True
                    })
                result += [branch]

        # Protect staging
        for branch in ['staging']:
            if branch in branches and branch not in protectedbranches:
                if not self.__dry_run:
                    project.protectedbranches.create({
                        'name': branch,
                        'merge_access_level': 30,
                        'push_access_level': 30,
                        'allow_force_push': True
                    })
                result += [branch]

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project protect tags, pylint: disable=too-many-branches
    def project_protect_tags(self, criteria: str, protect_level: str) -> List[str]:

        # Validate project feature
        result: List[str] = []
        project = self.project(criteria)
        try:
            assert project.tags.list(get_all=True)
        except (AssertionError, GitlabListError):
            return result

        # Prepare access level
        access_level: int
        if protect_level == 'no-one':
            access_level = 0
        elif protect_level == 'admins':
            access_level = 60
        elif protect_level == 'maintainers':
            access_level = 40
        elif protect_level == 'developers':
            access_level = 30
        else:
            raise SyntaxError(f'Unknown protection level: {access_level}')

        # Acquire protected tags
        protectedtags = [
            protectedtag.name for protectedtag in project.protectedtags.list(get_all=True)
        ]

        # Update protected tags
        for protectedtag in project.protectedtags.list(get_all=True):
            protectedtag_level = protectedtag.create_access_levels[0]['access_level']
            if protectedtag_level != 0 and (access_level == 0
                                            or protectedtag_level < access_level):
                name = protectedtag.name
                if not self.__dry_run:
                    protectedtag.delete()
                    project.protectedtags.create({
                        'name': name,
                        'create_access_level': access_level
                    })
                result += [name]

        # Protect unprotected tags
        for tag in project.tags.list(get_all=True):
            if tag.name not in protectedtags:
                if not self.__dry_run:
                    project.protectedtags.create({
                        'name': tag.name,
                        'create_access_level': access_level
                    })
                result += [tag.name]

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        result.sort()
        return result

    # Project reset features, pylint: disable=too-many-branches,too-many-statements
    def project_reset_features(self, criteria: str) -> List[str]:

        # Variables
        result: List[str] = []
        project = self.__gitlab.projects.get(criteria, statistics=True)

        # Disable unused feature (Issues)
        if project.issues_enabled and not project.issues.list(get_all=False):
            project.issues_enabled = False
            result += ['Issues']

        # Disable unused feature (Repository)
        try:
            assert project.commits.list(get_all=False)
        except (AssertionError, GitlabListError):
            if project.repository_access_level != 'disabled':
                project.repository_access_level = 'disabled'
                result += ['Repository']

        # Disable unused feature (Merge requests)
        try:
            if not project.mergerequests.list(get_all=False):
                pass
            elif len(project.branches.list(get_all=False)) > 1:
                pass
            else:
                assert False
        except (AssertionError, GitlabListError):
            if project.merge_requests_enabled:
                project.merge_requests_enabled = False
                result += ['Merge requests']

        # Disable unused feature (Forks)
        if project.forking_access_level != 'disabled' and not project.forks.list(
                get_all=False):
            project.forking_access_level = 'disabled'
            result += ['Forks']

        # Disable unused feature (Git LFS)
        if project.lfs_enabled and project.statistics['lfs_objects_size'] == 0:
            project.lfs_enabled = False
            result += ['Git LFS']

        # Disable unused feature (CI/CD)
        try:
            if project.jobs.list(get_all=False):
                pass
            elif any('name' in item and item['name'] == '.gitlab-ci.yml'
                     for item in project.repository_tree(get_all=True)):
                pass
            elif any('path_with_namespace' in item
                     and item['path_with_namespace'] != project.path_with_namespace
                     for item in self.__gitlab.http_get(
                         f'/projects/{project.id}/job_token_scope/allowlist',
                         get_all=True,
                     )):
                pass
            else:
                assert False
        except (AssertionError, GitlabGetError, GitlabListError):
            if project.jobs_enabled:
                project.jobs_enabled = False
                result += ['CI/CD']

        # Disable unused feature (Container registry)
        if project.container_registry_enabled and not project.repositories.list(
                get_all=False):
            project.container_registry_enabled = False
            result += ['Container registry']

        # Disable unused feature (Analytics)
        if project.analytics_access_level != 'disabled':
            project.analytics_access_level = 'disabled'
            result += ['Analytics']

        # Disable unused feature (Security and Compliance)
        if project.security_and_compliance_access_level != 'disabled':
            project.security_and_compliance_access_level = 'disabled'
            result += ['Security and Compliance']

        # Disable unused feature (Wiki)
        if project.wiki_enabled and not project.wikis.list(get_all=False):
            project.wiki_enabled = False
            result += ['Wiki']

        # Disable unused feature (Snippets)
        if project.snippets_enabled and not project.snippets.list(get_all=False):
            project.snippets_enabled = False
            result += ['Snippets']

        # Disable unused feature (Package registry)
        if project.packages_enabled and not project.packages.list(get_all=False):
            project.packages_enabled = False
            result += ['Package registry']

        # Disable unused feature (Model experiments)
        if project.model_experiments_access_level != 'disabled':
            project.model_experiments_access_level = 'disabled'
            result += ['Model experiments']

        # Disable unused feature (Model registry)
        if project.model_registry_access_level != 'disabled':
            project.model_registry_access_level = 'disabled'
            result += ['Model registry']

        # Disable unused feature (Pages)
        if project.pages_access_level != 'disabled':
            project.pages_access_level = 'disabled'
            result += ['Pages']

        # Disable unused feature (Monitor)
        if project.monitor_access_level != 'disabled':
            project.monitor_access_level = 'disabled'
            result += ['Monitor']

        # Disable unused feature (Environments)
        try:
            assert project.environments.list(get_all=False)
        except (AssertionError, GitlabListError):
            if project.environments_access_level != 'disabled':
                project.environments_access_level = 'disabled'
                result += ['Environments']

        # Disable unused feature (Feature flags)
        if project.feature_flags_access_level != 'disabled':
            project.feature_flags_access_level = 'disabled'
            result += ['Feature flags']

        # Disable unused feature (Infrastructure)
        if project.infrastructure_access_level != 'disabled':
            project.infrastructure_access_level = 'disabled'
            result += ['Infrastructure']

        # Disable unused feature (Releases)
        if project.releases_access_level != 'disabled' and not project.releases.list(
                get_all=False):
            project.releases_access_level = 'disabled'
            result += ['Releases']

        # Disable unused feature (Service Desk)
        if project.service_desk_enabled:
            project.service_desk_enabled = False
            result += ['Service Desk']

        # Disable unused feature (Auto DevOps)
        if project.auto_devops_enabled:
            project.auto_devops_enabled = False
            result += ['Auto DevOps']

        # Save project
        if not self.__dry_run:
            project.save()

        # Result
        return result

    # Project reset members
    def project_reset_members(self, criteria: str) -> None:

        # Remove project members
        if not self.__dry_run:
            project = self.project(criteria)
            for member in project.members.list(get_all=True):
                project.members.delete(member.id)

            # Save project
            project.save()

    # Project run housekeeping
    def project_run_housekeeping(self, criteria: str) -> None:

        # Run project housekeeping
        if not self.__dry_run:
            project = self.project(criteria)
            project.housekeeping()

    # Project set archive
    def project_set_archive(self, criteria: str, enabled: bool) -> None:

        # Archive project
        if not self.__dry_run and enabled:
            project = self.project(criteria)
            project.archive()

        # Unarchive project
        elif not self.__dry_run:
            project = self.project(criteria)
            project.unarchive()

    # Project set avatar
    def project_set_avatar(self, criteria: str, file: str) -> None:

        # Set project avatar
        if not self.__dry_run:
            project = self.project(criteria)
            with open(file, 'rb') as avatar:
                project.avatar = avatar

                # Save project
                project.save()

    # Project set description
    def project_set_description(self, criteria: str, description: str) -> None:

        # Set project description
        if not self.__dry_run:
            project = self.project(criteria)
            project.description = description

            # Save project
            project.save()

    # User
    def user(self, criteria: str) -> User:
        return self.__gitlab.users.list(username=criteria)[0]

    # URL
    @property
    def url(self) -> str:
        return str(self.__gitlab.api_url)
