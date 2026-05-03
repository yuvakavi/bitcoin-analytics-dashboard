from agents.payroll_graph import graph
from data.mock_data import mock_employees
from utils.json_generator import generate_payslip_json

import json

def run_payroll():
    print("\n🚀 Running Payroll Agent...\n")

    for emp in mock_employees:
        try:
            result = graph.invoke({"employee": emp})

            # generate JSON
            payslip_json = generate_payslip_json(emp, result["salary"])

            print(f"✔ Payslip generated for {emp['name']}")
            print(f"📄 File: {result['pdf_path']}")

            print("📊 JSON Output:")
            print(json.dumps(payslip_json, indent=4))
            print("-" * 40)

        except Exception as e:
            print(f"❌ Error processing {emp['name']}: {str(e)}")

if __name__ == "__main__":
    run_payroll()