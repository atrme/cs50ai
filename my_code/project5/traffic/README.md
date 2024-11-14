*__Tip:__ [Data set](https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb.zip) is needed to run the code*

## Trials

Diffenrent combinations of configuration is tried as bellows:

**number of filters:** [16, 32, 64]  
**number of nodes in hidden layer:** [32, 64, 128]  
**dropout rate in hidden layer:** [0, 0.25, 0.5]  

## Findings

- The configuration and accuracies of The 3 best models(with highest accuracy) as below:  
    - 1st: (filters: 32, nodes: 128, dropout rate: 0), accuracy: 0.9721  
    - 2nd: (filters: 64, nodes: 128, dropout rate: 0.25), accuracy: 0.9709  
    - 3rd: (filters: 64, nodes: 128, dropout rate: 0.5), accuracy: 0.9707

- The more **filters**, **nodes in hidden layer** are used, the more time is needed to build model

- Generally, the more **nodes in hidden layer** is, the more accurate model can be

- In model with less **filters**, high **dropout rate** results in low accuracy