#coding: utf-8

balance = 4213
annualInterestRate = 0.2
monthlyPaymentRate = 0.04


total_pay = 0
monthly_interest_rate =  annualInterestRate/12.0
remaining_balance = balance

for i in range(1,13):
    minimum_monthly_payment = round(monthlyPaymentRate * remaining_balance, 2)
    total_pay += minimum_monthly_payment
    monthly_unpaid_balance = remaining_balance - minimum_monthly_payment
    remaining_balance = round(monthly_unpaid_balance +
                        (monthly_interest_rate * monthly_unpaid_balance), 2)
    print 'Month: ' + str(i)
    print 'Minimum monthly payment: ' + str(minimum_monthly_payment)
    print 'Remaining balance: ' + str(remaining_balance)

print 'Total paid: ' + str(total_pay)
print 'Remaining balance: ' + str(remaining_balance)

