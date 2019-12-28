import unittest

from TB.TBApi.TBApiErrors import TBApiErrors

class Test_TBApiErrors(unittest.TestCase):
    """Тестирование класса TBApiErrors"""

    __apiErrors = TBApiErrors()

    def test_TBApiErrors(self):
        """
        Проверяет получение ошибки по её коду.
        Достаточно проверить лишь несколько кодов ошибок.
        """
        self.assertTrue(self.__apiErrors.getErrorDescription(0)  == 'Неизвестная ошибка')
        self.assertTrue(self.__apiErrors.getErrorDescription(-1) == self.__apiErrors.getErrorDescription(TBApiErrors.NOT_ANOUGHT_CURRENCY_FOR_BUY))
        self.assertTrue(self.__apiErrors.getErrorDescription(-2) == self.__apiErrors.getErrorDescription(TBApiErrors.NOT_ANOUGHT_CURRENCY_FOR_SALE))
        self.assertTrue(self.__apiErrors.getErrorDescription(-3) == self.__apiErrors.getErrorDescription(TBApiErrors.UNEXISTANCE_CURRENCY_PAIR))
        self.assertTrue(self.__apiErrors.getErrorDescription(-4) == self.__apiErrors.getErrorDescription(TBApiErrors.UNEXISTANCE_CURRENCY))

if __name__ == '__main__':
    unittest.main()