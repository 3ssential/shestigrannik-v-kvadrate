import reservuar

# Создаем объекты с разными параметрами
reservuar1 = reservuar.ShestigrannikVKvadrate(material="Сталь_ХВГ", emkost=200, koeffC=0.35)
reservuar2 = reservuar.ShestigrannikVKvadrate(material="Титановый_Сплав_Т12", emkost=250, koeffC=0.40)
reservuar3 = reservuar.ShestigrannikVKvadrate(material="Латунь_113", emkost=180, koeffC=0.30)

# Список для хранения объектов
reservuars = [reservuar1, reservuar2, reservuar3]

# Оптимизация и вывод информации для каждого объекта
for i, reservuar_obj in enumerate(reservuars, start=1):
    print(f"Резервуар {i}:")
    try:
        # Запуск оптимизации
        reservuar_obj.optimizaciya()
        
        # Вывод информации об объекте с помощью __str__()
        print(reservuar_obj)
        
        # Дополнительно выводим оптимизированные параметры
        print(f"Оптимальный внешний размер R: {reservuar_obj.RR}")
        print(f"Оптимальная высота H: {reservuar_obj.HH}")
        
    except ValueError as e:
        print(f"Ошибка при оптимизации: {e}")
    
    print()  # Для разделения выводов между объектами
