pypular
=======

The purpose of this tool is to download python packages from PYPI multiple times, to inflate the download counter.


How to use?
-----------

`pypular https://bla.com/bla.whl 300`


But why?
--------

This started with my [talk](https://codeberg.org/ltworf/pages/src/branch/master/owasp2024) about the security measures of PYPI.

Since for a while PYPI required stricter security for packages with an higher download count, I wanted to prove that download count is a bad measure.

Briefly after my talk, Snyk removed the download counter of python packages as a metric to evaluate quality. I don't know if this was related.

It is well known that the download counter is highly inaccurate (can be inflated artificially, doesn't take into account cached downloads, distributions, mirrors) and yet is taken into heavy consideration. I see no problem to play with it since it's a bad metric to begin with.

Donate
======
[Donate](https://liberapay.com/ltworf/donate)
