#!/usr/bin/env
#Will rename files formatted __ basename #.csv__ to __ #_basename.csv__
#Checks the headers of imported data, if no header or header = [0,1], no header will be saved, is str header, header will be saved

#***EDITS***
#check index?
#check path, if not correct, allow new input
#check that len(input list) == len(output list)

import os
import pandas as pd

class Files:
	def __init__(self,path=None):
		if path == None:
			path=input('What is the path where files to be renamed are located?\n\t')
		self.indir=self.check_path(path) #add code for what happens if path doesnt exist
		self.filelist=self.get_files(self.indir)

	def dir_summary(self):
		self.elem1, self.elem2, self.elem3, self.elem4 = self.inspect_files() #Checks the ending of file names, compares, returns results
		print(f'Element 1:{self.elem1}\nElement 2:{self.elem2}\nElement 3:{self.elem3}\nElement 4:{self.elem4}')

	def list_files(self):
		print('%s Files accessed:'%len(self.filelist))
		[print(file) for file in self.filelist]

	def get_files(self,path):
		'''Grabs only CSV files from input path
		TO BE DONE: allow for select only, exclude only option'''
		filelist=[file for file in os.listdir(path) if '.csv' in file]
		return filelist
	
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

	def isstring(self,x):
		'''dependancy of find_string'''
		try:
			float(x)
			return False #Value can be a float/int
		except ValueError:
			return True #Value is a string
	def find_string(self,input_list):
		'''dependacy of inspect_files'''
		single_string=''.join(list(set(input_list))) #convert from list to single string
		only_string_charaters=[e.lower() for e in single_string if self.isstring(e)==True] #test each character, see if it is a string
		result=list(set(only_string_charaters))
		return ''.join(result)
	
	def inspect_files(self):
		'''Looks at file names and parses out experimental information
		TO DO utilize the element unit function (maybe make output a dictionary ex{'s':[30s,60s]}'''
		elem1,elem2,elem3,elem4=[],[],[],[]
		for file in self.filelist:
			justname=file.split('.csv')[0]
			splits=justname.split('_')
			elem1.append(splits[-1])
			elem2.append(splits[-2])
			elem3.append(splits[-3])
			elem4.append(splits[-4])
		#element_units=[self.find_string(elem1), self.find_string(elem2), self.find_string(elem3), self.find_string(elem4)]
		return list(set(elem1)), list(set(elem2)), list(set(elem3)), list(set(elem4))	

class Rename(Files):
	'''Class Specific for Renaming Files'''
	def __init__(self,path=None): 
		super().__init__(path) #Inherent attributes from parent class
	
	def rename(self,alt):
		'''Function to ID if file has Frame or not, then direct to correct renaming function.
		Low priority TO DO = combine all 3 functions into 1'''
		if 'Frame' in alt:
			neu=self.frame_rename(alt)
		else:
			neu=self.frameless_rename(alt)
		return neu

	def frameless_rename(self, alt):
		'''Takes default numbering from lightfield and moves to head of file name
		NOT DESIGNED FOR FRAMES
		TO DO add FRAMES'''
		justname=alt.split('.csv')[0] #name without .csv ending
		name_space_split=justname.split(' ')
		spectra_num=name_space_split[len(name_space_split)-1] #Grab the last split in the file base name
		new_base_name=''.join(name_space_split[:-1]) #Replaces spaces (' ') with (''); joins renaming spilts incase there is more than 1
		result_name=spectra_num[-2:]+'_'+new_base_name+'.csv'
		return result_name
	
	def frame_rename(self,alt):
		justname=alt.split('.csv')[0] #name without .csv ending
		name_space_split=justname.split(' ')
		num_and_frame=name_space_split[len(name_space_split)-1] #Grab last split, contains spec#-Frame-f#
		spec_num, frame_num=num_and_frame.split('-Frame-')[0][-2:],num_and_frame.split('-Frame-')[1]
		new_base_name=''.join(name_space_split[:-1]) #Replaces spaces (' ') with (''); joins renaming spilts incase there is more than 1
		result_name=spec_num+'-'+frame_num+'_'+new_base_name+'.csv'
		return result_name

	def name_main(self):
		test_file=self.filelist[0]
		cont=input('\nThe file originally named \n\t%s \n\twill be renamed as \n\t%s \nContinue? (y or n)\t'%(test_file,self.rename(test_file)))
		
		if cont.lower()=='y':
			outdir=self.indir+'renamed/'
			self.check_dir(outdir) #ADD code to check dir and choose to continue
			for file in self.filelist:
				df,header_bool=self.import_csv(self.indir+file)
				df.to_csv(outdir+self.rename(file), index=False, header=header_bool)
			print('\nProgram complete. Files can now be found in %s'%outdir)
		else:
			print('\nProgram ended by User Input.')
		
if __name__=='__main__':
	'''TO DO
	Set a default path (like to the Data directory)
	Loop back if path does not exist
	Make exist code its own function
	'''
	print('\nWelcome to the File Circus.') #Define a prompt, give user options
	prompt ='\nEnter a directory path to begin\not enter \'quit\' to... quit.\n\t'
	
	def run(name,dic): #Call functions based on user input from dictionary
		dic[name][1]()

	while True:
		mypath=input(prompt)

		if mypath.lower()=='quit':
			break
		else:
			while True:
				exist=os.path.isdir(mypath)
				if exist == True: #Path exists, initalize object and offer selections
					print('\n\nThe Following functions are available to run on %s:\n'%mypath)

					options={'1':('List the .csv files in the directory.',Rename(mypath).list_files),
					'2':('Check file names for experimental info.',Rename(mypath).dir_summary),
					'3':('Execute file rename program.',Rename(mypath).name_main)}
					[print('\t%s : %s'%(o,options[o][0])) for o in options]

					select=input('\nEnter a number (or \'back\' to enter new path):\t')

					if select.lower()=='back':
						break
					else:
						print()
						run(select,options)
				elif exist == False:
					print('Path does not exist.')