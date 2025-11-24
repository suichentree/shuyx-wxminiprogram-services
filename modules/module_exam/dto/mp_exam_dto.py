from pydantic import BaseModel
from typing import Optional

# 定义Addr模型类型
class MpExamDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None             #  Optional[str] = None 类型表示 可以是str,也可以是 None
    type:Optional[str] = None
    isBan:Optional[int] = None
    status:Optional[str] = None
    createTime: Optional[str] = None

    page_num: Optional[int] = None
    page_size: Optional[int] = None
    total: int