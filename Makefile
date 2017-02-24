all: 
	cd /home/ec2-user/GOS_book/
	git pull origin
	texindy -L russian -C utf8 _main.idx 
	pdflatex -synctex=1 -interaction=nonstopmode -shell-escape _main.tex 
	pdflatex -synctex=1 -interaction=nonstopmode -shell-escape _main.tex 
	mv _main.pdf GOSBook.pdf
	cd /home/ec2-user/gosbookbot
	python broadcast.py