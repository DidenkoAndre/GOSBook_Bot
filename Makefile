all:
	$(MAKE) -C ../GOS_book book
	python broadcast.py
