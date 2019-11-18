from __future__ import print_function
from invoke import task,run
from pprint import pprint, pformat


@task
def myfunc(ctx, *args, **kwargs):
    """
    Note there is a bug where we couldn't do
       def mine(ctx, mypositionalarg, *args, **kwargs):
           pass

    But something is better than nothing :) Search "TODO 531"
    to find the comment describing our options.
    Keyword optional args work but they can be filled by positional args
    (because they're not KEYWORD_ONLY!) so we don't recommend their use.
    """
    print("args: {}".format(args))
    print("kwargs: {}".format(pformat(kwargs)))
    
@task
def install(c):
    c.run("rm -rf .pyenv")
    c.run("python3 -m venv .pyenv")
    with c.prefix('source .pyenv/bin/activate'):
        c.run("pip3 install -r requirements.txt")

@task(positional=['folder'],optional={"_dry":False,"skip_upload":False,"_parse_libraries":False,"_depth":1,"_email":""})
def run(c, folder,_dry=False,skip_upload=False,_depth=1,_email="",_parse_libraries=False):
    print("---------------------------")
    pprint({
        "folder":folder,
        "dry":_dry, 
        "skip_upload":skip_upload,
         "depth": _depth,
         "parse_libraries":_parse_libraries, 
         "email":_email}) 