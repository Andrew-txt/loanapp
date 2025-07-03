from fastapi import FastAPI
from fastapi.params import Query
from fastapi import HTTPException
import uvicorn
from app.classes.classes import Bank, Client, Credit

app = FastAPI()

banks_storage = []

#Bank-------------------------------------------
@app.get("/my_banks")
async def banks():
    return banks_storage

@app.post("/banks/{bank_name}/")
async def add_bank(bank_name: str):
    if any(bank.name == bank_name for bank in banks_storage):
        return {
            "detail": f"Bank {bank_name} already exists"
        }

    bank = Bank(name=bank_name)
    banks_storage.append(bank)

    return {
        f"Bank {bank.name} is in storage now."
    }

@app.delete("/banks/{bank_name}")
async def delete_bank(bank_name):
    bank_index = next(
        (i for i, bank in enumerate(banks_storage) if bank.name == bank_name),
        None
    )

    if bank_index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Bank not found"
        )

    deleted_bank = banks_storage.pop(bank_index)

    return {
        "detail": f"Bank {deleted_bank.name} deleted."
    }


@app.get("/banks/{bank_name}/statistics")
async def statistics(bank_name):
    bank = next((b for b in banks_storage if b.name == bank_name), None)
    return bank.statistics()

#Client----------------------------
@app.post("/banks/{bank_name}/clients")
async def add_client(bank_name, name, age, client_id, ):
    bank = next((b for b in banks_storage if b.name == bank_name), None)
    if any(client.client_id == client_id for bank in banks_storage for client in bank.clients):
        return {
                "detail": f"Client with {client_id} exists"
        }

    client = Client(name=name, age=age, client_id=client_id)
    bank.clients.append(client)

    return {
            "bank": bank_name,
            "client": {
                "name": client.name,
                "age": client.age,
                "client_id": client.client_id,
                "credit": []
            }
        }

@app.delete("/delete_client/banks/{bank_name}/clients/{client_id}")
async def delete_client(client_id, bank_name):
    bank = next((b for b in banks_storage if b.name == bank_name), None)
    for i, client in enumerate(bank.clients):
        if client.client_id == client_id:
            deleted_client = bank.clients.pop(i)
            return {
                "message": f"Lox {deleted_client.name}, with ID {deleted_client.client_id} deleted."
            }

#Credits---------------------------------------------------
@app.post("/add_credit/banks/{bank_name}/credits")
async def add_credit(
        bank_name: str,
        client_id: str = Query(...),
        credit_id: str = Query(...),
        size: float = Query(...),
        term: int = Query(...),
        annual_rate: float = Query(...),
        date: str = Query(..., regex="^\d{2}-\d{2}-\d{4}$",  example="02-03-2023")
):
    bank = next((b for b in banks_storage if b.name == bank_name), None)
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found.")

    client = next((c for c in bank.clients if c.client_id == client_id), None)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    # client = next((c for c in clients_storage if c.client_id == client_id), None)
    # if not client:
    #     raise HTTPException(status_code=404, detail="Client not found")

    credit = Credit(
        credit_id=credit_id,
        client_id=client_id,
        size=size,
        term=term,
        annual_rate=annual_rate
    )

    schedule = credit.amortize(size=size, annual_rate=annual_rate, term=term)

    if not hasattr(client, "credits"):
        client.credits = []
    client.credits.append(credit)

    return {
        "client": {
            "name": client.name,
            "age": client.age,
            "client_id": client.client_id
        },
        "credit": {
            "bank_name": bank_name,
            "credit_id": credit_id,
            "client_id": credit.client_id,
            "size": credit.size,
            "term": credit.term,
            "annual_rate": credit.annual_rate,
            "monthly_payment": credit.monthly_payment,
            "date": date
        },
            "payment_schedule": schedule

    }

@app.delete("/delete_credit/banks/{bank_name}/credits/{credit_id}")
async def delete_credit(bank_name, client_id: str, credit_id: str):
    bank = next((b for b in banks_storage if b.name == bank_name), None)

    client = next((c for c in bank.clients if c.client_id == client_id), None)

    for i, credit in enumerate(client.credits):
        if getattr(credit, "credit_id", None) == credit_id:
            deleted_credit = client.credits.pop(i)
            return {
                "detail": f"Credit with ID {deleted_credit.credit_id} deleted."
            }

    return {
        "detail": f"Credit not found."
    }










if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=2673)