# Modern skills timeline generator

all:
	python3 timeline.py && open public/index.html

# Legacy R version (backup)
r-version:
	R --no-save < timeline.r && open public/index.html

# Install Python dependencies
install:
	pip3 install -r requirements.txt

deploy:
	git add -A && git commit -m "Auto-commit from make deploy 🤖" && git push
