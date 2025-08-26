from fastapi import FastAPI
from pydantic import BaseModel
import math

# Initialize FastAPI app
app = FastAPI(title="Loan EMI Calculator API")

# Input model
class LoanDetails(BaseModel):
    loan_amount: float
    annual_roi: float  # Annual Rate of Interest (%)
    tenure_years: int  # Tenure in years

@app.post("/calculate_emi")
def calculate_emi(details: LoanDetails):
    P = details.loan_amount
    R = details.annual_roi / 12 / 100  # monthly interest rate
    N = details.tenure_years * 12      # tenure in months

    if R == 0:  # No interest loan
        emi = P / N
    else:
        emi = P * R * math.pow(1 + R, N) / (math.pow(1 + R, N) - 1)

    total_payment = emi * N
    total_interest = total_payment - P

    return {
        "Loan Amount": P,
        "Annual ROI (%)": details.annual_roi,
        "Tenure (Years)": details.tenure_years,
        "Monthly EMI": round(emi, 2),
        "Total Payment": round(total_payment, 2),
        "Total Interest": round(total_interest, 2)
    }
