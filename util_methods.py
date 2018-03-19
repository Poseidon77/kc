import requests

# config repo for this functionality (Consul Keeper)
last_processed_commit_org_repo_branch = 'Poseidon77/kc_config/master'

# in the Lambda, this can be an environment variable
organization_and_repo = 'Poseidon77/config-tests'

base_api_url = 'https://api.github.com/repos/' + organization_and_repo


def retrieve_last_processed_commit_on_repo():
    latest_commit_url = 'https://raw.githubusercontent.com/' + last_processed_commit_org_repo_branch \
                         + '/test_last_processed_commit'

    response = requests.get(latest_commit_url)
    return response.text.rstrip()


# def retrieve_latest_commit_on_repo(api_repo_url, branch):
def retrieve_latest_commit_on_repo():
    # branch_query_param = 'sha=' + branch
    # latest_commit_url = api_repo_url + '/commits?page=1&per_page=1&' + branch_query_param
    latest_commit_url = base_api_url + '/commits?page=1&per_page=1'

    print latest_commit_url

    response_latest_commit = requests.get(latest_commit_url)
    latest_commit_data = response_latest_commit.json()

    print latest_commit_data[0]['sha']
    return latest_commit_data[0]['sha']


def find_and_process_file_changes_between_commits(older_commit, newer_commit):
    url = 'https://api.github.com/repos/Poseidon77/config-tests/compare/' + older_commit + '...' + newer_commit
    r_contents = requests.get(url)
    contents_data = r_contents.json()

    file_changes = contents_data['files']
    print file_changes

    for file_change in file_changes:
        file_status = file_change['status']
        if file_status == 'added' or file_status == 'modified':
            put_adds_or_updated_kv(file_change['filename'], file_change['raw_url'])

        elif file_status == 'removed':
            delete_removed_kv(file_change['filename'])

        else:
            print 'error!'


def put_adds_or_updated_kv(filename, github_raw_url):
    print 'at the consul KV location of : ' + filename + '(which is the github path as well), we send a put request \n'
    print 'with a body we obtain from the raw Github URL of : ' + github_raw_url


def delete_removed_kv(filename):
    print 'send delete key request to Consul API with this as the key: ' + filename




find_and_process_file_changes_between_commits('8d89dd573eebd1e667adda4aea716c497dd59351',
                                  '436b809e545c8ed4d6c524cbc7dc8e2f3c7734aa')


# sample removed:
#   "files": [
#     {
#       "sha": "ae5b7b9f99a73a09d90d870d0dd544f21a67e344",
#       "filename": "configs/folder-one/test.key.one",
#       "status": "removed",
#       "additions": 0,
#       "deletions": 3,
#       "changes": 3,
#       "blob_url": "https://github.com/Poseidon77/config-tests/blob/a4d364228ebe60c0af0d51d37eba952a3cbcc947/configs/folder-one/test.key.one",
#       "raw_url": "https://github.com/Poseidon77/config-tests/raw/a4d364228ebe60c0af0d51d37eba952a3cbcc947/configs/folder-one/test.key.one",
#       "contents_url": "https://api.github.com/repos/Poseidon77/config-tests/contents/configs/folder-one/test.key.one?ref=a4d364228ebe60c0af0d51d37eba952a3cbcc947",
#       "patch": "@@ -1,3 +0,0 @@\n-this is a test\n-it is only a test\n-====1111"
#     }
#   ]


# sample added and modified:
#   "files": [
#     {
#       "sha": "a722b70574e61027ba0e5415e9efa7f5ac6c4cc7",
#       "filename": "configs/folder-one/one-layer-deeper/another-layer/text.test.l",
#       "status": "added",
#       "additions": 1,
#       "deletions": 0,
#       "changes": 1,
#       "blob_url": "https://github.com/Poseidon77/config-tests/blob/436b809e545c8ed4d6c524cbc7dc8e2f3c7734aa/configs/folder-one/one-layer-deeper/another-layer/text.test.l",
#       "raw_url": "https://github.com/Poseidon77/config-tests/raw/436b809e545c8ed4d6c524cbc7dc8e2f3c7734aa/configs/folder-one/one-layer-deeper/another-layer/text.test.l",
#       "contents_url": "https://api.github.com/repos/Poseidon77/config-tests/contents/configs/folder-one/one-layer-deeper/another-layer/text.test.l?ref=436b809e545c8ed4d6c524cbc7dc8e2f3c7734aa",
#       "patch": "@@ -0,0 +1 @@\n+changing the value"
#     }
# ]
# "files": [
#     {
#         "sha": "a722b70574e61027ba0e5415e9efa7f5ac6c4cc7",
#         "filename": "configs/folder-one/one-layer-deeper/another-layer/text.test.l",
#         "status": "modified",
#         "additions": 1,
#         "deletions": 1,
#         "changes": 2,
#         "blob_url": "https://github.com/Poseidon77/config-tests/blob/01217cd4f712a6dc414c8eff770eef3019564caa/configs/folder-one/one-layer-deeper/another-layer/text.test.l",
#         "raw_url": "https://github.com/Poseidon77/config-tests/raw/01217cd4f712a6dc414c8eff770eef3019564caa/configs/folder-one/one-layer-deeper/another-layer/text.test.l",
#         "contents_url": "https://api.github.com/repos/Poseidon77/config-tests/contents/configs/folder-one/one-layer-deeper/another-layer/text.test.l?ref=01217cd4f712a6dc414c8eff770eef3019564caa",
#         "patch": "@@ -1 +1 @@\n-another test value\n+changing the value"
#     }
#         ]
