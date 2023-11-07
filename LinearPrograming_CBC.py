from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable


def create_model():
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


# Nhập số lượng tham số
so_an = int(input("Nhập số lượng tham số: "))

# Nhập các hệ số của mục tiêu
objective_coefficients = [int(input(f"Nhập hệ số cho x{i}: ")) for i in range(1, so_an + 1)]

# Nhập số lượng ràng buộc
num_constraints = int(input("Nhập số lượng ràng buộc: "))

constraints = []
for i in range(num_constraints):
    coefficients = [int(val) for val in
                    input(f"Nhập các hệ số của ràng buộc {i + 1} (các số cách nhau bởi dấu cách): ").split()]
    rhs = int(input(f"Nhập giá trị bên phải của ràng buộc {i + 1}: "))
    name = input(f"Nhập tên của ràng buộc {i + 1}: ")
    constraints.append({'coefficients': coefficients, 'rhs': rhs, '' 'name': name})

# Tạo và giải mô hình
model, x = create_model()
status = model.solve()

# Lấy kết quả
print(f"status: {model.status}, {LpStatus[model.status]}")
print(f"objective: {model.objective.value()}")

for var in x.values():
    print(f"{var.name}: {var.value()}")

# for name, constraint in model.constraints.items():
#     print(f"{name}: {constraint.value()}")
