# Paper Title

**Author:** Bouchra Fakher
**Published in:** 2024 IWCMC 
**Date:** 2024
**DOI:** [[DOI link]](https://doi.org/10.1109/IWCMC61514.2024.10592511)

## Abstract

Federated Learning (FL) is rapidly growing in popularity as a decentralized approach and is being adopted in smart building systems and energy forecasting without accessing sensitive data. Specifically, clients train their models using their own data. After that, only their model parameters are sent to the central server, which aggregates them by averaging the weights and then sends back the newly formed model to each client. However, challenges arise when dealing with heterogeneous multivariate time-series data with different distributions. This leads to higher-performing clients contributing to the global update more than the others, and slower convergence where the global model takes more time to generalize across the clients. In this paper, we propose an enhanced aggregation approach, where the server sorts clients’ models based on their local training losses before swapping them all consecutively according to the best and worst-performing ones. Our proposed approach is applied to a smart building dataset and compared with two other FL approaches from the literature. Our simulation results demonstrate improved forecasting precision for each client and faster convergence. Moreover, we optimized the global model’s evaluation error scores and overall loss, reduced the communication rounds required for convergence, and ensured less bias and more fairness between clients during each training cycle.

# If you use this work, please cite it as follows:

```bibtex
@inproceedings{fedlbs,
  title={Fedlbs: Federated learning loss-based swapping approach for energy building’s load forecasting},
  author = {Fakher, Bouchra and Brahmia, Mohamed-el-Amine and Al Samara, Mustafa and Abouaissa, Abdelhafid},
  booktitle={2024 International Wireless Communications and Mobile Computing (IWCMC)},
  pages={949--954},
  year={2024},
  organization={IEEE}
}
