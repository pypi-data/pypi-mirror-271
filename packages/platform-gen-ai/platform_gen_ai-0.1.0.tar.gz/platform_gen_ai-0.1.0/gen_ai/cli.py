import click
import os
import shutil
import subprocess


@click.command()
def create_repo():
    """
    Step-by-step CLI to create a new repository from a specified template.
    """
    template_repo = "https://github.com/GoogleCloudPlatform/platform-gen-ai.git"
    branch = "main"
    client_name = click.prompt("Client name (client_name)", type=str)
    client_description = click.prompt("Client short description (Human readable)", type=str)
    output_dir = '.'
    new_project_dir = os.path.join(output_dir, f"platform-gen-ai-{client_name}")
    temp_clone_dir = os.path.join(output_dir, f"platform-gen-ai-temp")
    try:
        click.echo("Cloning template repository...")
        subprocess.run(["git", "clone", "--branch", branch, "--depth", "1", template_repo, temp_clone_dir], check=True)

        click.echo("Copying template files...")
        # Copy the cloned content to the new project directory
        shutil.copytree(temp_clone_dir, new_project_dir)

        # Remove the temporary directory
        shutil.rmtree(temp_clone_dir)

        click.echo(f"Project '{client_name}' created successfully at {new_project_dir}")

    except subprocess.CalledProcessError as error:
        click.echo(f"Error cloning template repository: {error}")
    except Exception as ex:
        click.echo(f"Error creating project: {ex}")


if __name__ == "__main__":
    create_repo()
