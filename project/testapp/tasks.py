from celery import shared_task


@shared_task()
def task1(x, y):
    return x + y


@shared_task
def task2(x, y):
    return x - y


@shared_task
def task3(x, y):
    return x * y
