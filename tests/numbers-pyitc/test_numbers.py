from decimal import Decimal

from pyitc import numbers


def test_convert_intelli_to_itc():
    a = numbers.convert_intelli_to_itc( 1e18 )
    assert Decimal( 1 ) == a

    b = numbers.convert_intelli_to_itc( 1e18 + 0.6 )
    assert Decimal( 1 ) == b

    c = numbers.convert_intelli_to_itc( "1" + ( "0" * 18 ) )
    assert Decimal( 1 ) == c

    d = numbers.convert_intelli_to_itc( Decimal( 1e18 ) )
    assert Decimal( 1 ) == d


def test_convert_itc_to_intelli():
    a = numbers.convert_itc_to_intelli( 1e-18 )
    assert Decimal( 1 ) == a

    b = numbers.convert_itc_to_intelli( 1.5 )
    assert Decimal( 1.5e18 ) == b

    c = numbers.convert_itc_to_intelli( "1" )
    assert Decimal( 1e18 ) == c

    d = numbers.convert_itc_to_intelli( Decimal( 1 ) )
    assert Decimal( 1e18 ) == d
