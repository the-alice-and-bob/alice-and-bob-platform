import click

from ezycourse import __version__
from ezycourse.sdk.auth import Auth
from ezycourse.sdk.communities import Communities


@click.group()
@click.version_option(__version__, '--version', help='Print the version of the CLI')
@click.pass_context
def cli(ctx):
    """An SDK for interacting with the EzyCourse API."""
    ctx.ensure_object(dict)


@cli.group(help='Authentication commands')
@click.option('--site', required=True)
@click.pass_context
def login(ctx, site):
    ctx.obj['site'] = site


@login.command(help='login interactively')
@click.pass_context
def interactive(ctx):
    click.echo('Logging in interactively...')


@login.command(help='do login with email and password', name='email')
@click.option('-e', '--email', required=True)
@click.option('-p', '--password', required=True)
@click.pass_context
def login_email(ctx, email, password):
    click.echo('Logging in with email and password...')

    auth = Auth()
    auth.do_login(ctx.obj['site'], email, password)
    auth.save()

    click.echo('Logged in!')

@login.command(help='login manually')
@click.pass_context
def manual(ctx):
    click.echo('Paste the session cookies...')
    cookies = click.prompt('Cookies')

    auth = Auth()
    auth.save_session_cookie(ctx.obj['site'], cookies)

    click.echo('Cookies saved!')


@cli.group(help='Communities commands', name='communities')
@click.pass_context
def communities_group(ctx):
    ctx.ensure_object(dict)


@communities_group.command(help='List communities', name='list')
@click.pass_context
def list_communities(ctx):
    click.echo('Listing communities...')

    auth = Auth()
    communities = Communities(auth)

    for community in communities.list():
        click.echo(f" - [{community.identifier}] {community.title}")


@communities_group.command(help='Get a community info', name='info')
@click.argument('community_id')
@click.pass_context
def get_community(ctx, community_id):
    click.echo(f'\nGetting community {community_id}...\n')

    auth = Auth()
    communities = Communities(auth)
    community = communities.get(community_id)

    click.echo(f"\tTitle: {community.title}")
    click.echo(f"\tDescription: {community.short_description}")
    click.echo(f"\tMembers: {community.total_members}")
    click.echo(f"\tPricing: {community.pricing.price}")
    click.echo('\n')


# new group: spaces
@communities_group.group(help='Spaces commands', name='spaces')
@click.pass_context
def spaces_group(ctx):
    ctx.ensure_object(dict)


@spaces_group.command(help='List community spaces', name='list')
@click.option('-c', '--community_id', required=True, type=int)
@click.pass_context
def list_community_spaces(ctx, community_id):
    click.echo(f'\nListing spaces for community {community_id}...\n')

    auth = Auth()
    communities = Communities(auth)

    for space in communities.get(community_id).list_spaces():
        click.echo(f" - [{space.identifier}] {space.name}")

    click.echo('\n')


@spaces_group.command(help="List space's posts", name='posts')
@click.option('-c', '--community_id', required=True, type=int)
@click.option('-s', '--space_id', required=True, type=int)
@click.pass_context
def list_space_posts(ctx, community_id, space_id):
    click.echo(f'\nListing posts for space "{space_id}" in community "{community_id}"...\n')

    auth = Auth()
    communities = Communities(auth)

    click.echo(f"{'-' * 60}")
    for post in communities.get(community_id).get_space(space_id).list_posts():
        click.echo(f"  ID: {post.identifier}")
        click.echo(f"  Title: {post.title}")
        click.echo(f"  Likes: {post.likes}")
        click.echo(f"  Created at: {post.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"  Updated at: {post.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"{'-' * 60}")

    click.echo('\n')


@spaces_group.command(help="Create new post in space", name='create-post')
@click.option('-c', '--community_id', required=True, type=int)
@click.option('-s', '--space_id', required=True, type=int)
@click.pass_context
def create_space_post(ctx, community_id, space_id):
    click.echo(f'\nCreating new post in space "{space_id}" in community "{community_id}"...\n')

    auth = Auth()
    communities = Communities(auth)
    space = communities.get(community_id).get_space(space_id)

    # Ask for post title and content
    content = click.prompt('Content', type=str)

    space.create_post(content)

    click.echo(f"Post created")


if __name__ == '__main__':
    cli()
