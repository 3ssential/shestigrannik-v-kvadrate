class ShestigrannikVKvadrate:
    def __init__(self, material, emkost, koeffC):
        self.__material = material
        self.__emkost = emkost  # Приватный атрибут
        self.__koeffC = koeffC

    # Геттер для емкости
    def get_emkost(self):
        return self.__emkost

    # Геттер для коэффициента c
    def get_koeffC(self):
        return self.__koeffC

    # Геттер для материала
    def get_material(self):
        return self.__material

    def optimizaciya(self):
        # Оптимизация
        pass

    def __str__(self):
        return f"Резервуар: материал={self.__material}, объем={self.__emkost}, коэффициент c={self.__koeffC}"
