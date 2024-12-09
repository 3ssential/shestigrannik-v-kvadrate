import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

class Subscriptable(type):
    """MetaClass for subscriptable class."""
    def __getitem__(cls, k):
        return cls.items[k]

class ReservuarClass(metaclass=Subscriptable):
    items = []

    def __init__(self, material, emkost, koeffC):
        self.material = material
        self.__emkost = emkost
        self.__koeffC = koeffC
        self.__RR = 0.0  # Initial outer size
        self.__HH = 0.0  # Initial height
        self.__FF = 0.0  # Initial surface area
        ReservuarClass.items.append(self)

    @property
    def emkost(self):
        return self.__emkost

    @property
    def koeffC(self):
        return self.__koeffC

    @property
    def HH(self):
        if self.__HH == 0:
            raise ValueError("Резервуар не оптимизирован")
        return self.__HH

    @property
    def RR(self):
        if self.__RR == 0:
            raise ValueError("Резервуар не оптимизирован")
        return self.__RR

    @property
    def FF(self):
        if self.__FF == 0:
            raise ValueError("Резервуар не оптимизирован")
        return self.__FF

    def Fpoverchnosti(self, H):
        """Abstract method for surface area."""
        raise NotImplementedError

    def Rfi(self, H):
        """Abstract method for outer size."""
        raise NotImplementedError

    def RaschetOptomParametrov(self):
        """Расчет оптимальных параметров"""
        H0 = self.emkost ** (1 / 3)
        print(f"Начальное приближение H0: {H0}")

        def target(H):
            R = self.Rfi(H)
            FF = self.Fpoverchnosti(H)
            return FF

        result = opt.minimize(target, H0, bounds=[(0.1, 100)])
        if not result.success:
            raise Exception("Оптимизация не удалась!")

        H_opt = result.x[0]
        R_opt = self.Rfi(H_opt)
        FF_opt = self.Fpoverchnosti(H_opt)

        # Устанавливаем значения
        self._update_optimized_parameters(H_opt, R_opt, FF_opt)

    def _update_optimized_parameters(self, H, R, FF):
        """Update optimized parameters."""
        self.__HH = H
        self.__RR = R
        self.__FF = FF
        print(f"Обновленные параметры: H={H}, R={R}, FF={FF}")

    def optimizaciya(self):
        """Основной метод для вызова оптимизации"""
        self.RaschetOptomParametrov()


class ShestigrannikVKvadrate(ReservuarClass):
    def Fpoverchnosti(self, H):
        """Calculate surface area given height H."""
        R = self.Rfi(H)
        # Площадь боковой поверхности и основания
        side_area = 6 * R * H
        base_area = 3 * np.sqrt(3) / 2 * (self.koeffC * R)**2
        return side_area + 2 * base_area

    def Rfi(self, H):
        """Calculate outer size R given height H."""
        return (self.emkost / (3 * np.sqrt(3) / 2 * (self.koeffC)**2 * H))**(1/3)

    def RaschetOptomParametrov(self):
        """Расчет оптимальных параметров"""
        H0 =  self.emkost ** (1 / 3)
        print(f"Начальное приближение H0: {H0}")

        def target(H):
            R = self.Rfi(H)
            FF = self.Fpoverchnosti(H)
            return FF

        result = opt.minimize(target, H0, bounds=[(0.1, 100)])
        if not result.success:
            raise Exception("Оптимизация не удалась!")

        H_opt = result.x[0]
        R_opt = self.Rfi(H_opt)
        FF_opt = self.Fpoverchnosti(H_opt)

        # Устанавливаем значения
        self._update_optimized_parameters(H_opt, R_opt, FF_opt)

    def optimizaciya(self):
        """Основной метод для вызова оптимизации"""
        self.RaschetOptomParametrov()


# Демонстрация работы
if __name__ == "__main__":
    # Исходные параметры
    material = "Титановый_Сплав_Т12"
    V = 200  # объем резервуара
    c = 0.35  # коэффициент отношения

    # Пример использования:
    reservuar = ShestigrannikVKvadrate(material, V, c)

    # Проверяем начальные параметры
    H_test = 5.0
    try:
        R_test = reservuar.Rfi(H_test)
        FF_test = reservuar.Fpoverchnosti(H_test)
        print(f"Test H: {H_test}, R: {R_test}, FF: {FF_test}")
    except Exception as e:
        print(f"Error during manual test: {e}")

    # Вызов метода оптимизации:
    reservuar.optimizaciya()

    # Вывод оптимальных параметров
    try:
        print(f"Материал: {reservuar.material}")
        print(f"Объем: {reservuar.emkost} м³")
        print(f"Коэффициент c: {reservuar.koeffC}")
        print(f"Оптимальный внешний размер R: {reservuar.RR}")
        print(f"Оптимальная высота H: {reservuar.HH}")
        print(f"Минимальная площадь поверхности FF: {reservuar.FF}")
    except ValueError as e:
        print(e)
