requirements.out:
	pip3 install -r requirements.txt

#updated_yt_data/2019-12-29__2020-01-05.csv: initial_downloader.py master_controller.py ytsearch.py devkeys.py requirements.out
#	python3 $<

analysis/all_week_data.csv analysis/week_view_count.png: basic_analysis.R updated_yt_data/2019-12-29__2020-01-05.csv
	Rscript $<

