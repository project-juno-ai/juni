using System;

public class BankAccount
{
    private string _accountHolderName;
    private decimal _balance;

    public BankAccount(string accountHolderName, decimal initialBalance)
    {
        _accountHolderName = accountHolderName;
        _balance = initialBalance;
    }

    public string AccountHolderName
    {
        get { return _accountHolderName; }
        set { _accountHolderName = value; }
    }

    public decimal Balance
    {
        get { return _balance; }
    }

    public void Deposit(decimal amount)
    {
        if (amount < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(amount), "Deposit amount must be positive.");
        }

        _balance += amount;
    }

    public void Withdraw(decimal amount)
    {
        if (amount < 0)
        {
            throw new ArgumentOutOfRangeException(nameof(amount), "Withdrawal amount must be positive.");
        }

        if (_balance < amount)
        {
            throw new InvalidOperationException("Insufficient funds for withdrawal.");
        }

        _balance -= amount;
    }
}