def splitbytes_at(bdata: bytes, splitter=b'\x1d'):
    data = []
    split_start = 0
    split_end = 0
    for idx, byte in enumerate(bdata):
        if byte.to_bytes(length=1, byteorder='big') == splitter:
            split_end = idx
            data.append(bdata[split_start+1: split_end].decode())
            split_start = split_end
    return data


class Decoder():
    """Decoder for DigiKey product barcode on a shipped package."""
    MIN_LENGTH = 30
    MIN_FIELDS = 4

    PART_PREFIX = "P"
    MFG_PART_PREFIX = "1P"
    QUANTITY_PREFIX = "Q"

    def __init__(self) -> None:
        pass

    def decode(self, sdata, split_at='\x1d'):
        """Decode DigiKey barcode and return field values."""
        if len(sdata) < self.MIN_LENGTH:
            raise ValueError(f"Invalid barcode string: {sdata} .")

        fields = list()
        if type(sdata) == bytes:
            fields = splitbytes_at(sdata, splitter=b'\x1d')
        elif type(sdata) == str:
            fields = sdata.split('.')

        num_fields = len(fields)
        if num_fields < self.MIN_FIELDS:
            raise ValueError(f"Invalid barcode string, at least {self.MIN_FIELDS} expected, got {num_fields}.")

        part_id, mfg_part_id, quantity = ("", "", 0)

        for field in fields:
            field = field.strip()
            if field.startswith(self.PART_PREFIX):
                part_id = field[len(self.PART_PREFIX):]
                continue
            if field.startswith(self.MFG_PART_PREFIX):
                mfg_part_id = field[len(self.MFG_PART_PREFIX):]
                continue
            if field.startswith(self.QUANTITY_PREFIX):
                quantity = int(field[len(self.QUANTITY_PREFIX):])
                continue

        return part_id, mfg_part_id, quantity
