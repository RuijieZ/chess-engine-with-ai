#!/usr/bin/env python3

from distutils.core import setup, Extension

extra_compile_args=["-O3"]
setup(
	name = "evaluation",
	version = "1.1",
	ext_modules = [Extension("evaluation", sources=["evaluation.c"], extra_compile_args=extra_compile_args)]
	);
