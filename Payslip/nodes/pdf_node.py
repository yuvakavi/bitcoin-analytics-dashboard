from utils.pdf_generator import create_payslip

def generate_pdf(state):
    emp = state["employee"]
    salary = state["salary"]

    file_path = create_payslip(emp, salary)

    return {"pdf_path": file_path}