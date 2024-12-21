from celery.backends.mongodb import MongoBackend
from kombu.exceptions import EncodeError
from pymongo.errors import InvalidDocument


class CustomBackend(MongoBackend):
    """Custom MongoDB backend for storing task results and metadata."""

    def _store_result(
        self, task_id, result, state, traceback=None, request=None, **kwargs
    ):
        task_info = self._get_result_meta(
            result=self.encode(result),
            state=state,
            traceback=traceback,
            request=request,
            format_date=False,
        )

        task_info["_id"] = task_id

        try:
            self.collection.update_one(
                {"_id": task_id}, {"$set": task_info}, upsert=True
            )
        except InvalidDocument as exc:
            raise EncodeError(exc)

        return result
