# -*- coding: utf-8 -*-

from acore_doc import api


def test():
    _ = api


if __name__ == "__main__":
    from acore_doc.tests import run_cov_test

    run_cov_test(__file__, "acore_doc.api", preview=False)
