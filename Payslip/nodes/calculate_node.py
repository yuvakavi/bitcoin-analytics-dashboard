POINT_RATE = 100

def calculate_salary(state):
    emp = state["employee"]

    if emp["role"] == "employee":
        fixed = emp["fixed_pay"]   # only employee has this
        leaves = emp.get("leaves", 0)

        salary = fixed - (fixed * leaves / 30)

    elif emp["role"] == "intern":
        total_points = sum(b["points"] for b in emp["bounties"])
        salary = total_points * POINT_RATE

    else:
        salary = 0

    return {"salary": salary}