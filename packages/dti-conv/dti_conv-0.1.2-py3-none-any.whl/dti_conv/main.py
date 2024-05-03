print("Loading")
import inquirer as iq
import shutil
from brukerapi.dataset import Dataset
import tkinter as tk
from tkinter import filedialog
#from dti import DTI
#from visual import qualityChecker
import subprocess
import warnings
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons
import nibabel as nib
from dipy.io.image import load_nifti, save_nifti
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.reconst.dti import TensorModel
from dipy.segment.mask import median_otsu
import dipy.reconst.dti as dti
from dipy.core.histeq import histeq
import math
import numpy as np
import time
import SimpleITK as sitk
import os
#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import db
#from uuid import getnode as get_mac
import sys

root = tk.Tk()
#root.mainloop()

print("Checking License")
warnings.filterwarnings("ignore")
"""
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "dwi-license",
  "private_key_id": "6c6c9e3f2d4629b5604c8abcc59db528534e5788",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDeHIC0gFc/slXK\nJYSRBpy3WwnRHJAtkiHaFvFNpC4QxVgG7OgWxVRue/1fne23Vq3uUWboFMAWlltD\nu4WAQ5JaR+e9I4Wsa4kaP0evfFjuPDCYuHYyvDECHNWg8AeZBKdEdx6KrzWg6is6\n2ly04+kYjHcHYWvNv/1rPvs2M+PS5IC980R3D5BufNNFNt7v7CGZuXLkD/XYexp0\nggCHuAFk61PpcTMmP+IYm6/xOiE7lIviWg6zw6pdBV2c64haZRMwYcgExEmYVfUR\nGP3/qpMqzyTpLPP+Mb4aXKx82MS5maQljc7UQgAV8+yjMARGEs+SAJlJNNtxMJjw\nMP08/8YFAgMBAAECggEADd6wyNTE3gToZ42tOBM2IRsNw2GpvTbFZ2WMXwFUIRb5\ntsD/g0CCU73pZhmqGQtQJDQwHWkCT8bG3zVsEkTl9D5OQdjghZJXhuyRsOsucH4Q\nuNC4DNYEp3Geg4TJrKwGN/fKT/W9/xTwayXsqR0cVryayDq0rS4CiLpvnIRkAyzE\n5vFucsfUg3YzGEdTm8kKFolCV7aXzRh9i8Ial4wBkoz1z/zedfWFX1K2kIb81Ynq\ndxphJIRhMFaqBTCkz8K/yPfRwZRBi3K8WpjF1giQUqxGvF8Rgy0UUamPoFYFGFeK\nDwBQKs+z3dz6587dxJiWVEyGs3dHKydXyZBog9yOpwKBgQD+mv8O2yyJLM0+nooC\nspV1pZzvEYXheljbSghhCv9ZCejcSZ4lrk4a95AUaYv0qyhmvxHtSJySsn5eV/4p\nkudRviHvFwy1tB1ovx68BV9TrVWcW8uWOkbeEWTiFcwM4v30UYHWUFjuTLLwlyLI\nJUXxKzH5TjOFBI/L5LCsUm1cVwKBgQDfU/GWxb+61Ew+BBKMSg8WUiuJDB+03jma\nAl5z8Mh55/DF8coUVDI/7fcQ1X5cUnKWe8X5A/gqGxH37aengO1ZH/Qsya+AJKIm\nlmcy4heOevdli1wOdqiBmHEYUb23qMeDAZf8csdnkvePr7yxSwhsn71kNg6XK+J0\nWZZEc4c3AwKBgFRpTua+A6X3FJUOOvNqAeNfZQhd5uU6ivspMF38J2x9vJZMUgJs\nJ7kJGtupop0boelur6Lb0A1S4FKnGbzu14JiZx29ppkXfiicNLRhk5lKfne4d2b3\nK0e0vJ24XE5pc4js/P7w5IsdIrZhZUa2FNpAV/Ev3CTdvk77Ixf+vANBAoGBAJjn\nuYZYeJBrYJQpZ6Wj4zaOJf6cTW0hpeCbdJ3/ItPMiR6OEKTgjNMWk81zzyNY09nS\nftai8BusEx5kGiDmdhtKdHzhzgZ3jonK+ndtM2G7MX3V7757YZ3xiKV0+ecwaQF6\natxOndZ9WoCHezMMQ4VTzXE6Tb0VL+QnnmnZi5+PAoGBAL5Fv8FrDpZ+5f4+l0ug\nHoWelE24IvXNx1o5CuKc/dlMN2SBKFLV9y2VfO8/xlmYcEOzVqlXNVjoGdWedaeT\nBcLFVEBDLykIfmeDm+lrmU/657HNvwJYy+ctSLIikYOplT3ULYzjufAXmD489z0g\nQ+Lcnsn80geo84mX1iCLnfeR\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-8f49g@dwi-license.iam.gserviceaccount.com",
  "client_id": "111248139098610310989",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-8f49g%40dwi-license.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred, {
    "databaseURL": "https://dwi-license-default-rtdb.firebaseio.com/"
})

ref = db.reference("/")
MAC_add = hex(get_mac())[2:].upper()
MAC_add = "-".join(MAC_add[i:i+2] for i in range(0, len(MAC_add), 2))
if MAC_add not in ref.get():
    print("Invalid License")
    sys.exit()
else:
    print("Confirmed License")

"""
class Pipeline:
	def __init__(self):
		self.premier_folder = ""
		self.SEPERATOR = "__________________________________"
		self.direction_omitter = {}

	def get_premier_folder(self):
		self.premier_folder = filedialog.askdirectory(title="Select folder containing scans.")
		print("Selected: " + os.path.abspath(self.premier_folder))
		self.dti_instance = DTI(self.premier_folder)
		print(self.SEPERATOR + "\n")

	def get_output_folder(self):
		self.output_folder = filedialog.askdirectory(title="Select output_folder")
		print("Selected: " + os.path.abspath(self.premier_folder))
		self.dti_instance.output_folder = self.output_folder
		print(self.SEPERATOR + "\n")

	def save_nifti(self, img, OUTPUT_PATH):
		nib.save(img, OUTPUT_PATH)

	def run_quality_checker(self):
		print("Creating quality_checkers...", end="")
		for scan, numb in self.dti_instance.dti_scans.items():
			OUTPUT_DIR = os.path.join(self.output_folder, os.path.basename(scan))
			if not os.path.isdir(OUTPUT_DIR):
				os.mkdir(OUTPUT_DIR)
			for idx, img in enumerate(self.dti_instance.dti_imgs[scan]):
				path = os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_" + os.path.basename(numb[idx]) + ".nii")
				self.save_nifti(img, path)
				qual = qualityChecker(path)
				qual.run()
				self.direction_omitter[os.path.basename(path)] = qual.directions
		print("Done")
		plt.close()
		print(self.SEPERATOR + "\n")

	def getParameters(self):
		questions = [iq.Checkbox('Saves',
							message="What files do you want to save?",
							choices=['Anatomy', 'FA', 'ADC', 'b0', "RD"],
							),]
		answers = iq.prompt(questions)
		return answers["Saves"]

	def parse_parameters(self):
		parameters = self.getParameters()

		self.bool_anatomy = False
		self.bool_fa = False
		self.bool_adc = False
		self.bool_b0 = False
		self.bool_rd = False

		if "Anatomy" in parameters:
			self.bool_anatomy = True
		if "FA" in parameters:
			self.bool_fa = True
		if "ADC" in parameters:
			self.bool_adc = True
		if "b0" in parameters:
			self.bool_b0 = True
		if "RD" in parameters:
			self.bool_rd = True

	def save_files(self):
		for scan, numb in self.dti_instance.dti_scans.items():
			OUTPUT_DIR = os.path.join(self.output_folder, os.path.basename(scan))
			if numb:
				if self.bool_fa or self.bool_adc or self.bool_b0:
					for number in numb:
						img = nib.load(os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+".nii"))
						dim = self.dti_instance.getVoxelSize(number)
						method_file = os.path.join(number, "method")
						self.dti_instance.generate_bvals(method_file, OUTPUT_DIR, (os.path.basename(scan) + "_"+str(os.path.basename(number))+".nii"), self.direction_omitter[(os.path.basename(scan) + "_"+str(os.path.basename(number))+".nii")])
						tenfit = self.dti_instance.dti_fit(OUTPUT_DIR, img, (os.path.basename(scan) + "_"+str(os.path.basename(number))+".nii"))
						if self.bool_b0:
							b0 = nib.Nifti1Image(img.get_fdata()[:,:,:,0], None)
							b0.header["pixdim"][1] = dim[0]
							b0.header["pixdim"][2] = dim[1]
							b0.header["pixdim"][3] = dim[2]
							b0.set_data_dtype("<f4")
							nib.save(b0, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_b0.nii"))
							print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_b0.nii"))
						if self.bool_fa:
							fa = nib.Nifti1Image(tenfit.fa, None)
							fa.header["pixdim"][1] = dim[0]
							fa.header["pixdim"][2] = dim[1]
							fa.header["pixdim"][3] = dim[2]
							fa.header["pixdim"][4] = dim[3]
							fa.set_data_dtype("<f4")
							nib.save(fa, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_fa.nii"))
							print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_fa.nii"))
						if self.bool_rd:
							rd = nib.Nifti1Image(tenfit.rd, None)
							rd.header["pixdim"][1] = dim[0]
							rd.header["pixdim"][2] = dim[1]
							rd.header["pixdim"][3] = dim[2]
							rd.header["pixdim"][4] = dim[3]
							rd.set_data_dtype("<f4")
							nib.save(rd, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_rd.nii"))
							print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_rd.nii"))
						if self.bool_adc:
							md = nib.Nifti1Image(tenfit.md, None)
							md.header["pixdim"][1] = dim[0]
							md.header["pixdim"][2] = dim[1]
							md.header["pixdim"][3] = dim[2]
							md.header["pixdim"][4] = dim[3]
							md.set_data_dtype("<f4")
							nib.save(md, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_adc.nii"))
							print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_adc.nii"))
				if self.bool_anatomy:
					number = self.dti_instance.rare_scans[scan]
					dim = self.dti_instance.getVoxelSize(number)
					img_anat = self.dti_instance.rare_imgs[scan]
					#nib.load(os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+".nii"))
					img_anat.header["pixdim"][1] = dim[0]
					img_anat.header["pixdim"][2] = dim[1]
					img_anat.header["pixdim"][3] = dim[2]
					nib.save(img_anat, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_anat.nii"))
					print("Saved " + str(os.path.join(OUTPUT_DIR, os.path.basename(scan) +"_"+str(os.path.basename(number))+"_anat.nii")))


	def introduction(self):
		subprocess.run("clear", shell=True)


		title = """
  ____ _____ ___   ____  _            _ _
 |  _ \_   _|_ _| |  _ \(_)_ __   ___| (_)_ __   ___
 | | | || |  | |  | |_) | | '_ \ / _ \ | | '_ \ / _ \ \n | |_| || |  | |  |  __/| | |_) |  __/ | | | | |  __/
 |____/ |_| |___| |_|   |_| .__/ \___|_|_|_| |_|\___|
						  |_|
 Created by Atul Phadke
		"""

		description = """

 This pipline contains all of the following features,
 1. Conversion between BRUKER and NIFTI file types
 2. DTI and generating FA, ADC, MD, etc.

		"""

		print(title)
		print(description)

		print("We would now like to input the files, \nPress enter to continue: ", end="")

		if input() != "":
			quit()
		else:
			print(self.SEPERATOR + "\n")

	def run(self):
		self.introduction()
		self.get_premier_folder()
		self.get_output_folder()
		self.run_quality_checker()
		self.parse_parameters()
		self.save_files()
		quit()

class DTI:
	def __init__(self, DTI_FOLDER):
		self.DTI_FOLDER = DTI_FOLDER
		self.output_folder = ""
		self.dti_scans, self.dti_imgs, self.rare_scans, self.rare_imgs = self.filter_scans()

	def generate_bvals(self, file, OUTPUT_FOLDER, new_name, directions):
		f=open(file)
		no_line_breaks = f.read()
		content = no_line_breaks.split("\n")

		bval = None
		dwDir = None
		GradOrient = None

		for line in content:
			if "PVM_DwBvalEach" in line and not bval:
				bval = content[content.index(line)+1]

			elif "PVM_SPackArrGradOrient" in line and not GradOrient:

				reshape = line.replace("##$PVM_SPackArrGradOrient=( ", "")
				reshape = reshape.replace(" )", "").replace(",", "")
				reshape = list(reshape.split(" "))
				reshape = tuple([int(item) for item in reshape])

				vals = np.prod(list(reshape))

				GradOrientArray = content[content.index(line)+1:content.index(line)+4]
				GradOrient = []

				for c in GradOrientArray:
					d = c.split(" ")
					for grd in d:
						GradOrient.append(grd)

				GradOrient = np.array(list(filter(None, GradOrient)))
				GradOrient = GradOrient[0:vals]
				GradOrient.shape = reshape
				GradOrient = np.squeeze(GradOrient)
				GradOrient = GradOrient.astype(float)

			elif "##$PVM_DwDir=" in line and not dwDir:

				dwDirArray = no_line_breaks[no_line_breaks.index(content[content.index(line)+1]):no_line_breaks.find("#", no_line_breaks.index(content[content.index(line)+2]))].split(" ")
				dwDir = [0,0,0]

				for idx, element in enumerate(dwDirArray):
					f = math.floor(idx/3) + 1
					if directions[("b"+str(f))]:
						dwDir.append(element.strip())

				dwDir = np.array(dwDir)
				dwDir.shape = (int(len(dwDir)/3),3)
				dwDir = dwDir.astype(float)

		bvec = np.dot(dwDir, GradOrient)
		bvec_file = open(os.path.join(OUTPUT_FOLDER, new_name+".bvec"), "w+")
		bval_file = open(os.path.join(OUTPUT_FOLDER, new_name+".bval"), "w+")

		bval_file.truncate()

		bvals=bval.split(" ")
		if len(bvals) == 1:
		    bval_file.write("0 " + (len(dwDir)-1)*(str(bval) + " "))
		else:
		    bval_file.write(bval)
		bval_file.close()

		bvec_file.truncate()

		bvec.shape = (len(dwDir), 3)

		for vector_array in bvec:
			for vector in vector_array:
				bvec_file.write(str(vector) + " ")
			bvec_file.write("\n")

		bvec_file.close()

	def dti_fit(self, OUTPUT_FOLDER, img, new_name):
		fbval = os.path.join(OUTPUT_FOLDER, new_name+".bval")
		fbvec = os.path.join(OUTPUT_FOLDER, new_name+".bvec")

		bvals, bvecs = read_bvals_bvecs(fbval, fbvec)
		gtab = gradient_table(bvals, bvecs)
		tenmodel = TensorModel(gtab)

		fdata = np.array(img.get_fdata())

		tenfit = tenmodel.fit(fdata)

		return tenfit

	def bruker2nifti(self,img):
		dataset = Dataset(img)
		return nib.Nifti1Image(dataset.data, None)

	def getOnlyDirs(self,path):
		return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

	def getVoxelSize(self,scan):
		method = open(os.path.join(scan, "method"))
		no_line_breaks = method.read()
		content = no_line_breaks.split("\n")
		foundSpat = False
		foundSlice = False
		sliceThickness = ""
		for line in content:
			if "PVM_SpatResol=" in line:
				foundSpat = True
				continue
			if foundSpat:
				foundSpat = False
				foundSlice = True
				spatial = line.split(" ")
				#print(spatial)
				continue
			if foundSlice:
				sliceThickness = line.replace("##$PVM_SliceThick=", "")
				#print(sliceThickness)
				foundSlice = False

		spatial.append(sliceThickness)

		return list(map(float, spatial))

	def checkMethod(self,scan_set):
		method_file = os.path.join(scan_set, "method")
		if os.path.exists(method_file):
			f = open(method_file, "r", encoding="ISO-8859-1")
			contents = f.read()
			if "Method=<Bruker:DtiEpi>" in contents:
				return True
			else:
				return False

	def checkRare(self,scan_set):
		method_file = os.path.join(scan_set, "method")
		if os.path.exists(method_file):
			f = open(method_file, "r",encoding="ISO-8859-1")
			contents = f.read()
			if "Method=<Bruker:RARE>" in contents:
				return True
			else:
				return False

	def filter_scans(self):
		dti_scans = {}
		dti_imgs = {}
		rare_scans = {}
		rare_imgs = {}

		for scan_folder in self.getOnlyDirs(self.DTI_FOLDER):
			scan_folder = os.path.join(self.DTI_FOLDER, scan_folder)
			for number in self.getOnlyDirs(scan_folder):
				number = os.path.join(scan_folder, number)
				if os.path.basename(number).isnumeric():
					if self.checkMethod(number):
						if number in dti_scans:
							dti_scans[scan_folder] += [(str(number))]
							dti_imgs[scan_folder] += [(self.bruker2nifti(os.path.join(number, "pdata", "1", "2dseq")))]
						else:
							dti_scans[scan_folder] = [(str(number))]
							dti_imgs[scan_folder] = [(self.bruker2nifti(os.path.join(number, "pdata", "1", "2dseq")))]
					if self.checkRare(number):
						rare_scans[scan_folder] = number
						rare_imgs[scan_folder] = self.bruker2nifti(os.path.join(number, "pdata", "1", "2dseq"))

		return dti_scans, dti_imgs, rare_scans, rare_imgs

class qualityChecker:
    def __init__(self, img):
        self.axarr0Click = False
        self.axarr1Click = False
        self.axarr2Click = False

        sitk_t1 = sitk.ReadImage(img)
        self.img = sitk.GetArrayFromImage(sitk_t1)

        self.AXIS2 = self.img.shape[-1]
        self.AXIS0 = self.img.shape[-2]
        self.AXIS1 = self.img.shape[-3]

        self.DIRECTION = 0

        self.f, self.axarr = plt.subplots(1, 3, figsize=(10,5))
        self.f.canvas.manager.set_window_title(os.path.basename(img))
        self.f.suptitle("B"+str(self.DIRECTION)+" Image", fontsize=15, fontweight="bold")
        self.axarr[1].set_title("Coronal", fontsize=12)
        self.axarr[0].set_title("Axial", fontsize=12)
        self.axarr[2].set_title("Saggital", fontsize=12)


        self.CURRENT1 = round(self.AXIS1/2)
        self.CURRENT0 = round(self.AXIS0/2)
        self.CURRENT2 = round(self.AXIS2/2)

        self.axarr[1].set_xlabel(str(self.CURRENT1)+"/"+str(self.AXIS1))
        self.axarr[0].set_xlabel(str(self.CURRENT0)+"/"+str(self.AXIS0))
        self.axarr[2].set_xlabel(str(self.CURRENT2)+"/"+str(self.AXIS2))

        self.img0 = self.axarr[0].imshow(self.img[self.DIRECTION,:,self.CURRENT0,:], cmap='gray')
        self.img1 = self.axarr[1].imshow(self.img[self.DIRECTION, self.CURRENT1,:,:], cmap='gray')
        self.img2 = self.axarr[2].imshow(self.img[self.DIRECTION,:,:,self.CURRENT2], cmap='gray')

        self.axprev = self.f.add_axes([0.7, 0.05, 0.1, 0.075])
        self.axnext = self.f.add_axes([0.81, 0.05, 0.1, 0.075])
        self.axfinish = self.f.add_axes([0.05, 0.05, 0.1, 0.075])
        #self.ax_elim = self.f.add_axes([0.412, 0.85, 0.2, 0.04])
        self.ax_check = self.f.add_axes([0.01, 0.75, 0.15, 0.2])

        self.ax0background = self.f.canvas.copy_from_bbox(self.axarr[0].bbox)
        self.axbackground = self.f.canvas.copy_from_bbox(self.axarr[1].bbox)
        self.ax2background = self.f.canvas.copy_from_bbox(self.axarr[2].bbox)

        self.eliminate = None
        self.check_status = []
        self.b_images = []
        self.vis = []
        for x in range(0, self.img.shape[0]):
            self.b_images.append("b"+str(x))
            self.vis.append(True)

        self.directions = {}

        for b in self.b_images:
            self.directions[str(b)] = True

        self.ax_check.set_visible(False)

        self.check = CheckButtons(self.ax_check, ["Keep Direction"], [True])
        self.check.on_clicked(self.func)

    def onclick_select(self, event):
        if event.inaxes == self.axarr[1]:
            if self.axarr1Click:
                self.axarr1Click = False
            else:
                self.axarr1Click = True
                self.axarr0Click = False
                self.axarr2Click = False
        elif event.inaxes == self.axarr[0]:
            if self.axarr0Click:
                self.axarr0Click = False
            else:
                self.axarr0Click = True
                self.axarr1Click = False
                self.axarr2Click = False
        elif event.inaxes == self.axarr[2]:
            if self.axarr2Click:
                self.axarr2Click = False
            else:
                self.axarr2Click = True
                self.axarr0Click = False
                self.axarr1Click = False
        elif event.inaxes == self.axnext:
            if self.DIRECTION < (self.img.shape[0]-1):
                self.DIRECTION +=1
                self.img0.set_data(self.img[self.DIRECTION, :,self.CURRENT0,:])
                self.img1.set_data(self.img[self.DIRECTION,self.CURRENT1, :, :])
                self.img2.set_data(self.img[self.DIRECTION,:,:,self.CURRENT2])
                self.f.suptitle("B"+str(self.DIRECTION)+" Image", fontsize=15, fontweight="bold")
                #print(self.directions["b"+str(self.DIRECTION)])
                if self.directions["b"+str(self.DIRECTION)] and not self.check.lines[0][0].get_visible():
                    self.check.set_active(0)

                if not self.directions["b"+str(self.DIRECTION)] and self.check.lines[0][0].get_visible():
                    self.check.set_active(0)

                if self.DIRECTION != 0:
                    self.ax_check.set_visible(True)
                else:
                    self.ax_check.set_visible(False)

                self.f.canvas.draw_idle()

        elif event.inaxes == self.axprev:
            if self.DIRECTION > 0:
                self.DIRECTION -=1
                self.img0.set_data(self.img[self.DIRECTION, :,self.CURRENT0,:])
                self.img1.set_data(self.img[self.DIRECTION,self.CURRENT1, :, :])
                self.img2.set_data(self.img[self.DIRECTION,:,:,self.CURRENT2])
                self.f.suptitle("B"+str(self.DIRECTION)+" Image", fontsize=15, fontweight="bold")

                if self.directions["b"+str(self.DIRECTION)] and not self.check.lines[0][0].get_visible():
                    self.check.set_active(0)

                if not self.directions["b"+str(self.DIRECTION)] and self.check.lines[0][0].get_visible():
                    self.check.set_active(0)

                if self.DIRECTION != 0:
                    self.ax_check.set_visible(True)
                else:
                    self.ax_check.set_visible(False)

                self.f.canvas.draw_idle()

        elif event.inaxes == self.axfinish:
            plt.close()

    def func(self,label):
        if self.check.lines[0][0].get_visible():
            self.directions["b"+str(self.DIRECTION)] = True
        else:
            self.directions["b"+str(self.DIRECTION)] = False

    def mouse_move(self, event):
        if event.inaxes == self.axarr[1]:
            if self.axarr1Click:
                x, y = round(event.xdata), round(event.ydata)
                if x > self.img.shape[-2]:
                    x = self.img.shape[-2]
                if y > self.img.shape[-1]:
                    y = self.img.shape[-1]
                self.img0.set_data(self.img[self.DIRECTION,:,x,:])
                self.img2.set_data(self.img[self.DIRECTION,:,:,y])

                self.axarr[0].set_xlabel(str(x)+"/"+str(self.AXIS0))
                self.axarr[2].set_xlabel(str(y)+"/"+str(self.AXIS2))
                self.CURRENT0 = x
                self.CURRENT2 = y
                self.f.canvas.draw_idle()
                self.f.canvas.flush_events()
                plt.pause(0.000001)
        elif event.inaxes == self.axarr[0]:
            if self.axarr0Click:
                x, y = round(event.xdata), round(event.ydata)
                if x > self.img.shape[-1]:
                    x = self.img.shape[-1]
                if y > self.img.shape[1]:
                    y = self.img.shape[1]

                self.img1.set_data(self.img[self.DIRECTION,y,:,:])
                self.img2.set_data(self.img[self.DIRECTION,:,:,x])
                self.axarr[1].set_xlabel(str(y)+"/"+str(self.AXIS1))
                self.axarr[2].set_xlabel(str(x)+"/"+str(self.AXIS2))
                self.CURRENT1 = y
                self.CURRENT2 = x
                self.f.canvas.draw_idle()
                self.f.canvas.flush_events()
                plt.pause(0.000001)
        elif event.inaxes == self.axarr[2]:
            if self.axarr2Click:
                x, y = round(event.xdata), round(event.ydata)
                if x > self.img.shape[-2]:
                    x = self.img.shape[-2]
                if y > self.img.shape[1]:
                    y = self.img.shape[1]
                self.img0.set_data(self.img[self.DIRECTION,:,x,:])
                self.img1.set_data(self.img[self.DIRECTION,y,:,:])
                self.axarr[0].set_xlabel(str(x)+"/"+str(self.AXIS0))
                self.axarr[1].set_xlabel(str(y)+"/"+str(self.AXIS1))
                self.CURRENT0 = x
                self.CURRENT1 = y
                self.f.canvas.draw_idle()
                self.f.canvas.flush_events()
                plt.pause(0.000001)

    def run(self):

        bnext = Button(self.axnext, 'Next')

        bprev = Button(self.axprev, 'Previous')

        finish = Button(self.axfinish, "Finish")

        directions = self.img.shape[0]

        self.f.canvas.mpl_connect("button_press_event",self.onclick_select)
        self.f.canvas.mpl_connect("motion_notify_event",self.mouse_move)

        plt.show()

instance = Pipeline()
instance.run()

"""

for scan, numb in dti_scans.items():
	if numb:
		if bool_fa or bool_adc or bool_b0:
			for number in numb:
				img_file = os.path.join(number, "pdata", "1", "2dseq")
				img = bruker2nifti(img_file)
				dim = getVoxelSize(number)
				method_file = os.path.join(number, "method")
				OUTPUT_DIR = os.path.join("processed", os.path.basename(scan))
				if not os.path.isdir(OUTPUT_DIR):
					os.mkdir(OUTPUT_DIR)
				diff = DTI(img, os.path.basename(scan), OUTPUT_DIR)
				diff.generate_bvals(method_file)
				tenfit = diff.dti_fit(img)
				if bool_b0:
					b0 = nib.Nifti1Image(img.get_fdata()[:,:,:,0], None)
					b0.header["pixdim"][1] = dim[0]
					b0.header["pixdim"][2] = dim[1]
					b0.header["pixdim"][3] = dim[2]
					nib.save(b0, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_b0.nii"))
					print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_b0.nii"))
				if bool_fa:
					fa = nib.Nifti1Image(tenfit.fa, None)
					fa.header["pixdim"][1] = dim[0]
					fa.header["pixdim"][2] = dim[1]
					fa.header["pixdim"][3] = dim[2]
					fa.header["pixdim"][4] = dim[3]
					nib.save(fa, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_fa.nii"))
					print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_fa.nii"))
				if bool_adc:
					md = nib.Nifti1Image(tenfit.md, None)
					md.header["pixdim"][1] = dim[0]
					md.header["pixdim"][2] = dim[1]
					md.header["pixdim"][3] = dim[2]
					md.header["pixdim"][4] = dim[3]
					nib.save(md, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_adc.nii"))
					print("Saved " + os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_adc.nii"))
		if bool_ognii:
			for number in numb:
				OUTPUT_DIR = os.path.join("processed", os.path.basename(scan))
				img_file = os.path.join(number, "pdata", "1", "2dseq")
				if not os.path.isdir(OUTPUT_DIR):
					os.mkdir(OUTPUT_DIR)
				img = bruker2nifti(img_file)
				dim = getVoxelSize(number)
				img_nii = nib.Nifti1Image(img.get_fdata(), None)
				img_nii.header["pixdim"][1] = dim[0]
				img_nii.header["pixdim"][2] = dim[1]
				img_nii.header["pixdim"][3] = dim[2]
				img_nii.header["pixdim"][4] = dim[3]
				nib.save(img_nii, os.path.join(OUTPUT_DIR, os.path.basename(scan) +"_"+str(os.path.basename(number))+"_og.nii"))
			print("Saved " + str(os.path.join(OUTPUT_DIR, os.path.basename(scan) +"_"+str(os.path.basename(number))+"_og.nii")))
		if bool_anatomy:
			OUTPUT_DIR = os.path.join("processed", os.path.basename(scan))
			if not os.path.isdir(OUTPUT_DIR):
				os.mkdir(OUTPUT_DIR)
			number = rare_scans[scan]
			img_file = os.path.join(number, "pdata", "1", "2dseq")
			img = bruker2nifti(img_file)
			dim = getVoxelSize(number)
			img_anat = nib.Nifti1Image(img.get_fdata(), None)
			img_anat.header["pixdim"][1] = dim[0]
			img_anat.header["pixdim"][2] = dim[1]
			img_anat.header["pixdim"][3] = dim[2]
			nib.save(img_anat, os.path.join(OUTPUT_DIR, os.path.basename(scan) + "_"+str(os.path.basename(number))+"_anat.nii"))
			print("Saved " + str(os.path.join(OUTPUT_DIR, os.path.basename(scan) +"_"+str(os.path.basename(number))+"_anat.nii")))

"""

#print(dti_scans)
