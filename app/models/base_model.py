import json
from datetime import datetime

from beanie import Document


class BaseDocument(Document):
    __doc__ = "基础模型"
    create_date: datetime = datetime.now()
    update_date: datetime = None

    def to_dict(self, *args, include_all=False, **kwargs):
        if not include_all:
            return json.loads(self.json(exclude={"revision_id", "update_date", "create_date"}, *args, **kwargs))
        return json.loads(self.json(*args, **kwargs))
