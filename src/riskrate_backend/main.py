from fastapi import FastAPI

from riskrate_backend.api.v1 import address, gpt_service_test

app = FastAPI()


app.include_router(address.router, prefix="/api/v1/addresses", tags=["Addresses"])
app.include_router(gpt_service_test.router, prefix="/api/v1/gpt", tags=["GPT - test"])
