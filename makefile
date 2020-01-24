# This makefile is just so I don't have to remember the command below

all:
	R --no-save < timeline.r && firefox public/index.html
