from agent.state_machine import ExpenseAgent

agent = ExpenseAgent("data/sample_transactions.csv")

result = agent.run()

print("\n---- REPORT ----\n")
print(result["report"])