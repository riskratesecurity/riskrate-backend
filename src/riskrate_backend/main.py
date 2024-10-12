from fastapi import FastAPI
from riskrate_backend.api.v1 import address, auth


app = FastAPI()


app.include_router(address.router, prefix="/api/v1/addresses", tags=["Addresses"])
app.include_router(auth.router)