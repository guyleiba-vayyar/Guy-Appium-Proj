import csv
import os
import operator
import time
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib

import tkinter as tk
import numpy as np

from datetime import datetime
from collections import defaultdict
import pandas as pd
import re


#global varibles
csv_result=[]



class Frame_Rater():

    def __init__(self,folder):
        self.destination_folder=folder
        self.plt=plt

    def trigger_analyzer(self):

        basepath = Path(self.destination_folder)
        files_in_basepath = basepath.iterdir()
        new_folder_path = os.path.join(basepath, "Scatters")
        self.new_folder_creator(new_folder_path)
        basepath_str = str(basepath)
        new_csv_file = basepath_str + '\\' + "FrameRateSummarization.csv"

        for item in files_in_basepath:  # loop log in folder
            if item.suffix == '.txt':

                if "log" in item.stem:
                    continue

                with open(item, 'rt') as logfile:
                    current_filename = str(item.name)  ## each line will get this value at start
                    csvfile = open(new_csv_file, 'w', newline='')
                    fieldnames = ['File Name', 'Mean FR', 'Mean FR below 300ms T2T', 'Mean FR below 500ms T2T',
                                  'Mean FR below 1000ms T2T', "Freezes % T2T", "Freeze mean T2T", "STD Freezes T2T",
                                  "STD FR T2T", "OTA version"]
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    trigger_list = self.csv_writer(logfile, current_filename)
                    self.create_scatter_plot(trigger_list, str(new_folder_path), item.stem)

                writer.writeheader()
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(csv_result)




    def create_scatter_plot(self,trigger_lst,folder_path,file_name):

    #trigger_lst is dict, the function creates scatters from the lists

        plt.clf()
        real_arr=[]
        ms_arr=[]
        for x in range(len(trigger_lst)):
            for time_real,time_ms in trigger_lst[x].items():
                ms_arr.append(float(time_ms))
                real_arr.append(float(time_real))

        plt.scatter(real_arr,ms_arr,s=10) #this currntly not accurete
        plt.xlabel('Time[S]')
        plt.ylabel('Freeze duration[ms]')
        plt.axhline(y=300, color='r', linestyle='-',label='Below 300ms')
        plt.axhline(y=500, color='b', linestyle='-',label='Below 500ms')
        plt.axhline(y=143, color='g', linestyle='-',label='Below 143ms')
        x1, x2, y1, y2 = plt.axis()
        plt.axis((x1, x2, 0, 500))
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.grid()
        plt.savefig(folder_path + '\\' + file_name + ".png", bbox_inches='tight')



    def csv_writer(self,logfile,filename):

        meanfr_lst=[]
        meanfr_low300_lst=[]
        meanfr_low500_lst=[]
        meanfr_low1000_lst=[]
        freeze_lst=[]
        freeze_mean=[]
        std_freeze=[]
        trig_list=self.trigger_creator(logfile) #trigger_creator is a function

        for i in range(len(trig_list)): # i index is neccessary cause this is a list of dictionaries
            for t_ms in trig_list[i].values(): #looping through the values of the dict
                meanfr_lst.append(float(t_ms))
                if float(t_ms)<=300:
                    meanfr_low300_lst.append(float(t_ms))
                elif float(t_ms)<=500:
                    meanfr_low500_lst.append(float(t_ms))
                elif float(t_ms)<=1000:
                    meanfr_low1000_lst.append(float(t_ms))
                elif float(t_ms) >= 1000:
                    freeze_lst.append(float(t_ms))

        try:
            meanfr=sum(meanfr_lst)/len(meanfr_lst)
            meanfr_low300= sum(meanfr_low300_lst)/len(meanfr_low300_lst)
            meanfr_low500 = sum(meanfr_low300_lst) / len(meanfr_low300_lst)
            meanfr_low1000 = sum(meanfr_low300_lst) / len(meanfr_low300_lst)
            freeze_precent= float(len(freeze_lst)/len(trig_list))
            std_fr=np.std(meanfr_lst)

            if (len(freeze_lst)>0):
                freeze_mean=sum(freeze_lst)/len(freeze_lst)
                std_freeze=np.std(freeze_lst)

        except ZeroDivisionError:
            print(logfile.name+ " is empty")

        if len(meanfr_lst)!=0:
            items = [filename,meanfr,meanfr_low300, meanfr_low500, meanfr_low1000,freeze_precent,freeze_mean,std_freeze,std_fr]
            csv_result.append(items)

        return trig_list

    def trigger_creator(self,logfile): #recievel logfile and returns dict with time:ms

        trigger_list=[]
        fir_index=0

        for current_line in logfile:

            if (current_line.find("vDIY version")!= -1):
                trigger_list = []

            if (current_line.find("API_START] WALABOT_RESULT Walabot_Trigger()")!= -1) and (fir_index==0):
                initial_time = current_line.split()[0]
                fir_index=1

            if (current_line.find("API_START] WALABOT_RESULT Walabot_Trigger()")!= -1) and (current_line.split()[0]!=initial_time):
                end_time= current_line.split()[0]
                fir_index=0

                diff_time= (float(end_time)-float(initial_time))*1000  #turning it to ms
                if (diff_time<=10000):
                    trigger_dict={ #dict containging the time and the ms
                        initial_time: str(diff_time).split('.')[0]
                    }
                    trigger_list.append(trigger_dict)


        return trigger_list


    def new_folder_creator(self,path):
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)


