# Table of Contents

1. [Description](#brotein)
2. [Screenshots](#screenshots)
  1. [Whey Powder Calculator](#whey-powder-calculator)
  2. [Protein Snack Calculator](#protein-barchipcookie-calculator)
3. [How tos](#how-tos)
  1. [Run](#run)
  2. [Host](#host)

# Brotein
Just a simple repo to compare protein powder of all types

# Screenshots

## Whey Powder Calculator
<img src="https://github.com/pomkos/brotein/blob/master/brotein_pro.png" width="620">

## Protein Bar/Chip/Cookie Calculator
<img src="https://github.com/pomkos/brotein/blob/master/brotein_snack.png" width="620">

# How tos
## Run

1. Clone the repository:
```
git clone https://github.com/pomkos/brotein
cd brotein
```

2. Create a conda environment (optional):

```
conda create --name "bro_env"
```

3. Activate environment, install python, install dependencies.

```
conda activate bro_env
conda install python=3.8
pip install -r requirements.txt
```
3. Start the application:
```
streamlit run brotein.py
```
5. Access the portfolio at `localhost:8501`

## Host

1. Create a new file outside the `brotein` directory:

```
cd
nano brotein.sh
```

2. Paste the following in it, then save and exit:

```
#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh

cd ~/brotein
conda activate bro_env

nohup streamlit run brotein.py --server.port 8502 &
```

3. Edit crontab so portfolio is started when server reboots

```
crontab -e
```

4. Add the following to the end, then save and exit

```
@reboot /home/brotein.sh
```

5. Access the website at `localhost:8502`
