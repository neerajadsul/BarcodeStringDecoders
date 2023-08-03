from tkinter import *
from tkinter import ttk

import br_decoder
from scanner_comm import BarcodeScanner
from scanner_comm import populate_comports

SOFTWARE_VERSION = '0.1'


class BarcodeExtractorUI:
    def __init__(self, root, barcode_scanner=None):
        self.root = root
        self.scanner = barcode_scanner
        self.decoder = br_decoder.Decoder()
        self.root.title("DigiKey Barcode Data")

        mainframe = ttk.Frame(self.root, padding="2 2 10 10")
        mainframe.grid(column=2, row=5, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text='Scanner COM Port').grid(column=0, row=0)
        ttk.Label(mainframe, text='Part ID').grid(column=0, row=1)
        ttk.Label(mainframe, text='MFG Part ID').grid(column=0, row=2)
        ttk.Label(mainframe, text='Quantity').grid(column=0, row=3)
        ttk.Label(mainframe, text=f'v.{SOFTWARE_VERSION}').grid(column=0, row=4)
        ttk.Label(mainframe, text=' Press Enter or click Scan Barcode button.').grid(column=0, row=4, columnspan=2, sticky=(E))

        comport_choice = ttk.Combobox(mainframe, width=30)
        comport_choice.state(['readonly'])
        comport_choice['values'] = (self.scanner.comport,)
        comport_choice.current(0)
        comport_choice.grid(column=1, row=0)

        self.part_id = StringVar()
        self.mfg_part_id = StringVar()
        self.quantity = IntVar()

        ttk.Entry(mainframe, textvariable=self.part_id, width=50).grid(column=1, row=1)
        ttk.Entry(mainframe, textvariable=self.mfg_part_id, width=50).grid(column=1, row=2)
        ttk.Entry(mainframe, textvariable=self.quantity, width=10).grid(column=1, row=3)

        scan_button = ttk.Button(mainframe, text="Scan Barcode", command=self.barcode_data,)
        scan_button.grid(column=3, row=4, columnspan=2)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        comport_choice.focus()
        root.bind("<Return>", self.barcode_data)

    def barcode_data(self, *args):
        bdata = self.scanner.scan(wait_time=3)
        part_id, mfg_part_id, quantity = self.decoder.decode(bdata)
        self.part_id.set(part_id)
        self.mfg_part_id.set(mfg_part_id)
        self.quantity.set(quantity)

        self.copy_to_clipboard(part_id)

    def copy_to_clipboard(self, data):
        self.root.clipboard_clear()
        self.root.clipboard_append(data)


if __name__ == '__main__':
    root = Tk()
    comports = populate_comports()
    if len(comports) < 1:
        raise Exception("No barcode scanner is connected")
    scanner = BarcodeScanner(comports[0].device)
    BarcodeExtractorUI(root, barcode_scanner=scanner)
    root.mainloop()
