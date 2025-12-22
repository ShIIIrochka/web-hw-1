# # -*- coding: utf-8 -*-
#
# from __future__ import annotations
#
# import asyncio
# import logging
# import os
#
# from datetime import datetime
# from uuid import UUID
#
# from punq import Container
# from taskiq import TaskiqScheduler
# from taskiq.schedule_sources import LabelScheduleSource
# from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend
#
# from src.domain.repositories.post_search_repository import (
#     BasePostSearchRepository,
# )
# from src.infra.container import container_builder
# from src.infra.providers.interfaces import CacheProvider, DBProvider
# from src.infra.providers.opensearch import OpenSearchClientProvider
#
#
# logger = logging.getLogger(__name__)
#
# # Настройка Redis broker для Taskiq
# redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# broker = ListQueueBroker(redis_url).with_result_backend(
#     RedisAsyncResultBackend(redis_url)
# )
#
# # Глобальный контейнер для воркера
# _worker_container: Container | None = None
#
#
# def get_worker_container() -> Container:
#     """Получить единый контейнер воркера."""
#     global _worker_container
#     if _worker_container is None:
#         raise RuntimeError("Worker container not initialized")
#     return _worker_container
#
#
# @broker.task(retry_on_error=True, max_retries=5)
# async def process_outbox_event(
#     event_id: str,
#     aggregate_type: str,
#     event_type: str,
#     payload: dict,
# ) -> None:
#     """Обработка одного события из outbox.
#
#     Args:
#         event_id: ID события
#         aggregate_type: Тип агрегата
#         event_type: Тип события
#         payload: Данные события
#     """
#     container = get_worker_container()
#
#     search_repo = container.resolve(BasePostSearchRepository)
#     outbox_repo = container.resolve("OutboxRepo")
#
#     try:
#         event_uuid = UUID(event_id)
#
#         if event_type == "post.created":
#             await _handle_post_created(search_repo, payload)
#         elif event_type == "post.updated":
#             await _handle_post_updated(search_repo, payload)
#         elif event_type == "post.deleted":
#             await _handle_post_deleted(search_repo, payload)
#         else:
#             logger.warning(f"Unknown event type: {event_type}")
#
#         await outbox_repo.mark_processed(event_uuid)
#
#         logger.info(f"Event {event_id} ({event_type}) processed successfully")
#
#     except Exception as e:
#         error_msg = str(e)
#         logger.error(
#             f"Error processing event {event_id}: {error_msg}",
#             exc_info=True,
#         )
#
#         await outbox_repo.mark_failed(event_uuid, error_msg)
#         raise
#
#
# async def _handle_post_created(
#     search_repo: BasePostSearchRepository, payload: dict
# ) -> None:
#     """Обработка создания поста."""
#     post = _payload_to_post(payload)
#     await search_repo.index(post)
#
#
# async def _handle_post_updated(
#     search_repo: BasePostSearchRepository, payload: dict
# ) -> None:
#     """Обработка обновления поста."""
#     post = _payload_to_post(payload)
#     await search_repo.update(post)
#
#
# async def _handle_post_deleted(
#     search_repo: BasePostSearchRepository, payload: dict
# ) -> None:
#     """Обработка удаления поста."""
#     await search_repo.delete(UUID(payload["id"]))
#
#
# def _payload_to_post(payload: dict):
#     """Преобразование payload в сущность Post."""
#     from src.domain.entities.post import Post
#
#     return Post(
#         id=UUID(payload["id"]),
#         title=payload["title"],
#         content=payload["content"],
#         author_id=UUID(payload["author_id"]),
#         created_at=datetime.fromisoformat(payload["created_at"]),
#         updated_at=datetime.fromisoformat(payload["updated_at"]),
#     )
#
#
# @broker.task(
#     schedule=[
#         {
#             "cron": "*/30 * * * *",  # Каждые 30 секунд
#         }
#     ]
# )
# async def poll_outbox_and_enqueue() -> None:
#     """Периодическая задача: забирает pending события и ставит в очередь."""
#     container = get_worker_container()
#
#     outbox_repo = container.resolve("OutboxRepo")
#
#     batch_size = int(os.getenv("OUTBOX_BATCH_SIZE", "10"))
#     lock_ttl = int(os.getenv("OUTBOX_LOCK_TTL", "300"))
#     worker_id = f"taskiq-{os.getpid()}"
#
#     events = await outbox_repo.claim_pending_events(
#         limit=batch_size, worker_id=worker_id, lock_ttl_seconds=lock_ttl
#     )
#
#     if not events:
#         return
#
#     logger.info(f"Claimed {len(events)} pending events to process")
#
#     for event in events:
#         await process_outbox_event.kiq(
#             event_id=str(event.id),
#             aggregate_type=event.aggregate_type,
#             event_type=event.event_type,
#             payload=event.payload,
#         )
#
#
# async def startup_worker() -> None:
#     """Инициализация воркера при старте."""
#     global _worker_container
#
#     _worker_container = container_builder()
#
#     db_provider = _worker_container.resolve(DBProvider)
#     cache_provider = _worker_container.resolve(CacheProvider)
#     opensearch_provider = _worker_container.resolve(OpenSearchClientProvider)
#
#     await db_provider.init()
#     await cache_provider.init()
#     await opensearch_provider.init()
#
#     logger.info("Taskiq worker initialized")
#
#
# async def shutdown_worker() -> None:
#     """Закрытие соединений при остановке воркера."""
#     container = get_worker_container()
#
#     db_provider = container.resolve(DBProvider)
#     cache_provider = container.resolve(CacheProvider)
#     opensearch_provider = container.resolve(OpenSearchClientProvider)
#
#     await opensearch_provider.close()
#     await cache_provider.close()
#     await db_provider.close()
#
#     logger.info("Taskiq worker shut down")
#
#
# # Регистрируем lifecycle handlers
# broker.add_event_handler("worker_startup", startup_worker)
# broker.add_event_handler("worker_shutdown", shutdown_worker)
#
#
# async def run_worker() -> None:
#     """Запуск Taskiq воркера."""
#     from src.infra.logging import setup_logging
#
#     setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
#
#     logger.info("Starting Taskiq worker...")
#
#     scheduler = TaskiqScheduler(
#         broker=broker,
#         sources=[LabelScheduleSource(broker)],
#     )
#
#     await broker.startup()
#     await scheduler.startup()
#
#     try:
#         while True:
#             await asyncio.sleep(1)
#     except KeyboardInterrupt:
#         logger.info("Received shutdown signal")
#     finally:
#         await scheduler.shutdown()
#         await broker.shutdown()
#
#
# if __name__ == "__main__":
#     asyncio.run(run_worker())
