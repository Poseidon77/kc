from util_methods import *


last_processed_commit = retrieve_last_processed_commit_on_repo()

print last_processed_commit

most_recent_commit = retrieve_latest_commit_on_repo()

print most_recent_commit

find_and_process_file_changes_between_commits(last_processed_commit, most_recent_commit)
