# MachineLearningScripts

This repository contains:

  * Caffe2 boiler-plates (not being used - switched to pytorch only)
    * CNN modeling
    * Dataset manipulation (creation)
  * Pytorch (All ML stuff)
  	* CNN Training
   * CNN Predictor
  * Python-based hidden web API (to be able to call python scripts from APIs for predictions)
  * ASP.NET MVC Core API
  * Simple SPA web page for communication with above API

Planned output:

> This project should be in it's final form serving web page, which communicates with API.
> This API will be able to receive Image files (probably one at a time). Then the hidden API (the python-based one)
> which will be very simple - with single endpoint accepting either file path or image itself (depends on whether I decide to
> save the images locally or to DB). The publicly visible API will then return the result (or maybe processed
> e.g saving info to MSSQL DB for later usage) of python API to the client.
