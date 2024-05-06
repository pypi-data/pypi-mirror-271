import click
import os
import shutil
import subprocess
import yaml


@click.command()
def create_repo():
    """
    Step-by-step CLI to create a new repository from a specified template.
    """
    template_repo = "https://github.com/GoogleCloudPlatform/platform-gen-ai.git"
    branch = "main"
    client_name = click.prompt("Client name (client_name)", type=str)
    client_description = click.prompt("Client short description (Human readable)", type=str)
    output_dir = "."

    bq_project_id = click.prompt("Google Cloud Project ID: ", type=str)
    gcs_source_bucket = click.prompt("GCS Source Bucket (e.g., gs://my_bucket/data)", type=str)
    vector_name = click.prompt("Vector name [chroma/vertexai]", type=str)

    new_project_dir = os.path.join(output_dir, f"platform-gen-ai-{client_name}")
    temp_clone_dir = os.path.join(output_dir, f"platform-gen-ai-temp")
    try:
        click.echo("Cloning template repository...")
        subprocess.run(["git", "clone", "--branch", branch, "--depth", "1", template_repo, temp_clone_dir], check=True)

        click.echo("Copying template files...")
        shutil.copytree(temp_clone_dir, new_project_dir)
        shutil.rmtree(temp_clone_dir)

        click.echo("Updating llm.yaml...")
        llm_yaml_path = os.path.join(new_project_dir, "gen_ai", "llm.yaml")

        # Load and modify llm.yaml file
        with open(llm_yaml_path, "r") as yaml_file:
            llm_data = yaml.safe_load(yaml_file)

        llm_data["gcs_source_bucket"] = gcs_source_bucket
        llm_data["bq_project_id"] = bq_project_id
        llm_data["vector_name"] = vector_name
        llm_data["dataset_name"] = client_name
        llm_data["simple_react_chain_prompt"] = (
            f"You are helping {client_name}. {client_description} ." + llm_data["simple_react_chain_prompt"]
        )

        # Save the updated YAML data back to the file
        with open(llm_yaml_path, "w") as yaml_file:
            yaml.safe_dump(llm_data, yaml_file, default_flow_style=False)

        click.echo(f"Project '{client_name}' created successfully at {new_project_dir}")

    except subprocess.CalledProcessError as error:
        click.echo(f"Error cloning template repository: {error}")
    except Exception as ex:
        click.echo(f"Error creating project: {ex}")


if __name__ == "__main__":
    create_repo()
