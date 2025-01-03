import subprocess
from celery import Celery
from tik_tok.core.config import settings

celery_app = Celery("tasks", broker=settings.rabbitmq_url)

@celery_app.task(bind=True, name="generate_video_thumbnail")
def generate_video_thumbnail(self, video_path: str, output_path: str):
    try:
        # Генерация миниатюры с помощью ffmpeg
        command = [
            "ffmpeg",
            "-i", video_path,
            "-ss", "00:00:01.000",
            "-vframes", "1",
            output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise self.retry(exc=e)
    

def s3_bucket_service_factory(config_file: str):
    class MockS3Service:
        async def upload_file(self, file_path, key):
            return True

        async def delete_file(self, key):
            return True

        async def list_files(self, prefix):
            return ["test1.mp4", "test2.mp4", "test3.mp4"]
    
    return MockS3Service()