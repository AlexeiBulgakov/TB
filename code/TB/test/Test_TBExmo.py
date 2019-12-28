import unittest
import random

from TBApi.TBCryptoExchange.TBExmo import TBExmo
from TBApi.TBApiErrors import TBApiErrors
from TBApi.TBApi import TradeRestricted, UserInfo, OrderAttributes
from Common.Common import *

class Test_TBExmo(unittest.TestCase):
    """Тестирование биржевого провайдера Exmo"""

    __exmo = TBExmo()

    def test_getAvalibleCurrency(self):
        """Тестирует функцию получения массива валют представленных на бирже Exmo"""
        self.assertTrue(len(self.__exmo.getAvalibleCurrency()) > 2)
        return True

    def test_getAvalibleCurrencyPair(self):
        """Тестирует функцию получения массива валютных пар представленных на бирже Exmo"""
        self.assertTrue(len(self.__exmo.getAvalibleCurrencyPair()) > 2)
        return True

    def test_getTradeRestricted(self):
        """Тестирование функции возвращащющую ограничения накладываемые биржей Exmo на торговлю"""
        def BadBehavior():
            """Проверка на ошибки"""
            self.assertTrue(TBApiErrors.UNEXISTANCE_CURRENCY_PAIR == self.__exmo.getTradeRestricted(pair='BTC_BTC'))
            self.assertTrue(TBApiErrors.UNEXISTANCE_CURRENCY_PAIR == self.__exmo.getTradeRestricted(pair=['BTC_USD', 'BTC_BTC']))
            self.assertTrue(TBApiErrors.UNEXISTANCE_CURRENCY_PAIR == self.__exmo.getTradeRestricted(pair=[TradeRestricted.MAX_AMOUNT, TradeRestricted.MIN_QUANTITY]))
            self.assertTrue(TBApiErrors.UNEXISTANCE_TRADE_RESTRICTED == self.__exmo.getTradeRestricted(restricted='MAX_PRICE_BTC'))
            self.assertTrue(TBApiErrors.UNEXISTANCE_TRADE_RESTRICTED == self.__exmo.getTradeRestricted(restricted=[TradeRestricted.MAX_AMOUNT, 'MAX_PRICE_BTC']))
            self.assertTrue(TBApiErrors.UNEXISTANCE_TRADE_RESTRICTED == self.__exmo.getTradeRestricted(restricted=['BTC_USD', 'XP_USD']))
            return True

        def NotPairAndNotRestricted():
            """{'p' : {'r' : num, 'r' : num, ...}, ...}"""
            allExmoTradeRestricted = self.__exmo.getTradeRestricted()
            self.assertTrue(len(allExmoTradeRestricted) == len(self.__exmo.getAvalibleCurrencyPair()))
            return True

        def NotPairAndManyRestricted():
            """{'p' : {'r' : num, 'r' : num}, ...}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(restricted=[TradeRestricted.MAX_AMOUNT, TradeRestricted.MIN_QUANTITY])
            for tradePair in result1.keys():
                self.assertTrue(tradePair in avalibleExmoCurrencyPair)
                self.assertTrue(len(result1[tradePair]) == 2)
                self.assertTrue(result1[tradePair][TradeRestricted.MAX_AMOUNT] == allExmoTradeRestricted[tradePair][TradeRestricted.MAX_AMOUNT])
                self.assertTrue(result1[tradePair][TradeRestricted.MIN_QUANTITY] == allExmoTradeRestricted[tradePair][TradeRestricted.MIN_QUANTITY])
            result2 = self.__exmo.getTradeRestricted(restricted=[TradeRestricted.MIN_PRICE])
            for tradePair in result2.keys():
                self.assertTrue(tradePair in avalibleExmoCurrencyPair)
                self.assertTrue(len(result2[tradePair]) == 1)
                self.assertTrue(result2[tradePair][TradeRestricted.MIN_PRICE] == allExmoTradeRestricted[tradePair][TradeRestricted.MIN_PRICE])
            return True

        def NotPairAndOneRestricted():
            """{'p' : num, 'p' : num, ...}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(restricted=TradeRestricted.MAX_AMOUNT)
            for tradePair in result1.keys():
                self.assertTrue(tradePair in avalibleExmoCurrencyPair)
                self.assertTrue(result1[tradePair] == allExmoTradeRestricted[tradePair][TradeRestricted.MAX_AMOUNT])
            return True

        def ManyPairAndNotRestricted():
            """{'p' : {'r' : num, 'r' : num, ...}, 'p' : {'r' : num, 'r' : num, ...}}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(pair=[avalibleExmoCurrencyPair[0], avalibleExmoCurrencyPair[1]])
            for tradePair in result1.keys():
                self.assertTrue(tradePair in avalibleExmoCurrencyPair)
                self.assertTrue(result1[tradePair] == allExmoTradeRestricted[tradePair])
            return True

        def ManyPairAndManyRestricted():
            """{'p' : {'r' : num, 'r' : num}, 'p' : {'r' : num, 'r' : num}}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(pair=[avalibleExmoCurrencyPair[0], avalibleExmoCurrencyPair[1]],
                                                     restricted=[TradeRestricted.MAX_AMOUNT, TradeRestricted.MIN_QUANTITY])
            for tradePair in result1.keys():
                self.assertTrue(tradePair in avalibleExmoCurrencyPair)
                self.assertTrue(len(result1[tradePair]) == 2)
                self.assertTrue(result1[tradePair][TradeRestricted.MAX_AMOUNT] == allExmoTradeRestricted[tradePair][TradeRestricted.MAX_AMOUNT])
                self.assertTrue(result1[tradePair][TradeRestricted.MIN_QUANTITY] == allExmoTradeRestricted[tradePair][TradeRestricted.MIN_QUANTITY])
            return True

        def ManyPairAndOneRestricted():
            """{'p' : num, 'p' : num, ...}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(pair=[avalibleExmoCurrencyPair[0], avalibleExmoCurrencyPair[1]],
                                                     restricted=TradeRestricted.MAX_AMOUNT)
            for tradePair in result1.keys():
                self.assertTrue(tradePair in avalibleExmoCurrencyPair)
                self.assertTrue(result1[tradePair] == allExmoTradeRestricted[tradePair][TradeRestricted.MAX_AMOUNT])
            return True

        def OnePairAndNotRestricted():
            """{'r' : num, 'r' : num, ...}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(pair=avalibleExmoCurrencyPair[0])
            self.assertTrue(result1 == allExmoTradeRestricted[avalibleExmoCurrencyPair[0]])
            return True

        def OnePairAndManyRestricted():
            """{'r' : num, 'r' : num}"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(pair=avalibleExmoCurrencyPair[0], restricted=[TradeRestricted.MAX_AMOUNT, TradeRestricted.MIN_QUANTITY])
            self.assertTrue(len(result1) == 2)
            self.assertTrue(result1[TradeRestricted.MAX_AMOUNT] == allExmoTradeRestricted[avalibleExmoCurrencyPair[0]][TradeRestricted.MAX_AMOUNT])
            self.assertTrue(result1[TradeRestricted.MIN_QUANTITY] == allExmoTradeRestricted[avalibleExmoCurrencyPair[0]][TradeRestricted.MIN_QUANTITY])
            return True

        def OnePairAndOneRestricted():
            """num"""
            nonlocal allExmoTradeRestricted
            nonlocal avalibleExmoCurrencyPair
            result1 = self.__exmo.getTradeRestricted(pair=avalibleExmoCurrencyPair[0], restricted=TradeRestricted.MAX_AMOUNT)
            self.assertTrue(result1 == allExmoTradeRestricted[avalibleExmoCurrencyPair[0]][TradeRestricted.MAX_AMOUNT])
            return True

        self.assertTrue(BadBehavior())
        allExmoTradeRestricted = self.__exmo.getTradeRestricted()
        avalibleExmoCurrencyPair = self.__exmo.getAvalibleCurrencyPair()
        self.assertTrue(NotPairAndNotRestricted())
        self.assertTrue(NotPairAndManyRestricted())
        self.assertTrue(NotPairAndOneRestricted())
        self.assertTrue(ManyPairAndNotRestricted())
        self.assertTrue(ManyPairAndManyRestricted())
        self.assertTrue(ManyPairAndOneRestricted())
        self.assertTrue(OnePairAndNotRestricted())
        self.assertTrue(OnePairAndManyRestricted())
        self.assertTrue(OnePairAndOneRestricted())
        return True

    def test_getUserInformation(self):
        """Тестирует функцию получения информации о пользователе биржи Exmo"""
        userInformation = self.__exmo.getUserInformation()
        self.assertTrue(len(userInformation) == 2)
        return True

    def test_getUserBalance(self):
        """Тестирует функцию предоставления информации о балансе пользователя"""
        def badBehavior():
            self.assertTrue(self.__exmo.getUserBalance(balance='XXX') == TBApiErrors.UNEXISTANCE_CURRENCY)
            self.assertTrue(self.__exmo.getUserBalance(balance=['XXX', 'YYY']) == TBApiErrors.UNEXISTANCE_CURRENCY)
            self.assertTrue(self.__exmo.getUserBalance(reserve='XXX') == TBApiErrors.UNEXISTANCE_CURRENCY)
            self.assertTrue(self.__exmo.getUserBalance(reserve=['XXX', 'YYY']) == TBApiErrors.UNEXISTANCE_CURRENCY)
            return True

        def notAnyRestricted():
            """{'BALANCE' : {'' : num, '' : num, ...}, 'RESERVE' : {'' : num, '' : num, ...}}"""
            nonlocal avalibleCurrency
            userBalance = self.__exmo.getUserBalance()
            self.assertTrue(len(userBalance) == 2)
            for currency in userBalance[UserInfo.BALANCE]:
                self.assertTrue(currency in avalibleCurrency)
                self.assertTrue(userBalance[UserInfo.BALANCE][currency] != 0)
                self.assertTrue(userBalance[UserInfo.BALANCE][currency] == self.__exmo.getCurrencyCountInAccess(currency))
            for currency in userBalance[UserInfo.RESERVE]:
                self.assertTrue(currency in avalibleCurrency)
                self.assertTrue(userBalance[UserInfo.RESERVE][currency] != 0)
                self.assertTrue(userBalance[UserInfo.RESERVE][currency] == self.__exmo.getCurrencyCountInOrder(currency))
            return True

        def anyRestrictedOnBoth():
            """{'BALANCE' : {'' : num, '' : num}, 'RESERVE' : {'' : num, '' : num}}"""
            requestCurrency = ['BTC', 'USD', 'XRP']
            userBalance = self.__exmo.getUserBalance(balance=requestCurrency, reserve=requestCurrency)
            self.assertTrue(len(userBalance) == 2)
            self.assertTrue(len(userBalance[UserInfo.BALANCE]) == len(requestCurrency))
            self.assertTrue(len(userBalance[UserInfo.RESERVE]) == len(requestCurrency))
            for currency in userBalance[UserInfo.BALANCE]:
                self.assertTrue(currency in requestCurrency)
                self.assertTrue(userBalance[UserInfo.BALANCE][currency] == self.__exmo.getCurrencyCountInAccess(currency))
            for currency in userBalance[UserInfo.RESERVE]:
                self.assertTrue(currency in requestCurrency)
                self.assertTrue(userBalance[UserInfo.RESERVE][currency] == self.__exmo.getCurrencyCountInOrder(currency))
            return True

        def balanceIsTrue():
            """{'' : num, '' : num, ...}"""
            userBalance = self.__exmo.getUserBalance(balance=True)
            self.assertTrue(userBalance == self.__exmo.getUserBalance()[UserInfo.BALANCE])
            return True

        def reserveIsTrue():
            """{'' : num, '' : num, ...}"""
            userBalance = self.__exmo.getUserBalance(reserve=True)
            self.assertTrue(userBalance == self.__exmo.getUserBalance()[UserInfo.RESERVE])
            return True

        def anyRestrictedOnBalance():
            """{'' : num, '' : num}"""
            requestCurrency = ['BTC', 'USD', 'XRP']
            userBalance = self.__exmo.getUserBalance(balance=requestCurrency)
            self.assertTrue(len(userBalance) == len(requestCurrency))
            for currency in userBalance:
                self.assertTrue(currency in requestCurrency)
                self.assertTrue(userBalance[currency] == self.__exmo.getCurrencyCountInAccess(currency))
            return True

        def anyRestrictedOnReserve():
            """{'' : num, '' : num}"""
            requestCurrency = ['BTC', 'USD', 'XRP']
            userBalance = self.__exmo.getUserBalance(reserve=requestCurrency)
            self.assertTrue(len(userBalance) == len(requestCurrency))
            for currency in userBalance:
                self.assertTrue(currency in requestCurrency)
                self.assertTrue(userBalance[currency] == self.__exmo.getCurrencyCountInOrder(currency))
            return True

        def oneRestrictedOnBoth():
            """[num, num]"""
            userBalance = self.__exmo.getUserBalance(balance='XRP', reserve='XRP')
            self.assertTrue(len(userBalance) == 2)
            self.assertTrue(userBalance[0] == self.__exmo.getCurrencyCountInAccess('XRP'))
            self.assertTrue(userBalance[1] == self.__exmo.getCurrencyCountInOrder('XRP'))
            return True

        def oneRestrictedOnBalance():
            """num"""
            userBalance = self.__exmo.getUserBalance(balance='XRP')
            self.assertTrue(userBalance == self.__exmo.getCurrencyCountInAccess('XRP'))
            return True

        def oneRestrictedOnReserve():
            """num"""
            userBalance = self.__exmo.getUserBalance(reserve='XRP')
            self.assertTrue(userBalance == self.__exmo.getCurrencyCountInOrder('XRP'))
            return True

        self.assertTrue(badBehavior())
        avalibleCurrency = self.__exmo.getAvalibleCurrency()
        self.assertTrue(notAnyRestricted())
        self.assertTrue(anyRestrictedOnBoth())
        self.assertTrue(balanceIsTrue())
        self.assertTrue(reserveIsTrue())
        self.assertTrue(anyRestrictedOnBalance())
        self.assertTrue(anyRestrictedOnReserve())
        self.assertTrue(oneRestrictedOnBoth())
        self.assertTrue(oneRestrictedOnBalance())
        self.assertTrue(oneRestrictedOnReserve())
        return True

    def test_getCurrencyCountInAccess(self):
        """Тестирует возвращение количества указанной валюты на аккаунте пользователя на текущий момент, которая находится в непосредственном доступе"""
        self.assertTrue(self.__exmo.getCurrencyCountInAccess('XXX') == TBApiErrors.UNEXISTANCE_CURRENCY)
        self.assertTrue(isinstance(self.__exmo.getCurrencyCountInAccess('XRP'), float))
        return True

    def test_getCurrencyCountInOrder(self):
        """Тестирует возвращение количества указанной валюты на аккаунте пользователя на текущий момент, которая задействована в активных ордерах"""
        self.assertTrue(self.__exmo.getCurrencyCountInOrder('XXX') == TBApiErrors.UNEXISTANCE_CURRENCY)
        self.assertTrue(isinstance(self.__exmo.getCurrencyCountInAccess('LTC'), float))
        return True

    def test_getOpenOrders(self):
        """Тестирует функцию получения информации об о всех открытых оредерах пользователя биржи Exmo"""

        def failBehaviour():
            """Проверка некорректного поведения при запросе получения открытых ордеров"""
            self.assertTrue(self.__exmo.getOpenOrders(pair='BTC_XXX') == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
            self.assertTrue(self.__exmo.getOpenOrders(type='BUY_SEL') == TBApiErrors.UNEXISTANCE_TYPE_ORDER_TO)
            self.assertTrue(self.__exmo.getOpenOrders(attributes='ID') == TBApiErrors.UNEXISTANCE_ORDER_ATTRIBUTE)
            return True

        def trueBehaviour():
            """Проверка корректного поведения при запросе получения открытых ордеров"""
            allOpenOrders = self.__exmo.getOpenOrders()
            # TODO: доделать тесты
            if len(allOpenOrders) > 0:
                avalibleCurrencyPair = self.__exmo.getAvalibleCurrencyPair()
                pass
            return True

        self.assertTrue(failBehaviour())
        self.assertTrue(trueBehaviour())
        return True

    def test_getClosedOrders(self):
        """Тестирует функцию возвращения информации о закрытых (завершённых) ордераз пользователя биржи Exmo"""

        def failBehaviour():
            """Проверка некорректного поведения при запросе получения закрытых ордеров"""
            self.assertTrue(self.__exmo.getClosedOrders(pair='BTC_XXX') == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
            self.assertTrue(self.__exmo.getClosedOrders(type='BUY_SEL') == TBApiErrors.UNEXISTANCE_TYPE_ORDER_TO)
            self.assertTrue(self.__exmo.getClosedOrders(attributes='ID') == TBApiErrors.UNEXISTANCE_ORDER_ATTRIBUTE)
            return True

        def trueBehaviour():
            """Проверка корректного поведения при запросе получения закрытых ордеров"""
            allClosedOrders = self.__exmo.getClosedOrders()
            # TODO: доделать тесты
            if len(allClosedOrders) > 0:
                avalibleCurrencyPair = self.__exmo.getAvalibleCurrencyPair()
                pass
            return True

        self.assertTrue(failBehaviour())
        self.assertTrue(trueBehaviour())
        return True

    def test_getDiscardOrders(self):
        """Тестирует функцию возвращения информации об отменённых оредрах пользователя биржи Exmo"""

        def failBehaviour():
            """Проверка некорректного поведения при запросе получения отменённых ордеров"""
            self.assertTrue(self.__exmo.getDiscardOrders(pair='BTC_XXX') == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
            self.assertTrue(self.__exmo.getDiscardOrders(type='BUY_SEL') == TBApiErrors.UNEXISTANCE_TYPE_ORDER_TO)
            self.assertTrue(self.__exmo.getDiscardOrders(attributes='ID') == TBApiErrors.UNEXISTANCE_ORDER_ATTRIBUTE)
            return True

        def trueBehaviour():
            """Проверка корректного поведения при запросе получения отменённых ордеров"""
            allDiscardOrders = self.__exmo.getDiscardOrders()
            if len(allDiscardOrders) > 1:
                avalibleCurrencyPairs = list(allDiscardOrders.keys())
                # проверка селлекции по валютной паре
                for currencyPair in avalibleCurrencyPairs[:2]:
                    self.assertTrue(allDiscardOrders[currencyPair] == self.__exmo.getDiscardOrders(pair=currencyPair))
                self.assertTrue({avalibleCurrencyPairs[0] : allDiscardOrders[avalibleCurrencyPairs[0]], avalibleCurrencyPairs[1] : allDiscardOrders[avalibleCurrencyPairs[1]]} == self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[:2]))
                # проверка селекции по типу сделки ордера
                for orders in self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[0], type=OrderAttributes.DealType.SELL_ORDER):
                    self.assertTrue(orders[OrderAttributes.TYPE] == OrderAttributes.DealType.SELL_ORDER)
                sellOrders = self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[:2], type=OrderAttributes.DealType.SELL_ORDER)
                for curencyPair in avalibleCurrencyPairs[:2]:
                    for orders in sellOrders[curencyPair]:
                        self.assertTrue(orders[OrderAttributes.TYPE] == OrderAttributes.DealType.SELL_ORDER)
                for orders in self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[0], type=OrderAttributes.DealType.BUY_ORDER):
                    self.assertTrue(orders[OrderAttributes.TYPE] == OrderAttributes.DealType.BUY_ORDER)
                buyOrders = self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[:2], type=OrderAttributes.DealType.BUY_ORDER)
                for curencyPair in avalibleCurrencyPairs[:2]:
                    for orders in buyOrders[curencyPair]:
                        self.assertTrue(orders[OrderAttributes.TYPE] == OrderAttributes.DealType.BUY_ORDER)
                # проверка селекции по атрибутам ордера
                for idOrder in self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[0], attributes=OrderAttributes.ID_ORDER):
                    self.assertTrue(isinstance(idOrder, int))
                for order in self.__exmo.getDiscardOrders(pair=avalibleCurrencyPairs[0], attributes=[OrderAttributes.ID_ORDER, OrderAttributes.TIME]):
                    self.assertTrue(isinstance(order[OrderAttributes.ID_ORDER], int))
                    self.assertTrue(isinstance(order[OrderAttributes.TIME], int))
                # проверка поиска ордера по идентификатору
                allDiscardOrdersId = self.__exmo.getDiscardOrders(attributes=OrderAttributes.ID_ORDER)
                for currencyPair in allDiscardOrdersId.keys():
                    if len(allDiscardOrdersId[currencyPair]) > 1:
                        for orderId in allDiscardOrdersId[currencyPair][:2]:
                            self.assertTrue(orderId == self.__exmo.getDiscardOrders(orderId, attributes=OrderAttributes.ID_ORDER))
                            findOrder = self.__exmo.getDiscardOrders(orderId, attributes=[OrderAttributes.ID_ORDER, OrderAttributes.TIME])
                            self.assertTrue(orderId == findOrder[OrderAttributes.ID_ORDER])
            return True

        self.assertTrue(failBehaviour())
        self.assertTrue(trueBehaviour())
        return True

    def test_getCurrentBuyPrice(self):
        """Тестирует получение текущей цены продажи (актуальную по биржевому курсу) валютной пары на бирже Exmo"""
        self.assertTrue(self.__exmo.getCurrentBuyPrice('BTC_XXX') == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
        self.assertTrue(self.__exmo.getCurrentBuyPrice('BTC_USD') > 0)
        self.assertTrue(len(self.__exmo.getCurrentBuyPrice()) > 2)
        return True

    def test_getCurrentSellPrice(self):
        """Тестирует получение текущей цены продажи (актуальную по биржевому курсу) валютной пары на бирже Exmo"""
        self.assertTrue(self.__exmo.getCurrentSellPrice('BTC_XXX') == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
        self.assertTrue(self.__exmo.getCurrentSellPrice('BTC_USD') > 0)
        self.assertTrue(len(self.__exmo.getCurrentSellPrice()) > 2)
        return True

    def test_createOrder(self):
        """Тестирует фукцию создания ордера на аккаунте текущего пользователя на бирже Exmo"""

        def failBehaviour():
            """Проверка некорректного поведения при создании ордеров"""

            def failBehaviourBuyOrder(currencyPair, currencyRestricted, avalibleCurrencyBalance):
                """Проверка некорректного поведения функции создания ордеров на покупку"""
                self.assertTrue(self.__exmo.createBuyOrder('XXX_YYY', currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.0, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.0) == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
                if (avalibleCurrencyBalance > currencyRestricted[TradeRestricted.MIN_AMOUNT]):
                    self.assertTrue(self.__exmo.createBuyOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 0.9, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.1, isTest=True) == TBApiErrors.UNAVALIBLE_MIN_QUANTITY_FOR_ORDER)
                    self.assertTrue(self.__exmo.createBuyOrder(currencyPair, currencyRestricted[TradeRestricted.MAX_QUANTITY] * 1.1, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.1, isTest=True) == TBApiErrors.UNAVALIBLE_MAX_QUANTITY_FOR_ORDER)
                    self.assertTrue(self.__exmo.createBuyOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.1, currencyRestricted[TradeRestricted.MIN_PRICE] * 0.9, isTest=True) == TBApiErrors.UNAVALIBLE_MIN_PRICE_FOR_ORDER)
                    self.assertTrue(self.__exmo.createBuyOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.1, currencyRestricted[TradeRestricted.MAX_PRICE] * 1.1, isTest=True) == TBApiErrors.UNAVALIBLE_MAX_PRICE_FOR_ORDER)
                    if currencyRestricted[TradeRestricted.MIN_PRICE] * currencyRestricted[TradeRestricted.MIN_QUANTITY] < currencyRestricted[TradeRestricted.MIN_AMOUNT]:
                        self.assertTrue(self.__exmo.createBuyOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.0, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.0, isTest=True) == TBApiErrors.UNAVALIBLE_MIN_AMOUNT_FOR_ORDER)
                    if currencyRestricted[TradeRestricted.MAX_PRICE] * currencyRestricted[TradeRestricted.MAX_QUANTITY] > currencyRestricted[TradeRestricted.MAX_AMOUNT]:
                        self.assertTrue(self.__exmo.createBuyOrder(currencyPair, currencyRestricted[TradeRestricted.MAX_QUANTITY] * 1.0, currencyRestricted[TradeRestricted.MAX_PRICE] * 1.0, isTest=True) == TBApiErrors.UNAVALIBLE_MAX_AMOUNT_FOR_ORDER)
                    marketBuyPrice = self.__exmo.getCurrentBuyPrice(currencyPair)
                    maxAvaluableQuantityForBuy = avalibleCurrencyBalance / marketBuyPrice
                    if (maxAvaluableQuantityForBuy * 0.5 > currencyRestricted[TradeRestricted.MIN_QUANTITY]):
                        self.assertTrue(self.__exmo.createBuyOrder(currencyPair, maxAvaluableQuantityForBuy * 1.1, marketBuyPrice * 1.0, isTest=True) == TBApiErrors.NOT_ANOUGHT_CURRENCY_FOR_BUY)
                        self.assertTrue(self.__exmo.createBuyOrder(currencyPair, maxAvaluableQuantityForBuy * 0.9, marketBuyPrice * 1.1, isTest=True) == TBApiErrors.PURCHASE_PRICE_MORE_THAN_MARKET)
                        self.assertTrue(self.__exmo.createBuyOrder(currencyPair, maxAvaluableQuantityForBuy * 0.99, marketBuyPrice * 1.01, isTest=True) == TBApiErrors.PURCHASE_PRICE_MORE_THAN_MARKET)
                return True

            def failBehaviourSellOrder(currencyPair, currencyRestricted, avalibleCurrencyBalance):
                """Проверка некорректного поведения функции создания ордеров на продажу"""
                self.assertTrue(self.__exmo.createSellOrder('XXX_YYY', currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.0, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.0) == TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
                if (avalibleCurrencyBalance > currencyRestricted[TradeRestricted.MIN_QUANTITY]):
                    self.assertTrue(self.__exmo.createSellOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 0.9, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.1, isTest=True) == TBApiErrors.UNAVALIBLE_MIN_QUANTITY_FOR_ORDER)
                    self.assertTrue(self.__exmo.createSellOrder(currencyPair, currencyRestricted[TradeRestricted.MAX_QUANTITY] * 1.1, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.1, isTest=True) == TBApiErrors.UNAVALIBLE_MAX_QUANTITY_FOR_ORDER)
                    self.assertTrue(self.__exmo.createSellOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.1, currencyRestricted[TradeRestricted.MIN_PRICE] * 0.9, isTest=True) == TBApiErrors.UNAVALIBLE_MIN_PRICE_FOR_ORDER)
                    self.assertTrue(self.__exmo.createSellOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.1, currencyRestricted[TradeRestricted.MAX_PRICE] * 1.1, isTest=True) == TBApiErrors.UNAVALIBLE_MAX_PRICE_FOR_ORDER)
                    if currencyRestricted[TradeRestricted.MIN_PRICE] * currencyRestricted[TradeRestricted.MIN_QUANTITY] < currencyRestricted[TradeRestricted.MIN_AMOUNT]:
                        self.assertTrue(self.__exmo.createSellOrder(currencyPair, currencyRestricted[TradeRestricted.MIN_QUANTITY] * 1.0, currencyRestricted[TradeRestricted.MIN_PRICE] * 1.0, isTest=True) == TBApiErrors.UNAVALIBLE_MIN_AMOUNT_FOR_ORDER)
                    if currencyRestricted[TradeRestricted.MAX_PRICE] * currencyRestricted[TradeRestricted.MAX_QUANTITY] > currencyRestricted[TradeRestricted.MAX_AMOUNT]:
                        self.assertTrue(self.__exmo.createSellOrder(currencyPair, currencyRestricted[TradeRestricted.MAX_QUANTITY] * 1.0, currencyRestricted[TradeRestricted.MAX_PRICE] * 1.0, isTest=True) == TBApiErrors.UNAVALIBLE_MAX_AMOUNT_FOR_ORDER)
                    marketSellPrice = self.__exmo.getCurrentSellPrice(currencyPair)
                    if (avalibleCurrencyBalance * 0.5 > currencyRestricted[TradeRestricted.MIN_QUANTITY]):
                        self.assertTrue(self.__exmo.createSellOrder(currencyPair, avalibleCurrencyBalance * 1.1, marketSellPrice * 1.0, isTest=True) == TBApiErrors.NOT_ANOUGHT_CURRENCY_FOR_SALE)
                        self.assertTrue(self.__exmo.createSellOrder(currencyPair, avalibleCurrencyBalance * 1.0, marketSellPrice * 0.9, isTest=True) == TBApiErrors.SELLING_PRICE_LESS_THAN_MARKET)
                        self.assertTrue(self.__exmo.createSellOrder(currencyPair, avalibleCurrencyBalance * 1.0, marketSellPrice * 0.99, isTest=True) == TBApiErrors.SELLING_PRICE_LESS_THAN_MARKET)
                return True

            nonlocal avaluableCurrencys
            nonlocal evaluableUserBalance
            nonlocal currencyTradeRestricted
            nonlocal avaluableExmoCurrencyPair
            for currencyPair in avaluableExmoCurrencyPair:
                if LPair(currencyPair) in avaluableCurrencys and RPair(currencyPair) in avaluableCurrencys:
                    self.assertTrue(failBehaviourBuyOrder(currencyPair, currencyTradeRestricted[currencyPair], evaluableUserBalance[RPair(currencyPair)]))
                    self.assertTrue(failBehaviourSellOrder(currencyPair, currencyTradeRestricted[currencyPair], evaluableUserBalance[LPair(currencyPair)]))
            return True

        def trueBehaviour():
            """Проверка корретного поведения при создании ордеров"""

            def trueBuyBehaviour(pair, price, quantity):
                self.assertTrue(self.__exmo.createBuyOrder(pair=pair, price=price/ceff, quantity=quantity, isTest=True) == TBApiErrors.CREATE_TEST_ORDER)
                return self.__exmo.createBuyOrder(pair=pair, price=price/ceff, quantity=quantity)

            def trueSellBehaviour(pair, price, tradeRestricted):
                self.assertTrue(self.__exmo.createSellOrder(pair=pair, price=price*ceff, quantity=tradeRestricted[TradeRestricted.MIN_QUANTITY], isTest=True) == TBApiErrors.CREATE_TEST_ORDER)
                return self.__exmo.createSellOrder(pair=pair, price=price*ceff, quantity=tradeRestricted[TradeRestricted.MIN_QUANTITY])

            nonlocal ceff
            nonlocal avaluableCurrencys
            nonlocal evaluableUserBalance
            nonlocal currencyTradeRestricted
            nonlocal avaluableExmoCurrencyPair
            evaluableUserBalance = self.__exmo.getUserBalance(balance=True)
            avaluableCurrencys = list(evaluableUserBalance.keys())
            for currencyPair in avaluableExmoCurrencyPair:
                lCurrency = LPair(currencyPair)
                rCurrency = RPair(currencyPair)
                if lCurrency in avaluableCurrencys and rCurrency in avaluableCurrencys:
                    tradeRestricted = currencyTradeRestricted[currencyPair]
                    currentMarketBuyPrice = self.__exmo.getCurrentBuyPrice(currencyPair)
                    # проверка выставления ордера на покупки и отмена только что выставленного ордера
                    if tradeRestricted[TradeRestricted.MIN_AMOUNT] < evaluableUserBalance[rCurrency]: # условие достаточности средств для покупки
                        avalibleQuantityForBuy = evaluableUserBalance[rCurrency] / (currentMarketBuyPrice / ceff) * 0.95
                        if tradeRestricted[TradeRestricted.MIN_QUANTITY] < avalibleQuantityForBuy: # условие достаточности покупаемой валюты
                            buyOrderId = trueBuyBehaviour(currencyPair, currentMarketBuyPrice, avalibleQuantityForBuy)
                            self.assertTrue(self.__exmo.cancelOrderById(buyOrderId))
                    # проверка выставления ордера на продажу и отмена только что выставленного ордера
                    #if tradeRestricted[TradeRestricted.MIN_QUANTITY] < evaluableUserBalance[lCurrency]:
                        #sellOrderId = trueSellBehaviour(currencyPair, currentMarketBuyPrice, tradeRestricted)
                        #self.assertTrue(self.__exmo.cancelOrderById(sellOrderId))
            return True

        ceff = 1.5 # коэффициент, на который умоножается цена покупки или продажи в расчёте на то, что соответствующий ордер не будет куплен/продар на реальных торгах
        avaluableExmoCurrencyPair = self.__exmo.getAvalibleCurrencyPair()
        currencyTradeRestricted = self.__exmo.getTradeRestricted()
        evaluableUserBalance = self.__exmo.getUserBalance(balance=True)
        avaluableCurrencys = list(evaluableUserBalance.keys())
        #self.assertTrue(failBehaviour())
        self.assertTrue(trueBehaviour())
        return True

    def test_Exmo(self):
        """Запускает тесты на выполнение"""
        self.assertTrue(self.test_getAvalibleCurrency())
        self.assertTrue(self.test_getAvalibleCurrencyPair())
        self.assertTrue(self.test_getTradeRestricted())
        self.assertTrue(self.test_getUserInformation())
        self.assertTrue(self.test_getCurrencyCountInAccess())
        self.assertTrue(self.test_getCurrencyCountInOrder())
        self.assertTrue(self.test_getOpenOrders())
        self.assertTrue(self.test_getClosedOrders())
        self.assertTrue(self.test_getDiscardOrders())
        self.assertTrue(self.test_getCurrentSellPrice())
        self.assertTrue(self.test_getCurrentBuyPrice())
        self.assertTrue(self.test_createBuyOrder())
        return

if __name__ == '__main__':
    random.seed()
    unittest.main()
