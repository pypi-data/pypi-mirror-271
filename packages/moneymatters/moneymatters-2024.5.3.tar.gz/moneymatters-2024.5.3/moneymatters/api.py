from bs4 import BeautifulSoup
import requests
from decimal import Decimal
from currency_converter import CurrencyConverter, RateNotFoundError, SINGLE_DAY_ECB_URL


class ExchangeAPI:
    _currency_converter = CurrencyConverter(SINGLE_DAY_ECB_URL)  # gets latest rates

    def __init__(self) -> None:
        pass

    def _service1(self, price, from_currency, to_currency):
        """ECB data based, major 30 currencies"""
        try:
            converted_price = self._currency_converter.convert(price, from_currency, to_currency)
        except (ValueError, RateNotFoundError):
            converted_price = None
        return converted_price

    def _service2(self, price, from_currency, to_currency):
        """https://github.com/fawazahmed0/exchange-api based, 150+ currencies"""

        endpoint = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1"
        try:
            response = requests.get(f"{endpoint}/currencies/{from_currency.lower()}.json")
            currency_exchange_rates = response.json()
            converted_price = price * currency_exchange_rates[from_currency.lower()][to_currency.lower()]
        except:
            converted_price = None
        return converted_price

    def _service3(self, price, from_currency, to_currency):
        """xe.com based, slowest and last resort"""
        try:
            data = requests.get(
                f"https://www.xe.com/currencyconverter/convert/?Amount={price}&From={from_currency}&To={to_currency}"
            )
            soup = BeautifulSoup(data.text, "html.parser")
            p_element = soup.find("p", class_="sc-1c293993-1 fxoXHw")
            full_text = p_element.get_text()
            numeric_text = "".join([char for char in full_text if char.isdigit() or char == "."])
            converted_price = float(numeric_text)
        except:
            converted_price = None
        return converted_price

    def convert(self, price, from_currency, to_currency):
        converted_price = self._service1(price, from_currency, to_currency)
        if not converted_price:
            converted_price = self._service2(price, from_currency, to_currency)
        if not converted_price:
            converted_price = self._service3(price, from_currency, to_currency)

        return converted_price


class Formatter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def apply_price_format(price, format):
        """
        Applies a specified formatting rule to a given price, rounding and adjusting it based on
        the format's suffix. The function supports the following ending patterns:
        1. decimals ending with .99, 4.9, 4.99, 8.99, 9.9, 9.98, 9.99
        2. integers ending with 0, 8, 99

        Parameters:
                price (str or Decimal): The original price to be formatted.
                format (str or Decimal): The target format indicating how the price should be rounded
                                            and adjusted. This can include patterns like "99", "9.99",
                                            or others specifying the rounding behavior.

        Returns:
                Decimal: The price adjusted to the closest specified format.
        """

        price = Decimal(price)  # Convert inputs to Decimal
        format = Decimal(format)
        rounded_price = None
        candidates = []

        # Determine suffix and the appropriate rounding mechanism
        if format == format.to_integral_value():
            ref_price_int_str = str(int(format))
            if ref_price_int_str.endswith("8"):
                candidates = [
                    (price / Decimal("10")).to_integral_value() * Decimal("10") + Decimal("8"),
                    (price / Decimal("10")).to_integral_value() * Decimal("10") - Decimal("2"),
                ]
            elif ref_price_int_str.endswith("99"):
                candidates = [
                    (price / Decimal("100")).to_integral_value() * Decimal("100") + Decimal("99"),
                    (price / Decimal("100")).to_integral_value() * Decimal("100") - Decimal("1"),
                ]
            else:  # also handles case where it endswith("0")
                candidates = [(price / Decimal("10")).to_integral_value() * Decimal("10")]
        else:
            ref_price_str = str(format)
            base_price = price.to_integral_value()

            if ref_price_str.endswith("4.99"):
                candidates = [base_price - (base_price % Decimal("10")) + Decimal("4.99")]
            elif ref_price_str.endswith("4.9"):
                candidates = [base_price - (base_price % Decimal("10")) + Decimal("4.9")]
            elif ref_price_str.endswith("9.98"):
                candidates = [
                    base_price - (base_price % Decimal("10")) + Decimal("9.98"),
                    base_price - (base_price % Decimal("10")) - Decimal("0.02"),
                ]
            elif ref_price_str.endswith("9.99"):
                candidates = [
                    base_price - (base_price % Decimal("10")) + Decimal("9.99"),
                    base_price - (base_price % Decimal("10")) - Decimal("0.01"),
                ]
            elif ref_price_str.endswith("9.9"):
                candidates = [
                    base_price - (base_price % Decimal("10")) + Decimal("9.9"),
                    base_price - (base_price % Decimal("10")) - Decimal("0.1"),
                ]
            elif ref_price_str.endswith("8.99"):
                candidates = [
                    base_price - (base_price % Decimal("10")) + Decimal("8.99"),
                    base_price - (base_price % Decimal("10")) - Decimal("1.01"),
                ]
            else:  # also handles the case where price is *.99
                candidates = [base_price + Decimal("0.99")]

        rounded_price = min(candidates, key=lambda x: abs(x - price))
        return rounded_price
