# Brotein
Just a simple repo to compare protein powder of all types

# How-To

1. Clone this repo `git clone https://github.com/pomkos/brotein`
2. Create a new conda environment with python 3.6, then install the libraries
  ```bash
  conda create --name bro_env python=3.6
  conda activate bro_env
  cd brotein
  pip install -r recommendations.txt
  ```
3. Run within the environment with `streamlit run brotein --server.port 8512`, it will be accessible at localhost:8512

To run in "prod":

* Create the following script
```
#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh

cd /dir/to/bro_env
conda activate bro_env # activate the new conda env

nohup streamlit run brotein.py --server.port 8512 & # run in background
```
* Make it executable with `chmod +x my_script.sh`
* You can exit the terminal and streamlit will continue serving the python file. 
* Cronjob to have the server start at each reboot:
```bash
crontab -e
@reboot /home/peter/scripts/payme.sh #add this line at the bottom
```

# Screenshot
![](image.png?raw=true)
