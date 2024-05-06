from sys import argv,exit
from abc import abstractmethod
import os
import boto3
from mltk.core import profile_model
import json
import matplotlib.pyplot as plt
import paramiko

class ModelBase:
    """
    Base SDK class consist of defined methods which are used on different templates 
    and abstract methods that need to be implemented in the sub classes
    """

    """
    Below mentioned methods are defined methods that are used in the template methods
    and these methods logic remanins the same
    """
    def __init__(self, s3_bucket, model_key, model_ouput_path):
        self.s3_bucket = s3_bucket
        self.model_key = model_key
        self.model_output_path = model_ouput_path
        # print("Bucket: %s" % self.s3_bucket)
        # print("Model key: %s" % self.model_key)

    def validateUser(self) ->None:
        print("check username availale in DB")
        print("validate user password in DB")
    
    def getAuthToken(self)->None:
        print("Fetch Auth Token implementation")
    
    def validateAuthToken(self)->None:
        print("Validate Fetched Auth Token")

    def getDataset(self, filePath)->None:
        print("Validate data set")
        if os.path.exists(filePath):
            print("File exists....")
            return filePath

        print("Dataset file does not exist, checking in repository")
        # TODO: check if the file exists in the list
        print("Downloading dataset file...")
        # bucket name, s3 file path, output file directory
        Bucket = self.s3_bucket
        Key = self.model_key + filePath
        Filename = self.model_output_path
        s3client = boto3.client('s3')
        s3client.download_file(Bucket, Key, Filename)
        filePath = self.model_output_path
        return filePath
    
    def getModel(self, filePath) -> str:
        if os.path.exists(filePath):
            print("File exists....")
            return filePath

        print("File does not exist, checking in repository")
        # TODO: check if the file exists in the list
        print("Downloading file...")
        # Key = "yolo-v8-pose/v1/yolov8n-pose_float32.tflite"
        Bucket = self.s3_bucket
        Key = self.model_key + filePath
        Filename = self.model_output_path
        s3client = boto3.client('s3')
        s3client.download_file(Bucket, Key, Filename)
        filePath = self.model_output_path
        return filePath

    def getProfileInfo(self , model_file)->None:
        print("Profiling for "+ model_file)
        profiling_results = profile_model(model_file,return_estimates=True).to_json(indent=2, format_units=True, exclude_null=True, full_summary=False)
        return profiling_results
    
    def compareMetrics(self , unQuantizedModel , quantizedModel)->None:
        print("Metrics Comparison")
        metrics_uq = self.getProfileInfo(unQuantizedModel)
        metrics_q = self.getProfileInfo(quantizedModel)
        prof_1 = json.loads(metrics_uq)
        prof_2 = json.loads(metrics_q)

        data1 = prof_1['summary']
        data2 = prof_2['summary']
        keys_to_drop = ["name", "accelerator" , "input_shape" , "input_dtype" , "output_shape" , "output_dtype"]
        val1 = data1['name']
        val2 = data2['name']
        # Drop the keys
        for key in keys_to_drop:
            if key in data1:
                del data1[key]
                
        for key in keys_to_drop:
            if key in data2:
                del data2[key]

        # Get the keys (assuming they are the same in both JSON objects)
        keys = list(data1.keys())

        # Calculate the number of rows and columns for the subplots
        n = len(keys)
        ncols = 4
        nrows = n // ncols + (n % ncols > 0)

        # Create a figure and a grid of subplots
        fig, axs = plt.subplots(nrows, ncols, figsize=(20, 5*nrows))

        # Flatten the array of axes
        axs = axs.flatten()


        # Generate a subplot for each key
        for i, key in enumerate(keys):
            values1 = data1[key]
            values2 = data2[key]
            axs[i].bar([val1 , val2], [values1, values2])  # Plot the values
            axs[i].set_title(f'Comparison of {key}')
            axs[i].set_ylim(0,20)

        # Remove unused subplots
        for j in range(i+1, len(axs)):
            fig.delaxes(axs[j])

        plt.tight_layout()
        plt.savefig("metrics_comparison_chart.png")
    
    def uploadModel(self, local_path, remote_path, hostname, username, password):
        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        # SCP a file from local to remote
        sftp = ssh.open_sftp()
        sftp.put(local_path, remote_path)
        print("Model upload successful")
        sftp.close()

        # Close SSH connection
        ssh.close()
        

    """
    Abstract class methos these methods doesn't have any implementation but these
    are requried to be implemented in the inherited subclasses
    """
    
    @abstractmethod
    def loadModel(self)->None:
        pass
    
    @abstractmethod
    def trainModel(self)->None:
        pass
    
    @abstractmethod
    def generateModel(self)->None:
        pass
    
    @abstractmethod
    def quantizeModel(self)->None:
        pass
    
    @abstractmethod
    def predictModel(self)->None:
        pass
    
    @abstractmethod
    def validateModel(self)->None:
        pass

class ModelFrameWork(ModelBase):
    """
Template Methods that define the template which follows a specific order of executing
above mentioned methods
"""
 
    def login(self)->None:
        self.validateUser()
        self.getAuthToken()
 
    def train(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.getDataset()
 
    def generate(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.loadModel()
        self.generateModel()
 
    def quantize(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.loadModel()
        self.quantizeModel()
 
    def predict(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.getDataset()
        self.loadModel()
        self.predictModel()
 
    def validate(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.getDataset()
        self.loadModel()
        self.validateModel()
 
    def profile(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.getModel()
        self.getProfileInfo()
 
    def compare(self)->None:
        self.validateAuthToken()
        self.getAuthToken()
        self.getModel()
        self.getProfileInfo()

class Auth:

    def validateUser(self) ->None:
        print("check username availale in DB")
        print("validate user password in DB")
    
    def getAuthToken(self)->None:
        print("Fetch Auth Token implementation")
    
    def validateAuthToken(self)->None:
        print("Validate Fetched Auth Token")      

class YOLO(ModelFrameWork):
    """
    Implementation of abstract class methods that required in the template method
    """ 

    def loadModel(self)->None:
        print("Implementation of Loadmodel")
    

    def trainModel(self)->None:
        print("Implementation of trainModel")
    

    def generateModel(self)->None:
         print("Implementation of generateModel")
    

    def quantizeModel(self)->None:
        print("Implementation of quantize Model")
    


    def predictModel(self)->None:
        print("Implementation of predict Model")
    
    def validateModel(self)->None:
        print("Implementation of validate Model")

class PyTorch(ModelFrameWork):
    """
    Implementation of abstract class methods that required in the template method
    """ 

    def loadModel(self)->None:
        print("Implementation of Loadmodel")
    

    def trainModel(self)->None:
        print("Implementation of trainModel")
    

    def generateModel(self)->None:
         print("Implementation of generateModel")
    

    def quantizeModel(self)->None:
        print("Implementation of quantize Model")
    

    def predictModel(self)->None:
        print("Implementation of predict Model")
    
    def validateModel(self)->None:
        print("Implementation of validate Model")

class TF(ModelFrameWork):
    """
    Implementation of abstract class methods that required in the template method
    """ 

    def loadModel(self)->None:
        print("Implementation of Loadmodel")
    

    def trainModel(self)->None:
        print("Implementation of trainModel")
    

    def generateModel(self)->None:
         print("Implementation of generateModel")
    

    def quantizeModel(self)->None:
        print("Implementation of quantize Model")
    

    def predictModel(self)->None:
        print("Implementation of predict Model")
    
    def validateModel(self)->None:
        print("Implementation of validate Model")
