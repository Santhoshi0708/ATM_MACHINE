import streamlit as st
import pandas as pd

# Title of the Streamlit app
st.title("ATM Machine")

# Initialize balance and transaction history if not already present in session state
if 'balance' not in st.session_state:
    st.session_state.balance = 20000

if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = []

# Pin for accessing the ATM
ATM_pin = "1234"

# Function to check balance
def check_balance(balance):
    st.write(f"The current balance is: {balance}")
    st.session_state.transaction_history.append(("Check Balance", "N/A", "N/A", st.session_state.balance))

# Function to withdraw amount
def withdraw_amount(balance):
    withdraw = st.text_input("Enter withdraw amount", placeholder="Enter amount ...", key='withdraw')
    if withdraw.isdigit() and int(withdraw) <= balance:
        st.session_state.balance -= int(withdraw)
        st.write(f"Your a/c no XXXXXXXXXXXX is debited for Rs.{withdraw}. Your current balance is {st.session_state.balance}")
        st.session_state.transaction_history.append(("Withdraw", withdraw, "N/A", st.session_state.balance))
    elif not withdraw.isdigit():
        st.write("Please enter a valid amount.")
    else:
        st.write("You have insufficient balance in your account.")

# Function to deposit amount
def deposit_amount(balance):
    deposit = st.text_input("Enter deposit amount", value=None, placeholder="Enter amount ...", key='deposit')
    if deposit.isdigit():
        st.session_state.balance += int(deposit)
        st.write(f"Your a/c no XXXXXXXXXXXX is credited for Rs.{deposit}. Your current balance is {st.session_state.balance}")
        st.session_state.transaction_history.append(("Deposit", "N/A", deposit, st.session_state.balance))
    else:
        st.write("Please enter a valid amount.")

# Input field for user to enter PIN
user_input_Pin = st.text_input("Enter PIN")

# Checking PIN validity
if user_input_Pin == ATM_pin:
    flag = False
    while not flag:
        try:
            # Dropdown for selecting transaction options
            choice = st.selectbox('Select the options', ('Check Balance', 'Withdraw Amount', 'Deposit Amount', 'Exit'), key='selectbox')
            if choice == 'Check Balance':
                check_balance(st.session_state.balance)
            if choice == 'Withdraw Amount':
                withdraw_amount(st.session_state.balance)
            if choice == 'Deposit Amount':
                deposit_amount(st.session_state.balance)
            if choice == 'Exit':
                flag = True
                st.session_state.clear()  # Clear session state
                st.markdown("<script>window.close();</script>", unsafe_allow_html=True)  # Close the Streamlit app
                break

            # Display transaction history
            st.write("Transaction History:")
            df = pd.DataFrame(st.session_state.transaction_history, columns=["Transaction Type", "Withdraw Amount", "Deposit Amount", "Balance"])
            st.write(df)
        except:
            pass

else:
    st.write("Incorrect PIN")
