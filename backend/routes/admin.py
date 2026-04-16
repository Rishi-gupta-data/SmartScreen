from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.schemas.admin_schema import AdminCreate, AdminUpdate, AdminResponse, AdminListResponse, AdminStats
from backend.db.connection import get_db
from backend.utils.deps import admin_only, get_current_user
from backend.services import admin as admin_service
from backend.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
    current_user=Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics - Admin only"""
    try:
        stats = admin_service.get_admin_stats(db)
        return AdminStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")


@router.get("/list", response_model=List[AdminListResponse])
def list_admins(
    current_user=Depends(admin_only),
    db: Session = Depends(get_db)
):
    """List all admin users - Admin only"""
    try:
        admins = admin_service.get_all_admins(db)
        return admins
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching admins: {str(e)}")


@router.get("/{admin_id}", response_model=AdminResponse)
def get_admin(
    admin_id: str,
    current_user=Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Get specific admin details - Admin only"""
    try:
        admin = admin_service.get_admin_by_id(db, admin_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching admin: {str(e)}")


@router.post("/create", response_model=AdminResponse)
def create_admin(
    admin_in: AdminCreate,
    current_user=Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Create a new admin user - Admin only"""
    try:
        # Check if email already exists
        existing = db.query(User).filter(User.email == admin_in.email).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create admin
        admin = admin_service.create_admin(db, admin_in.email, admin_in.password)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create admin"
            )
        return admin
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating admin: {str(e)}")


@router.put("/{admin_id}", response_model=AdminResponse)
def update_admin(
    admin_id: str,
    admin_in: AdminUpdate,
    current_user=Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Update admin details - Admin only"""
    try:
        admin = admin_service.update_admin(
            db,
            admin_id,
            email=admin_in.email,
            password=admin_in.password
        )
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found or email already in use")
        return admin
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating admin: {str(e)}")


@router.delete("/{admin_id}")
def delete_admin(
    admin_id: str,
    current_user=Depends(admin_only),
    db: Session = Depends(get_db)
):
    """Delete an admin user - Admin only"""
    try:
        # Prevent self-deletion
        if current_user["id"] == admin_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own admin account"
            )
        
        success = admin_service.delete_admin(db, admin_id)
        if not success:
            raise HTTPException(status_code=404, detail="Admin not found")
        
        return {"message": "Admin deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting admin: {str(e)}")
