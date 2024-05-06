
<a name="3.0.0"></a>
## [3.0.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.1.0...3.0.0) (2024-05-06)

### Bug Fixes

* **entrypoint:** resolve support for private user namespaces
* **entrypoint:** detect if GitLab actions can continue
* **entrypoint:** enforce against missing '.description' values
* **gitlab:** enforce 'group_delete' usage in '--dry-run' mode
* **gitlab:** delay groups deletion by 10s and projects by 5s
* **gitlab:** get all branches and tags upon 'list()' calls
* **gitlab:** get all members in 'project_reset_members'

### Ci

* **gitlab-ci:** move 'readme' job after 'build' and local 'install'

### Cleanups

* **gitlab:** minor comments changes in 'project_reset_features'

### Features

* **entrypoint:** preserve main group description if exists
* **entrypoint:** always flush progress output logs
* **gitlab:** detect multiple branches to keep 'Merge requests'
* **gitlab:** detect 'Token Access' usage for 'CI/CD' features
* **namespaces:** migrate 'Helper' class to 'Namespaces' class


<a name="2.1.0"></a>
## [2.1.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.0.2...2.1.0) (2024-04-28)

### Bug Fixes

* **entrypoint:** fix project '--update-description' logs output

### Features

* **entrypoint:** sort groups and projects recursively
* **entrypoint:** keep description if already contains group


<a name="2.0.2"></a>
## [2.0.2](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.0.1...2.0.2) (2024-04-28)

### Ci

* **gitlab-ci:** disable 'typing' mypy caching with 'MYPY_CACHE_DIR'

### Documentation

* **readme:** document GitLab tokens' creation instructions

### Features

* **main:** limit '--help' width to terminal width or 120 chars


<a name="2.0.1"></a>
## [2.0.1](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/2.0.0...2.0.1) (2024-04-28)

### Bug Fixes

* **entrypoint:** fix description updates faulty descriptions


<a name="2.0.0"></a>
## [2.0.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/1.1.0...2.0.0) (2024-04-27)

### Bug Fixes

* **gitlab:** enforce '--dry-run' usage and improve Python codestyle
* **settings:** apply 'subgroup' feature to subgroup groups

### Ci

* **gitlab-ci:** implement 'readme' local job to update README details

### Cleanups

* **gitlab:** minor Python codestyle improvements
* **settings:** minor Python codestyle improvements
* **src:** ignore 'import-error' over '__init__' and '__main__'

### Code Refactoring

* **entrypoint:** minor Python codestyle improvements
* **src:** isolate all sources under 'src/'

### Documentation

* **readme:** regenerate '--help' details in 'README.md'

### Features

* **cli:** isolate 'features/settings.py' to 'cli/entrypoint.py'
* **main:** align 'RawTextHelpFormatter' to 30 chars columns
* **main:** change '--set-description' metavar to 'TEXT'
* **settings:** change project/group descriptions color


<a name="1.1.0"></a>
## [1.1.0](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/1.0.1...1.1.0) (2024-04-25)

### Code Refactoring

* **settings:** minor functions codestyle improvement

### Features

* **main:** rename '--avoid-*' parameters to '--exclude-*'


<a name="1.0.1"></a>
## [1.0.1](https://gitlab.com/AdrianDC/gitlab-projects-settings/compare/1.0.0...1.0.1) (2024-04-24)

### Documentation

* **setup:** fix PyPI 'gitlab-projects-settings' documentation


<a name="1.0.0"></a>
## 1.0.0 (2024-04-24)

### Features

* **gitlab-projects-settings:** initial sources implementation

