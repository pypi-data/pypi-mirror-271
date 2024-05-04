
from wgse.data.microarray_converter import MicroarrayConverterTarget
from wgse.microarray.microarray_line_formatter import TARGET_FORMATTER_MAP


def test_every_target_has_formatter():
    assert all(x in TARGET_FORMATTER_MAP for x in MicroarrayConverterTarget)