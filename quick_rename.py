#!/usr/bin/env
#Will rename files formatted __ basename #.csv__ to __ #_basename.csv__
#Checks the headers of imported data, if no header or header = [0,1], no header will be saved, is str header, header will be saved

#***EDITS***
#check index?
#check path, if not correct, allow new input

import os
import pandas as pd

class Files:
	def __init__(self,path=None):
		if path == None:
			path=input('What is the path where files to be renamed are located?\n\t')
		self.indir=self.check_path(path) #add code for what happens if path doesnt exist
		self.filelist=self.get_files(self.indir)

	def summary(self):
		print('%s Files accessed to be renamed:'%len(self.filelist))
		[print(file) for file in self.filelist]

	def get_files(self,path):
		'''Grabs only CSV files from input path
		TO BE DONE: allow for select only, exclude only option'''
		filelist=[file for file in os.listdir(path) if '.csv' in file]
		return filelist
	
	def check_frames(self):
		pass

	def check_path(self,path):
		'''Takes path, formats for / at end,
		TO BE check that path exists and execute appropriate responce'''
		#os.path.exists(path)
		pathend=path[-1]
		if pathend=='/':
			pass
		else:
			path=path+'/'
		return path

	def check_dir(self,dir):
		'''Checks if Directory exists, if not make it
		TO BE DONE: check if files are already in Dir if it exists'''
		if os.path.isdir(dir)==False:
			os.mkdir(dir)
		print('\nFiles will be saved in:\n\t%s\n'%dir)

	def isfloat(self,value):
		'''Checks if input value is a float or int (True), if string/other (False)
		Returns as Bool'''
		try:
			float(value)
			return True #value = float/int
		except ValueError:
			return False #value = string

	def import_csv(self,filepath):
		'''Import csv, check and apply headers
		Tested and working for diff import csv header options: 01/25/23
		TO BE DONE check for input index + # of columns'''
		df=pd.read_csv(filepath) #Initial DF
		test_val=df.columns[0] #Value of 1st col/row -> to be used to test input header type

		'''Use test_val to check default headers
		Tested and working for diff import csv header options: 01/25/23'''
		if self.isfloat(test_val)==True: #1st row is int/float
			if int(test_val)==0: #Has headers, default of 0,1
				df=pd.read_csv(filepath)
				str_header=False
			else: #Assume no headers
				df=pd.read_csv(filepath,header=None)
				str_header=False
		else:  #1st row is strings (assume headers)
			df=pd.read_csv(filepath,header=0) #import data has headers and they are strings
			str_header=True
		
		return df, str_header

class Rename(Files):
	'''Class Specific for Renaming Files'''
	def __init__(self,path=None): 
		super().__init__(path) #Inherent attributes from parent class
	
	def single_rename(self, alt):
		'''Takes default numbering from lightfield and moves to head of file name
		NOT DESIGNED FOR FRAMES
		TO DO add FRAMES'''
		justname=alt.split('.csv')[0] #name without .csv ending
		name_space_split=justname.split(' ')
		spectra_num=name_space_split[len(name_space_split)-1] #Grab the last split in the file base name
		new_base_name=''.join(name_space_split[:-1]) #Replaces spaces (' ') with (''); joins renaming spilts incase there is more than 1
		result_name=spectra_num[-2:]+'_'+new_base_name+'.csv'
		return result_name

	def exe(self):
		test_file=self.filelist[0]
		cont=input('\nThe file originally named \n\t%s \n\twill be renamed as \n\t%s \nContinue? (y or n)\t'%(test_file,self.single_rename(test_file)))
		
		if cont.lower()=='y':
			outdir=self.indir+'renamed/'
			self.check_dir(outdir) #ADD code to check dir and choose to continue
			for file in self.filelist:
				df,header_bool=self.import_csv(self.indir+file)
				df.to_csv(outdir+self.single_rename(file), index=False, header=header_bool)
			print('\nProgram complete. Files can now be found in %s'%outdir)
		else:
			print('\nProgram ended by User Input.')
	

if __name__=='__main__':
	mydir=Rename()
	mydir.summary()
	mydir.exe()