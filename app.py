"""A small desktop Sudoku game built with tkinter."""

import tkinter as tk
from tkinter import messagebox


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

CELL_SIZE = 42
GIVEN_BACKGROUND = "#d9e7f5"
ENTRY_BACKGROUND = "#ffffff"
ERROR_BACKGROUND = "#f8c7c7"


class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.resizable(False, False)
        self.entries = []
        self._build_interface()

    def _build_interface(self):
        tk.Label(
            self,
            text="Sudoku",
            font=("Arial", 20, "bold"),
            pady=10,
        ).pack()
        tk.Label(
            self,
            text="คลิกช่องว่างแล้วพิมพ์เลข 1–9 เมื่อครบแล้วกด Done",
            font=("Arial", 10),
        ).pack(pady=(0, 10))

        board = tk.Frame(self, padx=12, pady=4)
        board.pack()
        for row in range(9):
            row_entries = []
            for column in range(9):
                value = PUZZLE[row][column]
                entry = tk.Entry(
                    board,
                    width=2,
                    font=("Arial", 16, "bold"),
                    justify="center",
                    relief="solid",
                    bd=1,
                    highlightthickness=0,
                )
                entry.grid(
                    row=row,
                    column=column,
                    ipady=7,
                    padx=(2 if column % 3 == 0 else 0, 2 if column % 3 == 2 else 0),
                    pady=(2 if row % 3 == 0 else 0, 2 if row % 3 == 2 else 0),
                )
                if value:
                    entry.insert(0, str(value))
                    entry.configure(state="readonly", readonlybackground=GIVEN_BACKGROUND)
                else:
                    entry.configure(bg=ENTRY_BACKGROUND)
                    entry.bind("<KeyRelease>", self._limit_input)
                row_entries.append(entry)
            self.entries.append(row_entries)

        tk.Button(
            self,
            text="Done",
            command=self.check_board,
            font=("Arial", 12, "bold"),
            bg="#2e7d32",
            fg="white",
            activebackground="#1b5e20",
            activeforeground="white",
            padx=22,
            pady=7,
            cursor="hand2",
        ).pack(pady=14)

    def _limit_input(self, event):
        entry = event.widget
        value = entry.get()
        if len(value) > 1 or (value and value not in "123456789"):
            entry.delete(0, tk.END)
            if value and value[-1] in "123456789":
                entry.insert(0, value[-1])

    def _read_board(self):
        return [
            [entry.get().strip() for entry in row]
            for row in self.entries
        ]

    def check_board(self):
        board = self._read_board()
        for row in self.entries:
            for entry in row:
                if entry.cget("state") == "normal":
                    entry.configure(bg=ENTRY_BACKGROUND)

        empty_cells = [
            (row, column)
            for row in range(9)
            for column in range(9)
            if board[row][column] not in {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        ]
        if empty_cells:
            for row, column in empty_cells:
                self.entries[row][column].configure(bg=ERROR_BACKGROUND)
            messagebox.showwarning("ยังไม่ครบ", "กรุณากรอกเลข 1–9 ให้ครบทุกช่องก่อนกด Done")
            self.entries[empty_cells[0][0]][empty_cells[0][1]].focus_set()
            return

        errors = set()
        for index in range(9):
            self._mark_duplicates([(index, column) for column in range(9)], board, errors)
            self._mark_duplicates([(row, index) for row in range(9)], board, errors)
        for box_row in range(0, 9, 3):
            for box_column in range(0, 9, 3):
                cells = [
                    (row, column)
                    for row in range(box_row, box_row + 3)
                    for column in range(box_column, box_column + 3)
                ]
                self._mark_duplicates(cells, board, errors)

        if errors:
            for row, column in errors:
                self.entries[row][column].configure(bg=ERROR_BACKGROUND)
            messagebox.showerror(
                "ยังไม่ถูกต้อง",
                "พบเลขซ้ำในแถว คอลัมน์ หรือกล่อง 3×3\nช่องสีแดงคือช่องที่ต้องแก้ไข",
            )
        else:
            messagebox.showinfo("สำเร็จ!", "ถูกต้องตามกฎ Sudoku ทุกข้อ")

    @staticmethod
    def _mark_duplicates(cells, board, errors):
        locations_by_value = {}
        for row, column in cells:
            locations_by_value.setdefault(board[row][column], []).append((row, column))
        for locations in locations_by_value.values():
            if len(locations) > 1:
                errors.update(locations)


if __name__ == "__main__":
    SudokuApp().mainloop()
