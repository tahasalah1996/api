from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Union

# نموذج بيانات Pydantic (كما عرفناه سابقاً)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    description: Union[str, None] = None

app = FastAPI()

# ฐานة بيانات مؤقتة (قائمة عناصر)
items_db: Dict[int, Item] = {
    1: Item(name="لابتوب", price=1200.0, is_offer=True),
    2: Item(name="هاتف ذكي", price=850.50, description="هاتف جديد ممتاز"),
}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item_data = items_db[item_id]
    return item_data

# نقطة النهاية POST التي أنشأناها سابقاً (لتلقي البيانات وإنشاء عنصر جديد)
# هنا يمكننا استخدامها لإضافة العناصر إلى items_db
@app.post("/items/")
def create_item(item: Item):
    # نحدد معرف (ID) جديد للعنصر
    new_id = max(items_db.keys()) + 1 if items_db else 1
    
    # إضافة العنصر الجديد إلى قاعدة البيانات المؤقتة
    items_db[new_id] = item
    
    # نرجع العنصر الجديد مع المعرّف الخاص به
    return {"id": new_id, **item.model_dump()}

# --------------------
# العمليات الجديدة أدناه
# --------------------
@app.put("/items/{item_id}")
def update_item(item_id: int, new_item: Item):
    # 1. التحقق من وجود العنصر
    if item_id not in items_db:
        # إذا لم يكن موجوداً، نُرجع خطأ HTTP 404 (Not Found)
        # نحتاج إلى استيراد HTTPException في البداية: from fastapi import FastAPI, HTTPException
        raise HTTPException(status_code=404, detail=f"العنصر ذو المعرّف {item_id} غير موجود.")
    
    # 2. تحديث العنصر في قاعدة البيانات المؤقتة
    items_db[item_id] = new_item
    
    # 3. إرجاع العنصر المحدث
    return {"id": item_id, **new_item.model_dump()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # 1. التحقق من وجود العنصر
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"العنصر ذو المعرّف {item_id} غير موجود.")

    # 2. حذف العنصر من قاعدة البيانات المؤقتة
    del items_db[item_id]
    
    # 3. إرجاع رسالة تأكيد
    return {"message": f"تم حذف العنصر ذو المعرّف {item_id} بنجاح."}
