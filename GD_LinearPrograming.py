import tkinter as tk
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
entry_objective_coefficients = []

def create_model(so_an, objective_coefficients, constraints):
    # Define the model
    model = LpProblem(name="Nhom11_LinearPrograming", sense=LpMaximize)

    # Define the decision variables
    x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, so_an + 1)}

    # Add constraints
    for i in range(len(constraints)):
        model += (
            lpSum(constraints[i]['coefficients'][j - 1] * x[j] for j in range(1, so_an + 1)) <= constraints[i]['rhs'],
            constraints[i]['name'])

    # Set the objective
    model += lpSum(objective_coefficients[i - 1] * x[i] for i in range(1, so_an + 1))

    return model, x

def update_grid():
    global num_rows, num_cols
    num_rows = int(entry_num_constraints.get())
    num_cols = int(entry_so_an.get())
    for widget in table_frame.winfo_children():
        widget.destroy()

    entry_coefficients.clear()
    entry_rhs.clear()

    for i in range(num_rows):
        row_entries = []
        for j in range(num_cols):
            entry = tk.Entry(table_frame, bg="white")
            entry.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
            row_entries.append(entry)
        entry_coefficients.append(row_entries)

        entry = tk.Entry(table_frame, bg="white")
        entry.grid(row=i, column=num_cols, padx=5, pady=5, sticky='nsew')
        entry_rhs.append(entry)

def show_constraints_input():
    num_objective_coefficients = int(entry_so_an.get())
    for widget in objective_coefficients_frame.winfo_children():
        widget.destroy()

    entry_objective_coefficients.clear()

    for i in range(num_objective_coefficients):
        label = tk.Label(objective_coefficients_frame, text=f"Hệ số x{i+1}:", bg="#d0f0c0")
        label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
        entry = tk.Entry(objective_coefficients_frame, bg="white")
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='nsew')
        entry_objective_coefficients.append(entry)

def calculate():
    try:
        # Lấy số lượng tham số và số lượng ràng buộc
        so_an = int(entry_so_an.get())
        num_constraints = int(entry_num_constraints.get())

        # Kiểm tra xem đã nhập đúng số lượng tham số và ràng buộc chưa
        if so_an <= 0 or num_constraints <= 0:
            raise ValueError

        # Tạo biến constraints
        constraints = []
        for i in range(num_constraints):
            coefficients = [int(entry_coefficients[i][j].get()) for j in range(so_an)]
            rhs = int(entry_rhs[i].get())
            name = f'Constraint {i+1}'
            constraints.append({'coefficients': coefficients, 'rhs': rhs, 'name': name})

        # Tính toán và hiển thị kết quả
        model, x = create_model(so_an, [int(e.get()) for e in entry_objective_coefficients], constraints)
        status = model.solve()

        # Hiển thị kết quả trong giao diện
        for i, var in enumerate(x.values()):
            tk.Label(table_frame, text=f"{var.name}:", bg="#d0f0c0").grid(row=num_rows+i, column=0, padx=5, pady=5, sticky='nsew')
            tk.Label(table_frame, text=f"{var.value()}", bg="white").grid(row=num_rows+i, column=1, padx=5, pady=5, sticky='nsew')

        # Hiển thị kết quả của hàm mục tiêu
        tk.Label(table_frame, text="Hàm mục tiêu:", bg="#d0f0c0").grid(row=num_rows+len(x), column=0, padx=5, pady=5, sticky='nsew')
        tk.Label(table_frame, text=f"{model.objective.value()}", bg="white").grid(row=num_rows+len(x), column=1, padx=5, pady=5, sticky='nsew')

    except ValueError:
        tk.messagebox.showerror("Lỗi", "Vui lòng nhập các giá trị hợp lệ.")

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("Giao diện tính toán")
root.configure(bg="#d0f0c0")

# Nhập số lượng tham số
label_so_an = tk.Label(root, text="Số lượng tham số:", bg="#d0f0c0")
label_so_an.grid(row=0, column=0, padx=5, pady=5)

entry_so_an = tk.Entry(root, bg="white")
entry_so_an.grid(row=0, column=1, padx=5, pady=5)

# Khung chứa hệ số của hàm mục tiêu
objective_coefficients_frame = tk.Frame(root, bg="#d0f0c0")
objective_coefficients_frame.grid(row=0, column=2, padx=5, pady=5)

# Nút hiển thị input hệ số của hàm mục tiêu
button_constraints_input = tk.Button(root, text="Nhập giá trị hàm mục tiêu", command=show_constraints_input, bg="#70ad47", fg="white")
button_constraints_input.grid(row=0, column=3, padx=5, pady=5)

# Nhập số lượng ràng buộc
label_num_constraints = tk.Label(root, text="Số lượng ràng buộc:", bg="#d0f0c0")
label_num_constraints.grid(row=1, column=0, padx=5, pady=5)

entry_num_constraints = tk.Entry(root, bg="white")
entry_num_constraints.grid(row=1, column=1, padx=5, pady=5)

# Khung chứa bảng
table_frame = tk.Frame(root, bg="#d0f0c0")
table_frame.grid(row=2, column=0, columnspan=4)

# Tạo grid ban đầu
num_rows, num_cols = 3, 3
entry_coefficients = []
entry_rhs = []
for i in range(num_rows):
    row_entries = []
    for j in range(num_cols):
        entry = tk.Entry(table_frame, bg="white")
        entry.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
        row_entries.append(entry)
    entry_coefficients.append(row_entries)

    entry = tk.Entry(table_frame, bg="white")
    entry.grid(row=i, column=num_cols, padx=5, pady=5, sticky='nsew')
    entry_rhs.append(entry)

# Tạo nút cập nhật grid
update_button = tk.Button(root, text="Ma trận ràng buôc", command=update_grid, bg="#70ad47", fg="white")
#update_button.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
update_button.grid(row=1, column=3, padx=5, pady=5)


# Tính toán và hiển thị kết quả
calculate_button = tk.Button(root, text="Tính", command=calculate, bg="#70ad47", fg="white")
calculate_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

# Chạy ứng dụng
root.mainloop()
