from shestigrannikvkvadrate5 import ShestigrannikVKvadrate  # Импортируем класс

# Создание списка объектов
reservuars = [
    ShestigrannikVKvadrate(material="Сталь_ХВГ", emkost=200, koeffC=0.35),
    ShestigrannikVKvadrate(material="Титановый_Сплав_Т12", emkost=150, koeffC=0.30),
    ShestigrannikVKvadrate(material="Латунь_113", emkost=250, koeffC=0.45),
    ShestigrannikVKvadrate(material="Алюминиевый_Сплав_А231", emkost=180, koeffC=0.25),
    ShestigrannikVKvadrate(material="Полимерный_Композит_ПК_421", emkost=220, koeffC=0.40)
]

# Сортировка по объему (emkost)
sorted_by_volume = sorted(reservuars, key=lambda r: r.get_emkost())
print("Сортировка по объему (emkost):")
for reservuar in sorted_by_volume:
    print(reservuar)

# Сортировка по коэффициенту c
sorted_by_koeffC = sorted(reservuars, key=lambda r: r.get_koeffC())
print("\nСортировка по коэффициенту c:")
for reservuar in sorted_by_koeffC:
    print(reservuar)

# Сортировка по материалу
sorted_by_material = sorted(reservuars, key=lambda r: r.get_material())
print("\nСортировка по материалу:")
for reservuar in sorted_by_material:
    print(reservuar)
