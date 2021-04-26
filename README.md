
<br />
<p align="center">
  <a href="https://github.com//025georgialynny/seminar">
  </a>

  <h3 align="center">Georgia Smith Senior Captone Project 2021</h3>

  <p align="center">
    <br />
    <a href="https://github.com//025georgialynny/seminar/present.ipynb"><strong>View the Final Code in Jupyter</strong></a>
    <br />
      <br />
    <a href="
  https://docs.google.com/presentation/d/1A_M0flqeaVUBLYcDWxXpWqazK4LhR_cObaeh_lXm0Ao/edit?usp=sharing"><strong>Final Presentation Available Here</strong></a>
    <br />
    <br />
     Usage: This code was written in Python 3.8.5
    <br />
     Requirements are listed in <a href="/requirements"><strong>requirements</strong></a>
    <br />
     Cuda is required to run
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Mental illness can be a burden for those whose lives are impacted from it, es-pecially those with serious mental illness. This burden is exasperated whenmultiple mental illnesses co-occur - a phenomenon known as psychiatric co-morbidity (further referred to as comorbidity). Recently, the field of psycho-metric analysis,  or the analysis of psychological measurement techniquesand theories, has had two major perspectives of how two analyze comorbid-ity:  the latent variable perspective and the network perspective.  We extendCramer et.  al.’s (2010) initial hypothesis of the usability of network analy-sis to latent network path analysis, identifying pathways of comorbidity toidentify causal symptoms of disorders. We will do this in a multi-stage pro-duction. First, we will develop networks of individuals in the NCSR buildingdirected graphs based on the onset age of symptoms.  Then, we will com-bine all of the networks for individuals with a comorbid diagnoses using theDeep Graph Library(Wang et al., 2019) (DGL). We then use the combinednetwork to identify latent symptom pathways using Graph Neural Networksusing SAGE Graphs with a backend of convolutional neural networks andLong Short-Term Memory (LSTM) Recurrent Neural Networks (RNN).

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com//025georgialynny/seminar.git
   ```




<!-- USAGE EXAMPLES -->
## Usage
1. Install all <a href="/requirements"><strong>requirements</strong></a>

2. Run ```python3 extract_age_vars.py```

3. Run ```python3 make_indiv_graphs.py```

4. Run ```./get_dsm_graphs.py```






<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact


Project Link: [https://github.com/025georgialynny/seminar](https://github.com/025georgialynny/seminar)
