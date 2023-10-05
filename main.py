import subprocess

def run(spider_name: str, **kwargs):
    # Define the command as a list of strings
    command = ["cd", "src", "&&", "scrapy", "crawl", spider_name]

    # Add the arguments
    if kwargs.get('export_dir'):
        if kwargs.get('overwrite'):
            command += ["-o", f"../results/{kwargs['export_dir']}", "-a", "dont_overwrite=False"]
        else:
            command += ["-o", f"../results/{kwargs['export_dir']}", "-a", "dont_overwrite=True"]
       
    if kwargs.get('nolog'):
        command += ["--loglevel=ERROR"]

    # Use subprocess to run the command
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    run(spider_name='quotes')
