"""A compact, button-driven desktop Sudoku game built with tkinter."""

import tkinter as tk
from tkinter import messagebox


# An easy puzzle: it has many pre-filled numbers, while still leaving spaces to play.
PUZZLE = [
    [5, 3, 4, 0, 7, 8, 9, 0, 2],
    [6, 7, 0, 1, 9, 5, 0, 4, 8],
    [1, 9, 8, 3, 0, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 0, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 0, 1],
    [7, 1, 3, 0, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

GIVEN_BACKGROUND = "#d9e7f5"
CELL_BACKGROUND = "#ffffff"
SELECTED_CELL_BACKGROUND = "#d9f0ff"
ERROR_BACKGROUND = "#f8c7c7"
NUMBER_BACKGROUND = "#e8eef5"
SELECTED_NUMBER_BACKGROUND = "#1976d2"


class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.resizable(False, False)
        self.selected_number = None
        self.cells = []
        self.given_cells = set()
        self._build_interface()

    def _build_interface(self):
        tk.Label(self, text="Sudoku", font=("Arial", 18, "bold"), pady=6).pack()
        self.help_text = tk.Label(
            self,
            text="เลือกเลขด้านล่าง แล้วคลิกช่องว่างที่ต้องการเติม",
            font=("Arial", 10),
        )
        self.help_text.pack(pady=(0, 6))

        board = tk.Frame(self, padx=8, pady=4)
        board.pack()
        for row in range(9):
            row_cells = []
            for column in range(9):
                value = PUZZLE[row][column]
                cell = tk.Button(
                    board,
                    text=str(value) if value else "",
                    width=2,
                    height=1,
                    font=("Arial", 13, "bold"),
                    relief="solid",
                    bd=1,
                    activebackground=SELECTED_CELL_BACKGROUND,
                    cursor="hand2" if not value else "arrow",
                    command=lambda r=row, c=column: self.fill_cell(r, c),
                )
                cell.grid(
                    row=row,
                    column=column,
                    ipadx=2,
                    ipady=2,
                    padx=(2 if column % 3 == 0 else 0, 2 if column % 3 == 2 else 0),
                    pady=(2 if row % 3 == 0 else 0, 2 if row % 3 == 2 else 0),
                )
                if value:
                    cell.configure(bg=GIVEN_BACKGROUND, activebackground=GIVEN_BACKGROUND)
                    self.given_cells.add((row, column))
                else:
                    cell.configure(bg=CELL_BACKGROUND)
                row_cells.append(cell)
            self.cells.append(row_cells)

        tk.Button(
            self,
            text="Done — ตรวจคำตอบ",
            command=self.check_board,
            font=("Arial", 11, "bold"),
            bg="#2e7d32",
            fg="white",
            activebackground="#1b5e20",
            activeforeground="white",
            padx=12,
            pady=4,
            cursor="hand2",
        ).pack(pady=(8, 6))

        tk.Label(self, text="เลือกตัวเลขที่จะเติม", font=("Arial", 10, "bold")).pack()
        number_pad = tk.Frame(self, padx=8, pady=4)
        number_pad.pack(pady=(0, 8))
        self.number_buttons = {}
        for number in range(1, 10):
            button = tk.Button(
                number_pad,
                text=str(number),
                width=2,
                font=("Arial", 12, "bold"),
                bg=NUMBER_BACKGROUND,
                activebackground=SELECTED_NUMBER_BACKGROUND,
                command=lambda n=number: self.select_number(n),
                cursor="hand2",
            )
            button.grid(row=0, column=number - 1, padx=2, ipady=2)
            self.number_buttons[number] = button

    def select_number(self, number):
        self.selected_number = number
        for button_number, button in self.number_buttons.items():
            if button_number == number:
                button.configure(bg=SELECTED_NUMBER_BACKGROUND, fg="white")
            else:
                button.configure(bg=NUMBER_BACKGROUND, fg="black")
        self.help_text.configure(text=f"เลือกเลข {number} แล้ว — คลิกช่องว่างที่ต้องการเติม")

    def fill_cell(self, row, column):
        if (row, column) in self.given_cells:
            return
        if self.selected_number is None:
            self.help_text.configure(text="กรุณาเลือกเลข 1–9 ด้านล่างก่อน")
            return
        self.cells[row][column].configure(text=str(self.selected_number), bg=SELECTED_CELL_BACKGROUND)

    def _read_board(self):
        return [[cell.cget("text") for cell in row] for row in self.cells]

    def _reset_player_cell_colors(self):
        for row in range(9):
            for column in range(9):
                if (row, column) not in self.given_cells:
                    self.cells[row][column].configure(bg=CELL_BACKGROUND)

    def check_board(self):
        board = self._read_board()
        self._reset_player_cell_colors()
        valid_numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        empty_cells = [
            (row, column)
            for row in range(9)
            for column in range(9)
            if board[row][column] not in valid_numbers
        ]
        if empty_cells:
            for row, column in empty_cells:
                self.cells[row][column].configure(bg=ERROR_BACKGROUND)
            messagebox.showwarning("ยังไม่ครบ", "กรุณากรอกเลข 1–9 ให้ครบทุกช่องก่อนกด Done")
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
                self.cells[row][column].configure(bg=ERROR_BACKGROUND)
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