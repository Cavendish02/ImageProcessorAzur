import azure.functions as func
import logging
import sys
from pathlib import Path

# إضافة مسار المشروع إلى sys.path
sys.path.append(str(Path(__file__).parent.parent))

from shared.image_processor import process_image

app = func.FunctionApp()

@app.function_name(name="ImageProcessor")
@app.blob_trigger(
    arg_name="myblob",
    path="uploads/{name}",
    connection="AzureWebJobsStorage"
)
@app.blob_output(
    arg_name="outputBlob",
    path="processed/{name}",
    connection="AzureWebJobsStorage"
)
def main(myblob: func.InputStream, outputBlob: func.Out[bytes]):
    """دالة الزناد لمعالجة الصور المرفوعة"""
    try:
        logging.info(f"بدء معالجة الصورة: {myblob.name}")
        process_image(myblob, outputBlob)
        logging.info(f"تم الانتهاء من معالجة {myblob.name}")
    except Exception as e:
        logging.error(f"فشل معالجة {myblob.name}: {str(e)}", exc_info=True)
        raise