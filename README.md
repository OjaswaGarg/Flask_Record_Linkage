# Flask_Record_Linkage
## Collaborators
### [Ojaswa Garg](https://github.com/OjaswaGarg)
### [Adhiraj Srivastava](https://github.com/adhirajms)
### [Vijay Nallapaneni](https://github.com/vij95)

This github repository helps in hosting a Flask API on Azure.
The record linkage models can be accessed with the help of below links-
- https://recordlinkage.azurewebsites.net/
- https://bit.ly/record_linkage

Through our project we wanted to provide a pipeline which helps in matching records while ensuring that privacy of the individuals is protected. The project focuses on finding an efficient approach to perform record linkage. Given two datasets which contain records, the record-linkage problem consists of determining all pairs that are similar to each other.

## How to run
- Run the command  ``` pip3 install -r requirements.txt ``` to install all the dependencies (Python 3).
- The script, ```test.py``` is the final script. The datasets are already provided. 
- Sample way to run the script via terminal is using the command ```python test.py output1.csv output2.csv output.csv```
