CAS for Open edX installations
==============================

|ci-badge| |license-badge|

Overview
---------

Support for `Centralized Authentication System (CAS)` that can be used by Open edX installations.

Implementation details
~~~~~~~~~~~~~~~~~~~~~~

- This plugin implements the CAS protocol based on the `django-cas-ng <https://github.com/django-cas-ng/django-cas-ng>`_ implementation.

- It's implemented to work as a `social-core <https://github.com/python-social-auth/social-core/>`_ backend.

- In order to integrate with the Open edX platform, as a temporary solution we're monkey-patching the `Registry model <https://github.com/eduNEXT/openedx-cas/blob/main/openedx_cas/models.py#L82-L85>`_ from the edx-platform
  so it recognizes the CAS backend. As a more stable solution, we're thinking on implementing an Open edX Filter that adds extra providers to the platform.

- This design allows the plugin to work out-of-the-box after installation.

Installation
------------

After this installation, the plugin will be added to the `AUTHENTICATION_BACKENDS <https://github.com/eduNEXT/openedx-cas/blob/main/openedx_cas/settings/common.py#L12-L13>`_ setting, enabling its
usage in Open edX installations.

.. code-block:: bash

    pip install git+https://github.com/eduNEXT/openedx-cas.git@v0.2.0

    # Then run data migrations
    ./manage.py lms migrate openedx_cas

Configuration
-------------

Assuming you have already setup a CAS service for identity verification, this configuration
will help you to integrate your IDP as a authentication mechanism for your Open edX installation.

The required configuration includes:

.. code-block:: json

    {
        "CAS_LOGOUT_URL": "https://cas-server/logout",
        "CAS_SERVER_URL": "https://cas-server/",
        "CAS_SERVICE_URL": "https://LMS_BASE/auth/complete/centralized-auth-service/?next=/"
    }

We advise you to use the following third party auth pipeline:

.. code-block:: json

    "SOCIAL_AUTH_CENTRALIZED_AUTH_SERVICE_PIPELINE": [
        "common.djangoapps.third_party_auth.pipeline.parse_query_params",
        "social_core.pipeline.social_auth.social_details",
        "social_core.pipeline.social_auth.social_uid",
        "social_core.pipeline.social_auth.auth_allowed",
        "social_core.pipeline.social_auth.social_user",
        "common.djangoapps.third_party_auth.pipeline.associate_by_email_if_login_api",
        "common.djangoapps.third_party_auth.pipeline.associate_by_email_if_saml",
        "common.djangoapps.third_party_auth.pipeline.associate_by_email_if_oauth",
        "common.djangoapps.third_party_auth.pipeline.get_username",
        "common.djangoapps.third_party_auth.pipeline.set_pipeline_timeout",
        "common.djangoapps.third_party_auth.pipeline.ensure_user_information",
        "social_core.pipeline.user.create_user",
        "social_core.pipeline.social_auth.associate_user",
        "social_core.pipeline.social_auth.load_extra_data",
        "social_core.pipeline.user.user_details",
        "common.djangoapps.third_party_auth.pipeline.user_details_force_sync",
        "common.djangoapps.third_party_auth.pipeline.set_id_verification_status",
        "common.djangoapps.third_party_auth.pipeline.set_logged_in_cookies",
        "common.djangoapps.third_party_auth.pipeline.login_analytics",
        "common.djangoapps.third_party_auth.pipeline.ensure_redirect_url_is_safe",
    ]

Now, to enable this new backend in your installation, you need to create a CAS provider configuration:

#. Go to `/admin/openedx_cas/`
#. Create a new provider configuration for CAS.
#. Fill in the fields that matches the behavior you're looking for.

And done.

Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block:: bash

  # Clone the repository
  git clone git@github.com:edx/openedx-cas.git
  cd openedx-cas

  # Set up a virtualenv using virtualenvwrapper with the same name as the repo and activate it
  mkvirtualenv -p python3.8 openedx-cas


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

  # Activate the virtualenv
  workon openedx-cas

  # Grab the latest code
  git checkout main
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

How To Contribute
-----------------

Contributions are very welcome.
Please read `How To Contribute <https://github.com/openedx/edx-platform/blob/master/CONTRIBUTING.rst>`_ for details.
Even though they were written with ``edx-platform`` in mind, the guidelines
should be followed for all Open edX projects.

The pull request description template should be automatically applied if you are creating a pull request from GitHub. Otherwise you
can find it at `PULL_REQUEST_TEMPLATE.md <.github/PULL_REQUEST_TEMPLATE.md>`_.

The issue report template should be automatically applied if you are creating an issue on GitHub as well. Otherwise you
can find it at `ISSUE_TEMPLATE.md <.github/ISSUE_TEMPLATE.md>`_.

Reporting Security Issues
-------------------------

Please do not report security issues in public. Please email technical@edunext.co.

Getting Help
------------

If you're having trouble, we have discussion forums at https://discuss.openedx.org where you can connect with others in the community.

Our real-time conversations are on Slack. You can request a `Slack invitation`_, then join our `community Slack workspace`_.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help

.. |ci-badge| image:: https://github.com/eduNEXT/openedx-cas/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-cas/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-cas.svg
    :target: https://github.com/eduNEXT/openedx-cas/blob/main/LICENSE.txt
    :alt: License
