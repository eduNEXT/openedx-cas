Change Log
----------

..
   All enhancements and patches to openedx_cas will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.

Unreleased
~~~~~~~~~~

[0.3.0] - 2026-03-30
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Support for Python 3.11 and 3.12.
* Support for Django 4.2 and 5.2 (compatible with Open edX Teak).
* New GitHub Actions test matrix with the supported Python/Django combinations.
* Set `DJANGO_SETTINGS_MODULE` in the `quality` tox environment to avoid pylint configuration errors.

Changed
_______

* Updated `social-auth-core` from 4.1.0 to 4.8.5.
* Upgraded all dependencies via `make upgrade`.
* Updated GitHub workflows (`ci.yml`, `pypi-publish.yml`) to use recent action versions.
* Updated `tox.ini` to test against the new Python and Django versions.
* Updated classifiers in `setup.py` to reflect Python 3.11/3.12 and Django 4.2/5.2.
* Updated `README.rst` compatibility table to include Teak.

Removed
_______

* Dropped support for Python 3.8.
* Dropped support for Django 2.2, 3.2, and 4.0.
* Removed obsolete pylint options (regenerated `.pylintrc` with edx-lint).

Fixed
_____

* Fixed pylint warnings in `setup.py` by using `with` statements for file operations.
* Fixed `tox.ini` to allow external commands in the `quality` environment.

[0.2.3] - 2022-08-11
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Added CAS_REDIRECT_WITHOUT_TICKET setting.

[0.2.2] - 2022-07-27
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Raise AuthMissingParameter if there is no ticket in the service response.


[0.2.1] - 2022-07-26
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* Missing setting from django-cas-ng implementation.


[0.2.0] - 2022-07-15
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First working implementation of CAS backend.
* Integration with the Maple Open edX Release.

[0.1.0] - 2022-06-17
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Added
_____

* First release on PyPI.
