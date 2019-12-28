
class TBApiErrors:
    """Коды возможных ошибок при взаимодействии с API биржи"""

    @classmethod
    def __init__(cls):
        # Отрицательный счётчик ошибок
        cls.__errorsCounter = 0
        # Словарь с описаниями ошибок.
        cls.__ERROS_DESCRIPTION = {0 : 'Неизвестная ошибка'}
        # ошибки API
        cls.NOT_ANOUGHT_CURRENCY_FOR_BUY      = cls.__setErrorCode('количество валюты для покупки превосходит доступные резервы пользователя')
        cls.NOT_ANOUGHT_CURRENCY_FOR_SALE     = cls.__setErrorCode('количество валюты для продажи превосходит доступные резервы пользователя')
        cls.UNEXISTANCE_CURRENCY_PAIR         = cls.__setErrorCode('несуществующая валютная пара')
        cls.UNEXISTANCE_ORDER_ATTRIBUTE       = cls.__setErrorCode('несуществующий атрибут ордера')
        cls.UNEXISTANCE_CURRENCY              = cls.__setErrorCode('несуществующая валюта')
        cls.UNEXISTANCE_TRADE_RESTRICTED      = cls.__setErrorCode('несуществующее ограничени на реализацию (осуществеление) торгов')
        cls.UNEXISTANCE_USER_INFO             = cls.__setErrorCode('несуществующий ключ доступа к информации, идентифицирующей пользователя на бирже')
        cls.UNEXISTANCE_TYPE_ORDER_FROM       = cls.__setErrorCode('с биржи (по запросу) пришёл ордер не идентифицируемого типа')
        cls.UNEXISTANCE_TYPE_ORDER_TO         = cls.__setErrorCode('несуществующий тип ордера')
        cls.UNEXISTANCE_ORDER_ID              = cls.__setErrorCode('запрашиваемый идентификатор ордера не существует')
        cls.PURCHASE_PRICE_MORE_THAN_MARKET   = cls.__setErrorCode('цена покупки больше рыночной')
        cls.SELLING_PRICE_LESS_THAN_MARKET    = cls.__setErrorCode('цена продажи меньше рыночной')
        cls.UNAVALIBLE_MIN_QUANTITY_FOR_ORDER = cls.__setErrorCode('недопустимое минимально количестовалюты которое можно задействовать в ордере')
        cls.UNAVALIBLE_MAX_QUANTITY_FOR_ORDER = cls.__setErrorCode('недопустимое максимальное количество валюты которое можно задействовать в ордере')
        cls.UNAVALIBLE_MIN_AMOUNT_FOR_ORDER   = cls.__setErrorCode('недопустимая минимально возможная итоговая стоимость ордера')
        cls.UNAVALIBLE_MAX_AMOUNT_FOR_ORDER   = cls.__setErrorCode('недопустимая максимально возможная итоговая стоимость ордера')
        cls.UNAVALIBLE_MIN_PRICE_FOR_ORDER    = cls.__setErrorCode('недопустимая минимальная цена которую можно выставить за валюту в ордере')
        cls.UNAVALIBLE_MAX_PRICE_FOR_ORDER    = cls.__setErrorCode('недопустимая максимальная цена которую можно выставить за валюту в ордере')
        cls.CREATE_TEST_ORDER                 = cls.__setErrorCode('попытка создания тестового ордера')

    @classmethod
    def __setErrorCode(cls, description):
        """
        Фиксирует новый код ошибки, добавляя её код и описание в список известных словарь.
        @param description описание новой ошибки.
        @return код присвоенный новой ошибке.
        """
        cls.__errorsCounter -= 1
        cls.__ERROS_DESCRIPTION[cls.__errorsCounter] = description
        return cls.__errorsCounter

    @classmethod
    def getErrorDescription(cls, code):
        """
        Возвращает описание ошибки по её коду.
        @param code код ошибки, описание которой необходимо получить.
        @return описание ошибки, в случае, если код ошибки существует; 'Неизвестная ошибка' - в противном случае.
        """
        if code in cls.__ERROS_DESCRIPTION:
            return cls.__ERROS_DESCRIPTION[code]
        return cls.__ERROS_DESCRIPTION[0]

# Производим инициализацию кодов ошибки, прежде всех остальных действий.
TBApiErrors()