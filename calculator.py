import tkinter as tk
from tkinter import messagebox
import math


# Calculator operations
def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    return "Error! Division by zero." if y == 0 else x / y


def modulus(x, y):
    return "Error! Division by zero." if y == 0 else x % y


def power(x, y):
    return x**y


def floor_div(x, y):
    return "Error! Division by zero." if y == 0 else x // y


def square_root(x):
    return "Error! Negative number." if x < 0 else math.sqrt(x)


# Function to handle button clicks
def calculate(operation):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get()) if entry2.get() else None

        if operation == "+":
            result = add(num1, num2)
        elif operation == "-":
            result = subtract(num1, num2)
        elif operation == "×":
            result = multiply(num1, num2)
        elif operation == "÷":
            result = divide(num1, num2)
        elif operation == "%":
            result = modulus(num1, num2)
        elif operation == "^":
            result = power(num1, num2)
        elif operation == "//":
            result = floor_div(num1, num2)
        elif operation == "√":
            result = square_root(num1)

        label_result.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers.")


# GUI setup
root = tk.Tk()
root.title("Full Calculator")
root.geometry("350x400")
root.resizable(False, False)

# Input fields
tk.Label(root, text="Enter first number:").pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter second number (leave empty for √):").pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack()

# Buttons with all operators
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

operators = [["+", "-", "×"], ["÷", "%", "^"], ["//", "√"]]

for row in operators:
    row_frame = tk.Frame(btn_frame)
    row_frame.pack()
    for op in row:
        tk.Button(
            row_frame,
            text=op,
            width=8,
            height=2,
            font=("Arial", 12),
            command=lambda o=op: calculate(o),
        ).pack(side=tk.LEFT, padx=5, pady=5)

# Result display
label_result = tk.Label(root, text="Result: ", font=("Arial", 14, "bold"))
label_result.pack(pady=20)

# Run app
root.mainloop()
