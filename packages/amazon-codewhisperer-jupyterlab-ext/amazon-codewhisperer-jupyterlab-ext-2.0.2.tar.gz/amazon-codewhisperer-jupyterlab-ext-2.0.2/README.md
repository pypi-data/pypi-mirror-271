# Amazon CodeWhisperer for JupyterLab

Amazon CodeWhisperer is an AI coding companion which provides developers with real-time code suggestions in JupyterLab. Individual developers can use CodeWhisperer for free in JupyterLab and AWS SageMaker Studio.

![Codewhisperer demo](https://docs.aws.amazon.com/images/codewhisperer/latest/userguide/images/codewhisperer-timestamp-record.png)

## Requirements

In order to use CodeWhisperer in JupyterLab, you must have a version of JupyterLab >= 4 installed. The previous major version of CodeWhisperer 1.x extension supports JupyterLab >= 3.5, <4. You will also need a free [AWS Builder ID](https://docs.aws.amazon.com/signin/latest/userguide/sign-in-aws_builder_id.html) account to access CodeWhisperer. (You can set that up the first time you log in.)

In order to use CodeWhisperer in SageMaker Studio, you must have set up a SageMaker Studio notebook instance, along with an execution role with the appropriate IAM Permissions. 

## Getting Started

Install [JupyterLab](https://pypi.org/project/jupyterlab) on your computer or if you already have JupyterLab installed, check it’s version by running the following command.

```
pip show jupyterlab
```

Note the version in the response, and follow the use the corresponding directions in one of the following sections.

### Installation Using Pip for Jupyter Lab version >= 4.0

You can install and enable the CodeWhisperer extension for JupyterLab 4 with the following commands. 

```
# JupyterLab 4
pip install amazon-codewhisperer-jupyterlab-ext
```

### Installation Using Pip for Jupyter Lab version >= 3.6 and < 4.0

You can install and enable the CodeWhisperer 1.x extension for JupyterLab 3 with the following commands. 

```
# JupyterLab 3
pip install amazon-codewhisperer-jupyterlab-ext~=1.0
jupyter server extension enable amazon_codewhisperer_jupyterlab_ext
```

Once installed, choose ****Start CodeWhisperer**** from the CodeWhisperer panel at the bottom of the window. This will enable to you log in to [AWS Builder ID](https://docs.aws.amazon.com/signin/latest/userguide/sign-in-aws_builder_id.html) to access CodeWhisperer. Refer to [Setting up CodeWhisperer with JupyterLab](https://docs.aws.amazon.com/codewhisperer/latest/userguide/jupyterlab-setup.html) for detailed setup instructions.

### SageMaker Studio

To setup the CodeWhisperer extension with a SageMaker Studio notebook instance, you must add IAM Permissions for 
`codewhisperer:GenerateRecommendations` for your user profile. Then you must install and enable the extension with the following commands.

```
conda activate studio
pip install amazon-codewhisperer-jupyterlab-ext~=1.0
jupyter server extension enable amazon_codewhisperer_jupyterlab_ext
conda deactivate
restart-jupyter-server
```

After you complete installation and refresh your browser, a CodeWhisperer panel will appear at the bottom of the window. Refer to [Setting up CodeWhisperer with SageMaker Studio](https://docs.aws.amazon.com/codewhisperer/latest/userguide/sagemaker-setup.html) for detailed setup instructions. 

## Features

### Code Completion

CodeWhisperer for JupyterLab provides AI powered suggestions as ghost text with the following default keybindings. These can be modified in the settings.


|              Action	                  |      Key Binding       |
| ------------------------------ | ----------- |
| Manually trigger CodeWhisperer | Alt C (Window) / ⌥ C (Mac)        |
| Accept a recommendation        | Tab       |
| Next recommendation            | Right arrow |
| Previous recommendation        | Left arrow  |
| Reject a recommendation        | ESC         |



Python is the only supported programming language for now. Users can start or pause suggestions by toggling the menu item in the CodeWhisperer panel that will appear at the bottom of the window.

### Code References

With the reference log, you can view references to code recommendations. You can also update and edit code recommendations suggested by CodeWhisperer.

To view Code References for accepted suggestions, choose **Open Code Reference Log** from the CodeWhisperer panel at the bottom of the window. Users can also turn off code suggestions with code references in Settings.


## More Resources

* [CodeWhisperer User Guide](https://docs.aws.amazon.com/codewhisperer/latest/userguide/what-is-cwspr.html)
* [Setting up Amazon CodeWhisperer with JupyterLab](https://docs.aws.amazon.com/codewhisperer/latest/userguide/jupyterlab-setup.html)
* [Setting up CodeWhisperer with Amazon SageMaker Studio](https://docs.aws.amazon.com/codewhisperer/latest/userguide/sagemaker-setup.html)

## Change Log

2.0.2
* Fix Tab, ArrowDown, ArrowUp button not working in JupyterLab 4.1

2.0.1
* Improved handling when Jupyter has no access to internet.
* Migrated network call to be made asynchronously.

2.0.0
* Initial release - Adoption of JupyterLab 4
