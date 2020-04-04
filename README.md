# ocr-information-on-id-drivers-license-passport
This program was created to retrieve data on ID cards (Indonesian Citizenship Cards), Indonesian driver's license, new versions of Indonesian driver's license and passports using the tesseract-ocr v4. First, mrz (machine-readable zone) will detect whether there is a zone that contains text. Then, it will take that area as a roi (region of interest).
Then, the roi results will be thresholded and extracted into text using tesseract-ocr.
## Pre-requisites
* Opencv
* Tesseract-ocr v4
* Flask
* Elasticsearch

## How to use
1. Run main.py on terminal
   ```
   $ python3 main.py
   ```
2. Start the elasticearch service on terminal
   ```
   $ sudo -i service elasticsearch start
   ```
3. There are two ways to enter the picture as input
   * Using terminal
     * ktp
       ```
       $ curl -F “ktp=@ktp.jpg” http://localhost:5000/
       ```
     * sim
       ```
       $ curl -F “sim=@sim.jpeg” http://localhost:5000/
       ```
     * sim_new
       ```
       $ curl -F “sim_new=@sim_new.jpeg” http://localhost:5000/
       ```
     * passport
       ```
       $ curl -F “paspor=@passport.jpg” http://localhost:5000/
       ```
   * Using Postman
     1. Setting request method to POST, click the 'body' tab.
     2. Select form-data. At first line, you'll see text boxes named key and value.
     3. Write 'ktp/sim/sim_new/paspor' to the key. 
     4. You'll see value type which is set to 'text' as default.
     5. Make it File and upload your file.
     6. And it will look like the picture below.
     ![Screenshot from 2020-04-04 14-59-51](https://user-images.githubusercontent.com/62472280/78424461-e60d6c00-7697-11ea-875f-eec6f9cf9e4e.png)
