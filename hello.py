import uvicorn
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3
#from botocore.client import Config
# fastapi app instance
app = FastAPI()
# s3 client instance
s3 = boto3.client('s3') 
# name of the s3 bucket
bucket_name = 'samydb'
# the origin of the requests to make a valid CORS request
origin:list[str] = ["*"]
# add CORS middleware to the apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# add a simple root path to the app
@app.get("/")
async def root():
    """
    this function handles the root path
    :return: hello world
    """
    return {"message": "Hello World"}



# file upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    this function handles uploading files to s3 bucket
    :param file: the file to upload
    :return: the filename of the uploaded file
    """
    file_content = await file.read()
    try:      
        s3.put_object(
            Bucket=bucket_name,
            Key=file.filename,
            Body=file_content,
            ContentType=file.content_type
        )
        return JSONResponse(content={"filename": file.filename,
                                      "message": "Upload successful"}, status_code=200)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    



# file list endpoint
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
    return JSONResponse(content={"files": files}, status_code=200)




# getting a pre-signed url for a file to download in the browser 
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
    # uvicorn config 
    uvicorn.run("hello:app", host="127.0.0.1",port=8000, reload=True)
