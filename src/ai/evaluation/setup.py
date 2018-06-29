#!/usr/bin/env python3

from distutils.core import setup, Extension

setup(
	name = "evaluation",
	version = "1.0",
	ext_modules = [Extension("evaluation", ["evaluation.c"])]
	);
