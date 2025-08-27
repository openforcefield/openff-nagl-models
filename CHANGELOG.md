# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
The rules for this file:
  * entries are sorted newest-first.
  * summarize sets of changes - don't reproduce every git log comment here.
  * don't ever delete anything.
  * keep the format consistent (79 char width, Y/M/D date format) and do not
    use tabs but use spaces for formatting
  * accompany each entry with github issue/PR number (Issue #xyz)
-->

## v0.4.1 - 2025-08-19

### Authors
<!-- GitHub usernames of contributors to this release -->
- @mattwthompson
- @j-wags
- @Ialibay

### Behaviors changed
- Temporarily re-enabled support for certain methods to accept absolute paths to model files as input. 


## v0.4.0 - 2025-08-11

### Authors
- @lilyminium
- @Yoshanuikabundi
- @mattwthompson
- @j-wags
- @jaclark5 (assisted with debugging caching issues)

### New features
- Added fetching by DOI, hash verification, and caching. (#44, #61, #62)

## v0.3.0 - 2024-07-29

### Authors
<!-- GitHub usernames of contributors to this release -->
- @lilyminium

### Added
- Added the openff-gnn-am1bcc-0.1.0-rc.3.pt model (PR #31)

## v0.2.0 - 2024-04-19

### Authors
<!-- GitHub usernames of contributors to this release -->
- @lilyminium

### Added
- Added the openff-gnn-am1bcc-0.1.0-rc.2.pt model (PR #26)

## v0.1.2 - 2024-02-09

### Authors
<!-- GitHub usernames of contributors to this release -->
- @lilyminium

### Fixed
- Replaced pkg_resources with importlib (Issue #14, PR #18)

### Changed
<!-- Changes in existing functionality -->
- Moved get_models_by_type to top-level import (Issue #16, PR #17)
