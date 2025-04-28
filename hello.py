import uvicorn
from fastapi import FastAPI
from fastapi import File, UploadFile
import boto3
app = FastAPI()
s3 = boto3.client('s3') 
bucket_name = 'samydb'

@app.get("/")
async def root():
    """
    this function handles the root path
    :return: hello world
    """
    return {"message": "Hello World"}
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    this function handles uploading files to s3 bucket
    :param file: the file to upload
    :return: the filename of the uploaded file
    """
    file_content = await file.read()
    try:
        s3.put_object(Bucket=bucket_name, Key=file.filename)        
        s3.put_object(
            Bucket=bucket_name,
            Key=file.filename,
            Body=file_content,
            ContentType=file.content_type
        )
    except Exception as e:
        return {"error": str(e)}
    return {"filename": file.filename}
    
    
@app.get("/file_list")
async def get_file_list():
    """
    this function handles getting the list of files in the s3 bucket
    :return: the list of files in the s3 bucket
    """
    
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        files = [item['Key'] for item in response['Contents']]
    else:
        files = []
    return {"files": files}
@app.get("/get_pre_signed_url{file_name}")
async def get_pre_signed_url(file_name: str):
    """
    this function handles getting the pre-signed url for a file in the s3 bucket
    :param file_name: the name of the file to get the pre-signed url for
    :return: the pre-signed url for the file
    """
   
    response = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': file_name},
        ExpiresIn=3600
    )
    return {"url": response}

if __name__ == "__main__":
    """
    this function handles running the app
    :return: none
    """
    uvicorn.run("hello:app", host="127.0.0.1",port=8000, reload=True)
