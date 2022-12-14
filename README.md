# cs4352-final-project
This repository contains code used to pull and analyze Twitter network data and node attributes. The project focused on created a GCN to predict verification across three representative networks and an artifically constructed network. Huge props to Steve Hedden for provided much of the baseline code for network scraping

## Important Files
- **[Scraping/Tweepy Network Scraping - Anyone.ipynb](https://github.com/MJRAJ01/cs4352-final-project/blob/main/Scraping/Tweepy%20Network%20Scraping%20-%20Anyone.ipynb)**: JuPyter Notebook that contains replicatable code to pull network and node information from a source node. The bulk of the scraping for this project lives here.
- **[Datasets Folder](https://github.com/MJRAJ01/cs4352-final-project/tree/main/Datasets)**: Contains the complete replications of the graphs used in this project in a .gml format to import into NetworkX and includes both network connections and node information
- **[Prediction Verfiication GCN.ipynb](https://github.com/MJRAJ01/cs4352-final-project/blob/main/Prediction%20Verification%20GCN.ipynb)**: Contains the GCN code used to train and test our models against the Twitter data we collected
- **[Twitter Influence and Verification.pdf](https://github.com/MJRAJ01/cs4352-final-project/blob/main/Twitter%20Influence%20and%20Verification%20-%20Atwood%2C%20Raj%2C%20Schultz.pdf)**: Final paper with full methodology and results for the explortation of Twitter verification
