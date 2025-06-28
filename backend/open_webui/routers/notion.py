from fastapi import APIRouter, Request, Depends, HTTPException, status, Query
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode
import requests

from open_webui.config import NOTION_CLIENT_ID, NOTION_CLIENT_SECRET, NOTION_REDIRECT_URI
from open_webui.utils.auth import get_verified_user
from typing import Optional
from pydantic import BaseModel
from open_webui.internal.wrappers.notion import NotionClient
from open_webui.models.notion_integration import NotionIntegrationTable, NotionIntegrationModel
from open_webui.models.notion_integration import NotionIntegration as SQLNotionIntegration
from open_webui.internal.db import engine
from sqlalchemy.exc import OperationalError

router = APIRouter()

@router.get("/connect", status_code=status.HTTP_302_FOUND)
async def notion_connect(
    request: Request,
    user=Depends(get_verified_user),
    project_id: str = Query(..., description="Project ID to connect Notion to")
):
    """
    Redirects the user to Notion's OAuth consent page, preserving the project_id in state.
    """
    client_id = NOTION_CLIENT_ID.value
    redirect_uri = NOTION_REDIRECT_URI.value
    if not client_id or not redirect_uri:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Notion OAuth is not configured. Set NOTION_CLIENT_ID and NOTION_REDIRECT_URI."
        )
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "owner": "user",
        "scope": "database.read database.write pages.read pages.write",
        "state": project_id,
    }
    url = f"https://api.notion.com/v1/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
async def notion_callback(
    request: Request,
    user=Depends(get_verified_user)
):
    """
    Handles the OAuth callback from Notion, exchanges the code for a token, reads project_id from state, and sets a secure cookie.
    """
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code or not state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code or state"
        )
    token_url = "https://api.notion.com/v1/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": NOTION_REDIRECT_URI.value,
    }
    auth = (NOTION_CLIENT_ID.value, NOTION_CLIENT_SECRET.value)
    headers = {"Content-Type": "application/json"}
    resp = requests.post(token_url, json=data, auth=auth, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Token exchange failed: {resp.text}"
        )
    token_data = resp.json()
    # Set the Notion access token in a secure HTTP-only cookie
    redirect_to = f"/projects/{state}/planning"
    response = RedirectResponse(url=redirect_to)
    response.set_cookie(
        key="notion_token",
        value=token_data.get("access_token"),
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return response

@router.get("/status")
async def notion_status(
    request: Request,
    user=Depends(get_verified_user),
    project_id: str = Query(..., description="Project ID to check connection for")
):
    """
    Returns whether the user has a Notion token cookie set.
    """
    token = request.cookies.get("notion_token")
    return JSONResponse({"connected": bool(token)})


class IntegrationForm(BaseModel):
    database_id: str

@router.get("/integration")
async def get_integration(
    request: Request,
    user=Depends(get_verified_user),
    project_id: str = Query(..., description="Project ID to get integration for")
):
    """Get the Notion database ID configured for this project"""
    try:
        row = NotionIntegrationTable.get_by_project(project_id)
    except OperationalError:
        # If the integration table doesn't exist yet, create it and return no integration
        SQLNotionIntegration.__table__.create(bind=engine, checkfirst=True)
        row = None
    return {"database_id": row.database_id if row else None}

@router.post("/integration")
async def set_integration(
    request: Request,
    form_data: IntegrationForm,
    user=Depends(get_verified_user),
    project_id: str = Query(..., description="Project ID to set integration for")
):
    """Set the Notion database ID for this project"""
    try:
        row = NotionIntegrationTable.upsert(project_id, form_data.database_id)
    except OperationalError:
        # If the integration table doesn't exist yet, create it then retry
        SQLNotionIntegration.__table__.create(bind=engine, checkfirst=True)
        row = NotionIntegrationTable.upsert(project_id, form_data.database_id)
    return {"database_id": row.database_id}

@router.get("/databases")
async def list_databases(
    request: Request,
    user=Depends(get_verified_user),
    project_id: str = Query(..., description="Project ID for context")
):
    """List available Notion databases in the connected workspace"""
    token = request.cookies.get("notion_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not connected to Notion")
    client = NotionClient(token)
    return client.list_databases()

@router.get("/pages")
async def list_pages(
    request: Request,
    user=Depends(get_verified_user),
    project_id: str = Query(..., description="Project ID for context"),
    start_cursor: Optional[str] = None
):
    """Query pages from the configured Notion database"""
    token = request.cookies.get("notion_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not connected to Notion")
    integration = NotionIntegrationTable.get_by_project(project_id)
    if not integration or not integration.database_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Notion database configured for this project")
    client = NotionClient(token)
    return client.query_database(
        database_id=integration.database_id,
        start_cursor=start_cursor,
    )