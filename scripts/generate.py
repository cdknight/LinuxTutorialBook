#!/usr/bin/python3

import os
import sys
import glob 
from distutils.dir_util import copy_tree
import shutil
import subprocess
from contextlib import contextmanager

TMP_OUTPUT_DIR = "../tmp"
FINAL_OUTPUT_DIR="../output"
CHAPTER_FILES_DIR="../chapters"
#xelatex variables
XELATEX_PATH="/usr/bin/xelatex"

#markdown, htmldoc vars
MPDF_PATH="/usr/local/bin/mdpdf"

#pdfjam vars
PDFJAM_PATH="/usr/bin/pdfjam"

BOOK_FILE_NAME=sys.argv[0]

DO_NOT_SHOW_OUTPUT = " > /dev/null"
STYLESHEET_PATH = "../styles/metro-vibes.css"
def genBookPDF():
	"""Generate the final book pdf"""
	#quick clean
	shutil.rmtree(FINAL_OUTPUT_DIR)
	shutil.rmtree(TMP_OUTPUT_DIR)
	os.mkdir(FINAL_OUTPUT_DIR)
	os.mkdir(TMP_OUTPUT_DIR)
	
	pdflist = [TMP_OUTPUT_DIR + "/title.pdf", TMP_OUTPUT_DIR + "/toc.pdf"]
	#gen graphics dir
	createTempGraphicsDir()
	
	# gen title, toc
	xelatexToPDF("../title.tex", TMP_OUTPUT_DIR + "/title.pdf")
	xelatexToPDF("../toc.tex", TMP_OUTPUT_DIR + "/toc.pdf")
	
	#gen chapter md, then conv to pdf
	for chapter in glob.glob(CHAPTER_FILES_DIR + "/Ch*"):
		chapter_name = chapter[-1]
		outputfilename = writeFullChapterMarkdown(chapter_name)
		markdownToPDF(outputfilename, TMP_OUTPUT_DIR + "/" + chapter_name + ".pdf", True)
		pdflist.append(TMP_OUTPUT_DIR + "/" + chapter_name + ".pdf")
	
	#ending things, glossary, bib
	
	#merge all files at end.
	concatPDFS(pdflist, FINAL_OUTPUT_DIR + "/output.pdf")
	
	#clean up
	shutil.rmtree(TMP_OUTPUT_DIR)
	os.mkdir(TMP_OUTPUT_DIR)
	
def xelatexToPDF(inputfile, outputfile):
	"""Write xelatex file as a4 pdf to output file"""
	print("converting " + inputfile + " to pdf " + outputfile)
	path_of_inputfile = os.path.dirname(inputfile)
	
	#filenames
	filename = os.path.basename(inputfile)
	filename_pdf = os.path.join(path_of_inputfile, os.path.splitext(filename)[0] + ".pdf")
	filename_log = os.path.splitext(filename)[0] + ".log"
	filename_aux = os.path.splitext(filename)[0] + ".aux"
	filename_synctex_gz = os.path.splitext(filename)[0] + ".synctex.gz"
	filename_filename = os.path.splitext(filename)[0] + "." + os.path.splitext(filename)[0]
	
	command = XELATEX_PATH +  ' -synctex=1 -interaction=nonstopmode -papersize="A4" ' + filename
	
	# gen
	with cd(path_of_inputfile):
		os.system(command + DO_NOT_SHOW_OUTPUT)
	#copy to output
	shutil.copyfile(filename_pdf, outputfile)
	#delete files
	os.remove(filename_pdf)
	with cd(path_of_inputfile):
		#os.remove(filename_filename)
		os.remove(filename_log)
		os.remove(filename_synctex_gz)
		os.remove(filename_aux)
	

def createTempGraphicsDir():
	"""Create the tmp graphics dir"""
	print("creating graphics directory")
	os.mkdir(TMP_OUTPUT_DIR + "/graphics")


def writeFullChapterMarkdown(chname):
	"""Write the full markdown of each chapter to tmp file chname.md. Also copy images since markdown uses relative paths."""
	chname = str(chname)
	
	full_md_str = str()
	
	md_files_list = glob.glob(CHAPTER_FILES_DIR + "/Ch" + chname + "/" + chname + "_*.md")
	
	#read preface to full_md_str
	with open(CHAPTER_FILES_DIR + "/Ch" + chname + "/preface.md") as preface_obj:
		print("concat " + CHAPTER_FILES_DIR + "/Ch" + chname + "/preface.md" + " to " + chname + ".md")
		full_md_str += preface_obj.read()
	full_md_str += "\n"
	
	#read all chapter md files into full_md_str
	for md_file in md_files_list: 
		print("concat " + md_file + " to " + chname + ".md")
		with open(md_file) as md_file_obj:	
			full_md_str += md_file_obj.read()
			
	#write this to final file
	with open(TMP_OUTPUT_DIR + "/" + chname + ".md", 'w') as output_obj:
		output_obj.write(full_md_str)
		
	for file in glob.glob(CHAPTER_FILES_DIR + "/Ch" + chname + "/graphics/*"):
		print("copy " + file + " to " + TMP_OUTPUT_DIR + "/graphics")
	copy_tree(CHAPTER_FILES_DIR + "/Ch" + chname + "/graphics", TMP_OUTPUT_DIR + "/graphics")
	return TMP_OUTPUT_DIR + "/" + chname + ".md"
	
def markdownToPDF(inputfile, outputfile, styles):
	"""Convert markdown file inputfile to pdf file outputfile on portrait A4 paper. Requires markdown-pdf"""
	print("converting " + inputfile + " to pdf at " + outputfile)
	if not styles:
		command = MPDF_PATH + " --orientation=portrait --format=A4 " + inputfile + " " + outputfile
	else: 
		command = MPDF_PATH + " --styles=" + STYLESHEET_PATH + " --orientation=portrait --format=A4 " + inputfile + " " + outputfile
	#print(command)
	os.system(command + DO_NOT_SHOW_OUTPUT)
	
	
def concatPDFS(inputlist, outputfile):
	command = PDFJAM_PATH + " "
	for inputfile in inputlist:
		command += inputfile + " "
	
	command += "-o " + outputfile
	#print(command)
	print("joining files to pdf")
	os.system(command + DO_NOT_SHOW_OUTPUT)
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        
        
if __name__=='__main__':
	genBookPDF()
