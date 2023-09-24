import subprocess

# Define the command as a list of strings
command = ["cd", "src", "&&", "scrapy", "crawl", "quotes"]

options = ["--nolog","-o","../results/hi.jsonl"]

# Use subprocess to run the command
subprocess.run(command + options, shell=True)
