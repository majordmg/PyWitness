# Usage

```
python witness.py domains.txt
```

where "domains.txt" is the path to the file containing your domains, one domain on each line, e.g.:

```
reddit.com
instagram.com
python.org
```

Make sure you've got the Firefox geckodriver in your PATH variable. 

# How it works

This script uses nmap to scan the domain input file for common web ports, then opens the domains with selenium and saves a screenshot. You will see a progress bar while the script works.

After it's complete, it will open a final view of each domain (with port and protocol) and a thumbnail image in the selenium browser. 

# Results 

You will see the results in the headful browser that the script opens after completion, but the images and viewer will also be saved in a timestamped subfolder under "archives", so you can view them any time. 

# The motivation

My goal was to create a very lightweight and easy to use alternative to EyeWitness and others. EyeWitness wouldn't work in my environment, and so I figured it was faster to just code my own version for my own purposes. This is nowhere near complete or perfect, but I really don't need it to be. PyWitness does not include batteries by design -- I don't want to have to run a setup script, or an executable, have a big GUI experience, or anything like that. This is a tool I wrote for myself, that might be useful for other coders who are interested in OSINT and security. Hope you get the same mileage out of this tool as I do. 

Feel free to open issues or suggest features! 