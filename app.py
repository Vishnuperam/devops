import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import streamlit as st

def days_between_dates(start_date, end_date):
    """
    Calculate the number of days between two dates
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return (end_date - start_date).days

def calculate_simple_interest(principal, rate_per_hundred, taken_date, closure_date):
    """
    Calculates the simple interest where rate is in rupees per hundred per month
    
    Args:
        principal (float): The initial amount
        rate_per_hundred (float): Rate in rupees per hundred rupees per month
        taken_date (str): Start date in YYYY-MM-DD format
        closure_date (str): End date in YYYY-MM-DD format
    
    Returns:
        tuple: (interest amount, final amount)
    """
    days = days_between_dates(taken_date, closure_date)
    # Calculate interest for the entire period without compounding
    interest = math.ceil((principal * rate_per_hundred * days) / (365/12 * 100))
    final_amount = principal + interest
    return int(interest), int(final_amount)

def calculate_compound_interest(principal, rate_per_hundred, taken_date, closure_date):
    """
    Calculates compound interest annually with remaining time calculated as simple interest
    Rate is in rupees per hundred rupees per month
    
    Args:
        principal (float): The initial amount
        rate_per_hundred (float): Rate in rupees per hundred rupees per month
        taken_date (str): Start date in YYYY-MM-DD format
        closure_date (str): End date in YYYY-MM-DD format
    
    Returns:
        tuple: (final amount, total interest)
    """
    start_date = datetime.strptime(taken_date, "%Y-%m-%d")
    end_date = datetime.strptime(closure_date, "%Y-%m-%d")
    current_principal = principal
    total_interest = 0
    
    # Calculate the total years and remaining days
    total_days = (end_date - start_date).days
    complete_years = total_days // 365
    remaining_days = total_days % 365
    
    print(f"\nDetailed Calculation:")
    print(f"Total days: {total_days}")
    print(f"Complete years: {complete_years}")
    print(f"Remaining days: {remaining_days}")
    
    # Calculate interest for complete years
    current_date = start_date
    for year in range(complete_years):
        next_year_date = current_date + relativedelta(years=1)
        interest, _ = calculate_simple_interest(
            current_principal, 
            rate_per_hundred,
            current_date.strftime("%Y-%m-%d"),
            next_year_date.strftime("%Y-%m-%d")
        )
        print(f"\nYear {year + 1}:")
        print(f"Principal: ₹{current_principal:,}")
        print(f"Interest: ₹{interest:,}")
        
        total_interest += interest
        current_principal += interest
        current_date = next_year_date
    
    # Calculate interest for remaining days
    if remaining_days > 0:
        final_interest, _ = calculate_simple_interest(
            current_principal,
            rate_per_hundred,
            current_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        print(f"\nRemaining period ({remaining_days} days):")
        print(f"Principal: ₹{current_principal:,}")
        print(f"Interest: ₹{final_interest:,}")
        
        total_interest += final_interest
        current_principal += final_interest
    
    return current_principal, total_interest



def main():
    st.title("Interest Calculator")
    st.write("This calculator helps you calculate simple and compound interest for a given period.")

    tab1, tab2 = st.tabs(["Simple Interest", "Compound Interest"])
    principal = tab1.number_input("principal Amount", value=None, placeholder="type a Principal amount", key="simple principal")
    rate = tab1.number_input("Rate", value=None, placeholder="type a rate", key="simple rate")
    start_date = str(tab1.date_input("Start Date", key="simple strt"))
    end_date = str(tab1.date_input("End Date", key="simple end"))
    button = tab1.button("claculte", key="simple button")
    if button:
        interest, final_amount = calculate_simple_interest(principal, rate, start_date, end_date)
        tab1.write(f"Principle Amount: ₹ {int(principal)}")
        tab1.write(f"Interest: ₹ {int(interest)}")
        tab1.write(f"Final Amount: ₹ {int(final_amount)}")
    
    principal = tab2.number_input("principal Amount", value=None, placeholder="type a Principal amount", key="compound principal")
    rate = tab2.number_input("Rate", value=None, placeholder="type a rate", key="compound rate")
    start_date = str(tab2.date_input("Start Date", key="compound start"))
    end_date = str(tab2.date_input("End Date", key="compound end"))
    button2 = tab2.button("claculte", key="compound button")
    if button2:
        final_amount, total_interest = calculate_compound_interest(principal, rate, start_date, end_date)
        tab2.write(f"Principle Amount: ₹ {int(principal)}")
        tab2.write(f"Interest: ₹ {int(total_interest)}")
        tab2.write(f"Final Amount: ₹ {int(final_amount)}")


if __name__ == "__main__":
    main()

