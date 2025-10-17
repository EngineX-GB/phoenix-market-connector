# usage:
# sh .././run.sh --watchlist <userId>								Adds the userId to the Watch List
# sh .././run.sh --region <regionId>								Retrieves client data for a given region
# sh .././run.sh --all												Retrieves client data for all regions
# sh .././run.sh --report											Generates Client and Watch list report for London Region
# sh .././run.sh --group <start_region_number> <end_region_number>	Downloads data between start_region_number and end_region_number
# sh .././run.sh --stats											Get Stats on Available data (stored on the service provider)

load() {
	python .././src/Runner.py 1
	python HtmlGenerator.py
	python .././src/Runner.py 2
	python .././src/Runner.py 3
	python .././src/Runner.py 4
	python .././src/Runner.py 5
	python .././src/Runner.py 6
	python .././src/Runner.py 7
	python .././src/Runner.py 8
	python .././src/Runner.py 9
	python .././src/Runner.py 10
	python .././src/Runner.py 11
	python .././src/Runner.py 12
	python .././src/Runner.py 14
}


# To Be Deprecated
loadx() {
	python PhoenixMobileConnector_v4.py 1
	python HtmlGenerator.py
	python PhoenixMobileConnector_v4.py 2
	python PhoenixMobileConnector_v4.py 3
	python PhoenixMobileConnector_v4.py 4
	python PhoenixMobileConnector_v4.py 5
	python PhoenixMobileConnector_v4.py 6
	python PhoenixMobileConnector_v4.py 7
	python PhoenixMobileConnector_v4.py 8
	python PhoenixMobileConnector_v4.py 9
	python PhoenixMobileConnector_v4.py 10
	python PhoenixMobileConnector_v4.py 11
	python PhoenixMobileConnector_v4.py 12
	python PhoenixMobileConnector_v4.py 14
}

help_info() {
	echo "usage:"
	echo "sh .././run.sh --watchlist <userId>"
	echo "sh .././run.sh --region <regionId>"
	echo "sh .././run.sh --all"
	echo "sh .././run.sh --report"
	echo "sh .././run.sh --group <r1> <r2>"
	echo "sh .././run.sh --stats"
	echo "sh .././run.sh --query <string> <yyyy-MM-dd>"
	echo "sh .././run.sh --query <string>"
	echo "sh .././run.sh --feeds"
	echo "sh .././run.sh --master-file"
	echo "sh .././run.sh --image --standard <yyyy-MM-dd (optional)>"
	echo "sh .././run.sh --image --advanced <yyyy-MM-dd (optional)>"
	echo "sh .././run.sh --image --verify"
	echo "sh .././run.sh --image --verify-empty-folders"
	echo "sh .././run.sh --image --delete-empty-folders"
	echo "sh .././run.sh --image --master-file <yyyy-MM-dd (optional)>"
	echo "sh .././run.sh --image --custom <user_id>"
	echo "sh .././run.sh --image --subgroup <number_of_subgroups> <selected_subgroup>"
	echo "sh .././run.sh --loop 10"
	echo "sh .././run.sh --robomode"
	echo "sh .././run.sh --experimental --region <yyyy-MM-dd> <regionId>"
	echo "sh .././run.sh --experimental --all <yyyy-MM-dd>"
	echo "sh .././run.sh --experimental --delete <yyyy-MM-dd>"
	echo "sh .././run.sh --feedback --standard"
	echo "sh .././run.sh --feedback --advanced"
	echo "sh .././run.sh --feedback --robomode"
	echo "sh .././run.sh --feedback --userId <userId>"
	echo "sh .././run.sh --feedback-data --f <Positive|Negative|FeedbackOnly|ALL> --userId <userId>"
	echo "sh ../run.sh --regionx 1 --range 1 3"
	echo "sh ../run.sh --regionx 1 --page 2"
	echo "sh ../run.sh --chkdup <date (optional)>"
	echo "sh ../run.sh --fixdup <date (optional)>"
	echo "sh ../run.sh --chkdup-all"
	echo "sh ../run.sh --fixdup-all"
}

#
# Define a 'start' region number ($1) and 'end' region number ($2).
# The function will download data between and including $1 and $2.
#
load_region_in_groups() {
	echo "Downloading data from Region $1 to $2 inclusive"
	for i in `seq $1 $2`
	do
		python .././src/Runner.py $i
	done
}

#
# To be deprecated
#
# Define a 'start' region number ($1) and 'end' region number ($2).
# The function will download data between and including $1 and $2.
#
load_region_in_groupsx() {
	echo "Downloading data from Region $1 to $2 inclusive"
	for i in `seq $1 $2`
	do
		python PhoenixMobileConnector_v4.py $i
	done
}


load_in_loop() {
	echo "Looping process with $1 second(s) sleep"
	while true
	do
		load
		echo "Sleeping for $1 second(s)"
		sleep $1
	done
}

# To be deprecated
load_in_loopx() {
	echo "Looping process with $1 second(s) sleep"
	while true
	do
		load
		echo "Sleeping for $1 second(s)"
		sleep $1
	done
}

load_feedback_in_loop() {
	echo "Downloading feedback data in loop mode"
	while true
	do
		python .././src/Runner.py feedback --advanced
		sleep 1
	done
}

load_experimental_data_by_date() {
	python ExpressConnector_v4.py 1 $1
	python ExpressConnector_v4.py 2 $1
	python ExpressConnector_v4.py 3 $1
	python ExpressConnector_v4.py 4 $1
	python ExpressConnector_v4.py 5 $1
	python ExpressConnector_v4.py 6 $1
	python ExpressConnector_v4.py 7 $1
	python ExpressConnector_v4.py 8 $1
	python ExpressConnector_v4.py 9 $1
	python ExpressConnector_v4.py 10 $1
	python ExpressConnector_v4.py 11 $1
	python ExpressConnector_v4.py 12 $1
	python ExpressConnector_v4.py 14 $1
}


if [ $1 = '--report' ]
	then python .././src/runner.py report $2;
elif [ $1 = '--help' ]
	then help_info
elif [ $1 = '--all' ]
	then load
elif [ $1 = '--region' ]
	then python .././src/Runner.py $2
elif [ $1 = '--regionx' ] && [ $3 = '--range' ]
	then python .././src/Runner.py region $2 start $4 end $5
elif [ $1 = '--regionx' ] && [ $3 = '--page' ]
	then python .././src/Runner.py region $2 page $4
elif [ $1 = '--stats' ]
	then python .././src/Runner.py stats
elif [ $1 = '--watchlist' ]
	then python .././src/Runner.py watchlist $2
elif [ $1 = '--group' ]
	then load_region_in_groups $2 $3
elif [ $1 = '--query' ]
	then python PhoenixMobileConnectorUtil.py search $2 $3
elif [ $1 = '--chkdup' ]
	then python PhoenixMobileConnectorUtil.py duplicates $2
elif [ $1 = '--chkdup-all' ]
	then python PhoenixMobileConnectorUtil.py duplicates-all
elif [ $1 = '--fixdup' ]
	then python PhoenixMobileConnectorUtil.py duplicates-fix $2
elif [ $1 = '--chkfeed' ]
	then python PhoenixMobileConnectorUtil.py corrupt-data $2
elif [ $1 = '--chkfeed-all' ]
	then python PhoenixMobileConnectorUtil.py corrupt-data-all	
elif [ $1 = '--fixdup-all' ]
	then python PhoenixMobileConnectorUtil.py duplicates-fix-all
elif [ $1 = '--history' ]
	then python PhoenixMobileConnectorUtil.py historysearch $2
elif [ $1 = '--master-file' ]
	then python PhoenixMobileConnectorUtil.py master-file
elif [ $1 = '--feeds' ]
	then python PhoenixMobileConnectorUtil.py feeds
elif [ $1 = '--image' ] && [ $2 = '--update' ]
	then python .././src/Runner.py image update $3
elif [ $1 = '--image' ] && [ $2 = '--update-british-data' ]
	then python .././src/Runner.py image update-british-data
elif [ $1 = '--image' ] && [ $2 = '--standard' ]
	then python .././src/Runner.py image standard $3
elif [ $1 = '--image' ] && [ $2 = '--advanced' ]
	then python .././src/Runner.py image advanced $3
elif [ $1 = '--image' ] && [ $2 = '--master-file' ]
	then python .././src/Runner.py image master-file $3
elif [ $1 = '--image' ] && [ $2 = '--custom' ]
	then python .././src/Runner.py image custom $3
elif [ $1 = '--image' ] && [ $2 = '--verify' ]
	then python .././src/Runner.py image verify $3
elif [ $1 = '--image' ] && [ $2 = '--verify-empty-folders' ]
	then python .././src/Runner.py image verify-empty-folders
elif [ $1 = '--image' ] && [ $2 = '--delete-empty-folders' ]
	then python .././src/Runner.py image delete-empty-folders
elif [ $1 = '--image' ] && [ $2 = '--subgroup' ]
	then python .././src/Runner.py image subgroup $3 $4
elif [ $1 = '--loop' ]
	then load_in_loop $2
elif [ $1 = '--robomode' ]
	then load_in_loop 0
elif [ $1 = '--experimental' ] && [ $2 = '--all' ]
	then load_experimental_data_by_date $3
elif [ $1 = '--experimental' ] && [ $2 = '--delete' ]
	then python ExpressConnector_v4.py delete-experimental-data $3
elif [ $1 = '--experimental' ] && [ $2 = '--region' ]
	then python ExpressConnector_v4.py $4 $3
elif [ $1 = '--feedback' ] && [ $2 = '--standard' ]
	then python .././src/Runner.py feedback --standard
elif [ $1 = '--feedback' ] && [ $2 = '--robomode' ]
	then load_feedback_in_loop
elif [ $1 = '--feedback' ] && [ $2 = '--advanced' ]
	then python .././src/Runner.py feedback --advanced
elif [ $1 = '--feedback' ] && [ $2 = '--userId' ]
	then python .././src/Runner.py feedback --userId $3
elif [ $1 = '--userids' ]
	then python .././src/runner.py userIds $2
elif [ $1 = '--load-userids' ]
	then python .././src/Runner.py loadList ../static/watchlist.txt
elif [ $1 = '--details' ]
	then python .././src/Runner.py details
elif [ $1 = '--feedback-data' ] && [ $2 = '--f' ] && [ $4 = '--userId' ]
	then python PhoenixMobileConnectorUtil.py feedback-data today $3 $5
elif [ $1 = '--get-british-list' ]
	then python PhoenixMobileConnectorUtil.py "get-british-list"
elif [ $1 = '--get-ratings' ]
	then python .././src/Runner.py get-ratings
elif [ $1 = '--sp-update']
  then python .././src/Runner.py sp-update $2
fi

