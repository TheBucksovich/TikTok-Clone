from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tik_tok.core.database import get_async_session
from tik_tok.core.s3_client import S3Client
from tik_tok.core.config import settings
from tik_tok.models.videos import Video

router = APIRouter()
s3_client = S3Client(bucket_name=settings.s3_bucket_name)

@router.post("/upload/")
async def upload_video(file: UploadFile = File(...), 
                       db: AsyncSession = Depends(get_async_session),
                       ):
    if file.content_type not in ["video/mp4", "video/mkv"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Test S3 connectivity
    try:
        await s3_client.test_connection()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"S3 connection failed: {e}")

    video = Video(
        title=file.filename, 
        file_url=f"{settings.s3_endpoint}/{settings.s3_bucket_name}/{file.filename}"
    )
    db.add(video)
    await db.commit()

    try:
        await s3_client.upload_file(file, file.filename)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {e}")

    return {"message": "Видео загружено успешно"}

@router.delete("/delete/{key}")
async def delete_video(key: str):
    await s3_client.delete_file(key)
    return {"message": "File deleted successfully"}

@router.get("/download/{key}")
async def download_video(key: str):
    file_content = await s3_client.download_file(key)
    return {"file_content": file_content}

@router.get("/videos/")
async def list_videos():
    try:
        files = await s3_client.list_files("uploads")
        return {"videos": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching videos: {e}")