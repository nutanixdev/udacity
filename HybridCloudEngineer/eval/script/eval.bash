#!/bin/bash

# set some script-wide variables
ERROR_PREFIX="[ERROR]"
OK_PREFIX="[OK]"
INFO_PREFIX="[INFO]"
PASS_PREFIX="[PASS]"
FAIL_PREFIX="[FAIL]"
LINE_BREAK="----------------------------------------"

echo ""
echo "$INFO_PREFIX Evaluation script started at `date`"
echo ""

echo "$INFO_PREFIX Checking environment."

# checking required binaries are found and are executable
COMMANDS=( "calm" "jq" )
for i in "${COMMANDS[@]}"
do
	:
	# check that each binary exists
	if ! command -v $i &> /dev/null
	then
		echo "[ERROR] '$i' command could not be found.  Please ensure the $i command exists and is executable before running this script."
		exit
	else
		echo "$OK_PREFIX '$i' command found in `which $i`.  Continuing."
	fi
done

echo "$INFO_PREFIX Environment OK."

# function used to display script usage help, when required
function show_help {
	echo ""
	echo "Usage: eval.bash [ARGS]"
	echo ""
	echo "Args:"
	echo "  -h  Show this help and exit."
	echo "  -d  Location of user blueprints"
	echo "  -b  Blueprint name to evaluate"
	echo "  -c  Evaluation criteria file to use for comparison"
	echo ""
	echo "Note:"
	echo "  -b  value can be \"all\", to batch process all JSON blueprints in the specified directory"
	echo ""
	echo "Examples:"
	echo "  eval.bash -c eval.json -d ~/blueprints -b blueprint1"
	echo "  eval.bash -c eval.json -d . -b all"
	echo ""
	exit
}
function process_json() {
	echo $LINE_BREAK
	# with the blueprint directory found and a blueprint specified, concatenate to make future work easier
	BP_FULL="$BLUEPRINT_DIRECTORY/$1"
	# verify the specified blueprint exists
	if [ ! -f "$BP_FULL" ]
	then
		echo "$ERROR_PREFIX $1 not found.  Please specify a valid blueprint by using the -d and -b arguments."
		show_help
		exit
	else
		echo "$OK_PREFIX $1 found.  Continuing."
	fi
	# verify the blueprint is valid
	# at this point the blueprint directory and blueprint itself have been found in the user-specified locations
	calm decompile bp --file "$BP_FULL" > /tmp/null 2>&1
	COMPILE_RESULT=$?
	if [ ! "$COMPILE_RESULT" == "0" ]
	then
		echo "$ERROR_PREFIX The specified blueprint cannot be decompiled.  Please ensure the blueprint contains valid JSON."
		exit
	else
		echo "$OK_PREFIX Blueprint decompiled successfully.  Continuing."
	fi

	# read the evaluation criteria from the supplied evaluation file
	JSON_CRITERIA="`cat ${CRITERIA_FILE}`"

	echo ""
	echo "$INFO_PREFIX Starting evaluation of $BP_FULL."
	echo ""

	# go over each of the criteria keys in the evaluation file
	# compare each key's 'expected' value to that key's value in the student's JSON blueprint
	for row in $(echo "${JSON_CRITERIA}" | jq -r '.criteria[] | @base64')
	do
		KEY=`echo ${row} | base64 -d | jq -r '.key'`
		DESCRIPTION=`echo ${row} | base64 -d | jq -r '.description'`
		EXPECTED_VALUE=`echo ${row} | base64 -d | jq -r '.expected'`
		KEY_VALUE=`cat "$BP_FULL" | jq -r "$KEY | length"`
		# do the comparison
		if [ "$EXPECTED_VALUE" == "$KEY_VALUE" ]
		then
			echo "$PASS_PREFIX ${DESCRIPTION} | Expected ${EXPECTED_VALUE} | Found ${KEY_VALUE}"
		else
			echo "$FAIL_PREFIX ${DESCRIPTION} | Expected ${EXPECTED_VALUE} | Found ${KEY_VALUE}"
		fi
	done

	echo ""
	echo "$INFO_PREFIX Evaluation of $BP_FULL completed.  Please see results above."
	echo ""
}

# verify the required command-line parameters i.e. the BP directory and the BP we want to work with
echo "$INFO_PREFIX Verifying command-line arguments."
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
		\?) echo "$ERROR_PREFIX Unrecognised command-line argument specified: -$OPTARG" >&2
		;;
	esac
done

# verify the blueprint directory exists
if [ ! -d "$BLUEPRINT_DIRECTORY" ]
then
	echo "$ERROR_PREFIX Specified blueprint directory not found or not specified using the -d argument."
	show_help
	exit
else
	echo "$OK_PREFIX Blueprint directory found.  Continuing."
fi

# verify a blueprint has been specified using the -b parameter as a command-line argument
if [ -z "$BLUEPRINT" ]
then
        echo "$ERROR_PREFIX No blueprint specified.  Please specify a blueprint by name by using the -b argument."
	show_help
	exit
else
        echo "$OK_PREFIX Blueprint name specified.  Continuing."
fi

# verify an evaluation criteria file has been specified using the -c parameter as a command-line argument
if [ ! -z "$CRITERIA_FILE" ]
then
	if [ ! -f "$CRITERIA_FILE" ]
	then
		echo "$ERROR_PREFIX Evaluation criteria file not found.  Please specify a valid evaluation criteria file by using the -c argument."
	        show_help
	        exit
	else
        	echo "$OK_PREFIX Evaluation criteria file specified and found.  Continuing."
	fi
else
	echo "$ERROR_PREFIX Evaluation criteria file not specified.  Please specify an evaluation criteria file by using the -c argument."
	show_help
        exit
fi

# check to see if the user has indicated they want to parse all blueprints in the specified blueprint directory
if [ "$BLUEPRINT" == "all" ]
then
	echo "$INFO_PREFIX All JSON blueprints in $BLUEPRINT_DIRECTORY will be processed."
	echo ""
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
	echo "$INFO_PREFIX Only $BLUEPRINT in $BLUEPRINT_DIRECTORY will be processed."
	echo ""
	process_json $BLUEPRINT
fi

echo $LINE_BREAK

# cleanup
echo "$INFO_PREFIX Cleaning up."

echo "$OK_PREFIX Evaluation completed."
echo ""

echo "$INFO_PREFIX Evaluation script finished at `date`"
echo ""
