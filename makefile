# This makefile is just so I don't have to remember the command below

all:
	R --no-save < timeline.r && firefox public/index.html

deploy:
	git add -A && git commit -m "Auto-commit from make deploy 🤖" && git push
