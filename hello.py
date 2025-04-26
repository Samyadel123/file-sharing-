import uvicorn
from fastapi import FastAPI
from fastapi import File, UploadFile
import boto3
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    this function handles uploading files to s3 bucket
    :param file: the file to upload
    :return: the filename of the uploaded file
    """
    #TODO: make the upload logic
    return {"filename": file.filename}
@app.get("/file_list")
async def get_file_list():
    """
    this function handles getting the list of files in the s3 bucket
    :return: the list of files in the s3 bucket
    """
    #TODO: make the get file list logic
    return {"files": ["file1.txt", "file2.txt"]}
@app.get("/get_pre_signed_url{file_name}")
async def get_pre_signed_url(file_name: str):
    """
    this function handles getting the pre-signed url for a file in the s3 bucket
    :param file_name: the name of the file to get the pre-signed url for
    :return: the pre-signed url for the file
    """
    #TODO: make the get pre-signed url logic
def main():
    config = uvicorn.Config("hello:app", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.serve()


if __name__ == "__main__":
    main()
