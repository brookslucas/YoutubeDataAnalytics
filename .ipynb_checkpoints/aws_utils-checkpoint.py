from fastapi import FastAPI, UploadFile, File
from aws_utils import upload_to_s3

app = FastAPI()

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    location = f"temp/{file.filename}"
    with open(location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Now upload to S3
    result = upload_to_s3(location, "your-s3-bucket-name")
    if result:
        return {"message": "File uploaded successfully"}
    else:
        return {"message": "File upload failed"}
