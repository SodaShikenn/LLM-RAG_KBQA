import click
from tasks.demo_task import task as demo_task

@click.command("test_task")
def run():
    # # Execute immediately
    # demo_task.delay('exec now')
    # Execute after 10 seconds delay
    demo_task.apply_async(
        kwargs = {'msg': 'exec async'},
        countdown = 10
    )
    click.echo("success.")