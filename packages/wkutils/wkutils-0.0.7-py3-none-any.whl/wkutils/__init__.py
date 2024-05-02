import numpy_financial as npf

def find_nth(haystack: str, needle: str, n: int) -> int:
    '''
        This will find the nth occurrence of a substring in a string 
    '''
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def twoDecimalPlaces(answer):
    '''
        This simply formats the input as two decimal places.
    '''
    return("%.2f" % answer)

def gross_payment(rate, nper, pv):
    '''
        
    '''
    return float(twoDecimalPlaces(npf.pmt(rate/(nper*12), nper*12, pv)))

def net_payment(grosspayment):
    return float(twoDecimalPlaces(grosspayment * (1-0.22)))

def calculate_loan_payments(rate, nper, pv):
    gp = gross_payment(rate, nper, pv)
    np = net_payment(gp)
    print('Gross payment:', gp)
    print('Net payment:', np)