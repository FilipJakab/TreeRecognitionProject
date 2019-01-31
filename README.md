# MachineLearningScripts

This repository contains:

  * Caffe2 boiler-plates (nearly done)
    * CNN modeling
    * Dataset manipulation (creation)
  * Python-based API (to be able to call python scripts for predictions)
  * ASP.NET MVC Core API (TODO)
  * Simple SPA web page for communication with above API (TODO)

Planned output:

> This project should be in it's final form serve web page, which communicates with API.
> This API will be able to receive Image files (probably one at time). Then the hidden API (the python-based one)
> which will be very simple - with single endpoint accepting either file path (these APIs will be server on same machine)
> or image itself (topic to think about). The publicly visible API will then return the result (or maybe processed
> e.g saving info to MSSQL DB for later usage) of python API to the client.
