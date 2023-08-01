import pytest

from . import br_decoder


class TestBarcodeStringExtraction():
    """Verify extraction of field values with sample data from previous orders."""


    barcode_data = [
        b"[)>06\x1dP4463-D1CPC0306QR050FF-T50CT-ND\x1d1PD1CPC0306QR050FF-T50\x1dK202301100001\x1d1K79514818"
        b"\x1d10K94852328\x1d11K1\x1d4LCN\x1dQ10\x1d11ZPICK\x1d12Z16735650\x1d13Z924360\x1d20Z0000000000000",  # noqa: E702
        b"[)>06\x1dP160-1350-5-ND\x1d1PLTV-814H\x1dK6666190045\x1d1K59394301\x1d10K67935666\x1d11K1\x1d4LTH"
        b"\x1dQ4\x1d11ZPICK\x1d12Z385820\x1d13Z194779\x1d20Z000000000000",  # noqa: E702
        b"[)>06\x1dP36-783-C-ND\x1d1P783-C\x1dK202301100001\x1d1K79514818\x1d10K94852328\x1d11K1\x1d4LUS\x1dQ1"
        b"\x1d11ZPICK\x1d12Z4499466\x1d13Z924361\x1d20Z00000000000000",  # noqa: E702
        b"[)>06\x1dP3191-S14CT-ND\x1d1PS14\x1d30P3191-S14CT-ND\x1dK202307210001\x1d1K82398896\x1d10K98878108"
        b"\x1d9D2307\x1d1TBA030123021303300\x1d11K1\x1d4LCN\x1dQ100\x1d11ZPICK\x1d12Z13913090"
        b"\x1d13Z999999\x1d20Z0000000000",  # noqa: E702
        b"[)>06\x1dP1292-WR06X221JTLCT-ND\x1d1PWR06X221 JTL\x1d30P1292-WR06X221JTLCT-ND\x1dK202307210001"
        b"\x1d1K82398896\x1d10K98878108\x1d9D\x1d1T128977\x1d11K1\x1d4LCN\x1dQ478\x1d11ZPICK\x1d12Z13242498"
        b"\x1d13Z999999\x1d20Z000000000000",  # noqa: E702
        b"[)>06\x1dP2648-SC0889-ND\x1d1PSC0889\x1d30P2648-SC0889-ND\x1dK202307210001\x1d1K82398896"
        b"\x1d10K98878108\x1d9D08/02/2023\x1d1T\x1d11K1\x1d4LGB\x1dQ1\x1d11ZPICK\x1d12Z17877576"
        b"\x1d13Z999999\x1d20Z0000000000000",  # noqa: E702
    ]

    expected_prefix = ["P", "1P", "Q"]

    expected_fields = [
        ("4463-D1CPC0306QR050FF-T50CT-ND", "D1CPC0306QR050FF-T50", 10),
        ("160-1350-5-ND", "LTV-814H", 4),
        ("36-783-C-ND", "783-C", 1),
        ("3191-S14CT-ND", "S14", 100),
        ("1292-WR06X221JTLCT-ND", "WR06X221 JTL", 478),
        ("2648-SC0889-ND", "SC0889", 1),
    ]

    def test_string_extraction(self):
        """Test for correct extraction of field values."""
        decoder = br_decoder.Decoder()

        for idx, data in enumerate(self.barcode_data):
            assert decoder.decode(data) == self.expected_fields[idx]


class TestSplitBytesAt:
    def test_split_bytes_at(self):
        test_data = b']d1[)>\x1e06\x1dND\x1dPC03-T50\x1dK2023\x1d4LCN\x1dQ10\x1d20Z0000'
        expected = ['d1[)>\x1e06', 'ND', 'PC03-T50', 'K2023', '4LCN', 'Q10']
        actual = br_decoder.splitbytes_at(test_data, b'\x1d')
        assert expected == actual
