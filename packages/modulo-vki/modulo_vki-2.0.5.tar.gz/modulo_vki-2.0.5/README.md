

MODULO - latest update 2.0
===================

This repository contains version 2.0 of MODULO (MODal mULtiscale pOd), a software developed at the von Karman Institute to perform data-driven modal decompositions and, in particular, the Multiscale Proper Orthogonal Decomposition (mPOD).

The old version based on MATLAB implementation and related GUI is no longer maintained but will remain available on the branch "Old_Matlab_Implementation". We also keep the first Python implementation in the branch "Old_Python_Implementation". See the Readme file in these branches for more information.

#### Documentation

The full documentation is available at https://modulo.readthedocs.io/en/latest/intro.html.
This documentation is stored alongside the source code and linked to a specific version of MODULO.

## What is MODULO, and what are data-driven decompositions?

MODULO allows to compute data-driven decompositions of experimental and numerical data. To have a concise overview of the context, we refer to: 

- Ninni, D., Mendez, M. A. (2020), "MODULO: A Software for Multiscale Proper Orthogonal Decomposition of data", Software X, Vol 12, 100622, https://doi.org/10.1016/j.softx.2020.100622.

- Poletti, R., Schena, L., Ninni, D., Mendez, M.A (2024) "MODULO: a python toolbox for data-driven modal decomposition", Submitted to Journal of Open Source Software. Preprint available [here](https://www.researchgate.net/publication/376885484_MODULO_a_python_toolbox_for_data-driven_modal_decomposition)

The first article also presents the first version of MODULO (available in the OLD_Matlab_Implementation branch) and its GUI developed by D. Ninni. The second introduces MODULO v2 in this branch and alternative open source projects. While many projects allows for computing common decompositions such as POD, DMD and the SPODs, MODULO is currently the only opensource project allowing to compute the mPOD.

For a more comprehensive overview on the theory of data-driven decompositions, we refer to the chapter:

- Mendez, M. A. (2023) "Generalized and Multiscale Modal Analysis". In : Mendez M.A., Ianiro, A., Noack, B.R., Brunton, S. L. (Eds), "Data-Driven Fluid Mechanics: Combining First Principles and Machine Learning". Cambridge University Press, 2023:153-181. https://doi.org/10.1017/9781108896214.013. The pre-print is available at https://arxiv.org/abs/2208.12630. 

and the article that first presented the complete treatment of the mPOD :

- Mendez, M. A., Balabane, M., Buchlin, J.-M. (2019) "Multi-Scale Proper Orthogonal Decomposition of Complex Fluid Flows" Journal of Fluid Mechanics 870:988-1036, https://doi.org/10.1017/9781108896214.013. The pre-print is available at https://arxiv.org/abs/2208.12630. 

Ongoing works on nonlinear methods are discussed here:

- Mendez, M. A. (2023) "Linear and Nonlinear Dimensionality Reduction from Fluid Mechanics to Machine Learning", Meas. Sci. Technol. 34(042001), https://doi.org/10.1088/1361-6501/acaffe. The pre-print is available at https://arxiv.org/abs/2208.07746.   

## What is new in this V 2.0? 

This version expands considerably the version v1 in "Old_Python_Implementation", for which a first tutorial was provided by L. Schena in https://www.youtube.com/watch?v=y2uSvdxAwHk. 
The major updates are the following :

1. Faster EIG/SVD algorithms, using powerful randomized svd solvers from scikit_learn (see [this](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html) and [this](https://scikit-learn.org/stable/modules/generated/sklearn.utils.extmath.randomized_svd.html) ). It is now possible to select various options as "eig_solver" and "svd_solver", offering different trade-offs in terms of accuracy vs computational time.

2. In addition to the traditional POD computation using the K matrix (Sirovinch's method), it is now possible to compute the POD directly via SVD using any of the four "svd_solver" options.
This is generally faster but requires more memory.

3. Faster subscale estimators for the mPOD: the previous version used the rank of the correlation matrix in each scale to define the number of modes to be computed in each portion of the splitting vector before assembling the full basis. This is computationally very demanding. This estimation has been replaced by a frequency-based threshold (i.e. based on the frequency bins within each portion) since one can show that the frequency-based estimator is always more "conservative" than the rank-based estimator.

4. Major improvement on the memory saving option: the previous version of modulo always required in input the matrix D. Then, if the memory saving option was active, the matrix was partitioned and stored locally to free the RAM before computing the correlation matrix (see [this tutorial by D. Ninni](https://www.youtube.com/watch?v=LclxO1WTuao)). In the new version, it is possible to initialize a modulo object *without* the matrix D (see exercise 5 in the examples). Instead, one can create the partitions without loading the matrix D.

5. Implementation of Dynamic Mode Decomposition (DMD) from [Schmid, P.J 2010](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/dynamic-mode-decomposition-of-numerical-and-experimental-data/AA4C763B525515AD4521A6CC5E10DBD4).

6. Implementation of the two Spectral POD formulations, namely the one from [Sieber et al 2016](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/spectral-proper-orthogonal-decomposition/DCD8A6EDEFD56F5A9715DBAD38BD461A), and the one from [Towne et al 2018](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/spectral-proper-orthogonal-decomposition-and-its-relationship-to-dynamic-mode-decomposition-and-resolvent-analysis/EC2A6DF76490A0B9EB208CC2CA037717)

7. Implementation of a kernel version of the POD, in which the correlation matrix is replaced by a kernel matrix. This is described in Lecture 15 of the course [Hands on Machine Learning for Fluid dynamics 2023](https://www.vki.ac.be/index.php/events-ls/events/eventdetail/552/-/online-on-site-hands-on-machine-learning-for-fluid-dynamics-2023). See also [this](https://arxiv.org/abs/2208.07746).

8. Implementation of a formulation for non-uniform meshes, using a weighted matrix for all the relevant inner products. This is currently available only for POD and mPOD but allows for handling data produced from CFD simulation without resampling on a uniform grid (see exercise 4). It can be used both with and without the memory-saving option.

## New Tutorials 

The installation provides five exercises to explore MODULO's features while familiarizing with data-driven decompositions. These are available in the /exercise/ folder in plain Python format and jupyter notebooks. 

- Exercise 1. In this exercise, we consider the flow past a cylinder. The dataset was created via Large Eddy Simulations (LES) by Denis Dumoulin during his STP at VKI in 2016 (Report available on request). For convenience, the data was first mapped to a Cartesian grid. This test case is by far the most popular because it's well-known to have a simple low-order representation with modes that have nearly harmonic temporal structures. We compute the POD and the DMD and compare the results... the difference between DMD and POD modes is hardly distinguishable!

- Exercise 2. We consider the flow of an impinging gas jet, taken from [this](https://arxiv.org/abs/1804.09646) paper. This dataset was collected via Time-Resolved Particle Image Velocimetry (TR-PIV). Only the first 200 POD modes were stored. This dataset has much richer dynamics than the previous one and cannot be easily approximated using a few modes. We use it to explore the differences between the DFT, the SPODs and the mPOD. These have different purposes and look for different features.

- Exercise 3. We take back the cylinder test case to explore the differences between the POD and the generalized Karhunen–Loève (KL) expansion in which a kernel matrix replaces the correlation matrix. The POD is a particular case of KL where the kernel function generating the kernel matrix is the plain inner product. Here, we also consider a Gaussian kernel. Different kernel functions define similarity in different ways and thus produce widely different modes. Different modal structures tell different stories about the dataset, but... what can you say about efficiency in data compression? 

- Exercise 4. We consider the flow past a cylinder again, but this time in transient conditions and on an experimental test case taken from [this](https://arxiv.org/abs/2001.01971) paper. In this exercise, you can reproduce the same results from the article to see how the mPOD allows to achieve both time and frequency localization without compromising much of the convergence of the POD. The dataset is quite large, so you might have difficulties handling it if you have less than 32 GB of RAM. But fear not: the memory saving feature allows to compute POD and mPOD without loading the data into memory!

- Exercise 5. We consider the flow of an impinging gas jet again, but this time on a numerical test case. This dataset was produced by Yannic Lowenstein during his STP at VKI at the end of 2023, with the help of Dr. Maria Faruoli. The Reynolds number is two orders of magnitude higher than in exercise 2, yet the flow features you will observe are pretty similar, at least qualitatively. From a learning perspective, the key feature of this test case is that the data is not available on a uniform grid. But fear not: with the new features, it is possible to compute the decompositions using appropriate weights!
 
