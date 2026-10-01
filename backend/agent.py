from langgraph.graph import StateGraph, START, END
from typing import TypedDict
import re
from rag.rag_answer import retrieve_rules, find_matching_rule
import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv("backend/.env")

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in backend/.env")

llm_client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

class TaxState(TypedDict):
    documents: list
    document_types: dict
    extracted_data: dict
    validation_result: str
    missing_fields: list
    client_response: str
    annual_income: int
    tax_rule: str
    tax_amount: float
    final_validation: str
    ca_decision: str
    case_summary: str
    error_message: str




def classify_documents(state: TaxState):

    print("Classifying documents...")

    documents = state["documents"]

    document_types = {}

    for document in documents:

        name = document.lower()

        if "form16" in name or "form_16" in name:
            document_types[document] = "Form 16"

        elif "salary" in name:
            document_types[document] = "Salary Slip"

        elif "bank" in name:
            document_types[document] = "Bank Statement"

        elif "investment" in name:
            document_types[document] = "Investment Proof"

        elif "loan" in name:
            document_types[document] = "Home Loan Statement"

        else:
            document_types[document] = "Unknown"

    return {
        "document_types": document_types
    }


def extract_salary_data(state: TaxState):

    print("Extracting salary information...")

    with open("backend/documents/salary_slip.txt", "r") as file:
        document_text = file.read()

    extracted_data = {}

    for line in document_text.splitlines():

        if ":" in line:

            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            if key in [
                "Basic Salary",
                "HRA",
                "Other Allowance",
                "Gross Salary",
                "TDS",
                "Net Salary"
            ]:
                value = int(value)

            extracted_data[key] = value

    return {
        "extracted_data": extracted_data
    }

def check_missing_information(state: TaxState):

    print("Checking for missing information...")

    data = state["extracted_data"]

    required_fields = [
        "Employee Name",
        "Basic Salary",
        "HRA",
        "Other Allowance",
        "Gross Salary",
        "TDS",
        "Net Salary"
    ]

    missing_fields = []

    for field in required_fields:

        if field not in data:
            missing_fields.append(field)

    if missing_fields:
        print("Missing fields:", missing_fields)
    else:
        print("No information is missing.")

    return {
        "missing_fields": missing_fields
    }

def decide_after_missing_check(state: TaxState):

    if state["missing_fields"]:
        return "missing"

    return "complete"


def ask_client(state: TaxState):

    missing_fields = state["missing_fields"]

    print("⚠️ Information is missing.")
    print("Please provide:", missing_fields)

    return {}




def parse_client_response_with_llm(response, field):

    print("Understanding client response with LLM...")

    prompt = f"""
The client was asked to provide the following field:

Field: {field}

Client response:
{response}

Extract the value for the requested field.

Return ONLY valid JSON in exactly this format:

{{
    "field": "{field}",
    "value": "extracted value"
}}

If you cannot find the value, return:

{{
    "field": "{field}",
    "value": null
}}
"""

    llm_response = llm_client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = llm_response.choices[0].message.content.strip()

    print("LLM response:", result)

    try:

        data = json.loads(result)

        returned_field = data.get("field")

        if returned_field != field:

            print("LLM returned the wrong field.")

            return "INVALID"

        value = data.get("value")

        if value is None:

            return "INVALID"

        # Clean numeric values
        if field in [
            "Basic Salary",
            "HRA",
            "Other Allowance",
            "Gross Salary",
            "TDS",
            "Net Salary"
        ]:

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                str(value)
            )

            if not numbers:

                print("Could not find a number.")

                return "INVALID"

            value = numbers[0]

            print("Extracted numeric value:", value)

            return value

        print("Extracted value:", value)

        return str(value)

    except json.JSONDecodeError:

        print("LLM returned invalid JSON.")

        return "INVALID"



def process_client_response(state: TaxState):

    print("Processing client response...")

    response = state["client_response"].strip()

    missing_field = state["missing_fields"][0]

    print("Processing missing field:", missing_field)

    if not response:

        print("No information provided.")

        return {
            "extracted_data": state["extracted_data"],
            "missing_fields": state["missing_fields"],
            "error_message": "Client did not provide the required information."
        }

    if missing_field:

        try:
            # Ask the LLM to understand the client's response
            parsed_response = parse_client_response_with_llm(
                response,
                missing_field
            )

            if parsed_response == "INVALID":

                print(
                    f"Could not understand the value for {missing_field}."
                )

                return {
                    "extracted_data": state["extracted_data"],
                    "missing_fields": state["missing_fields"],
                    "error_message": f"Could not understand the value for {missing_field}."
                }

            # Numeric fields
            if missing_field in [
                "Basic Salary",
                "HRA",
                "Other Allowance",
                "Gross Salary",
                "TDS",
                "Net Salary"
            ]:

                value = int(parsed_response)

                # Validate numeric value
                if value < 0:

                    print(
                        f"Invalid negative value for {missing_field}."
                    )

                    return {
                        "extracted_data": state["extracted_data"],
                        "missing_fields": state["missing_fields"],
                        "error_message": f"{missing_field} cannot be negative."
                    }
                if value > 10000000:

                    print(f"Value is too large for {missing_field}."
                          )

                    return {
                            "extracted_data": state["extracted_data"],
                             "missing_fields": state["missing_fields"],
                            "error_message": f"{missing_field} value is unrealistically high."
                    }

            # Text fields
            else:

                value = parsed_response

            # Store the extracted value
            state["extracted_data"][missing_field] = value

            # Remove the field from missing fields
            state["missing_fields"].remove(missing_field)

            print(f"{missing_field} received:", value)

            return {
                "extracted_data": state["extracted_data"],
                "missing_fields": state["missing_fields"],
                "error_message": ""
            }

        except ValueError:

            print(f"Invalid value for {missing_field}.")

            return {
                "extracted_data": state["extracted_data"],
                "missing_fields": state["missing_fields"],
                "error_message": f"Invalid value for {missing_field}."
            }



def decide_after_client_response(state: TaxState):

    if state["missing_fields"]:
        return "still_missing"

    return "complete"





def validate_salary_data(state: TaxState):

    print("Validating salary information...")

    data = state["extracted_data"]

    basic_salary = data["Basic Salary"]
    hra = data["HRA"]
    other_allowance = data["Other Allowance"]
    gross_salary = data["Gross Salary"]
    tds = data["TDS"]
    net_salary = data["Net Salary"]

    # Check gross salary
    calculated_gross = basic_salary + hra + other_allowance

    if calculated_gross != gross_salary:

        return {
            "validation_result": "Salary data has a gross salary discrepancy"
        }

    # Check TDS
    if tds > gross_salary:

        return {
            "validation_result": "Salary data has invalid TDS"
        }

    # Check net salary
    calculated_net = gross_salary - tds

    if calculated_net != net_salary:

        return {
            "validation_result": "Salary data has a net salary discrepancy"
        }

    # All validations passed
    result = "Salary data is valid"

    print(result)

    return {
        "validation_result": result,
        "error_message": ""
    }

def decide_after_validation(state: TaxState):

    if state["validation_result"] == "Salary data is valid":
        return "continue"

    return "flag_case"


def flag_case(state: TaxState):

    print("⚠️ Case flagged for CA review.")

    reason = state["validation_result"]
    

    print("Reason:", reason)

    return {
        "validation_result": "result",
        "error_message": reason
    }




def calculate_annual_income(state: TaxState):

    print("Calculating annual income...")

    monthly_income = state["extracted_data"]["Gross Salary"]

    annual_income = monthly_income * 12

    print("Monthly income:", monthly_income)
    print("Annual income:", annual_income)

    return {
        "annual_income": annual_income
    }



def tax_rules_rag(state: TaxState):

    print("Retrieving tax rules...")

    income = state["annual_income"]

    question = f"What is the tax rate for income of {income}?"

    documents = retrieve_rules(question)

    tax_rule = find_matching_rule(
        question,
        documents
    )

    if tax_rule:

        print("Tax rule found:")
        print(tax_rule)

        return {
            "tax_rule": tax_rule
        }

    else:

        print("No matching tax rule found.")

        return {
            "tax_rule": "",
            "error_message": "Tax rule not found for the given income."
        }

def decide_after_tax_rules(state: TaxState):

    if state["tax_rule"]:
        return "rule_found"

    return "rule_missing"




def calculate_tax(state: TaxState):

    print("Calculating tax...")

    annual_income = state["annual_income"]
    tax_rule = state["tax_rule"]

    if not tax_rule:

        print("Cannot calculate tax: tax rule is missing.")

        return {
            "tax_amount": 0,
            "error_message": "Cannot calculate tax because the tax rule is missing."
        }

    # Extract tax percentage from the rule
    match = re.search(r"taxed at (\d+)%", tax_rule)

    if match:

        tax_rate = int(match.group(1))

        tax_amount = annual_income * tax_rate / 100

        print("Annual income:", annual_income)
        print("Tax rate:", tax_rate, "%")
        print("Tax amount:", tax_amount)

        return {
            "tax_amount": tax_amount
        }

    print("Could not determine tax rate.")

    return {
        "tax_amount": 0,
        "error_message": "Could not determine tax rate from the tax rule."
    }

def final_validation(state: TaxState):

    print("Performing final validation...")

    annual_income = state["annual_income"]
    tax_rule = state["tax_rule"]
    tax_amount = state["tax_amount"]

    if not tax_rule:
        return {
            "final_validation": "Failed: Tax rule not found"
        }

    if tax_amount < 0:
        return {
            "final_validation": "Failed: Invalid tax amount"
        }

    if annual_income < 0:
        return {
            "final_validation": "Failed: Invalid annual income"
        }

    print("Final validation successful.")

    return {
        "final_validation": "Passed"
    } 


def ca_review(state: TaxState):

    print("\n--- CA REVIEW ---")

    print("Annual income:", state["annual_income"])
    print("Tax amount:", state["tax_amount"])
    print("Tax rule:")
    print(state["tax_rule"])

    decision = input("CA decision (approve/reject): ").strip().lower()

    if decision not in ["approve", "reject"]:

        print("Invalid CA decision.")

        return {
            "ca_decision": "",
            "error_message": "Invalid CA decision. Expected approve or reject."
        }

    if decision == "approve":

        print("CA approved the case.")

    else:

        print("CA rejected the case.")

    return {
        "ca_decision": decision,
        "error_message": ""
    }

def decide_after_ca_review(state: TaxState):

    if state["ca_decision"] == "approve":
        return "approved"

    if state["ca_decision"] == "reject":
        return "rejected"

    return "invalid"    



def generate_case_summary(state: TaxState):

    print("\nGenerating case summary...")

    summary = f"""
      ===== TAX CASE SUMMARY =====

    Employee: {state["extracted_data"]["Employee Name"]}
    Monthly Income: ₹{state["extracted_data"]["Gross Salary"]}
    Annual Income: ₹{state["annual_income"]}
    Calculated Tax: ₹{state["tax_amount"]}
    CA Decision: {state["ca_decision"].upper()}
    Validation: {state["final_validation"]}
    """

    print(summary)

    return {
        "case_summary": summary
    }

def create_final_output(state: TaxState):

    return {
        "employee": state["extracted_data"]["Employee Name"],
        "annual_income": state["annual_income"],
        "tax_amount": state["tax_amount"],
        "validation": state["final_validation"],
        "ca_decision": state["ca_decision"],
        "case_summary": state["case_summary"],
        "error_message": state["error_message"]
    }


# 3. Create Graph

builder = StateGraph(TaxState)

builder.add_node(
    "classify_documents",
    classify_documents
)

builder.add_node(
    "extract_salary_data",
    extract_salary_data
)

builder.add_node(
    "check_missing_information",
    check_missing_information
)

builder.add_node(
    "validate_salary_data",
    validate_salary_data
)

builder.add_node(
    "calculate_annual_income",
    calculate_annual_income
)

builder.add_node(
    "tax_rules_rag",
    tax_rules_rag
)

builder.add_node(
    "calculate_tax",
    calculate_tax
)

builder.add_node(
    "final_validation",
    final_validation
)

builder.add_node(
    "ca_review",
    ca_review
)

builder.add_node(
    "generate_case_summary",
    generate_case_summary
)


builder.add_node(
    "ask_client",
    ask_client
)

builder.add_node(
    "process_client_response",
    process_client_response
)

builder.add_node(
    "flag_case",
    flag_case
)


# ---------- Edges ----------


builder.set_entry_point("classify_documents")

builder.add_edge(
    "classify_documents",
    "extract_salary_data"
)

builder.add_edge(
    "extract_salary_data",
    "check_missing_information"
)


# ---------- Missing Information Routing ----------

builder.add_conditional_edges(
    "check_missing_information",
    decide_after_missing_check,
    {
        "missing": "ask_client",
        "complete": "validate_salary_data"
    }
)


# ---------- Client Response ----------

builder.add_edge(
    "ask_client",
    "process_client_response"
)

builder.add_conditional_edges(
    "process_client_response",
    decide_after_client_response,
    {
        "still_missing": END,
        "complete": "validate_salary_data"
    }
)


# ---------- Validation Routing ----------

builder.add_conditional_edges(
    "validate_salary_data",
    decide_after_validation,
    {
        "continue": "calculate_annual_income",
        "flag_case": "flag_case"
    }
)

# ---------- Annual Income ----------

builder.add_edge(
    "calculate_annual_income",
    "tax_rules_rag"
)

# ---------- Tax Rules RAG ---------- 
builder.add_conditional_edges(
    "tax_rules_rag",
    decide_after_tax_rules,
    {
        "rule_found": "calculate_tax",
        "rule_missing": END
    }
)

builder.add_edge(
    "calculate_tax",
    "final_validation"
)

builder.add_edge(
    "final_validation",
    "ca_review"
)

builder.add_conditional_edges(
    "ca_review",
    decide_after_ca_review,
    {
        "approved": "generate_case_summary",
        "rejected": "generate_case_summary",
        "invalid": END
    }
)

builder.add_edge(
    "generate_case_summary",
    END
)


# ---------- Flag Case ----------

builder.add_edge(
    "flag_case",
    END
)


# 4. Compile
graph = builder.compile()


# 5. Test
client_response = input("Enter missing information: ")
result = graph.invoke({
    "documents": [
        "Form16.pdf",
        "Salary_April.pdf",
        "Salary_May.pdf",
        "Bank_Statement.pdf",
        "Investment_Proof.pdf",
        "Home_Loan.pdf"
    ],
    "document_types": {},
    "extracted_data": {},
    "validation_result": "",
    "missing_fields": [],
    "client_response": client_response,
    "annual_income": 0,
    "tax_rule": "",
    "tax_amount": 0,
    "final_validation": "",
    "ca_decision": "",
    "case_summary": ""
})

final_output = create_final_output(result)

print("\nFINAL OUTPUT:")
print(final_output)

response = "My TDS amount is 5000 rupees"
field = "TDS"

test_response = parse_client_response_with_llm(
    response,
    field
)

print("TEST RESULT:", test_response)

