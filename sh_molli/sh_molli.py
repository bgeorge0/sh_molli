import pydicom
import os
import numpy as np
from sh_molli_fit import *
import tqdm
import PIL

def do_fitting(x,y):
	try:
		return exp_fit(x,y)
	except np.linalg.LinAlgError as e:
		return [-1, -1, -1, -1]

def process_folder(path):
	files = os.listdir(path)
	time = np.zeros((len(files)))
	inv_time = np.zeros((len(files)))
	img_comments = np.zeros((len(files)))
	for i, file in enumerate(files):
		dcm = pydicom.read_file(os.path.join(path,file))
		if i == 0:
			images = np.zeros((dcm.pixel_array.shape[0], dcm.pixel_array.shape[0], len(files)))
		images[:,:,i] = dcm.pixel_array
		time[i] = dcm.TriggerTime
		inv_time[i] = dcm.InversionTime
		img_comments[i] = float(dcm.ImageComments.split()[1])
	
	rngs = [time.max() - time.min(), inv_time.max() - inv_time.min(), img_comments.max() - img_comments.min()]
	ind = rngs.index(max(rngs))
	if ind == 0:
		print('time')
		inv_time = time
	elif ind == 1:
		print('inv_time')
		inv_time = inv_time
	elif ind == 2:
		print('img_comments')
		inv_time = img_comments
		
	sort_inds = np.argsort(inv_time)
	sorted_images = np.zeros(images.shape)
	sorted_images[:,:,range(len(sort_inds))] = images[:,:,sort_inds]
	inv_time.sort()
	
	mask0 = np.ones(len(inv_time))
	mask0[0:0] = -1 # For some symmetry
	
	mask1 = np.ones(len(inv_time))
	mask1[0:1] = -1
	
	mask2 = np.ones(len(inv_time))
	mask2[0:2] = -1
	
	mask3 = np.ones(len(inv_time))
	mask3[0:3] = -1
	
	x_size, y_size, _ = images.shape
	out_array = np.zeros((x_size,y_size))
	for x in tqdm.tqdm(range(x_size)):
		for y in range(y_size):
			#print(x)
			#print(y)
			vals = sorted_images[x,y,:]
			if (vals.max() - vals.min()) > 100:
				out0 = do_fitting(inv_time, mask0 * vals)
				out1 = do_fitting(inv_time, mask1 * vals)
				out2 = do_fitting(inv_time, mask2 * vals)
				out3 = do_fitting(inv_time, mask3 * vals)
				sse = [out0[3], out1[3], out2[3], out3[3]]
				best_fit_ind = sse.index(min(sse))
				if best_fit_ind == 0:
					out_array[x][y] = out0[2] * ((out0[1] / out0[0]) - 1)
				elif best_fit_ind == 1:
					out_array[x][y] = out1[2] * ((out1[1] / out1[0]) - 1)
				elif best_fit_ind == 2:
					out_array[x][y] = out2[2] * ((out2[1] / out2[0]) - 1)
				elif best_fit_ind == 3:
					out_array[x][y] = out3[2] * ((out3[1] / out3[0]) - 1)
	return out_array

def write_image(t1map, filename):
	img = PIL.Image.fromarray(t1map)
	img.save(filename)

def display(t1map):
	from matplotlib import pyplot as plt
	plt.imshow(t1map)
	plt.show()

def __help_string():
	return 'process_sh_molli_series.py -i <inputfolder> -o <outputfilename> -p <plot_flag>'

def __main__():
	import sys
	import getopt
	
	inputfolder = None
	outputfilename = None
	showImage = False
		
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:o:p:",["inputfolder=","outputfilename=","plot="])
	except getopt.GetoptError:
		print(__help_string())
		sys.exit(2)
	
	if len(opts) == 0:
		print(__help_string())
		return
	else:
		for opt, arg in opts:
			if opt == '-h':
				print(__help_string())
				sys.exit()
			elif opt in ("-i", "--inputfolder"):
				inputfolder = arg
			elif opt in ("-o", "--outputfilename"):
				outputfilename = arg
			elif opt in ("-p", "--plot"):
				showImage = arg
	
	if inputfolder is not None:
		t1map = process_folder(inputfolder)
	if outputfilename is not None:
		write_image(t1map, outputfilename)
	if showImage:
		display(t1map)

if __name__ == "__main__":
	__main__()
