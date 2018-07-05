Project for Artificial Intelligence Fellowship at Insight Data Science '18B

Questions and comments welcome at garry.yangguang [AT] gmail [DOT] com


## Overview
Wouldn't it be nifty if you could transform your voice to sound like someone else? 'Refashion Your Voice' is a deployed end-to-end application that does voice style transfer using neural networks (based on this existing project https://github.com/andabi/deep-voice-conversion)


## Getting Started
To deploy it yourself, you need have a kubernetes cluster and look under the kube/ folder for the kube objects that you need to create


## Data
Training data for different voice profiles come from audiobooks. preprocessing helper scripts in bash are in scripts/


## API
The code for API is under snapi/. Currently it is coupled with inference logic


## Acknowledgement
Big thanks to Dabi Ahn for the deep-voice-conversion project which made this possible. Note that some files from https://github.com/andabi/deep-voice-conversion had to be copied over for modifications to make inference more flexible. These changes will be PR'd to the original repo that can be turned into a package in a future date.
