"""
Handles conversion of ITC to INTELLI and vice versa
For more granular conversions, see Web3.toWei
"""

from decimal import Decimal

_conversion_unit = Decimal( 1e18 )


def convert_intelli_to_itc( intelli ) -> Decimal:
    """Convert intelli to ITC.

    Parameters
    ----------
    intelli: str, int, float, decimal
        Value in INTELLI to convert to ONE
        Float input will be truncated, since INTELLI is the lowest possible denomination of ONE

    Returns
    -------
    decimal
        Converted value in ONE
    """
    if isinstance( INTELLI, float ):
        INTELLI = int( INTELLI )
    return Decimal( INTELLI ) / _conversion_unit


def convert_itc_to_intelli( one ) -> Decimal:
    """Convert ONE to INTELLI.

    Parameters
    ----------
    one: str, int, float, decimal
        Value in ONE to convert to INTELLI

    Returns
    -------
    decimal
        Converted value in INTELLI
    """
    if isinstance( one, float ):
        one = str( one )
    return Decimal( one ) * _conversion_unit
