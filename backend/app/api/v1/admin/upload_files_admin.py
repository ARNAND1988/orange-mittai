# routes/admin_products.py
from fastapi import APIRouter, UploadFile, File
from services.gcs import upload_product_image
from app.utils.admin import require_admin


router = APIRouter()

@router.post("/upload-image")
async def upload_image(
        file: UploadFile = File(...),
        admin: User = Depends(require_admin)  # 🔒 ONLY ADMINS
):
    print("Upload file")
    image_url = upload_product_image(file)
    return {"image_url": image_url}