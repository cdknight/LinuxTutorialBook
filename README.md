# The Linux Tutorial Book

A book written in Markdown and XeLaTex (currently geared for Linux Mint). This book uses Python to generate a final PDF.

## Getting Started

You need the following programs: 
```bash
mdpdf
xelatex
pdfjam
python3
```
Debian-based Distros:
```bash
sudo apt install npm texlive texlive-xelatex
sudo npm install mdpdf -g
```

Fedora (untested): 
```bash
sudo dnf -y install texlive texlive-latex texlive-xetex texlive-collection-latex texlive-collection-latexrecommended texlive-xetex-def texlive-collection-xetex install texlive-collection-latexextra npm

sudo npm install mdpdf -g
```

Solus (untested):
```bash
sudo eopkg it texlive nodejs
sudo npm install mdpdf -g
```

Search the programs with a search engine if I haven't listed your distro yet.

## Extending

The book is easily extensible. All book files are in `chapters/`. To access a book file you need to navigate to the "chapter" it is in. Chapter in quotes since any section of the book (like the preface) is in the `chapters/` directory. The sections are in chronological order of reading, so the prefaces section is in the directory `chapters/Ch1`.

Therefore you must create a new chapter under `chapters/` if you are writing a chapter. To add the new section to the table of contents, you may use this template:

```TeX
\addcontentsline{toc}{section}{Chapter X: New Chapter}
	\addcontentsline{toc}{subsection}{X.1 New Chapter Subsection}
	\addcontentsline{toc}{subsection}{X.2 New Chapter Subsection}
```
This is added to `toc.tex` before `\end{document}`. Hopefully in the future this table of contents is automatically generated.

## Exporting

When you're done making changes, exporting the book to a pdf is a matter of doing this (from the root of the repository)
```bash
cd scripts
./generate.py
cd ../output
xdg-open output.pdf
```

**Note: Do not run this python script if you are not inside the scripts directory. It will not work.**
This problem can be fixed by using absolute paths of the relative paths by using ```os.path.abspath(varname)```, but the generation script is still a WIP.

## Hacking the Generation Script
The generation script is very simple. 
Functions in the Python file: 

* `xelatexToPDF(inputfile, outputfile)`: This will generate a PDF to an output directory from a XeLaTex file. Requires `xelatex`.
* `createTempGraphicsDir()`: This creates a temporary graphics directory so images from the Markdown files are rendered correctly
* `writeFullChapterMarkdown(chname)`: This will create a file with all the subsections and preface and place it in the `tmp` directory (relative to the root of the project). 
* `markdownToPDF(inputfile, outputfile, styles)`: This will create a PDF file from the Markdown file. Requires `mdpdf`. Styles is for enabling or disable custom styling (**Note: Styles do not seem to work as of now**).
* `concatPDFS(inputlist, outputfile)`: This joins a list of pdfs (the list has the paths of the pdfs) and writes it to the outputfile. Requires `pdfjam`.

The script first renders the table of contents and title page. Then it uses globs in order to get all chapters from `chapters/`. In each chapter directory, globs are used to find each markdown file. This is concatenated into a single markdown file for each chapter, which is subsequently rendered into a PDF file. Finally, all the PDF files are turned into a single PDF, `output/output.pdf`.

### What's Done:
* Basic Book PDF Generation

### What's Not Done/Todo for Script:
* EPUB Generation
* Page Numbers
* Auto-Generation of Title
* Using XeLaTex for Chapters in the book

## What Editor do I Use?

I'm using Remarkable Markdown Editor (subject to change), and TeXStudio. Any markdown/LaTeX editor will work as long as the correct directory structure for the book is preserved.

## Todo
* CI for each commit to the book
* Multiple branches for different chapters to be worked on
* Styling the book with a stylesheet
* Makefile