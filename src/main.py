import argparse
from init import initialize
import os
from ui.questions import Questions
import logging
from pprint import pprint
from pathlib import Path,PurePosixPath

for filename in Path('src').glob('**/*.c'):
    print(filename)

FORMAT = '[%(asctime)s] %(message)s'
logging.basicConfig(format=FORMAT, datefmt="%d/%m/%Y %H:%M:%S", level=logging.INFO)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'directory', help='Path to the repository. Example usage: run.sh path/to/directory')
    parser.add_argument('--output', default='./repo_data.json', dest='output',
                        help='Path to the JSON file that will contain the result')
    parser.add_argument('--skip_obfuscation', default=False, dest='skip_obfuscation', action='store_true',
                        help='If true it won\'t obfuscate the sensitive data such as emails and file names. Mostly for testing purpuse')
    parser.add_argument('--parse_libraries',  default=False, action='store_true',
                        dest='parse_libraries', help='If true, used libraries will be parsed')
    parser.add_argument('--email', default='',
                        dest='email', help='If set, commits from this email are preselected on authors list')
    parser.add_argument('--skip_upload',  default=False, action='store_true',
                        dest='skip_upload', help="If true, don't prompt for inmediate upload")
    parser.add_argument('--depth',  default=1,  dest='depth', help="Search repos recursively up to this depth from <directory>")
    
    try:
        args = parser.parse_args()
        folders=[]
        directory=Path(args.directory)
        if(args.depth!=1):
            for folder in directory.glob('*/*.git'):
                folders.append('%s' % (folder.parent))
        
        output=args.output.replace('.json','')
        if len(folders) > 1:
            os.makedirs('%s' %(directory.name), mode=0o777, exist_ok=True)
            q = Questions()
            repos = q.ask_which_repos(folders)
            if 'chosen_repos' not in repos or len(repos['chosen_repos']) == 0:
                print("No repos chosen, will exit")
                os._exit(0)
            for repo in repos['chosen_repos']:
                repo_name = os.path.basename(repo).replace(' ','_')
                output=('./%s/%s.json' % (directory.name, repo_name))
                initialize(repo, args.skip_obfuscation, output, args.parse_libraries, args.email, args.skip_upload)
                logging.info('Finished analyzing %s ' % (repo_name))

        else:
            output=('./%s.json' % (output))
            initialize(args.directory, args.skip_obfuscation,  output, args.parse_libraries, args.email, args.skip_upload)
            pprint(args)
            #logging.log('Finished analyzing %s ' % (directory))
    except KeyboardInterrupt:
        print ("Cancelled by user")
        os._exit(0)
    except Exception as e:
        logging.exception(e)
        os._exit(0)

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.set_start_method('spawn', True)
    main()

