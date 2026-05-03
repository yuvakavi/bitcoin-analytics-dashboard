import datetime

POINT_RATE = 100

def generate_payslip_json(emp, salary):
    today = datetime.date.today().strftime("%d %B %Y")

    if emp["role"] == "employee":
        return {
            "name": emp["name"],
            "role": "employee",
            "salary_type": "fixed",
            "fixed_pay": emp["fixed_pay"],
            "leaves": emp.get("leaves", 0),
            "final_salary": salary,
            "generated_date": today
        }

    elif emp["role"] == "intern":
        points = sum(b["points"] for b in emp["bounties"])

        return {
            "name": emp["name"],
            "role": "intern",
            "salary_type": "performance",
            "performance_points": points,
            "rate_per_point": POINT_RATE,
            "final_salary": salary,
            "generated_date": today
        }

    else:
        return {
            "error": "Unknown role"
        }