import os
import uuid
import requests
from dotenv import load_dotenv
import oss2


class OSSUtil:
    # 通过类属性来设置通用配置
    load_dotenv()
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = os.getenv('ACCESS_KEY_SECRET')
    ENDPOINT = 'http://oss-cn-guangzhou.aliyuncs.com'
    BUCKET_NAME = 'socket-demo'

    @staticmethod
    def download(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download image from {url}")

    @staticmethod
    def upload_image(image_url):
        # 从 URL 下载图片
        image_data = OSSUtil.download(image_url)

        # 生成 UUID 作为文件名
        file_name = f"{uuid.uuid4()}.jpg"

        # 创建 OSS Bucket 实例
        auth = oss2.Auth(OSSUtil.ACCESS_KEY_ID, OSSUtil.ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, OSSUtil.ENDPOINT, OSSUtil.BUCKET_NAME)

        # 上传到 OSS
        bucket.put_object(file_name, image_data)

        # 返回文件的 URL
        return f"https://{OSSUtil.BUCKET_NAME}.{OSSUtil.ENDPOINT.split('//')[1]}/{file_name}"
