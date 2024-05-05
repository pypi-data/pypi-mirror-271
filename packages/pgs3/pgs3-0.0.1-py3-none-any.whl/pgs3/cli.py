import os
from pydantic import BaseModel, Field
from collections import defaultdict
import argparse
import boto3
from datetime import datetime
import json
import subprocess
import sys
import click
import subprocess

def run_command(command, env):
    # Start the subprocess using Popen and specify that stdout and stderr should be piped
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, env={**os.environ, **env})

    # Continuously read and print output from stdout and stderr
    while True:
        output = process.stdout.readline()
        if output:
            print("STDOUT:", output.strip())
        error = process.stderr.readline()
        if error:
            print("STDERR:", error.strip())

        # Break from the loop if the process has completed and there's no more output
        if output == '' and process.poll() is not None:
            break

    # Optionally, handle any post-process output or error cleanup
    if process.returncode != 0:
        print(f"Command failed with return code {process.returncode}")


# Define Pydantic models for the configuration
class DBProfile(BaseModel):
    user: str = ''
    password: str = ''
    host: str = ''
    port: int = 5432
    database: str = ''

class S3Profile(BaseModel):
    bucket: str = ''
    path: str = ''
    region: str = ''
    access_key: str = ''
    secret_key: str = ''
    endpoint_url: str = Field(default='', description="Optional endpoint URL for S3-compatible services")

class Config(BaseModel):
    db: DBProfile
    s3: S3Profile

# S3 client initialization
def s3_client(config):
    s3_config = {
        'region_name': config.s3.region,
        'aws_access_key_id': config.s3.access_key,
        'aws_secret_access_key': config.s3.secret_key
    }

    if config.s3.region:
        s3_config['region_name'] = config.s3.region

    if config.s3.endpoint_url:
        s3_config['endpoint_url'] = config.s3.endpoint_url

    return boto3.client('s3', **s3_config)

SCHEMA_DUMP = 'schema_dump.sql'
DB_DUMP = 'db_dump.sql'

def create_key(config, version, schema_only):
    filename_end = SCHEMA_DUMP if schema_only else DB_DUMP
    filename = f"{config.s3.path}{version}/{filename_end}"
    return filename


def create_local_filename(version, schema_only):
    filename_end = SCHEMA_DUMP if schema_only else DB_DUMP
    filename = f"backup_{version}_{filename_end}"
    return filename


# Fetch backups from S3
def list_backups(config: Config) -> list[str]:
    """
    Return a list of versions from the provided config.
    For example if the following path exists:
        ${config.s3.path}/20200101_120000/db_dump.sql
        ${config.s3.path}/20200101_120000/schema_dump.sql
        ${config.s3.path}/20190202_110000/schema_dump.sql

    This function should return ['20200101_120000', '20200202_110000']

    """
    client = s3_client(config)
    bucket_path = config.s3.path
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=config.s3.bucket, Prefix=bucket_path)

    versions = defaultdict(set)
    for page in pages:
        for obj in page.get('Contents', []):
            path_elements = obj['Key'].split('/')
            if len(path_elements) > 2 and path_elements[-1] in [SCHEMA_DUMP, DB_DUMP]:
                version = path_elements[-2]
                if path_elements[-1].startswith(SCHEMA_DUMP):
                    versions[version].add('Schema')
                if path_elements[-1].startswith(DB_DUMP):
                    versions[version].add('Data')

    versions = [(v, list(ts)) for v, ts in versions.items()]
    return sorted(versions, key=lambda x: x[0])

# Command functions
def backup(config, schema_only, upload):
    version = datetime.now().strftime("%Y%m%d_%H%M%S")

    local_filename = create_local_filename(version, schema_only)

    # PostgreSQL dump command
    cmd = ["pg_dump", "-h", config.db.host, "-U", config.db.user, "-d", config.db.database, "-f", local_filename]
    if schema_only:
        cmd.append('--schema-only')
    cmd = ' '.join(cmd)
    run_command(cmd, {'PGPASSWORD': config.db.password})
    print(f"Backup saved to {local_filename}")

    if upload:
        # Upload to S3
        s3_filename = create_key(config, version, schema_only)
        client = s3_client(config)
        client.upload_file(local_filename, config.s3.bucket, s3_filename)
        print(f"Backup uploaded to s3://{config.s3.bucket}/{s3_filename}")

def restore_or_download(config, version, restore, schema_only):
    if not version:
        backups = list_backups(config)
        version, _ = backups[-1]
        print(f'Using the latest version {version}.')

    filename = create_key(config, version, schema_only)
    local_filename = create_local_filename(version, schema_only)

    # Download from S3
    client = s3_client(config)
    client.download_file(config.s3.bucket, filename, local_filename)
    print(f"Downloaded to {local_filename}.")

    if restore:
        # PostgreSQL restore command
        cmd = ["psql", "-h", config.db.host, "-U", config.db.user, "-d", config.db.database, "-f", local_filename]
        cmd = ' '.join(cmd)
        run_command(cmd, {'PGPASSWORD': config.db.password})
        print("Database restored.")


def create_config(path: str):
    """
    Create an empty config file with all key init as empty string, and save it to the path,
    but throw an error if the file exists.
    
    Args:
    path (str): The file path where the config should be saved.

    Raises:
    FileExistsError: If the file already exists at the specified path.
    """
    if os.path.exists(path):
        raise FileExistsError(f"The file '{path}' already exists.")

    config = Config(
        db= DBProfile(),
        s3= S3Profile(),
    )
    with open(path, 'w') as f:
        json.dump(config.model_dump(mode='json'), f, indent=4)

    print(f"Configuration file created at {path}")


def get_profile(profile: str):
    if not os.path.exists(profile):
        raise ValueError(f'config file {profile} do not exist.')

    with open(profile, 'r') as file:
        config_dict = json.load(file)
        config = Config(**config_dict)
        return config

@click.group()
def cli():
    """
    A command line app that help you backup/restore postgresql to a s3 compatible file storage system.

    S3 will be upload to s3://$S3_BUCKET/$S3_PATH/$DATETIME/[schema_dump|db_dump].sql
    * DATETIME should be like 20240101_121212, and we use this as version name.

    """
    pass

DEFAULT_PROFILE = './pgs3.config.json'

@cli.command(name='init')
@click.option('-p', '--profile', default=DEFAULT_PROFILE, help='Path to the JSON profile configuration file')
def cmd_init(profile):
    create_config(profile)

@cli.command(name='backup')
@click.option('--schema-only', '-s', is_flag=True, help='Backup only the schema without data')
@click.option('-p', '--profile', default=DEFAULT_PROFILE, help='Path to the JSON profile configuration file')
@click.option('--upload','-u', is_flag=True, show_default=True, default=False, help='Upload back to s3.')
def cmd_backup(schema_only, profile, upload):
    config = get_profile(profile)
    backup(config, schema_only, upload)

# List backups available in S3
@cli.command(name='list-backup')
@click.option('-p', '--profile', default=DEFAULT_PROFILE, help='Path to the JSON profile configuration file')
def cmd_list_backup(profile):
    config = get_profile(profile)
    VERSION_LEN = len('  20240504_044406')
    SCHEMA_LEN = len('  Schema, Data   ')
    l1 = '  |'.join([
            "  Index".rjust(8, ' '),
            '  Version'.rjust(VERSION_LEN, ' '),
            '  Backup Type'.rjust(SCHEMA_LEN, ' '),
    ])
    sep_line = "-" * len(l1)
    print(sep_line)
    print(l1)
    print(sep_line)
    for idx, (version, types) in enumerate(reversed(list_backups(config))):
        ts = ','.join(types)
        line = '  |'.join([
                f"  {idx}".rjust(8, ' '),
                f'  {version}'.rjust(VERSION_LEN, ' '),
                f'  {ts}'.rjust(SCHEMA_LEN, ' '),
        ])
        print(line)


    print(sep_line)
    # print("Total: " * len(backup))

# Command to download a specific backup
@cli.command(name='download')
@click.option('--version','-v', default=None, help='Specify the backup version to download')
@click.option('--schema-only','-s', is_flag=True, default=False, help='download only the schema without data')
@click.option('-p', '--profile', default=DEFAULT_PROFILE, help='Path to the JSON profile configuration file')
@click.option('--restore','-r', is_flag=True, default=False, help='Restore db with that data.')
def cmd_download(version, schema_only, profile, restore):
    config = get_profile(profile)
    restore_or_download(config, version=version, restore=restore, schema_only=schema_only)

if __name__ == "__main__":
    cli(obj={})
