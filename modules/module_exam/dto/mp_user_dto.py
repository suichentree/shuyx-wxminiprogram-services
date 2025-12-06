from pydantic import BaseModel
from typing import Optional

# 定义用户模型类型
# 注意：DTO 是数据传输对象，用于在不同层之间传递数据，而不是直接与数据库交互。
# 因此 DTO 中不需要包含数据库模型中定义的所有字段，而只需要包含在不同层之间传递的字段即可。
class MpUserDTO(BaseModel):
    id:Optional[int] = None          # Optional[int] = None 表示类型可以是int,也可以是 None，默认值为 None
    name:Optional[str] = None
    password:Optional[str] = None
    phone:Optional[str] = None
    wxOpenId:Optional[str] = None
    wxUnionId:Optional[str] = None
    headUrl:Optional[str] = None
    age:Optional[int] = None
    address:Optional[str] = None
    gender:Optional[int] = None
    email:Optional[str] = None
    isAdmin:Optional[int] = None



