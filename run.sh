#!/usr/bin/env bash
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BLUE=`tput setaf 4`
PURPLE=`tput setaf 5`
CYAN=`tput setaf 6`
BRIGHT=`tput setaf 7`

BRED=`tput bold && tput setaf 1`
BGREEN=`tput bold && tput setaf 2`
BYELLOW=`tput bold && tput setaf 3`
BBLUE=`tput bold && tput setaf 4`
BPURPLE=`tput bold && tput setaf 5`
BCYAN=`tput bold && tput setaf 6`
BBRIGHT=`tput bold && tput setaf 7`

RESET=`tput sgr0`
exitfn () {
    trap SIGINT              
    echo; echo 'Interrupted by user!!'
    exit                     
}
red() {
  return "${RED}$1${WHITE}"
}

trap "exitfn" INT
local_projects() {
  repos=`find $folder -maxdepth $depth  -type d  -wholename "*/.git" -exec dirname {} \;`
  number_of_repos=`echo $repos | wc -w`

  for REPO_PATH in $repos
  do
    rm -rf 1
	  REPO_NAME=`echo $REPO_PATH | sed -e 's/\/$//g' | rev | cut -d'/' -f 1 | rev `  >&2;
    FILE_NAME="./"$REPO_NAME".json"
	  if [ "$dry_run" != 0 ]; then
      echo "found repo ${BGREEN}$REPO_NAME${RESET}"
    else
      echo "repo ${BGREEN}$REPO_NAME${RESET} will be saved as ${BCYAN}$FILE_NAME${RESET}"
      python src/main.py "$REPO_PATH" --output $FILE_NAME --default_email "$email" --upload $upload && wait
	  fi
	  echo " "
  done;

}

#python src/main.py "$REPO_PATH" --output $FILE_NAME


depth=1
dry_run=0
folder="${!#}"
paramnum=$#
email=""
upload='default'
optspec=":h-:"
while getopts "$optspec" optchar; do
     case "${optchar}" in
        -)
            case "${OPTARG}" in
                dry=*)
                    val=${OPTARG#*=}
                    opt=${OPTARG%=$val}
                    if [ "$val" != "0" ]; then
                      echo "${BCYAN}Dry run${RESET}, will only list repos"
                    fi
                    dry_run=$val
                    ;;
                depth=*)
                    val=${OPTARG#*=}
                    opt=${OPTARG%=$val}
                    depth=$val
                    ;;
                upload=*)
                    val=${OPTARG#*=}
                    opt=${OPTARG%=$val}
                    upload=$val
                    ;;
                email=*)
                    val=${OPTARG#*=}
                    opt=${OPTARG%=$val}
                    email=$val
                    if [ "$val" != "" ]; then
                      echo "Commits from ${BCYAN}${email}${RESET}, will be preselected" >&2
                    fi
                    ;;
                *)
                    if [ "$OPTERR" = 1 ] && [ "${optspec:0:1}" != ":" ]; then
                        echo "Unknown option --${OPTARG}" >&2
                    fi
                    ;;
            esac;;
        h)
            echo -e ""
            echo -e "collect your repos info using: "
            echo -e ""
            echo -e "    ${GREEN}make collect${RESET} ${BCYAN}<folder>${RESET} ${BBRIGHT}[depth=<depth>] [dry=0|1] [email=user@domain.com] [upload=skip]${RESET}"
            echo -e ""
            echo -e "Examples:"
            echo -e "  ${GREEN}make help${RESET}                                  display this help message"
            echo -e "  ${GREEN}make collect${RESET} ${BCYAN}~/my_repo${RESET}                     get info of ${BCYAN}my_repo${RESET}"
            echo -e "  ${GREEN}make collect${RESET} ${BCYAN}~/my_repo${RESET} ${BBRIGHT}email=me@mail.com${RESET}   same as above, but preselect ${BCYAN}me@mail.com${RESET} in author list"
            echo -e "  ${GREEN}make collect${RESET} ${BCYAN}~/projects${RESET} ${BBRIGHT}depth=2${RESET}            get info every repo under ${BCYAN}~/projects${RESET} until a given depth"
            echo -e "  ${GREEN}make collect${RESET} ${BCYAN}~/my_repo${RESET} ${BBRIGHT}dry=1${RESET}               just display repos that will be examined"
            echo -e "  ${GREEN}make collect${RESET} ${BCYAN}~/my_repo${RESET} ${BBRIGHT}upload=skip${RESET}         skip auto upload prompt"
            echo -e ""
            echo -e "Combine them all"
            echo -e "  ${GREEN}make collect${RESET} ${BCYAN}~/projects${RESET} depth=2 dry=1 email=me@mail.com upload=skip"
            echo ""
            exit 0
            ;;
       
            
      
        *)
            if [ "$OPTERR" != 1 ] || [ "${optspec:0:1}" = ":" ]; then
                echo "Non-option argument: '-${OPTARG}'" >&2
            fi
            ;;
    esac
done 

  echo "Search repos on ${BPURPLE}$folder${RESET}, ${BCYAN}$depth${RESET} folders deep"
  local_projects
  echo "Finished"
  
trap SIGINT
exit 0