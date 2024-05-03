# MoneyMatters

MoneyMatters is a Python package designed to simplify several common monetary operations, such as currency conversion and money formatting. It integrates functionalities from multiple sources to provide a unified solution for handling monetary values, leveraging real-time data for accurate currency conversions and providing various formatting options.

## Features

- **Currency Conversion**: Convert amounts from one currency to another using real-time exchange rates.
- **Money Formatting**: Format monetary values into a more readable form or according to specific cultural norms.

## Installation

To install MoneyMatters, run the following command:

```bash
pip install moneymatters
```

Ensure you have Python 3.7 or later installed on your system.

## Usage

### Currency Conversion

To convert currency, use the `ExchangeAPI` class:

```python
from moneymatters.api import ExchangeAPI

# Create an instance of the ExchangeAPI
converter = ExchangeAPI()

# Convert 100 USD to EUR
converted_amount = converter.convert(100, 'USD', 'EUR')
print(f"100 USD is equivalent to {converted_amount} EUR")
```

### Money Formatting

To format money values, use the `Formatter` class:

```python
from moneymatters.api import Formatter

# Format a price in a specific pattern
formatted_price = Formatter.apply_price_format(1234.56, '99.99')
print(f"The formatted price is {formatted_price}")
```

## Additional Information

- **API Sources**:
  - ECB for major 30 currencies.
  - Fawaz Ahmed's exchange-api for 150+ currencies.
  - XE.com for detailed and possibly more accurate data as a last resort.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## License

This project is licensed under the Affero GNU Public License v3 - see the [LICENSE](LICENSE) file for details.

## Contact

- **Author**: Gopala Krishna Koduri
- **Email**: [gopal@riyazapp.com](mailto:gopal@riyazapp.com)
- [GitHub Repository](https://github.com/musicmuni/moneymatters)
- [Issue Tracker](https://github.com/musicmuni/moneymatters/issues)
- [LinkedIn](https://linkedin.com/in/gopalkoduri)
- [Learn to Sing with Riyaz App](https://riyazapp.com)

## Acknowledgments

Thanks to all contributors who have helped shape MoneyMatters, making it easier to deal with currency related stuff for developers around the globe.
