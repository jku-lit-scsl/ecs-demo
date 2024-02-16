# Cyber-Resilient Edge Computing: A Holistic Approach with Multi-Level MAPE-K Loops

Welcome to the GitHub repository for the proof of concept implementation accompanying the paper titled "Cyber-Resilient Edge Computing: A Holistic Approach with Multi-Level MAPE-K Loops." This repository serves as a demonstration of the concepts and methodologies proposed in the paper, offering a tangible illustration of cyber-resilient edge computing systems.

## About the Paper

As edge computing continues to play a pivotal role in modern computing architectures, ensuring robust cybersecurity becomes imperative. 
This paper introduces our emerging results on a comprehensive approach to bolster the cyber-resilience of edge computing systems by incorporating the MAPE-K (Monitor, Analyze, Plan, Execute, and Knowledge) loop.
The proposed methodology involves the application of the MAPE-K loop at different levels of an edge computing architecture, aiming to create a holistic defense mechanism against cyber attacks.
We present a prototype of our framework and assess its viability and efficacy by leveraging real-world edge devices deployed in an industrial production setting.
Initial evidence from our results suggests that this novel approach leads us to reconsider how we construct more resilient edge computing architectures.

## Repository Contents

- Proof of Concept Implementation: A practical demonstration of the proposed cyber-resilient edge computing framework, showcasing its functionality and effectiveness.
- Documentation: Documentation to guide you through setting up and running the proof of concept. (c.f. "Getting Started")
- Additional Resources: Supplementary materials, datasets, and resources used in the implementation and evaluation (c.f. `evaluation` and `dos`).

## Getting Started

There is a shell script for setting up the environment.
It assumes the system it is running on is Ubuntu 20.04:

- `chmod +x setup.sh`
- `sudo ./setup.sh`
- update `config/config.py` with IPs of own machine + the server/client IPs
- start project running the virtual environment (printed out by the script) with the `main.py` file as root

Note: 
For convenience in setting up the evaluation some additional commands are contained in the `setup.py` file (e.g., setting the timezone to central Europe etc.). 
Before executing the script, check out what it does.

## Contact

For any questions, feedback, or inquiries related to the paper or this repository, feel free to contact the authors directly.

Thank you for your interest in our work. We hope you find this repository informative and useful in your exploration of cyber-resilient edge computing.
