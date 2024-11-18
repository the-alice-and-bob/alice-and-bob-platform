import json
import csv
from datetime import datetime

import click

from rich.table import Table
from rich.console import Console

from ezycourse import __version__
from ezycourse.sdk import Courses
from ezycourse.sdk.auth import Auth
from ezycourse.sdk.users import Users
from ezycourse.sdk.communities import Communities
from ezycourse.sdk.forms import Forms, FormError


def parse_date(date: datetime | None) -> str:
    try:
        return date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "N/A"


@click.group()
@click.version_option(__version__, '--version', help='Print the version of the CLI')
@click.pass_context
def cli(ctx):
    """An SDK for interacting with the EzyCourse API."""
    ctx.ensure_object(dict)


# region login
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


# endregion

# region communities
@cli.group(help='Communities commands', name='communities')
@click.pass_context
def communities_group(ctx):
    ctx.ensure_object(dict)


@communities_group.command(help='List communities', name='list')
@click.pass_context
def list_communities(ctx):
    click.echo('Listing communities...')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    communities = Communities(auth)

    table = Table(title="All communities")
    table.add_column("ID", justify="center")
    table.add_column("Title")
    table.add_column("Members")

    for community in communities.list():
        table.add_row(
            str(community.identifier),
            community.title,
            str(community.total_members)
        )

    console = Console()
    console.print(table)


@communities_group.command(help='Get a community info', name='info')
@click.argument('community_id')
@click.pass_context
def get_community(ctx, community_id):
    click.echo(f'\nGetting community {community_id}...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

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
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    communities = Communities(auth)

    table = Table(title="All spaces")
    table.add_column("ID", justify="center")
    table.add_column("Name")

    for space in communities.get(community_id).list_spaces():
        table.add_row(
            str(space.identifier),
            space.name
        )

    console = Console()
    console.print(table)


@spaces_group.command(help="List space's posts", name='posts')
@click.option('-c', '--community_id', required=True, type=int)
@click.option('-s', '--space_id', required=True, type=int)
@click.pass_context
def list_space_posts(ctx, community_id, space_id):
    click.echo(f'\nListing posts for space "{space_id}" in community "{community_id}"...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

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
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    communities = Communities(auth)
    space = communities.get(community_id).get_space(space_id)

    # Ask for post title and content
    content = click.prompt('Content', type=str)

    space.create_post(content)

    click.echo(f"Post created")


# endregion

# region courses
@cli.group(help='Courses commands', name='courses')
@click.pass_context
def courses_group(ctx):
    ctx.ensure_object(dict)


@courses_group.command(help='List courses', name='list')
@click.pass_context
def list_courses(ctx):
    click.echo('Listing courses...')

    auth = Auth()
    auth.restore()

    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    courses = Courses(auth)

    table = Table(title="All courses")
    table.add_column("ID", justify="center")
    table.add_column("Title")
    table.add_column("Enrollments")
    table.add_column("Reviews")
    table.add_column("Lessons")
    table.add_column("Orders")

    for course, statistics in courses.list_courses():
        table.add_row(
            str(course.identifier),
            course.title,
            str(statistics.total_enrollments),
            str(statistics.total_reviews),
            str(statistics.total_lessons),
            str(statistics.total_orders)
        )

    console = Console()
    console.print(table)


@courses_group.command(help='Get a course statistics', name='statistics')
@click.argument('course_id')
@click.pass_context
def course_statistics(ctx, course_id):
    click.echo(f'\nGetting course statistics for course {course_id}...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    courses = Courses(auth)
    course = courses.get(course_id)

    table = Table(title=f"Statistics for course {course_id}", min_width=290)
    table.add_column("User ID", justify="center")
    table.add_column("User Name", no_wrap=True)
    table.add_column("Last access", no_wrap=True)
    table.add_column("Lessons completed")
    table.add_column("Progress")

    for stats_per_user in course.get_statistics():
        try:
            last_access = stats_per_user.last_access.strftime('%Y-%m-%d')
        except (TypeError, ValueError, AttributeError):
            last_access = "N/A"

        table.add_row(
            str(stats_per_user.student.identifier),
            stats_per_user.student.full_name,
            last_access,
            str(stats_per_user.lessons_completed),
            f"{stats_per_user.progress}%"
        )

    console = Console()
    console.print(table, no_wrap=True, crop=False, soft_wrap=False)


# Enrollments
@courses_group.command(help='List course enrollments', name='enrollments')
@click.argument('course_id')
@click.option('-o', '--output-file', type=click.File('w'))
@click.option('-f', '--output-format', type=click.Choice(['csv', 'json']), default='csv')
@click.pass_context
def list_enrollments(ctx, course_id, output_file, output_format):
    click.echo(f'\nGetting enrollments for course {course_id}...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    courses = Courses(auth)

    try:
        course_id = int(course_id)
    except ValueError:
        click.echo(f"[!] Invalid course ID: {course_id}", err=True, color=True)
        return

    try:
        course = courses.get(course_id)
    except FormError as e:
        click.echo(f"[!] {e}", err=True, color=True)
        return

    table = Table(title=f"Enrollments for course {course_id}")
    table.add_column("User ID", justify="center")
    table.add_column("User Name")
    table.add_column("Email")
    table.add_column("Enrolled At")
    table.add_column("Progress")
    table.add_column("Last Visit")
    table.add_column("Completed At")

    enrollments = course.get_enrolled()

    for enrollment in enrollments:
        table.add_row(
            str(enrollment.student.identifier),
            enrollment.student.full_name,
            enrollment.student.email,
            parse_date(enrollment.start_date),
            f"{enrollment.progress}%",
            parse_date(enrollment.last_visit),
            parse_date(enrollment.course_completion_date)
        )

    console = Console()
    console.print(table)

    # Save to file
    if output_file:
        if output_format == 'csv':
            with output_file:
                csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # "course","course_id","student_id","student_name","email","start_date","complete_date","last_visit_in","progress_report"
                csv_writer.writerow(
                    ["course", "course_id", "student_id", "student_name", "email", "start_date", "complete_date", "last_visit_in",
                     "progress_report"])
                for enrollment in enrollments:
                    csv_writer.writerow([
                        course.title,
                        course.identifier,
                        enrollment.student.identifier,
                        enrollment.student.full_name,
                        enrollment.student.email,
                        parse_date(enrollment.start_date),
                        parse_date(enrollment.course_completion_date),
                        parse_date(enrollment.last_visit),
                        f"{enrollment.progress}%"
                    ])

        else:
            output_file.write(json.dumps([enrollment.student.__dict__ for enrollment in enrollments], indent=4))


@courses_group.command(help='Get a course info', name='info')
@click.argument('course_id')
@click.pass_context
def get_course(ctx, course_id):
    click.echo(f'\nGetting course {course_id}...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    courses = Courses(auth)
    course = courses.get(course_id)

    click.echo(f"\tTitle: {course.title}")
    click.echo(f"\tDescription: {course.short_description}")
    click.echo(f"\tType: {course.course_type.value}")
    click.echo(f"\tLanguage: {course.language}")
    click.echo(f"\tChapters: {len(course.chapters)}")
    click.echo('\n')


# Now users
@cli.group(help='Users commands', name='users')
@click.pass_context
def users_group(ctx):
    ctx.ensure_object(dict)


@users_group.command(help='List users', name='list')
@click.pass_context
@click.option('-o', '--output-file', type=click.File('w'))
@click.option('-f', '--output-format', type=click.Choice(['csv', 'json']), default='csv')
@click.option('-m', '--max-users', type=int, default=100)
@click.option('-l', '--only-leads', is_flag=True)
@click.option('-c', '--only-contacts', is_flag=True)
def users_list(ctx, output_file, output_format, max_users, only_leads, only_contacts):
    click.echo(f'\nGetting users...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    table = Table(title="All users")
    table.add_column("ID", justify="center")
    table.add_column("Full Name")
    table.add_column("Email")
    table.add_column("Status")
    table.add_column("Created At")
    table.add_column("Last Login")

    users = []

    user_obj = Users(auth)
    if only_leads:
        gen = user_obj.get_leads(show_progress=True)

    elif only_contacts:
        gen = user_obj.get_contacts(show_progress=True)

    else:
        gen = user_obj.get_users(max_users=max_users)

    for u in gen:
        users.append(u)
        table.add_row(
            str(u.identifier),
            u.full_name,
            u.email,
            u.status.value,
            str(u.created_at),
            str(u.last_login) if u.last_login else "N/A"
        )

    console = Console()
    console.print(table)

    # Save to file
    if output_file:
        if output_format == 'csv':
            with output_file:
                csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(["ID", "First Name", "Last Name", "Full Name", "Email", "Status", "Created At", "Last Login"])
                for u in users:
                    try:
                        last_login = u.last_login.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        last_login = "N/A"

                    try:
                        created_at = u.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        created_at = "N/A"

                    csv_writer.writerow([
                        u.identifier,
                        u.first_name,
                        u.last_name,
                        u.full_name,
                        u.email,
                        u.status,
                        created_at,
                        last_login
                    ])

        else:
            output_file.write(json.dumps([u.__dict__ for u in users], indent=4))


# forms
@cli.group(help='Forms commands', name='forms')
@click.pass_context
def forms_group(ctx):
    ctx.ensure_object(dict)


@forms_group.command(help='List forms', name='list')
@click.pass_context
def list_forms(ctx):
    click.echo('Listing forms...')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    forms = Forms(auth)

    table = Table(title="All forms")
    table.add_column("ID", justify="center")
    table.add_column("Name")
    table.add_column("Responses")

    for form in forms.list_forms():
        table.add_row(
            str(form.identifier),
            form.name,
            str(form.count_responses)
        )

    console = Console()
    console.print(table)


# responses
@forms_group.command(help='List responses for a form', name='responses')
@click.argument('form_id')
@click.option('-o', '--output-file', type=click.File('w'))
@click.option('-f', '--output-format', type=click.Choice(['csv', 'json']), default='csv')
@click.pass_context
def list_responses(ctx, form_id, output_file, output_format):
    click.echo(f'\nGetting responses for form {form_id}...\n')

    auth = Auth()
    auth.restore()
    if not auth.is_logged:
        click.echo('[!] You need to login first!', err=True, color=True)
        return

    forms = Forms(auth)

    try:
        form_id = int(form_id)
    except FormError:
        click.echo(f"[!] Invalid form ID: {form_id}", err=True, color=True)
        return

    try:
        form = forms.get(form_id)
    except FormError as e:
        click.echo(f"[!] {e}", err=True, color=True)
        return

    schema = form.get_schema()

    table = Table(title=f"Responses for form {form_id}")

    for field in schema:
        table.add_column(field, justify="left")

    responses = form.get_responses()
    for response in responses:
        row_values = [response.get(field, '') for field in schema]
        table.add_row(*row_values)

    console = Console()
    console.print(table)

    # Save to file
    if output_file:
        if output_format == 'csv':
            with output_file:
                csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(schema)
                for response in responses:
                    csv_writer.writerow([response.get(field, '') for field in schema])

        else:
            output_file.write(json.dumps(responses, indent=4))


if __name__ == '__main__':
    cli()
