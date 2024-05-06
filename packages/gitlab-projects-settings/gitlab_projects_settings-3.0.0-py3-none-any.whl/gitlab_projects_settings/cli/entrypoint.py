#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace

# Modules libraries
from gitlab.exceptions import GitlabGetError
from gitlab.v4.objects import Group as GitLabGroup, Project as GitLabProject, User as GitLabUser

# Components
from ..features.gitlab import GitLabFeature
from ..prints.colors import Colors
from ..system.platform import Platform
from ..types.namespaces import Namespaces

# Entrypoint class, pylint: disable=too-few-public-methods
class Entrypoint:

    # CLI, pylint: disable=too-many-branches
    @staticmethod
    def cli(options: Namespace) -> bool:

        # Variables
        group: GitLabGroup = None
        project: GitLabProject = None
        user: GitLabUser = None

        # Header
        print(' ')

        # GitLab client
        gitlab = GitLabFeature(
            options.gitlab,
            options.token,
            options.dry_run,
        )
        print(f'{Colors.BOLD} - GitLab host: '
              f'{Colors.GREEN}{gitlab.url}'
              f'{Colors.RESET}')
        Platform.flush()

        # GitLab path
        try:
            group = gitlab.group(options.path)
            print(f'{Colors.BOLD} - GitLab group: '
                  f'{Colors.GREEN}{group.full_path}'
                  f'{Colors.CYAN} ({group.description})'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
        except GitlabGetError as exception:
            try:
                if '/' in options.path:
                    raise TypeError from exception
                user = gitlab.user(options.path)
                namespace = gitlab.namespace(user.namespace_id)
                print(f'{Colors.BOLD} - GitLab user namespace: '
                      f'{Colors.GREEN}{namespace.full_path}'
                      f'{Colors.CYAN} ({namespace.name})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()
            except (GitlabGetError, TypeError):
                project = gitlab.project(options.path)
                print(f'{Colors.BOLD} - GitLab project: '
                      f'{Colors.GREEN}{project.path_with_namespace}'
                      f'{Colors.CYAN} ({project.description})'
                      f'{Colors.RESET}')
                print(' ')
                Platform.flush()

        # Handle single project
        if project:
            Entrypoint.project(
                options,
                gitlab,
                project.id,
            )

        # Handle group recursively
        elif group:

            # Handle group
            if not options.exclude_group:
                if not Entrypoint.group(
                        options,
                        gitlab,
                        group.id,
                ):
                    return False

            # Iterate through subgroups
            if not options.exclude_subgroups:
                for group_subgroup in sorted(
                        group.descendant_groups.list(
                            get_all=True,
                            include_subgroups=True,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.full_path,
                ):
                    if not Entrypoint.group(
                            options,
                            gitlab,
                            group_subgroup.id,
                            True,
                    ):
                        return False

            # Iterate through projects
            if not options.exclude_projects:
                for group_project in sorted(
                        group.projects.list(
                            get_all=True,
                            include_subgroups=not options.exclude_subgroups,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.path_with_namespace,
                ):
                    if not Entrypoint.project(
                            options,
                            gitlab,
                            group_project.id,
                    ):
                        return False

        # Handle user recursively
        elif user:

            # Iterate through projects
            if not options.exclude_projects:
                for user_project in sorted(
                        user.projects.list(
                            get_all=True,
                            order_by='path',
                            sort='asc',
                        ),
                        key=lambda item: item.path_with_namespace,
                ):
                    if not Entrypoint.project(
                            options,
                            gitlab,
                            user_project.id,
                    ):
                        return False

        # Result
        return True

    # Group
    @staticmethod
    def group(
        options: Namespace,
        gitlab: GitLabFeature,
        criteria: str,
        subgroup: bool = False,
    ) -> bool:

        # Acquire group
        group = gitlab.group(criteria)

        # Acquire parent group
        parent_group: GitLabGroup = None
        if group.parent_id:
            parent_group = gitlab.group(group.parent_id)

        # Get parent description
        parent_description: str = ''
        parent_name: str = ''
        if parent_group:
            parent_description = parent_group.description
            parent_name = parent_group.name

        # Show group details
        group_type = 'subgroup' if subgroup else 'group'
        print(f'{Colors.BOLD} - GitLab {group_type}: '
              f'{Colors.YELLOW_LIGHT}{group.full_path} '
              f'{Colors.CYAN}({group.description})'
              f'{Colors.RESET}')
        Platform.flush()

        # Delete group
        if options.delete_group:
            gitlab.group_delete(criteria)
            print(f'{Colors.BOLD}   - Delete {group_type}: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
            return subgroup

        # Set group description
        if options.set_description:
            gitlab.group_set_description(criteria, options.set_description)
            print(f'{Colors.BOLD}   - Set description: '
                  f'{Colors.CYAN}{options.set_description}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Update group description
        elif options.update_description:
            parent_description_text: str = ''
            if parent_name:
                parent_description_text = ' - ' + Namespaces.describe(
                    name=parent_name,
                    description=parent_description,
                )
            if not group.description or subgroup and ( \
                        not parent_description_text or \
                        not group.description.endswith(f'{parent_description_text}') \
                    ):
                description = f'{Namespaces.describe(name=group.name)}' \
                              f'{parent_description_text}'
                gitlab.group_set_description(criteria, description)
                print(f'{Colors.BOLD}   - Updated description: '
                      f'{Colors.CYAN}{description}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Kept description: '
                      f'{Colors.GREEN}{group.description}'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset group members
        if options.reset_members:
            gitlab.group_reset_members(criteria)
            print(f'{Colors.BOLD}   - Reset members: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Set group avatar
        if options.set_avatar:
            gitlab.group_set_avatar(criteria, options.set_avatar)
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return True

    # Project, pylint: disable=too-many-branches,too-many-statements
    @staticmethod
    def project(
        options: Namespace,
        gitlab: GitLabFeature,
        criteria: str,
    ) -> bool:

        # Acquire project
        project = gitlab.project(criteria)

        # Show project details
        print(f'{Colors.BOLD} - GitLab project: '
              f'{Colors.YELLOW_LIGHT}{project.path_with_namespace} '
              f'{Colors.CYAN}({project.description})'
              f'{Colors.RESET}')
        Platform.flush()

        # Delete project
        if options.delete_project:
            gitlab.project_delete(criteria)
            print(f'{Colors.BOLD}   - Delete project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            print(' ')
            Platform.flush()
            return True

        # Set project description
        if options.set_description:
            gitlab.project_set_description(criteria, options.set_description)
            print(f'{Colors.BOLD}   - Set description: '
                  f'{Colors.CYAN}{options.set_description}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Update project description
        elif options.update_description:
            namespace_description: str
            if project.namespace['kind'] == 'user':
                namespace = gitlab.namespace(project.namespace['id'])
                namespace_description = namespace.name
            else:
                group = gitlab.group(project.namespace['id'])
                namespace_description = Namespaces.describe(
                    name=group.name,
                    description=group.description,
                )
            if not project.description or \
                    not project.description.endswith(f' - {namespace_description}'):
                description = f'{Namespaces.describe(name=project.name)}' \
                              f' - {namespace_description}'
                gitlab.project_set_description(criteria, description)
                print(f'{Colors.BOLD}   - Updated description: '
                      f'{Colors.CYAN}{description}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Kept description: '
                      f'{Colors.GREEN}{project.description}'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset project features
        if options.reset_features:
            features = ', '.join(gitlab.project_reset_features(criteria))
            if features:
                print(f'{Colors.BOLD}   - Reset features: '
                      f'{Colors.CYAN}{features}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Reset features: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Reset project members
        if options.reset_members:
            gitlab.project_reset_members(criteria)
            print(f'{Colors.BOLD}   - Reset members: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Set project avatar
        if options.set_avatar:
            gitlab.project_set_avatar(criteria, options.set_avatar)
            print(f'{Colors.BOLD}   - Set avatar: '
                  f'{Colors.CYAN}{options.set_avatar}'
                  f'{Colors.RESET}')
            Platform.flush()

        # Run project housekeeping
        if options.run_housekeeping:
            gitlab.project_run_housekeeping(criteria)
            print(f'{Colors.BOLD}   - Ran housekeeping: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Archive project
        if options.archive_project:
            gitlab.project_set_archive(criteria, True)
            print(f'{Colors.BOLD}   - Archive project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Unarchive project
        elif options.unarchive_project:
            gitlab.project_set_archive(criteria, False)
            print(f'{Colors.BOLD}   - Unarchive project: '
                  f'{Colors.GREEN}Success'
                  f'{Colors.RESET}')
            Platform.flush()

        # Protect project branches
        if options.protect_branches:
            branches = ', '.join(gitlab.project_protect_branches(criteria))
            if branches:
                print(f'{Colors.BOLD}   - Protecting branches: '
                      f'{Colors.CYAN}{branches}'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Protecting branches: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Protect project tags
        if options.protect_tags:
            tags = ', '.join(gitlab.project_protect_tags(criteria, options.protect_tags))
            if tags:
                print(f'{Colors.BOLD}   - Protecting tags: '
                      f'{Colors.CYAN}{tags}'
                      f'{Colors.GREEN} (level: {options.protect_tags})'
                      f'{Colors.RESET}')
                Platform.flush()
            else:
                print(f'{Colors.BOLD}   - Protecting tags: '
                      f'{Colors.GREEN}Already done'
                      f'{Colors.RESET}')
                Platform.flush()

        # Footer
        print(' ')
        Platform.flush()

        # Result
        return True
