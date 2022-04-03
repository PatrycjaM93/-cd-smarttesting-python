from invoke import task


@task
def test(ctx):
    """Uruchom testy"""
    ctx.run("pytest")


@task
def lint(ctx):
    """Uruchom lintera flake8."""
    ctx.run("flake8 ./")


@task(lint, test)
def qa(_ctx):
    """Uruchom lintera i testy."""
