transactions = [
    {"reference": "tx001", "type": "deposit", "amount": 5000, "account": "ACC1001"},
    {"reference": "tx002", "type": "withdrawal", "amount": 2000, "account": "ACC1001"},
    {"reference": "tx003", "type": "deposit", "amount": 10000, "account": "ACC2001"},
    {"reference": "tx001", "type": "deposit", "amount": 5000, "account": "ACC1001"},  # duplicate transaction
    {"reference": "tx004", "type": "withdrawal", "amount": 100000, "account": "ACC1001"},  # insufficient funds
    {"reference": "tx005", "type": "deposit", "amount": 2345, "account": "ACC9999"},  # non-existent account
]

accounts = {
    "ACC1001": {"name": "Moosa", "balance": 3000},
    "ACC2001": {"name": "Jane", "balance": 500}
}

def transaction_processor(transactions, accounts):
    notifications = []
    failed = []
    seen = set()
    total_deposits = 0
    total_withdrawals = 0

    for transaction in transactions:
        if transaction["reference"] in seen:
            failed.append({"reference": transaction["reference"], "reason": "Duplicate transaction"}) # Added duplicate transactions to failed list
        else:
            seen.add(transaction["reference"]) # This adds the reference to seen, to that it is not duplicated.

            if transaction["account"] in accounts:
                # this block checks the transaction type and performs the transaction
                if transaction["type"] == "deposit":
                    accounts[transaction["account"]]["balance"] += transaction["amount"]
                    notifications.append(accounts[transaction["account"]]["name"] + " received " + str(transaction["amount"]) 
                                         + ". New balance: " + str(accounts[transaction["account"]]["balance"]))
                    total_deposits += transaction["amount"] # bonus point
                else:
                    if accounts[transaction["account"]]["balance"] >= transaction["amount"]:
                        accounts[transaction["account"]]["balance"] -= transaction["amount"]
                        notifications.append(accounts[transaction["account"]]["name"] + " withdrew " + str(transaction["amount"]) 
                                             + ". New balance: " + str(accounts[transaction["account"]]["balance"]))
                        total_withdrawals += transaction["amount"] # bonus point
                    else:
                        failed.append({"reference": transaction["reference"], "reason": "Insufficient funds"})

            else:
                failed.append({"reference": transaction["reference"], "reason": "The account does not exist"})

    return{
        "notifications": notifications,
        "failed": failed,
        "summary": {
            "total_deposits": total_deposits,
            "total_withdrawals": total_withdrawals,
            "failed_transactions": failed
        }
    }

display = transaction_processor(transactions, accounts)
print(display["notifications"], display["failed"], )
print(display["summary"])
