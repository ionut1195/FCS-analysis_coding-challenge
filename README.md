# FCS Analysis

## Build docker image and start container

### Run `docker build -t fcs-analysis .` command to build the docker image

### Run `docker run -d -p 8000:8000 --name fcs-analysis fcs-analysis` command to start the container mapping the port 8000 of the localhost to port 8000 of the container

## Analyze data

### Step 1 - upload **.fcs** file

#### Run `curl -X POST -F "file=@<file-path>" http://localhost:8000/upload-fcs/` command

Replace **<file-path>** with the **.fcs** file path.  
Example: _C:/Users/ion/Desktop/RobotDreams/0001[WDF].fcs_

### Step 2 - retrieve predictions

#### Run `curl http://localhost:8000/predictions/` command to retrieve predictions

The predictions are stored in a dictionary  
Sample _{"scatter_Side_Scatter_Signal_vs_Side_Fluorescence_Signal":0.5068019032478333,"scatter_Side_Scatter_Signal_vs_Forward_Scatter_Signal":0.5052300095558167}_

### Retrieve a scatterplot image

#### Run `curl -OJ http://localhost:8000/plot/<plot-name>` to retreive an image, use one of the keys in the dictionary returned after running the previous command

Replace **<plot-name>** with the respective key and add **.png**  
Example: _curl -OJ http://localhost:8000/plot/scatter_Side_Scatter_Signal_vs_Side_Fluorescence_Signal.png_
