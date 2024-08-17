#Homework A - Mortgage Calculator - Jack Miller

"""Perform fixed-rate mortgage calculations."""

from argparse import ArgumentParser
import math
import sys


def get_min_payment(principal, interest_rate, years=30, payments=12): 
    #calculates the minimum payment for the mortgage
    r=interest_rate / payments
    n=years * payments
    A=principal * r * (1+r) / ((1+r)**n-1)
    return math.ceil(A)

def interest_due(balance, interest_rate, payments=12):
    #calculates interest due on payment for the next month
    r=interest_rate / payments
    return balance * r

def remaining_payments(balance, interest_rate, target_payment, payments=12):
    #number of remaining payments required to pay off the mortgage
    payments=0
    while balance>0:
        interest=interest_due(balance, interest_rate, payments)
        balance-=(target_payment - interest)
        payments+=1
    return payments

def main(principal, interest_rate, years=30, payments=12, target_payment=None):
    min_payment = get_min_payment(principal, interest_rate, years, payments)
    print('Minimum payment: $', min_payment)
    if target_payment is None:
        target_payment = min_payment
    if target_payment < min_payment:
        print("Your target payment is less than the minimum payment for this mortgage.")
    else:
        total_remaining = remaining_payments(principal, interest_rate, target_payment, payments)
        print('If you make payments of $', target_payment, 'you will pay off the mortgage in', total_remaining, 'payments.')


def parse_args(arglist):
    """Parse and validate command-line arguments.

    Args:
        arglist (list of str): list of command-line arguments.

    Returns:
        namespace: the parsed arguments (see argparse documentation for
        more information)

    Raises:
        ValueError: encountered an invalid argument.
    """
    # set up argument parser
    parser = ArgumentParser()
    parser.add_argument("mortgage_amount", type=float,
                        help="the total amount of the mortgage")
    parser.add_argument("annual_interest_rate", type=float,
                        help="the annual interest rate, as a float"
                             " between 0 and 1")
    parser.add_argument("-y", "--years", type=int, default=30,
                        help="the term of the mortgage in years (default: 30)")
    parser.add_argument("-n", "--num_annual_payments", type=int, default=12,
                        help="the number of payments per year (default: 12)")
    parser.add_argument("-p", "--target_payment", type=float,
                        help="the amount you want to pay per payment"
                        " (default: the minimum payment)")
    # parse and validate arguments
    args = parser.parse_args()
    if args.mortgage_amount < 0:
        raise ValueError("mortgage amount must be positive")
    if not 0 <= args.annual_interest_rate <= 1:
        raise ValueError("annual interest rate must be between 0 and 1")
    if args.years < 1:
        raise ValueError("years must be positive")
    if args.num_annual_payments < 0:
        raise ValueError("number of payments per year must be positive")
    if args.target_payment and args.target_payment < 0:
        raise ValueError("target payment must be positive")

    return args


if __name__ == "__main__":
    try:
        args = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    main(args.mortgage_amount, args.annual_interest_rate, args.years,
         args.num_annual_payments, args.target_payment)