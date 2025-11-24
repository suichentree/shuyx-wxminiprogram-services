# mp_exam_dao.py 优化版本
from typing import List, Optional
from config.database_config import session_maker
from modules.module_exam.models.mp_exam_model import MpExamModel
from modules.module_exam.dto.mp_exam_dto import MpExamDTO
from loguru import logger


class MpExamDao:
    @classmethod
    def get_list(cls, page_size: int, page_num: int) -> List[MpExamModel]:
        """获取考试列表（分页）"""
        try:
            with session_maker() as db_session:
                offset_value = (page_num - 1) * page_size
                res = db_session.query(MpExamModel).offset(offset_value).limit(page_size).all()
                logger.info(f"获取考试列表成功，页码: {page_num}, 每页条数: {page_size}, 结果数: {len(res)}")
                return res
        except Exception as e:
            logger.error(f"获取考试列表失败: {str(e)}")
            raise

    @classmethod
    def get_total(cls) -> int:
        """获取考试总数"""
        with session_maker() as db_session:
            return db_session.query(MpExamModel).count()

    @classmethod
    def get_list_by(cls, dto: MpExamDTO) -> List[MpExamModel]:
        """根据条件查询考试列表"""
        try:
            with session_maker() as db_session:
                query = db_session.query(MpExamModel)

                # 动态构建查询条件
                if dto.name:
                    query = query.filter(MpExamModel.name == dto.name)
                if dto.type:
                    query = query.filter(MpExamModel.type == dto.type)
                if dto.isBan is not None:
                    query = query.filter(MpExamModel.isBan == dto.isBan)

                res = query.all()
                logger.info(f"条件查询考试成功，结果数: {len(res)}")
                return res
        except Exception as e:
            logger.error(f"条件查询考试失败: {str(e)}")
            raise

    @classmethod
    def update_by_id(cls, dto: MpExamDTO) -> bool:
        """根据ID更新考试信息"""
        try:
            with session_maker() as db_session:
                # 转换为字典，只更新非None字段
                update_data = dto.dict(exclude_unset=True, exclude={"id"})
                if not update_data:
                    logger.warning("没有需要更新的字段")
                    return True

                res = db_session.query(MpExamModel).filter(MpExamModel.id == dto.id).update(update_data)
                logger.info(f"更新考试成功，ID: {dto.id}, 更新行数: {res}")
                return res > 0
        except Exception as e:
            logger.error(f"更新考试失败，ID: {dto.id}, 错误: {str(e)}")
            raise

    @classmethod
    def delete_by_id(cls, exam_id: int) -> bool:
        """根据ID删除考试"""
        try:
            with session_maker() as db_session:
                res = db_session.query(MpExamModel).filter(MpExamModel.id == exam_id).delete()
                logger.info(f"删除考试成功，ID: {exam_id}, 删除行数: {res}")
                return res > 0
        except Exception as e:
            logger.error(f"删除考试失败，ID: {exam_id}, 错误: {str(e)}")
            raise

    @classmethod
    def add(cls, dto: MpExamDTO) -> MpExamModel:
        """添加考试"""
        try:
            with session_maker() as db_session:
                # 过滤掉非模型字段
                exam_data = dto.dict(exclude_unset=True, exclude={"page_num", "page_size", "total"})
                exam = MpExamModel(**exam_data)
                db_session.add(exam)
                db_session.flush()  # 获取新生成的ID但不提交事务
                logger.info(f"添加考试成功，ID: {exam.id}")
                return exam
        except Exception as e:
            logger.error(f"添加考试失败: {str(e)}")
            raise
