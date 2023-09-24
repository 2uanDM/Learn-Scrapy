import subprocess

def run(spider_name: str, export_file: str):
    # Define the command as a list of strings
    command = ["cd", "src", "&&", "scrapy", "crawl", spider_name]

    options = ["--nolog","-o",f"../results/{export_file}","-a","dont_overwrite=True"]

    # Use subprocess to run the command
    subprocess.run(command + options, shell=True)

if __name__ == '__main__':
    run(spider_name='authors', export_file='authors.csv')
