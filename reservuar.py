import math
from scipy import optimize

class ReservuarClass:
    def __init__(self, material, emkost, koeffC):
        self.material = material  # Материал
        self._emkost = emkost     # Объем (защищенный атрибут)
        self.koeffC = koeffC      # Коэффициент c
        self.optimized = False    # Флаг успешности оптимизации

    def __str__(self):
        return f"Резервуар (Материал: {self.material}, Объем: {self._emkost} м³, Коэффициент c: {self.koeffC})"

class ShestigrannikVKvadrate(ReservuarClass):
    def __init__(self, material, emkost, koeffC):
        super().__init__(material, emkost, koeffC)
        self._RR = None  # Внешний размер R
        self._HH = None  # Высота H

    # Метод для расчета оптимизированных параметров
    def optimizaciya(self):
        self.RaschetOptomParametrov()
        self.optimized = True  # Устанавливаем флаг успешной оптимизации

    def RaschetOptomParametrov(self):
        """
        Расчет оптимальных параметров для резервуара
        """
        def target(H):
            """
            Целевая функция для оптимизации
            """
            R = self.RaschetR(H)
            return self.FF_func(H, R)

        # Начальное приближение для высоты
        H0 = self._emkost ** (1 / 3)
        result = optimize.minimize(target, H0, bounds=[(0.1, 100)])

        if result.success:
            self._HH = result.x[0]
            self._RR = self.RaschetR(self._HH)
        else:
            raise ValueError("Оптимизация не удалась.")

    def RaschetR(self, H):
        """
        Расчет внешнего размера R
        """
        return (self._emkost / (math.pi * H)) ** (1 / 2)

    def FF_func(self, H, R):
        """
        Функция для расчета значения FF (например, поверхности или других параметров)
        """
        return math.pi * R * (R + H)  # Примерный расчет площади

    @property
    def RR(self):
        """
        Возвращает внешний размер R, если оптимизация успешна
        """
        if not self.optimized:
            raise ValueError("Резервуар не оптимизирован")
        return self._RR

    @property
    def HH(self):
        """
        Возвращает высоту H, если оптимизация успешна
        """
        if not self.optimized:
            raise ValueError("Резервуар не оптимизирован")
        return self._HH
