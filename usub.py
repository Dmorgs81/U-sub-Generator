import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sympy as sp
import random
import matplotlib.pyplot as plt
from io import BytesIO

def latex_to_image(latex_expr):
    plt.figure(figsize=(2, 0.5))  # Adjust figure size as needed
    plt.text(0.5, 0.5, f"${latex_expr}$", fontsize=20, horizontalalignment='center', verticalalignment='center')
    plt.axis('off')
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')  # Use bbox_inches='tight' for tight bounding box
    buffer.seek(0)
    image = Image.open(buffer)
    return ImageTk.PhotoImage(image)

def generate_problem():
    global integrand, correct_integral, choices, correct_index
    
    x = sp.symbols('x')
    
    # Generate a random polynomial u-substitution
    u_choices = [
        x**2 + 1,
        x**3 + 2,
        2*x + 3,
        x**2 - x + 1,
        sp.sin(x),
        sp.exp(x),
        sp.log(x + 1)
    ]
    u = random.choice(u_choices)
    
    # Generate a random integrand function
    integrand_functions = [
        lambda u, x: sp.sin(u) * sp.diff(u, x),
        lambda u, x: sp.cos(u) * sp.diff(u, x),
        lambda u, x: sp.exp(u) * sp.diff(u, x),
        lambda u, x: sp.log(u) * sp.diff(u, x),
        lambda u, x: sp.diff(u, x) / (u + 1),
        lambda u, x: sp.diff(u, x) * u,
        lambda u, x: sp.diff(u, x) * u**2,
        lambda u, x: sp.diff(u, x) / sp.sqrt(u)
    ]
    integrand_fn = random.choice(integrand_functions)
    integrand = integrand_fn(u, x)
    
    correct_integral = sp.integrate(integrand, x)
    problem_text = sp.latex(sp.Integral(integrand, x))
    problem_img = latex_to_image(problem_text)
    problem_label.config(image=problem_img)
    problem_label.image = problem_img
    
    # Generate multiple-choice options
    choices = generate_choices(correct_integral)
    
    # Update the buttons with the new choices
    for i, button in enumerate(choice_buttons):
        choice_img = latex_to_image(choices[i])
        button.config(image=choice_img, command=lambda i=i: check_answer(i))
        button.image = choice_img
        if choices[i] == sp.latex(correct_integral):
            correct_index = i

def generate_choices(correct_integral):
    choices = [correct_integral]
    x = sp.symbols('x')

    while len(choices) < 4:
        wrong_integral = correct_integral + sp.Rational(random.randint(-5, 5), random.randint(1, 3))
        if wrong_integral not in choices:
            choices.append(wrong_integral)

    random.shuffle(choices)
    return [sp.latex(choice) for choice in choices]

def check_answer(selected_choice):
    global correct_integral
    
    if selected_choice == correct_index:
        messagebox.showinfo("Result", "Correct! Well done.")
        generate_problem()  # Generate a new problem if the answer is correct
    else:
        messagebox.showerror("Result", f"Incorrect. The correct answer was: {sp.latex(correct_integral)}")

def main():
    global root, problem_label, choice_buttons, correct_index
    
    root = tk.Tk()
    root.title("U-substitution Practice")
    root.geometry("600x400")

    problem_label = tk.Label(root)
    problem_label.pack(pady=10)

    choice_buttons = []
    for i in range(4):
        button = tk.Button(root)
        button.pack(pady=5)
        choice_buttons.append(button)

    generate_button = tk.Button(root, text="Generate New Problem", command=generate_problem, font=("Helvetica", 12))
    generate_button.pack(pady=20)

    generate_problem()  # Generate the initial problem

    root.mainloop()

if __name__ == "__main__":
    main()
