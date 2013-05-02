balance = 4773 
annualInterestRate = 0.2

mini_monthly_payment = 10
pre_balance = balance

while True:
    #calculate 1 year remaining balance
    for i in range(1, 13):
        monthly_interest_rate = annualInterestRate / 12.0
        monthly_upaid_balance = pre_balance - mini_monthly_payment
        pre_balance = monthly_upaid_balance + monthly_interest_rate * monthly_upaid_balance

    if pre_balance < 0:
        print 'Lowest Payment: ' + str(mini_monthly_payment)
        break
    else:
        #reset balance and increat monthly payment
        pre_balance = balance
        mini_monthly_payment += 10
