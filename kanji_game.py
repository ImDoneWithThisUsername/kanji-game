import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import random

class KanjiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Kanji Practice Game")
        self.root.geometry("400x300")
        
        # Initialize variables
        self.kanji_data = None
        self.current_pair = None
        self.remaining_pairs = []
        
        # Create UI elements
        self.setup_ui()
        
        # Start by asking for Excel file
        self.load_excel_file()

    def setup_ui(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Kanji display
        self.kanji_label = tk.Label(self.main_frame, text="", font=('Times New Roman', 36))
        self.kanji_label.pack(pady=10)
        
        # Meaning display
        self.meaning_label = tk.Label(self.main_frame, text="", font=('Times New Roman', 14))
        self.meaning_label.pack(pady=5)
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_field = tk.Entry(self.main_frame, textvariable=self.input_var, font=('Times New Roman', 14))
        self.input_field.pack(pady=10)
        self.input_field.bind('<Return>', lambda e: self.check_answer())
        self.input_field.config(state='normal')  # Ensure the input field is enabled
        self.input_field.focus_set()  # Give focus to the input field
        
        # Feedback label
        self.feedback_label = tk.Label(self.main_frame, text="", font=('Times New Roman', 12))
        self.feedback_label.pack(pady=10)
        
        # End button
        self.end_button = tk.Button(self.main_frame, text="End Game", command=self.end_game)
        self.end_button.pack(pady=10)

    def load_excel_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if file_path:
            try:
                # Read Excel file
                df = pd.read_excel(file_path)
                # Get three columns - column A (0) is romaji, column B (1) is kanji, column C (2) is meaning
                self.kanji_data = list(zip(df.iloc[:, 1], df.iloc[:, 0], df.iloc[:, 2]))
                self.reset_game()
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {str(e)}")
                self.root.quit()
        else:
            messagebox.showwarning("Warning", "No file selected. Game will close.")
            self.root.quit()

    def reset_game(self):
        self.remaining_pairs = self.kanji_data.copy()
        random.shuffle(self.remaining_pairs)
        self.show_next_kanji()

    def show_next_kanji(self):
        if self.remaining_pairs:
            self.current_pair = self.remaining_pairs.pop()
            self.kanji_label.config(text=self.current_pair[0])  # Kanji
            self.meaning_label.config(text=f"({self.current_pair[2]})")  # Meaning
            self.input_var.set("")
            self.feedback_label.config(text="")
            self.input_field.focus()
        else:
            self.kanji_label.config(text="Game Complete!")
            self.meaning_label.config(text="")
            self.input_field.config(state='disabled')

    def check_answer(self):
        user_answer = self.input_var.get().strip()
        correct_answer = self.current_pair[1].strip()
        
        if user_answer.lower() == correct_answer.lower():
            self.feedback_label.config(text="Correct!", fg="green")
            self.root.after(1000, self.show_next_kanji)
        else:
            self.feedback_label.config(text=f"Incorrect! Correct answer: {correct_answer}", fg="red")

    def end_game(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to end the game?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = KanjiGame(root)
    root.mainloop()

if __name__ == "__main__":
    main() 