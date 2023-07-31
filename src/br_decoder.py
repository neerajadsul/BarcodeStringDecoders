class Decoder():
    """Decoder for DigiKey product barcode on a shipped package."""
    MIN_LENGTH = 30
    MIN_FIELDS = 4

    PART_PREFIX = "P"
    MFG_PART_PREFIX = "1P"
    QUANTITY_PREFIX = "Q"

    def __init__(self) -> None:
        pass

    def decode(self, sdata):
        """Decode DigiKey barcode and return field values."""
        if len(sdata) < self.MIN_LENGTH:
            raise ValueError(f"Invalid barcode string: {sdata} .")

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
