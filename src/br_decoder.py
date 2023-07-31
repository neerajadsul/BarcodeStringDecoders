class Decoder():
    "Decoder for DigiKey product barcode on a shipped package."
    MIN_LENGTH = 30
    MIN_FIELDS = 4

    def __init__(self) -> None:
        pass

    def decode(self, sdata):
        "Decode DigiKey barcode and return field values."
        if len(sdata) < self.MIN_LENGTH:
            raise ValueError(f"Invalid barcode string: {sdata} .")
        
        s = sdata.split('.')
        num_fields = len(s)
        if num_fields < self.MIN_FIELDS:
            raise ValueError(f"Invalid barcode string, at least {self.MIN_FIELDS} expected, got {num_fields}.")
        
        part_number = ""
        mfg_part_number = ""
        quantity = 0

        return part_number, mfg_part_number, quantity