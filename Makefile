# Makefile for source rpm: mutt
# $Id$
NAME := mutt
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
