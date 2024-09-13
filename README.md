# Artificial Self: ΑΙ Agents Manifest the Self-Serving Bias

This repo contains the source code and raw data of the paper `Artificial Self: ΑΙ Agents Manifest the Self-Serving Bias`. 
We only support Python3 for now.
Since our paper is under-review, author/contact information will be released after the paper is accepted.  

## Repository Overview

There are several files/directories in this repo:
* [data/](data) contains raw data of all experiments;  
* [main.py](main.py) is the entrance of all experiments;
* [expt.py](expt.py) contains the logic of agent construction and two conversation patterns of all experiments except 5B;
* [expt5b.py](expt.py) similar to expt.py, targeting Experiment 5B;
* [prompt.py](prompt.py) contains all prompting text;
* Other files, including [analysis.py](analysis.py) and [utils.py](utils.py) provide supporting functions.



## Quickstart
1. Open a terminal and clone this repo to the local directory;
    ```bash
    cd your/target/folder
    git clone https://github.com/fusiwei339/agent_self.git
    cd agent_self
    ```

2. Create and activate virtual environment;
    ```bash
    # This example shows venv, you can use Anaconda as well
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install dependencies;
    ```bash
    pip3 install -r requirements.txt
    ```

4. Add OpenAI base and key to the environment (taking Linux / MacOS as an example);
    ```bash
    echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
    echo "export OPENAI_API_BASE='https://api.openai.com'" >> ~/.zshrc
    source ~/.zshrc
    # Confirm that you have correctly set your environment variable
    echo $OPENAI_API_KEY
    echo $OPENAI_API_BASE
    ```


5. See results of all experiments;
    ```bash
    python3 main.py
    ```

6. You can edit main.py (from line 100 to line 172) to run your own experiments. 

## Contact 
TBD

## Acknowledgements
TBD

## Citation
TBD