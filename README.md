# bruteforce-wallet-balance

If you found this uselful, please submit a STAR ⭐

Scripts with the functionality of create 12 words seed, create BTC wallet and check online if the balance is positive, in case save the address and the private key.
With my API, it can check around 500 wallet every second (300 on AWS istance), but it depends on your hardware. 500 is achieve on pc with Ryzen 4600U, 16GB RAM and NVME SSD.

To run it you need to replace with your OWN endpoint here:
```
MULTIPLE_ADDRESS_ENDPOINT = {
    "api1":["url1",100],
    "api2":["url2",200],
    "name endpoint":["url endpoint",50]
    
}
```
The number after "url endpoint" is the number of address that append to link when make the request. If your endpoint support only one address per request put 1.

## A lot of API key
You can add many API to search in more thread

## Setup
Run ```pip install name_module``` to install missing modules

## Start
```python3 multithreading_multiple_address.py```

## Run on aarch64
Run it on low istance on AWS or raspberry pi 4b can not work, sometimes it throw this error ***ValueError: unsupported hash type ripemd160***

[Solution source](https://stackoverflow.com/questions/72409563/unsupported-hash-type-ripemd160-with-hashlib-in-python/72508879#72508879)

To avoid this and run without problems, follow this steps:
Find where is your openssl directory: ```openssl version -d```

You can now go to the directory and edit the config file with sudo: ```nano openssl.cnf```

Make sure that the config file contains following lines:
```
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
legacy = legacy_sect

[default_sect]
activate = 1

[legacy_sect]
activate = 1
```

## Tip
BTC Address to donate
```bc1q9wcw572a6k5q58kegjf49k4m49cakf8uavtt95```

