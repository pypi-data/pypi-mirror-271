from unittest import TestCase

from pbsrollout.main import get_tag


class Test(TestCase):
    def test_get_tag(self):
        tag = get_tag([
            "pbs",
            "--tag=abc"
        ])
        assert tag == "abc"
