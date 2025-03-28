from PIL import Image
import io
import logging

def process_image(input_blob, output_blob):
    """تحويل الصور إلى تدرج رمادي وتحسينها"""
    try:
        # التحقق من نوع الملف
        if not input_blob.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            logging.warning(f"نوع الملف غير مدعوم: {input_blob.name}")
            return

        # معالجة الصورة
        with Image.open(io.BytesIO(input_blob.read())) as img:
            # تغيير الحجم إذا كان كبيرًا
            if max(img.size) > 2048:
                img.thumbnail((2048, 2048))
            
            # تحويل إلى تدرج رمادي
            gray_img = img.convert('L')
            
            # حفظ النتيجة مع تحسين
            with io.BytesIO() as output:
                gray_img.save(
                    output,
                    format='PNG',
                    optimize=True,
                    quality=85
                )
                output_blob.set(output.getvalue())

        logging.info(f"تم معالجة {input_blob.name} بنجاح")

    except Exception as e:
        logging.error(f"خطأ في معالجة الصورة: {str(e)}")
        raise