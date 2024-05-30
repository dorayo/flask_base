from flask import current_app
from obs import ObsClient
from obs import PutObjectHeader
import os
import traceback
from app.utils.file_upload import get_storage_path

ak = os.getenv("HW_Access_Key_ID")
sk = os.getenv("HW_Secret_Access_Key")
server = "https://obs.cn-north-4.myhuaweicloud.com"
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)

def upload_file(file,file_name):
  '''
  上传文件到华为云对象存储服务（OBS）
  '''
  try:
      # 读取文件流
      content = file.stream
      bucketName = "storage-bucket-2024"
      objectKey = get_storage_path(file_name)
      # 流式上传
      resp = obsClient.putContent(bucketName, objectKey, content)

      # 返回码为2xx时，接口调用成功，否则接口调用失败
      if resp.status < 300:
          current_app.logger.debug('Put Content Succeeded')
          current_app.logger.debug(f'requestId: {resp.requestId}')
          img_url = f"https://storage-bucket-2024.obs.cn-north-4.myhuaweicloud.com/{objectKey}"
          return img_url
      else:
          current_app.logger.error(f'Put Content Failed')
          current_app.logger.error(f'requestId:', {resp.requestId})
          current_app.logger.error(f'errorCode:', {resp.errorCode})
          current_app.logger.error(f'errorMessage:', {resp.errorMessage})
          return False
  except:
      current_app.logger.error('Put Content Failed')
      return False
