# PemsBay2022

## Preprocessing codes for Pems-BAY-2022 dataset

1. Step 1 : Download raw data

    1-1. go to https://pems.dot.ca.gov/ and log in
  
    1-2. go to https://pems.dot.ca.gov/?dnode=Clearinghouse
  
    1-3. select "Station 5-Minute" and "District 4"
  
    1-4. Click files in "Available Files"
  
    1-5. make a folder named "raw_data" and make folders by month ex) 01, 02, 03, ...
    
    1-6. put the downloaded files in the folders
  
2. Step 2 : Preprocess

    2-1. run 
  ```
  python process.py
  ```
  
3. Step 3 : Enjoy


## Download preprocessed data

https://drive.google.com/drive/folders/1mKajP35NChMTJ1dqIzD9J-z2QNvqJXlo?usp=sharing

## Related Links
PEMS-BAY data was first used in https://github.com/liyaguang/DCRNN, which contained observations from Jan 1st 2017 to May 31th 2017.


## Notes
Sensors ['401495', '402288', '402289', '402368', '402369', '404554'] doesn't have observations at all.
