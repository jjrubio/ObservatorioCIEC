from celery import task
import time


@task
def trada():
    for a in xrange(1,50):
        print a