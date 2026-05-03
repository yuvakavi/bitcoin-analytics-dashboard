from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import os

from config.settings import OUTPUT_DIR

styles = getSampleStyleSheet()

# ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# point conversion rate
POINT_RATE = 100  # 1 point = Rs.100


def create_payslip(emp, salary):
    file_path = f"{OUTPUT_DIR}{emp['name'].replace(' ', '_')}_payslip.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)

    elements = []

    # 🔹 Header
    elements.append(Paragraph("<b>Across the Global</b>", styles['Title']))
    elements.append(Paragraph("Employee Payslip - May 2026", styles['Normal']))
    elements.append(Spacer(1, 20))

    # 🔹 Employee Details
    emp_data = [
        ["Name", emp["name"]],
        ["Role", emp["role"].capitalize()],
        ["Generated Date", datetime.date.today().strftime("%d %B %Y")]
    ]

    emp_table = Table(emp_data, colWidths=[120, 250])
    emp_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
    ]))

    elements.append(Paragraph("<b>Employee Details</b>", styles['Heading3']))
    elements.append(emp_table)
    elements.append(Spacer(1, 20))

    # 🔹 Salary Details (FIXED LOGIC)
    if emp["role"] == "employee":
        salary_data = [
            ["Fixed Pay", f"Rs. {emp['fixed_pay']}"],
            ["Leaves", emp.get("leaves", 0)],
            ["Final Salary", f"Rs. {salary}"]
        ]

    elif emp["role"] == "intern":
        points = sum(b["points"] for b in emp["bounties"])

        salary_data = [
            ["Performance Points", points],
            ["Rate per Point", f"Rs. {POINT_RATE}"],
            ["Final Salary", f"Rs. {salary}"]
        ]

    else:
        salary_data = [
            ["Error", "Unknown Role"]
        ]

    salary_table = Table(salary_data, colWidths=[150, 200])
    salary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
    ]))

    elements.append(Paragraph("<b>Salary Details</b>", styles['Heading3']))
    elements.append(salary_table)

    # 🔹 Footer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("This is a system-generated payslip.", styles['Italic']))

    doc.build(elements)

    return file_path