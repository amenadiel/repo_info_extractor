import argparse
from init import initialize

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'directory', help='Path to the repository. Example usage: run.sh path/to/directory')
    parser.add_argument('--output', default='./repo_data.json', dest='output',
                        help='Path to the JSON file that will contain the result')
    parser.add_argument('--skip_obfuscation', default=False, dest='skip_obfuscation',
                        help='If true it won\'t obfuscate the sensitive data such as emails and file names. Mostly for testing purpuse')
    parser.add_argument('--parse_libraries', default=False,
                        dest='parse_libraries', help='If true, used libraries will be parsed')
    parser.add_argument('--default_email', default='',
                        dest='default_email', help='If set, commits from this email are preselected on authors list')
    parser.add_argument('--skip_upload', default=False,
                        dest='skip_upload', help='If true, skip the prompt to upload automatically')

    args = parser.parse_args()
    initialize(args.directory, args.skip_obfuscation, args.output, args.parse_libraries, args.default_email, args.skip_upload)


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', True)
    main()

