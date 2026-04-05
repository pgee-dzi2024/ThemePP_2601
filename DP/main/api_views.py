from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .serializers import MediaUploadSerializer
from .services.task_manager import create_task, get_task


class TranscribeCreateAPIView(GenericAPIView):
    serializer_class = MediaUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["media_file"]
        media_dir = Path(settings.MEDIA_ROOT) / "uploads"
        media_dir.mkdir(parents=True, exist_ok=True)

        saved_path = media_dir / uploaded_file.name
        with default_storage.open(str(saved_path), "wb") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        task_id = create_task(saved_path)

        return Response(
            {
                "task_id": task_id,
                "status": "pending",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class TranscribeStatusAPIView(GenericAPIView):
    def get(self, request, task_id: str, *args, **kwargs):
        task = get_task(task_id)
        if task is None:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        payload = {
            "task_id": task_id,
            "status": task["status"],
        }

        if task["status"] == "done" and task["result"]:
            payload.update(task["result"])

        if task["status"] == "error":
            payload["error"] = task["error"]

        return Response(payload)