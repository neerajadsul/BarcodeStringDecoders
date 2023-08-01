from tkinter import *
from tkinter import ttk


class BarcodeExtractorUI:
    def __init__(self, root, barcode_scanner=None):
        self.scanner = barcode_scanner
        root.title("DigiKey Barcode Data")

        mainframe = ttk.Frame(root, padding="2 2 10 10")
        mainframe.grid(column=2, row=5, sticky=(N, W, E, S))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text='Scanner COM Port').grid(column=0, row=0)
        ttk.Label(mainframe, text='Part ID').grid(column=0, row=1)
        ttk.Label(mainframe, text='MFG Part ID').grid(column=0, row=2)
        ttk.Label(mainframe, text='Quantity').grid(column=0, row=3)

        self.comport = StringVar()
        comport_entry = ttk.Combobox(mainframe, width=10, textvariable=self.comport)
        comport_entry.grid(column=1, row=0)

        self.part_id = StringVar()
        self.mfg_part_id = StringVar()
        self.quantity = IntVar()

        ttk.Label(mainframe, textvariable=self.part_id).grid(column=1, row=1)
        ttk.Label(mainframe, textvariable=self.mfg_part_id).grid(column=1, row=2)
        ttk.Label(mainframe, textvariable=self.quantity).grid(column=1, row=3)

        scan_button = ttk.Button(mainframe, text="Scan Barcode", command=self.barcode_data)
        scan_button.grid(column=3, row=5, columnspan=2)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        comport_entry.focus()
        root.bind("<Return>", self.barcode_data)

    def barcode_data(self, *args):
        part_id = "R0805-ND"
        mfg_part_id = "R0805"
        quantity = 200
        self.part_id.set(part_id)
        self.mfg_part_id.set(mfg_part_id)
        self.quantity.set(quantity)


root = Tk()
BarcodeExtractorUI(root, barcode_scanner=None)
root.mainloop()
