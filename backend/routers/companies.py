"""Companies router — multi-tenant workspace & team management"""
import logging
import uuid
from datetime import datetime
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, EmailStr

from dependencies.auth import TokenData, get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory store — replace with Supabase + RLS in production
_COMPANIES: dict = {}
_MEMBERS: dict = {}


class CompanyRegisterRequest(BaseModel):
    company_name: str
    slug: str
    industry: str
    admin_name: str
    email: EmailStr
    password: str


class InviteMemberRequest(BaseModel):
    email: EmailStr
    role: Literal["admin", "analyst", "viewer"]  # validated — no arbitrary role strings
    name: Optional[str] = None


@router.post("/register", status_code=201)
async def register_company(req: CompanyRegisterRequest):
    """Public endpoint — called during onboarding before user has a token."""
    if req.slug in _COMPANIES:
        raise HTTPException(status_code=409, detail=f"Workspace '{req.slug}' already exists.")
    cid = str(uuid.uuid4())
    _COMPANIES[req.slug] = {
        "id": cid,
        "name": req.company_name,
        "slug": req.slug,
        "industry": req.industry,
        "plan": "starter",
        "created_at": datetime.utcnow().isoformat(),
    }
    _MEMBERS[cid] = [
        {
            "id": str(uuid.uuid4()),
            "company_id": cid,
            "name": req.admin_name,
            "email": str(req.email),
            "role": "admin",
            "status": "active",
            "last_active": datetime.utcnow().isoformat(),
        }
    ]
    return {"message": "Workspace created", "company_id": cid, "redirect": f"/dashboard/{req.slug}"}


@router.get("/{company_id}")
async def get_company(
    company_id: str = Path(...),
    current_user: TokenData = Depends(get_current_user),
):
    for slug, co in _COMPANIES.items():
        if co["id"] == company_id or slug == company_id:
            return co
    raise HTTPException(status_code=404, detail="Company not found.")


@router.get("/{company_id}/team")
async def get_team(
    company_id: str = Path(...),
    current_user: TokenData = Depends(get_current_user),
):
    return _MEMBERS.get(company_id, [])


@router.post("/{company_id}/invite", status_code=201)
async def invite_member(
    req: InviteMemberRequest,
    company_id: str = Path(...),
    current_user: TokenData = Depends(get_current_user),
):
    if current_user.role not in ("admin",):
        raise HTTPException(status_code=403, detail="Only admins can invite members.")
    if company_id not in _MEMBERS:
        raise HTTPException(status_code=404, detail="Company not found.")
    member = {
        "id": str(uuid.uuid4()),
        "company_id": company_id,
        "name": req.name or str(req.email).split("@")[0].title(),
        "email": str(req.email),
        "role": req.role,
        "status": "pending",
        "last_active": None,
    }
    _MEMBERS[company_id].append(member)
    return {"message": f"Invite sent to {req.email}", "member_id": member["id"]}


@router.delete("/{company_id}/team/{member_id}")
async def remove_member(
    company_id: str,
    member_id: str,
    current_user: TokenData = Depends(get_current_user),
):
    if current_user.role not in ("admin",):
        raise HTTPException(status_code=403, detail="Only admins can remove members.")
    members = _MEMBERS.get(company_id, [])
    updated = [m for m in members if m["id"] != member_id]
    if len(updated) == len(members):
        raise HTTPException(status_code=404, detail="Member not found.")
    _MEMBERS[company_id] = updated
    return {"message": "Member removed"}
