PREREQUIREMENTS:
    ubuntu: 23.10
    python: 3.11.6
    cudnn_version: 8
    cuda_version: 12.2

BUILD:
    sudo apt install nvidia-cuda-toolkit
	pip install tensorflow[and-cuda]
	
