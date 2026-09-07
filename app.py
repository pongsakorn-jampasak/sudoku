"""A compact, button-driven desktop Sudoku game built with tkinter."""

import random
import tkinter as tk
from tkinter import messagebox


DIFFICULTIES = {
    "ง่าย": 30,
    "ปานกลาง": 45,
}

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
        self.puzzle = []
        self.current_difficulty = None
        self._show_difficulty_selection()

    def _clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _show_difficulty_selection(self):
        self._clear_window()
        tk.Label(self, text="Sudoku", font=("Arial", 18, "bold"), pady=10).pack()
        tk.Label(
            self,
            text="เลือกระดับความยากก่อนเริ่มเกม",
            font=("Arial", 11),
        ).pack(pady=(0, 10))
        choices = tk.Frame(self, padx=18, pady=4)
        choices.pack()
        tk.Button(
            choices,
            text="ง่าย\nช่องว่าง 30 ช่อง",
            command=lambda: self.start_game("ง่าย"),
            width=16,
            font=("Arial", 11, "bold"),
            bg="#d9e7f5",
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=4)
        tk.Button(
            choices,
            text="ปานกลาง\nช่องว่าง 45 ช่อง",
            command=lambda: self.start_game("ปานกลาง"),
            width=16,
            font=("Arial", 11, "bold"),
            bg="#e8eef5",
            pady=7,
            cursor="hand2",
        ).pack(side="left", padx=4)

    def start_game(self, difficulty):
        self.current_difficulty = difficulty
        self.puzzle = self._generate_puzzle(DIFFICULTIES[difficulty])
        self.selected_number = None
        self.cells = []
        self.given_cells = set()
        self._clear_window()
        self._build_interface()

    @staticmethod
    def _generate_puzzle(blank_count):
        """Create a valid Sudoku solution, then remove random positions."""
        row_order = [
            band * 3 + row
            for band in random.sample(range(3), 3)
            for row in random.sample(range(3), 3)
        ]
        column_order = [
            stack * 3 + column
            for stack in random.sample(range(3), 3)
            for column in random.sample(range(3), 3)
        ]
        numbers = random.sample(range(1, 10), 9)
        solution = [
            [
                numbers[(3 * (row % 3) + row // 3 + column) % 9]
                for column in column_order
            ]
            for row in row_order
        ]
        puzzle = [row[:] for row in solution]
        for position in random.sample(range(81), blank_count):
            puzzle[position // 9][position % 9] = 0
        return puzzle

    def _build_interface(self):
        tk.Label(
            self,
            text=f"Sudoku — ระดับ{self.current_difficulty}",
            font=("Arial", 18, "bold"),
            pady=6,
        ).pack()
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
                value = self.puzzle[row][column]
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

        actions = tk.Frame(self)
        actions.pack(pady=(8, 6))
        tk.Button(
            actions,
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
        ).pack(side="left", padx=3)
        tk.Button(
            actions,
            text="เริ่มเกมใหม่",
            command=self._show_difficulty_selection,
            font=("Arial", 11, "bold"),
            bg="#e8eef5",
            padx=10,
            pady=4,
            cursor="hand2",
        ).pack(side="left", padx=3)

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
