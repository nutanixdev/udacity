#!/bin/bash

# colours
RED="\e[31m"
GREEN="\e[32m"
BLUE="\e[34m"
NC="\e[39m"

# set some script-wide variables
ERROR_PREFIX="$RED[ERROR]$NC"
OK_PREFIX="$BLUE[OK]$NC"
INFO_PREFIX="$BLUE[INFO]$NC"
PASS_PREFIX="$GREEN[PASS]$NC"
FAIL_PREFIX="$RED[FAIL]$NC"
LINE_BREAK="----------------------------------------"

# set this to 1 if you want to bail out when a blueprint
# can't be decompiled successfully
VALID_BP_ONLY=0

# set this to 1 to show extended debug info
# for example, if a specific evaluation fails, dump the value that was found
# this can make the output look "messy" but will help diagnose what the
# student did vs what was expected
DEBUG=0

echo -e ""
echo -e "$INFO_PREFIX Evaluation script started at `date`"
echo -e ""

echo -e "$INFO_PREFIX Checking environment."

# checking required binaries are found and are executable
COMMANDS=( "calm" "jq" )
for i in "${COMMANDS[@]}"
do
	:
	# check that each binary exists
	if ! command -v $i &> /dev/null
	then
		echo -e "$ERROR_PREFIX '$i' command could not be found.  Please ensure the $i command exists and is executable before running this script."
		exit
	else
		echo -e "$INFO_PREFIX '$i' command found in `which $i`.  Continuing."
	fi
done

echo -e "$INFO_PREFIX Environment OK."

# function used to display script usage help, when required
function show_help {
	echo -e ""
	echo -e "Usage: eval.bash [ARGS]"
	echo -e ""
	echo -e "Args:"
	echo -e "  -h  Show this help and exit."
	echo -e "  -d  Location of user blueprints"
	echo -e "  -b  Blueprint name to evaluate"
	echo -e "  -c  Evaluation criteria file to use for comparison"
	echo -e ""
	echo -e "Note:"
	echo -e "  -b  value can be \"all\", to batch process all JSON blueprints in the specified directory"
	echo -e ""
	echo -e "Examples:"
	echo -e "  eval.bash -c eval.json -d ~/blueprints -b blueprint1"
	echo -e "  eval.bash -c eval.json -d . -b all"
	echo -e ""
	exit
}
function process_json() {
	echo -e $LINE_BREAK
	# with the blueprint directory found and a blueprint specified, concatenate to make future work easier
	BP_FULL="$BLUEPRINT_DIRECTORY/$1"
	# verify the specified blueprint exists
	if [ ! -f "$BP_FULL" ]
	then
		echo -e "$ERROR_PREFIX $1 not found.  Please specify a valid blueprint by using the -d and -b arguments."
		show_help
		exit
	else
		echo -e "$INFO_PREFIX $1 found.  Continuing."
	fi
	# verify the blueprint is valid
	# at this point the blueprint directory and blueprint itself have been found in the user-specified locations
	if [ "$VALID_BP_ONLY" == "1" ];
	then
		calm decompile bp --file "$BP_FULL" > /tmp/null 2>&1
		COMPILE_RESULT=$?
		if [ ! "$COMPILE_RESULT" == "0" ]
		then
			echo -e "$ERROR_PREFIX The specified blueprint cannot be decompiled.  Please ensure the blueprint contains valid JSON."
			exit
		else
			echo -e "$INFO_PREFIX Blueprint decompiled successfully.  Continuing."
		fi
	fi

	# read the evaluation criteria from the supplied evaluation file
	JSON_CRITERIA="`cat ${CRITERIA_FILE}`"

	echo -e ""
	echo -e "$INFO_PREFIX Starting evaluation of $BP_FULL."
	echo -e ""

	# go over each of the criteria keys in the evaluation file
	# compare each key's 'expected' value to that key's value in the student's JSON blueprint
	for row in $(echo -e "${JSON_CRITERIA}" | jq -r '.criteria[] | @base64')
	do
		TYPE=`echo -e ${row} | base64 -d | jq -r '.type'`
		MATCH=`echo -e ${row} | base64 -d | jq -r '.match'`
		KEY=`echo -e ${row} | base64 -d | jq -r '.key'`
		DESCRIPTION=`echo -e ${row} | base64 -d | jq -r '.description'`
		EXPECTED_VALUE=`echo -e ${row} | base64 -d | jq -r '.expected'`
		# compare the expected vs evaluated values, based on the expected data type
		if [ "$TYPE" == "number" ];
		then
			KEY_VALUE=`cat "$BP_FULL" | jq -r "$KEY | length"`
		else
			KEY_VALUE=`cat "$BP_FULL" | jq -r "$KEY"`
		fi
		# do the comparison but compare based on the "match" setting in the evaluation file
		# string values can be "exact" or "contains"
		# "match" is ignored for number types
		if [ "$TYPE" == "string" ];
		then
			if [ "$MATCH" == "exact" ];
			then
				if [ "$EXPECTED_VALUE" == "$KEY_VALUE" ];
				then
					RESULT=1
				else
					RESULT=0
				fi
			else
				if [[ "$KEY_VALUE" == *"$EXPECTED_VALUE"* ]];
				then
					RESULT=1
				else
					RESULT=0
				fi
			fi
		else
			if [ "$EXPECTED_VALUE" == "$KEY_VALUE" ]
			then
				RESULT=1
			else
				RESULT=0
			fi
		fi
		if [ "$RESULT" == "1" ]
		then
			if [ "$DEBUG" == "1" ];
			then
				echo -e "$PASS_PREFIX $TYPE | $MATCH | ${DESCRIPTION} | Expected ${EXPECTED_VALUE} | Found ${KEY_VALUE}"
			else
				echo -e "$PASS_PREFIX $TYPE | $MATCH | ${DESCRIPTION} | Expected ${EXPECTED_VALUE}"
			fi
		else
			if [ "$DEBUG" == "1" ];
			then
				echo -e "$FAIL_PREFIX $TYPE | $MATCH | ${DESCRIPTION} | Expected ${EXPECTED_VALUE} | Found ${KEY_VALUE}"
			else
				echo -e "$FAIL_PREFIX $TYPE | $MATCH | ${DESCRIPTION} | Expected ${EXPECTED_VALUE}"
			fi
		fi
	done

	echo -e ""
	echo -e "$INFO_PREFIX Evaluation of $BP_FULL completed.  Please see results above."
	echo -e ""
}

# verify the required command-line parameters i.e. the BP directory and the BP we want to work with
echo -e "$INFO_PREFIX Verifying command-line arguments."
while getopts ":b:d:c:h:" opt; do
	case $opt in
		b) export BLUEPRINT="$OPTARG"
		;;
		d) export BLUEPRINT_DIRECTORY="$OPTARG"
		;;
		c) export CRITERIA_FILE="$OPTARG"
		;;
		h) show_help
		;;
		\?) echo -e "$ERROR_PREFIX Unrecognised command-line argument specified: -$OPTARG" >&2
		;;
	esac
done

# verify the blueprint directory exists
if [ ! -d "$BLUEPRINT_DIRECTORY" ]
then
	echo -e "$ERROR_PREFIX Specified blueprint directory not found or not specified using the -d argument."
	show_help
	exit
else
	echo -e "$INFO_PREFIX Blueprint directory found.  Continuing."
fi

# verify a blueprint has been specified using the -b parameter as a command-line argument
if [ -z "$BLUEPRINT" ]
then
        echo -e "$ERROR_PREFIX No blueprint specified.  Please specify a blueprint by name by using the -b argument."
	show_help
	exit
else
        echo -e "$INFO_PREFIX Blueprint name specified.  Continuing."
fi

# verify an evaluation criteria file has been specified using the -c parameter as a command-line argument
if [ ! -z "$CRITERIA_FILE" ]
then
	if [ ! -f "$CRITERIA_FILE" ]
	then
		echo -e "$ERROR_PREFIX Evaluation criteria file not found.  Please specify a valid evaluation criteria file by using the -c argument."
	        show_help
	        exit
	else
        	echo -e "$INFO_PREFIX Evaluation criteria file specified and found.  Continuing."
	fi
else
	echo -e "$ERROR_PREFIX Evaluation criteria file not specified.  Please specify an evaluation criteria file by using the -c argument."
	show_help
        exit
fi

# check to see if the user has indicated they want to parse all blueprints in the specified blueprint directory
if [ "$BLUEPRINT" == "all" ]
then
	echo -e "$INFO_PREFIX All JSON blueprints in $BLUEPRINT_DIRECTORY will be processed."
	echo -e ""
	# go over all JSON files in the specified blueprint directory
	for BP_JSON_FILE in *.json
	do
		# only process the current JSON file if it is not the specified evaluation criteria file
		if [[ ! "$BP_JSON_FILE" == *"$CRITERIA_FILE"* ]]
		then
			process_json $BP_JSON_FILE
		fi
	done
else
	echo -e "$INFO_PREFIX Only $BLUEPRINT in $BLUEPRINT_DIRECTORY will be processed."
	echo -e ""
	process_json $BLUEPRINT
fi

echo -e $LINE_BREAK

# cleanup
echo -e "$INFO_PREFIX Cleaning up."

echo -e "$INFO_PREFIX Evaluation completed."
echo -e ""

echo -e "$INFO_PREFIX Evaluation script finished at `date`"
echo -e ""
