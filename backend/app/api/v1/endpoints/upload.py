from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import List
from app.core.security import get_current_admin_user
from app.services.s3_service import S3Service

router = APIRouter()


@router.post("/")
def upload_image(
    file: UploadFile = File(...),
    folder: str = "general",
    current_user=Depends(get_current_admin_user)
):
    """Upload image to S3 (admin only)."""
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Generate unique filename
    import uuid
    file_ext = file.filename.split(".")[-1]
    file_name = f"{folder}/{uuid.uuid4()}.{file_ext}"

    # Upload to S3
    s3_service = S3Service()
    url = s3_service.upload_file(file.file, file_name, file.content_type)

    if not url:
        raise HTTPException(status_code=500, detail="Failed to upload image")

    return {"url": url}
