import numpy as np
from scipy import optimize
import math

class ShestigrannikVKvadrate:
    def __init__(self, material, emkost, koeffC):
        self.material = material  # материал
        self.__emkost = emkost    # объём
        self.koeffC = koeffC      # коэффициент c
        self.R = None             # внешний размер R
        self.H = None             # высота H
        self.FF = None            # площадь поверхности

    @property
    def emkost(self):
        return self.__emkost

    def calculate_F(self, H):
        # Функция для вычисления площади поверхности F
        # Предположим, что площадь F пропорциональна H^2 (по аналогии с цилиндром)
        return math.pi * (self.R**2) + 4 * self.R * H

    def calculate_R(self):
        # Функция для вычисления оптимального R (внешнего размера)
        def target(H):
            # Функция для минимизации площади F по H
            self.R = self.calculate_R_for_H(H)  # вычисляем R для данной H
            return self.calculate_F(H)  # минимизируем площадь F

        # Начальное приближение для оптимизации
        H0 = self.__emkost ** (1 / 3)
        bounds = [(0.1, 100)]  # Ограничения на H
        result = optimize.minimize(target, H0, bounds=bounds)
        
        if result.success:
            self.H = result.x[0]  # Оптимальная высота
            self.R = self.calculate_R_for_H(self.H)  # Оптимальный R
            self.FF = self.calculate_F(self.H)  # Площадь поверхности F
            print(f"Оптимизация успешна! R: {self.R}, H: {self.H}, FF: {self.FF}")
        else:
            raise ValueError("Не удалось найти оптимальный R")

    def calculate_R_for_H(self, H):
        # Функция для вычисления внешнего размера R на основе H
        return (self.__emkost / (math.pi * H)) ** (1/3)

    def __str__(self):
        return f"Резервуар ({self.material}): R = {self.R}, H = {self.H}, F = {self.FF}"

# Пример создания объектов с различными параметрами
if __name__ == "__main__":
    reservuar1 = ShestigrannikVKvadrate("Сталь_ХВГ", 200, 0.35)
    reservuar2 = ShestigrannikVKvadrate("Титановый_Сплав", 300, 0.4)
    reservuar3 = ShestigrannikVKvadrate("Латунь", 150, 0.45)

    # Вычисляем оптимальные параметры для каждого резервуара
    reservuar1.calculate_R()
    reservuar2.calculate_R()
    reservuar3.calculate_R()

    print(reservuar1)
    print(reservuar2)
    print(reservuar3)
