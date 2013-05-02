balance = 999999
annualInterestRate = 0.18


monthly_interest_rate = annualInterestRate / 12.0 
lower_bound = balance / 12.0
upper_bound = (balance * (1 + monthly_interest_rate) ** 12) / 12.0

#mini_monthly_payment = (lower_bound + upper_bound) / 2 
remain_balance = balance

while abs(remain_balance) >= 0.01:
    remain_balance = balance
    mini_monthly_payment = (lower_bound + upper_bound) / 2
    #calculate 1 year remaining balance
    for i in range(0, 12):
        monthly_upaid_balance = remain_balance - mini_monthly_payment
        remain_balance = monthly_upaid_balance + monthly_interest_rate * monthly_upaid_balance
    
    if round(remain_balance, 2) < 0.01:
        upper_bound = mini_monthly_payment
    else :
        lower_bound = mini_monthly_payment
 
print 'Lowest Payment: ' + str(round(mini_monthly_payment, 2))
