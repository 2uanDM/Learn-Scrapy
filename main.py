import subprocess

# Define the command as a list of strings
command = ["cd", "src", "&&", "scrapy", "crawl", "quotes"]

options = ["--nolog","-o","../results/hi.csv","-s","FEED_EXPORT_ENCODING=utf-8","-a","dont_overwrite=True"]

# Use subprocess to run the command
subprocess.run(command + options, shell=True)
