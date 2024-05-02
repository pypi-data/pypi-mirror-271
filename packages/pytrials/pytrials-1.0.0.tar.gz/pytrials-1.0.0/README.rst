========
pytrials
========


.. image:: https://img.shields.io/pypi/v/pytrials.svg
        :target: https://pypi.python.org/pypi/pytrials

.. image:: https://github.com/jvfe/pytrials/workflows/pytest/badge.svg
        :target: https://github.com/jvfe/pytrials/actions

.. image:: https://img.shields.io/pypi/l/pytrials
        :target: https://github.com/jvfe/pytrials/blob/master/LICENSE

.. image:: https://readthedocs.org/projects/pytrials/badge/?version=latest
        :target: https://pytrials.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Python wrapper around the clinicaltrials.gov API.
Documentation for the API can be found here: https://clinicaltrials.gov/api/


* Free software: BSD license
* Documentation: https://pytrials.readthedocs.io.


Tutorial
--------
To install::

    $ pip install pytrials

Basic Usage
^^^^^^^^^^^
::

    from pytrials.client import ClinicalTrials

    ct = ClinicalTrials()

    # Get 50 full studies related to Coronavirus and COVID in csv format.
    ct.get_full_studies(search_expr="Coronavirus+COVID", max_studies=50)

    # Get the NCTId, Condition and Brief title fields from 1000 studies related to Coronavirus and Covid, in csv format.
    corona_fields = ct.get_study_fields(
        search_expr="Coronavirus+COVID",
        fields=["NCT Number", "Conditions", "Study Title"],
        max_studies=1000,
        fmt="csv",
    )

    # Read the csv data in Pandas
    import pandas as pd

    pd.DataFrame.from_records(corona_fields[1:], columns=corona_fields[0])

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
