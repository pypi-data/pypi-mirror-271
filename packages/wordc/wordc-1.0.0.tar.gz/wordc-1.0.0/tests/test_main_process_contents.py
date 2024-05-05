
from collections import Counter
from wordc import wordc


sample = """
the the the The th
Hi hi hI
"$%^&
"""


def test_process():
    words = wordc.process_contents(sample)
    assert words == Counter({'the': 4, 'hi': 3, 'th': 1})


