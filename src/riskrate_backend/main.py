from fastapi import FastAPI

from riskrate_backend.api.v1 import address

app = FastAPI()


app.include_router(address.router, prefix="/api/v1/addresses", tags=["Addresses"])
