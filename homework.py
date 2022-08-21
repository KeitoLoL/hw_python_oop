from dataclasses import asdict, dataclass
from typing import ClassVar, Dict


def hours_to_minits(hours: int) -> int:
    """Функция переводящая часы в минуты"""
    return hours * 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = (
                            'Тип тренировки: {training_type}; '
                            'Длительность: {duration:.3f} ч.; '
                            'Дистанция: {distance:.3f} км; '
                            'Ср. скорость: {speed:.3f} км/ч; '
                            'Потрачено ккал: {calories:.3f}.'
                             )

    def get_message(self) -> str:
        dict = asdict(self)
        return self.MESSAGE.format(**dict)


class Training:
    """Базовый класс тренировки. Принимает на вход количество шагов в штуках,
       длительность активности в часах и вес в киллограммах"""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(
                self,
                action: int,
                duration: float,
                weight: float,
                ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
                'Определите run в %s.' % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
                           self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег. Принимает на вход количество шагов в штуках,
       длительность активности в часах и вес в киллограммах"""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight
                / self.M_IN_KM * hours_to_minits(self.duration))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба. Принимает на вход количество
       шагов в штуках, длительность активности в часах
       и вес в киллограммах и рост в сантимметрах"""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029

    def __init__(
                self,
                action: int,
                duration: float,
                weight: float,
                height: float
                ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.weight + (self.get_mean_speed()
                ** 2 // self.height) * self.COEFF_CALORIE_2 * self.weight)
                * hours_to_minits(self.duration))


class Swimming(Training):
    """Тренировка: плавание. Принимает на вход количество
       шагов в штуках, длительность активности в часах
       и вес в киллограммах, длинну бассейна в метрах
       и колличество проплытых бассейнов в штуках"""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(
                self,
                action: int,
                duration: float,
                weight: float,
                length_pool: float,
                count_pool: int
                ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:

        """Получить среднюю скорость движения."""
        return ((self.length_pool * self.count_pool
                / self.M_IN_KM) / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.COEFF_CALORIE_1)
                * self.COEFF_CALORIE_2 * self.weight)


def read_package(workout_type: str, data: int) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: Dict[str, type[Training]] = {
                                                "SWM": Swimming,
                                                "RUN": Running,
                                                "WLK": SportsWalking
                                                }
    if workout_type not in training_dict:
        return print("Неправильные входные аргументы")
    else:
        return training_dict[workout_type](*data)


def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
