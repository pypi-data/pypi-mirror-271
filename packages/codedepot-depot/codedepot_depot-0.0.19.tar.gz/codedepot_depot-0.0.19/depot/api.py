from urllib import response

from depot_api.models.repository_in import RepositoryIn
import inquirer
from depot.config import DepotConfig
from depot_api.exceptions import ApiException
from depot_api.models.ssh_key_in import SshKeyIn
from prettytable import PrettyTable
from depot.cluster_spec import ClusterSpec
from depot.jobfile import JobSpec
from depot.provider_spec import ProviderSpec
from depot_api.api import default_api
from depot_api.api.default_api import DefaultApi
from depot_api.models.job_instance_in import JobInstanceIn
from depot_api.models.cluster_in import ClusterIn
from depot_api.models.provider import Provider
from git_ai.metrics.experiment import get_new_exp_name
from git_ai.cmd.ai_repo import AIRepo
import pygit2
import os
from urllib.parse import urlparse


def login(username: str, password: str):
    default_api.DefaultApi().login_login_post(username=username, password=password)


def list_clusters(config: DepotConfig):

    response = config.api().list_clusters_clusters_get()
    providers = config.api().list_providers_providers_get()
    provider_types = config.api().list_providers_types_provider_types_get()
    provider_type_dict2 = {p['id']: p['name'] for p in provider_types}
    provider_type_dict = {
        prov['id']: provider_type_dict2[prov['provider_type_id']] for prov in providers}
    provider_dict = {p['id']: p['name'] for p in providers}
    table = PrettyTable()
    table.field_names = ['Name', 'Provider', 'Provider Type']
    for cluster in response:
        table.add_row([cluster['name'], provider_dict[cluster['provider_id']],
                      provider_type_dict[cluster['provider_id']]])
    print(table)


def list_provider_types(config: DepotConfig):
    response = config.api().list_providers_types_provider_types_get()
    table = PrettyTable()
    table.field_names = ['Name', 'Module']
    for provider_type in response:
        table.add_row([provider_type['name'], provider_type['module']])
    print(table)


def list_providers(config: DepotConfig):
    provider_types = config.api().list_providers_types_provider_types_get()
    provider_types_dict = {p['id']: p['name'] for p in provider_types}
    response = config.api().list_providers_providers_get()
    table = PrettyTable()
    table.field_names = ['Name', 'Type']
    for provider in response:
        table.add_row(
            [provider['name'], provider_types_dict[provider['provider_type_id']]])
    print(table)


def list_jobs(config: DepotConfig):
    response = config.api().list_job_instances_job_instances_get()
    table = PrettyTable()
    table.field_names = ['Name', 'Status', 'Repository', 'Cluster']
    for job in response:
        table.add_row([job['name'], job['status'],
                      job['repository_url'], job['cluster_name']])
    print(table)


def stop_job(config: DepotConfig, job_name: str):
    instances = config.api().list_job_instances_job_instances_get()
    try:
        repo_folder = pygit2.discover_repository(os.getcwd())
        if not repo_folder:
            print("Cannot find a git repository in the current folder. Please run this command from a git repository.")
            return

        repo = AIRepo(repo_folder)
        url = repo.remotes['origin'].url
    except Exception as e:
        print(f"Error stopping job: {e}")
        return 1

    instance = [i for i in instances if i['name']
                == job_name and i['repository_url'] == url]
    if not instance:
        print(f"Job {job_name} does not exist.")
        return
    instance = instance[0]
    response = config.api().delete_job_instance_job_instances_job_instance_id_delete(
        instance['id'])
    print(f"Job {job_name} stopped.")


def __canonize_url(url: str) -> str:
    # Try to match it to an http url
    parse_results = urlparse(url)
    if parse_results.scheme == 'http' or parse_results.scheme == 'https':
        url = (parse_results.netloc
               if '@' not in parse_results.netloc else
               parse_results.netloc.split('@')[1])
        return f"git@{url}{parse_results.path}"
    elif parse_results.scheme == 'ssh':
        return url
    elif "git@" in url:
        return url
    else:
        print("Error: This repository does not user a protocol that is supported" +
              "by Depot. Please add a remote named 'origin' with an ssh or http url.")
        return None


def __get_repository_key_name(config: DepotConfig, repo_url: str) -> str | None:
    key_name = None

    if 'codedepot.ai' in repo_url:
        need_new_key = False
        try:
            response = config.api().get_managed_ssh_key_managed_ssh_keys_get("codedepot")
            key_name = response['name']
        except ApiException as e:
            need_new_key = True

        if need_new_key:
            print("This repository is hosted on codedepot.ai." +
                  " A new ssh key will be created for it.")
            try:
                response = config.api().create_managed_ssh_key_managed_ssh_keys_post("codedepot")
                key_name = response['name']
            except ApiException as e:
                print(f"Error creating managed ssh key in codedepot.ai.")
                return None
    else:
        try:
            response = config.api().list_ssh_keys_ssh_keys_get()
        except ApiException as e:
            print(f"Error reading ssh keys.")
            return None

        ssh_keys = [key['name'] for key in response]
        questions = [
            inquirer.List(
                'key',
                message=(
                    f"Please select an ssh key to use for the repository {repo_url}."),
                choices=ssh_keys + [' > New Key', ' > Cancel'])
        ]
        answers = inquirer.prompt(questions)
        if answers['key'] == ' > Cancel':
            return None
        elif answers['key'] == ' > New Key':
            questions = [
                inquirer.Text('name', message='Enter a name for the new key'),
                inquirer.Text(
                    'path', message='Enter the path to the private key file in the OpenSSH format')
            ]
            result = __register_ssh_key(
                config, answers['name'], answers['path'])
            if not result:
                return None
            key_name = result['name']
        else:
            key_name = answers['key']

    return key_name


def __register_repo(config: DepotConfig, repo_url: str, key_name: str):
    """Register a repository with Depot. First check with user if they have a valid
    ssh key for the repository. If they do not, create a new ssh key and register it
    with Depot.

    Args:
        config (DepotConfig): depot api object
        repo_url (str): url to repository

    Returns:
        dict: Repository object
    """
    repo = RepositoryIn(
        url=repo_url,
        repository_key=key_name,
        userlogin=config.login
    )

    try:
        response = config.api().create_repository_repositories_post(repo)
    except ApiException as e:
        if 'detail' in e.body and 'already exists' in e.body:
            print(f"Repository {repo_url} already exists.")
            return None
        if 'detail' in e.body and 'Key not found' in e.body:
            print(f"Key {key_name} was not found.")
            return None
        else:
            print(f"Error registering repository.")
            return None

    return response


def start_job(config: DepotConfig, cluster_name: str):
    try:
        repo_folder = pygit2.discover_repository(os.getcwd())
        if not repo_folder:
            print("Error: Cannot find a git repository in the current folder. Please run this command from a git repository.")
            return

        repo = AIRepo(repo_folder)
        if not repo.is_ai_initialized:
            print(
                "Warning: This repository is not initialized with Git AI. Some services will not work.")
    except Exception as e:
        print(f"Error opening repository.")
        return 1

    try:
        job_spec = JobSpec.from_file(
            os.path.join(repo.workdir, '.jobfile.yaml'))
    except FileNotFoundError:
        print(
            "Error: No jobfile found. Please create a .jobfile.yaml in the root of the repository.")
        return 1

    job_instance_name = repo.head.target.hex[0:8]
    clusters = config.api().list_clusters_clusters_get()
    cluster = [c for c in clusters if c['name'] == cluster_name]
    if not cluster:
        print(f"Cluster {cluster_name} does not exist.")
        return
    cluster = cluster[0]
    repo_url = __canonize_url(repo.remotes['origin'].url)
    if not repo_url:
        # Canonize printed error already
        return 1

    # Check if the repository is already registered
    need_new_key = False
    need_to_regiser = False
    response = None
    try:
        response = config.api().read_repository_by_name_repositories_by_name_get(repo_url)
    except ApiException as e:
        if 'detail' in e.body and 'not found' in e.body:
            need_to_regiser = True
        else:
            print(e)
            print(
                f"Error reading repository from Depot. Check if the server is accessible.")
            return 1

    key_name = None
    if need_to_regiser or not response['valid_key']:
        try:
            key_name = __get_repository_key_name(config, repo_url)
            if not key_name:
                return 1
        except Exception as e:
            print(f"Error creating ssh key for depot.")
            return 1
        # Update repo if neede
        if not need_to_regiser:
            try:
                response = config.api().update_repository_repositories_by_name_patch(
                    repo_url, key_name)
            except ApiException as e:
                print(f"Error updating repository with new key.")
                return 1

    if need_to_regiser:
        response = __register_repo(config, repo_url, key_name)
        if not response:
            return 1

    try:
        response = config.api().create_job_instance_job_instances_post(JobInstanceIn(
            repository_url=repo_url,
            starting_commit=repo.head.target.hex,
            userlogin=config.login,
            job_name=job_spec.name,
            cluster_id=cluster['id'],
            name=job_instance_name
        ))

        job_launched = config.api().read_job_instance_job_instances_job_instance_id_get(
            response['id'])
    except ApiException as e:
        print(e)
        print(f"Error launching job. Check the logs for more information.")
        return 1
    print(f"Job {job_launched['name']} started.")
    return 0


def log(config: DepotConfig, job_name: str):
    try:
        repo_folder = pygit2.discover_repository(os.getcwd())
        if not repo_folder:
            print("Cannot find a git repository in the current folder. Please run this command from a git repository.")
            return

        repo = AIRepo(repo_folder)
        url = repo.remotes['origin'].url
    except Exception as e:
        print(f"Job {job_name} does not exist.")
        return 1

    instances = config.api().list_job_instances_job_instances_get()
    instance = [i for i in instances if i['name']
                == job_name and i['repository_url'] == url]
    instances = config.api().list_job_instances_job_instances_get()
    if not instance:
        print(f"Job {job_name} does not exist.")
        return 1

    instance = instance[0]
    response = config.api().read_log_logs_job_instance_id_get(instance['id'])
    print(response['log'])


def create_provider(config: DepotConfig, spec_file: str) -> int:

    try:
        spec = ProviderSpec.from_file(spec_file)
        with open(spec.credentials, 'r') as file:
            credentials = file.read()
        provider_types = config.api().list_providers_types_provider_types_get()
        provider_type = [
            p for p in provider_types if p['name'] == spec.provider_type]
        if not provider_type:
            print(f"Provider type {spec.provider_type} is not supported")
            return 1
        response = config.api().create_provider_providers_post(Provider(
            name=spec.name,
            provider_type_id=int(provider_type[0]['id']),
            credentials=credentials,
            userlogin=config.login))
        return 0
    except Exception as e:
        print(f"Error creating provider.")
        return 1


def create_cluster(config: DepotConfig, spec_file: str) -> int:
    try:
        spec = ClusterSpec.from_file(spec_file)
        providers = config.api().list_providers_providers_get()
        provider = [
            p for p in providers if p['name'] == spec.provider]
        if not provider:
            print(f"Provider {spec.provider} does not exist.")
            return 1
        response = config.api().create_cluster_clusters_post(ClusterIn(
            name=spec.name,
            provider_id=provider[0]['id'],
            nodes=spec.nodes,
            userlogin=config.login))
        return 0
    except Exception as e:
        print(f"Error creating cluster.")
        return 1


def __register_ssh_key(config: DepotConfig, name: str, path: str) -> dict:
    try:
        with open(path, 'r') as file:
            private_key = file.read()

        with open(path + '.pub', 'r') as file:
            public_key = file.read()
    except Exception as e:
        print(f"Error reading key files.")
        return None

    response = None
    try:
        response = config.api().create_ssh_key_ssh_keys_post(SshKeyIn(
            name=name,
            userlogin=config.login,
            public_key=public_key,
            private_key=private_key
        ))
    except ApiException as e:
        if 'detail' in e.body and 'already exists' in e.body:
            print(f"Key {name} already exists.")
            return None
        else:
            print(f"Error registering ssh key.")
            return None

    return response


def create_ssh_key(config: DepotConfig, name: str, path: str) -> int:
    response = __register_ssh_key(config, name, path)
    if not response:
        return 1
    print(f"Key {name} created.")
    return 0


def delete_ssh_key(config: DepotConfig, name: str) -> int:
    try:
        response = config.api().delete_ssh_key_ssh_keys_key_name_delete(key_name=name)
        return 0
    except ApiException as e:
        if 'detail' in e.body and 'not found' in e.body:
            print(f"Key {name} does not exist.")
            return 1


def list_ssh_keys(config: DepotConfig) -> int:
    try:
        response = config.api().list_ssh_keys_ssh_keys_get()
        table = PrettyTable()
        table.field_names = ['Name', "Managed"]
        for key in response:
            table.add_row([key['name'], key['managed']])
        print(table)
        return 0
    except Exception as e:
        print(f"Error listing ssh keys.")
        return 1


def refresh_managed_ssh_key(config: DepotConfig) -> int:
    try:
        response = config.api().create_managed_ssh_key_managed_ssh_keys_post("codedepot")
        print(
            f"Key {response['name']} created and registered with codedepot.ai.")
        return 0
    except Exception as e:
        print(f"Error creating managed ssh key.")
        return 1
