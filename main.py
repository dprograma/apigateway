# main.py
import json
from fastapi import FastAPI, Request, Response, status
import httpx
from fastapi.middleware.cors import CORSMiddleware
from httpx import Timeout
from urllib.parse import urlparse, urlunparse

app = FastAPI()

# Middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the URLs of Django services
USERSERVICE_URL = 'http://localhost:8001/gateway/api/v1'
MERCHANTSERVICE_URL = 'http://localhost:8002/api/onboarding'
KYCSERVICE_URL = 'http://localhost:8002/api/kyc'
PAYMENTGATEWAYSERVICE_URL = 'http://localhost:8003/gateway/api/v0'
WALLETSERVICE_URL = 'http://localhost:8004/wallets'
WALLETTRASACTIONSERVICE_URL = 'http://localhost:8004/wallets/transactions'

# Define the URLs of the Frontend service
CLIENTSERVICE_URL = 'http://127.0.0.1:3000'



@app.api_route('/userservice/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def userservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None
    
    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the UserService
        response = await client.request(
            method=request.method,
            url=f"{USERSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        if response.status_code in (301, 302):
            # Get the original Location header
            location = response.headers.get('Location')
            # Modify the Location header to include the correct port
            new_location = modify_location_header(location, 8001)

            # Create a new RedirectResponse
            return Response(status_code=status.HTTP_301_MOVED_PERMANENTLY, headers={"Location": new_location})
    
        # return response.json()
        if response.status_code != 200:
            # Handle non-200 responses or add more specific checks
            return Response(content=response.content, status_code=response.status_code)

        try:
            return response.json()
        except json.JSONDecodeError:
            # Handle the case where response is not JSON
            # Forward the original response content and status code
            return Response(content=response.content, status_code=response.status_code)
    
    

@app.api_route('/merchantservice/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def merchantservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None
    
    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the MerchantService
        response = await client.request(
            method=request.method,
            url=f"{MERCHANTSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        
        if response.status_code in (301, 302):
            # Get the original Location header
            location = response.headers.get('Location')
            # Modify the Location header to include the correct port
            new_location = modify_location_header(location, 8002)

            # Create a new RedirectResponse
            return Response(status_code=status.HTTP_301_MOVED_PERMANENTLY, headers={"Location": new_location})
    
        # return response.json()
        if response.status_code != 200:
            # Handle non-200 responses or add more specific checks
            return Response(content=response.content, status_code=response.status_code)

        try:
            return response.json()
        except json.JSONDecodeError:
            # Handle the case where response is not JSON
            # Forward the original response content and status code
            return Response(content=response.content, status_code=response.status_code)
        
        
@app.api_route('/kycservice/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def merchantservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None
    
    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the MerchantService
        response = await client.request(
            method=request.method,
            url=f"{KYCSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        
        if response.status_code in (301, 302):
            # Get the original Location header
            location = response.headers.get('Location')
            # Modify the Location header to include the correct port
            new_location = modify_location_header(location, 8002)

            # Create a new RedirectResponse
            return Response(status_code=status.HTTP_301_MOVED_PERMANENTLY, headers={"Location": new_location})
    
        # return response.json()
        if response.status_code != 200:
            # Handle non-200 responses or add more specific checks
            return Response(content=response.content, status_code=response.status_code)

        try:
            return response.json()
        except json.JSONDecodeError:
            # Handle the case where response is not JSON
            # Forward the original response content and status code
            return Response(content=response.content, status_code=response.status_code)
    
    
@app.api_route('/paymentgatewayservice/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def paymentgatewayservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None

    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the PaymentGatewayService
        response = await client.request(
            method=request.method,
            url=f"{PAYMENTGATEWAYSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        return response.json()
    
    
@app.api_route('/walletservice/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def walletservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None

    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the WalletService
        response = await client.request(
            method=request.method,
            url=f"{WALLETSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        return response.json()
    

@app.api_route('/wallettransactionservice/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def wallettransactionservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None

    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the WalletTransactionService
        response = await client.request(
            method=request.method,
            url=f"{WALLETTRASACTIONSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        return response.json()


@app.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def userservice_proxy(request: Request, path: str):
    # Remove problematic headers
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'content-length']}

    # Determine the correct content to send
    content = await request.body() if request.method in ["POST", "PUT"] else None
    
    timeout = Timeout(60.0)
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Forward the request to the UserService
        response = await client.request(
            method=request.method,
            url=f"{CLIENTSERVICE_URL}/{path}",
            headers=headers,
            content=content,
            params=request.query_params,
        )
        if response.status_code in (301, 302):
            # Get the original Location header
            location = response.headers.get('Location')
            # Modify the Location header to include the correct port
            new_location = modify_location_header(location, 8001)

            # Create a new RedirectResponse
            return Response(status_code=status.HTTP_301_MOVED_PERMANENTLY, headers={"Location": new_location})
    
        # return response.json()
        if response.status_code != 200:
            # Handle non-200 responses or add more specific checks
            return Response(content=response.content, status_code=response.status_code)

        try:
            return response.json()
        except json.JSONDecodeError:
            # Handle the case where response is not JSON
            # Forward the original response content and status code
            return Response(content=response.content, status_code=response.status_code)


def modify_location_header(location, new_port):
    parsed_url = urlparse(location)

    # Split the netloc into host and (optional) current port
    host, _, current_port = parsed_url.netloc.partition(':')

    host = "127.0.0.1"
    if current_port:
        new_netloc = f"{host}:{new_port}"
    else:
        new_netloc = f"{host}:{new_port}"

    # Construct the new URL with the updated netloc
    new_url = urlunparse(parsed_url._replace(netloc=new_netloc))
    return new_url

