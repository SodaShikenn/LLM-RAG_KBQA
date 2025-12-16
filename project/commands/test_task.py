import click
from tasks.dataset_segment_embed_task import task as dataset_segment_embed_task

@click.command("test_task")
def run():
    # # Execute immediately
    # demo_task.delay('exec now')
    # # Execute after 10 seconds delay
    # demo_task.apply_async(
    #     kwargs = {'msg': 'exec async'},
    #     countdown = 10
    # )

    # dataset_segment_embed_task.delay(1)
    dataset_segment_embed_task.delay(None, 618)

    click.echo("success.")
