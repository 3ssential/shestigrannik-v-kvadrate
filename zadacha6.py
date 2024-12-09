import matplotlib.pyplot as plt
import csv
import os
import pandas as pd
from shestigrannikvkvadrate6 import ShestigrannikVKvadrate

# Константы
VOLUME = 100
H_values = [i for i in range(1, 21)]  # Шаги для H
c_values = [0.3, 0.35, 0.4]  # Значения коэффициентов c

# Подготовка папки для сохранения
output_folder = "results"
os.makedirs(output_folder, exist_ok=True)

# Данные для графиков и сохранения
R_curves = []
F_curves = []
results = []

for c in c_values:
    R_curve = []
    F_curve = []
    for H in H_values:
        reservuar = ShestigrannikVKvadrate(material="Сталь_ХВГ", emkost=VOLUME, koeffC=c)
        reservuar.H = H  # Устанавливаем H напрямую
        reservuar.R = (VOLUME / (H * (3**0.5) / 2)) ** (1 / 2)  # Рассчитываем R напрямую
        R_curve.append(reservuar.R)
        F_curve.append(2 * (3**0.5 / 4 * (reservuar.R**2)) + 6 * reservuar.R * reservuar.H)  # Вычисляем F
    R_curves.append(R_curve)
    F_curves.append(F_curve)
    results.append({
        "c": c,
        "H_values": H_values,
        "R_values": R_curve,
        "F_values": F_curve,
    })

# Сохранение в текстовый файл
txt_file = os.path.join(output_folder, "results.txt")
with open(txt_file, "w") as file:
    for result in results:
        file.write(f"c = {result['c']}\n")
        file.write("H_values: " + ", ".join(map(str, result["H_values"])) + "\n")
        file.write("R_values: " + ", ".join(map(str, result["R_values"])) + "\n")
        file.write("F_values: " + ", ".join(map(str, result["F_values"])) + "\n")
        file.write("\n")

# Сохранение в CSV
csv_file = os.path.join(output_folder, "results.csv")
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["c", "H", "R", "F"])
    for result in results:
        for H, R, F in zip(result["H_values"], result["R_values"], result["F_values"]):
            writer.writerow([result["c"], H, R, F])

# Сохранение в Excel
excel_file = os.path.join(output_folder, "results.xlsx")
df_data = []
for result in results:
    for H, R, F in zip(result["H_values"], result["R_values"], result["F_values"]):
        df_data.append({"c": result["c"], "H": H, "R": R, "F": F})
df = pd.DataFrame(df_data)
df.to_excel(excel_file, index=False)

# Построение графиков
fig, axes = plt.subplots(len(c_values), 1, figsize=(8, 15), sharex=True)

for idx, c in enumerate(c_values):
    axes[idx].plot(H_values, R_curves[idx], label=f"R(H), c={c}")
    axes[idx].plot(H_values, F_curves[idx], label=f"F(H), c={c}")
    axes[idx].set_title(f"Зависимости R(H) и F(H) для c={c}")
    axes[idx].set_xlabel("H")
    axes[idx].set_ylabel("Значения")
    axes[idx].legend()
    axes[idx].grid()

plt.tight_layout()
jpg_file = os.path.join(output_folder, "curves_separated.jpg")
plt.savefig(jpg_file)
plt.show()
