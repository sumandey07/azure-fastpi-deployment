# Azure FastAPI

A [FastAPI](https://fastapi.tiangolo.com/) service packaged for **Azure Functions**
using the Python v2 programming model. Every HTTP request is forwarded to FastAPI
via the ASGI middleware, so you write plain FastAPI code and deploy it serverless.

## Project layout

```
function_app.py        # Azure Functions entry point (wraps the FastAPI app)
host.json              # Functions host config (routePrefix = "api")
local.settings.json    # Local-only settings (not deployed)
requirements.txt       # Python dependencies
app/
  main.py              # FastAPI app factory + root/health routes
  schemas.py           # Pydantic models
  store.py             # Example in-memory data store
  routers/items.py     # Item CRUD routes
tests/test_api.py      # FastAPI tests (no Functions host needed)
```

Because `host.json` sets `routePrefix: "api"`, all endpoints are served under
`/api`. `ROOT_PATH=/api` keeps the OpenAPI docs and links correct.

## Prerequisites

- Python 3.10–3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Azure Functions Core Tools v4](https://learn.microsoft.com/azure/azure-functions/functions-run-local)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- An Azure subscription

## Run locally

```powershell
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt

# Start the Functions host (needs Azurite or a storage connection string)
func start
```

Then open:

- Swagger UI: http://localhost:7071/api/docs
- Health: http://localhost:7071/api/health
- Items: http://localhost:7071/api/items

Run the tests directly against FastAPI (no host required):

```powershell
uv pip install pytest httpx
uv run pytest
```

## Deploy to Azure

1. Sign in and pick a subscription:

   ```powershell
   az login
   ```

2. Create the resources (Linux Consumption plan). Storage account names must be
   globally unique and lowercase:

   ```powershell
   $rg="rg-azure-fastapi"
   $loc="eastus"
   $storage="stfastapi$((Get-Random))"
   $app="func-fastapi-$((Get-Random))"

   az group create --name $rg --location $loc
   az storage account create --name $storage --resource-group $rg --location $loc --sku Standard_LRS
   az functionapp create --resource-group $rg --consumption-plan-location $loc `
     --runtime python --runtime-version 3.11 --functions-version 4 `
     --name $app --storage-account $storage --os-type Linux
   ```

3. Configure the root path so docs/links resolve behind `/api`:

   ```powershell
   az functionapp config appsettings set --name $app --resource-group $rg `
     --settings ROOT_PATH=/api
   ```

4. Publish the code:

   ```powershell
   func azure functionapp publish $app
   ```

After publishing, your API is at:
`https://<app-name>.azurewebsites.net/api/docs`

## Extending

- Replace `app/store.py` with a real database (Azure Cosmos DB, Azure SQL, etc.).
- Add routers under `app/routers/` and include them in `app/main.py`.
- Set `http_auth_level=func.AuthLevel.FUNCTION` in `function_app.py` to require a
  function key instead of anonymous access.
