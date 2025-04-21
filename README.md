# Bond Pricing Library

A comprehensive Python library for fixed income pricing, risk analysis, and portfolio management.

## Overview

This library provides tools for pricing various types of bonds, calculating risk metrics, and conducting stress tests and scenario analysis. It's designed to be extensible, allowing for easy addition of new bond types and risk metrics.

## Features

- **Multiple Bond Types**: Support for fixed-rate, floating-rate, and zero-coupon bonds
- **Yield Curve Modeling**: Interpolation and discount factor calculation
- **Risk Metrics**: Duration, modified duration, convexity, DV01, etc.
- **Stress Testing**: Pre-defined and custom stress test scenarios
- **Value at Risk**: Various VaR calculation methodologies
- **Flexible I/O**: CSV import/export with extensible adapter pattern


## Getting Started



# Run the example
python basic_usage.py

## Architecture

The library is organized into several modules:

- **core**: Base classes and fundamental financial concepts (Bond, Cash Flow, Interest Rate Curve)
- **instruments**: Concrete bond implementations (Fixed Rate, Floating Rate, Zero Coupon)
- **risk**: Risk measurement and stress testing tools
- **adapters**: I/O interfaces for data loading and result export
- **utils**: Configuration, logging, and mathematical utilities

This modular design supports extensibility and clear separation of concerns.

## Assumptions

The library makes the following simplifying assumptions:

- **Day Count Convention**: Actual/365
- **Payment Frequency**: Semi-annual (default)
- **Business Days**: Calendar days (no holiday/business day adjustments)
- **Settlement**: No settlement lags considered

These assumptions can be modified by extending the appropriate classes.



## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request