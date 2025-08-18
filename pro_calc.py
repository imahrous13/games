import tkinter as tk
import math


class ProCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("360x520")
        self.root.resizable(False, False)

        self.expression = ""

        # ---- Display ----
        self.input_text = tk.StringVar()
        display = tk.Entry(
            root,
            textvariable=self.input_text,
            font=("Arial", 24),
            bd=10,
            relief=tk.FLAT,
            bg="#222",
            fg="white",
            justify="right",
        )
        display.pack(fill="both", ipadx=8, ipady=20, padx=10, pady=10)

        # ---- Buttons Layout ----
        btns = [
            ["C", "⌫", "√", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "%", "="],
        ]

        frame = tk.Frame(root, bg="#333")
        frame.pack(expand=True, fill="both")

        for r, row in enumerate(btns):
            for c, char in enumerate(row):
                b = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 20, "bold"),
                    bg=(
                        "#ff5c5c"
                        if char == "C"
                        else "#ff9f43"
                        if char == "⌫"
                        else "#4CAF50"
                        if char == "="
                        else "#444"
                    ),
                    fg="white",
                    bd=0,
                    relief=tk.FLAT,
                    command=lambda ch=char: self.on_click(ch),
                )
                b.grid(
                    row=r, column=c, sticky="nsew", padx=2, pady=2, ipadx=5, ipady=15
                )

        # Equal grid sizing
        for i in range(5):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i, weight=1)

        # Keyboard bindings
        root.bind("<Return>", lambda event: self.on_click("="))
        root.bind("<BackSpace>", lambda event: self.backspace())
        for key in "0123456789+-*/.%":
            root.bind(key, lambda event, k=key: self.on_click(k))

    def on_click(self, char):
        if char == "C":
            self.expression = ""
            self.input_text.set("")
        elif char == "⌫":
            self.backspace()
        elif char == "=":
            try:
                expr = (
                    self.expression.replace("÷", "/")
                    .replace("×", "*")
                    .replace("^", "**")
                    .replace("√", "math.sqrt")
                )
                result = str(eval(expr))
                self.input_text.set(result)
                self.expression = result
            except Exception:
                self.input_text.set("Error")
                self.expression = ""
        else:
            self.expression += str(char)
            self.input_text.set(self.expression)

    def backspace(self):
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)


# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = ProCalculator(root)
    root.mainloop()
