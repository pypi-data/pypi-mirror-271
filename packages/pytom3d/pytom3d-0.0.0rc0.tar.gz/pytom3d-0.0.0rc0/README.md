# PyToM-3D: Python Topography Manipulator in 3D

PyToM-3D is a Python package to transform and fit 3-dimensional topographies. It provides methods to perform traditional geometric transformations and visualise the results as well.

[Geometric Transformations](#geometric-transformations)

- [Translation](#translation)

- [Rotation](#rotation)

- [Flip](#flip)

- [Cut](#cut)

[Singular Value Decomposition (SVD)](#svd)

- [Introduction](#intro-svd)

- [Using SVD](#using-svd) 

[Data Regression](#data-regression)

- [Gaussian Process Regression](#gpr)

- [Spline Fitting](#spline)

[Data Inspection](#data-inspection)

- [2D Views](#2d)

- [3D Views](#3d)

# Initialising a Topography

Initially, we need to istantiate a `Topography`:

```python
t = Topography()
```

We have a multitude of options:

- reading from a `.csv` file;

- generating a grid and add synthetic data.

# Geometric Transformations <a name="geometric-transformations"></a>

In order to understand each geometric transformation remember that the points of the topography are stored in the attribute ```P```, which is a $N\times 3$ matrix:

$$\mathbf{P} = \begin{bmatrix}  x_1 & y_1 & z_1 \\\ x_2 & y_2 & z_2 \\\ \vdots & \vdots & \vdots \\\ x_N & y_N & z_N\end{bmatrix},$$

where $\mathbf{p}_i = \left[x_i\quad y_i \quad z_i\right]$ is the *i*th point of the topography. In practice the altitude $z_i$ is determined upon a latent function of the coordinates, hence $z_i = f(x_i, y_i)$.

## Translation <a name="translation"></a>

Let us define a vector $\mathbf{v} = \left[x_v\quad y_v\quad z_v \right]$. By calling:

```python
t.translate([xv,yv,zv])
```

we translate $\mathbf{P}$ by $\mathbf{v}$ as:

$$\mathbf{p}_i \leftarrow \mathbf{p}_i + \mathbf{v}\quad\forall\ i = 1,2,\dots,N.$$

## Rotation <a name="rotation"></a>
This method performs the rotation about the centre given three rotation angles $\theta_x$, $\theta_y$, $\theta_z$. The method builds the corresponding rotation matrices:

$$\mathbf{R}_x = \begin{bmatrix}  1 & 0 & 0 \\\ 0 & \cos(\theta_x) & \sin(\theta_x) \\\ 0 & -\sin(\theta_x) & \cos(\theta_x) \\\ \end{bmatrix},$$

$$\mathbf{R}_y = \begin{bmatrix}  \cos(\theta_y) & 0 & \sin(\theta_y) \\\ 0 & 1 & 0 \\\ -\sin(\theta_y) & 0 & \cos(\theta_y) \end{bmatrix},$$

$$\mathbf{R}_z = \begin{bmatrix} \cos(\theta_z) & \sin(\theta_z) & 0 \\\  -\sin(\theta_z) & \cos(\theta_z) & 0 \\\ 0 & 0 & 1 \end{bmatrix},$$

$$\mathbf{R} = \mathbf{R}_x\mathbf{R}_y\mathbf{R}_z.$$

Then each point is rotated as:

$$\mathbf{p}_i \leftarrow \mathbf{R}\mathbf{p}_i.$$

This is accomplished via:

```python
t.rotate(t_deg=[t_x, t_y, t_z])
```

The method supports passing a rotation matrix too:

```python
t.rotate(rot_mat=R)
```

In case on wishes to rotate about a given centre $c=\left[c_x\quad c_y\quad c_z\right]^\top$, they would call the wrapper method:

```pyhton
t.rotate_about_centre(c=[c_x, c_y, c_z]t_deg=[t_x, t_y, t_z])
```

or by providing a rotation matrix `rot_mat`.


## Flip <a name="flip"></a>

This method allows mirroring data with respect to a given vector $\mathbf{v}=\left[v_x\quad v_y\quad v_z \right]$ which represent the outward normal of the intended flipping plane. Assuming one wishes to flip the data about the $yz$ plane, they would define $\mathbf{v}=\left[-1\quad 1\quad 1 \right]$, and call:

```python
t.flip([-1,1,1])
```

This operation performs $(\mathbf{p}_i = \left[x_i\quad y_i \quad z_i\right])$:

$$\left[x_i\quad y_i \quad z_i\right] \leftarrow \left[x_i\cdot v_x\quad y_i\cdot vy\quad z_i\cdot vz\right] \quad\forall\ i = 1,2,\dots,N.$$

## Cut <a name="cut"></a>

Suppose you would like to remove some outliers from topography. Although the same procedure applies to the other axes identically, we focus on the z-axis. We also assume two threshold $l$ and $u$, whereby we filter each $i$th datum using the criterion:

$$z_i \leftarrow z_i:\quad z_i > l\quad \text{and}\quad z_i < u.$$

To do so, we call:

```python
t.cut(ax="z", lo=l, up=u, out=False)
```

If `out=True` the method keep the points complying with:

$$z_i \leftarrow z_i:\quad z_i < l\quad \text{and}\quad z_i > u.$$

# Singular Value Decomposition (SVD) <a name="svd"></a>

## Introduction <a name="intro-svd"></a>
Let $\mathbf{P}$ be a generic matrix belonging to $\mathbb{R}^{m\times n}$. SVD allows $\mathbf{P}$ to be decomposed into the product of three matrices:

$$\mathbf{P} = \mathbf{U}\mathbf{S}\mathbf{V^\top},$$

where $\mathbf{U}\in \mathbb{R}^{m\times m}$ , and $\mathbf{V}^\top\in \mathbb{R}^{n\times n}$ are called respectively *left-* and *right-principal* matrix (both orthonormal), whereas $\mathbf{S}\in \mathbb{R}^{m\times n}$ is the so-called Singular Value Matrix.

We do SVD via:

```python
t.svd()
```

## Using SVD <a name="using-svd"></a>

Suppose that the points of the topography are distributed according to three preferred directions, which are identifiable by visual inspection. Assume that these directions define a reference frame $`\{x_s,y_s,z_s\}`$. Conversely, assume that the points forming the point topography have been acquired with respect to another (arbitrary) reference frame $`\{x,y,z\}`$, which (unfortunately) is not aligned with $`\{x_s,y_s,z_s\}`$. However, expressing the acquired points with respect to $`\{x_s,y_s,z_s\}`$ would be of considerable interest, e.g. for further numerical computations. From a mathematical standpoint, a change of reference frame, i.e. change of basis, from $`\{x,y,z\}`$ to $`\{x_s,y_s,z_s\}`$ is sought as well as the associated matrix.

In this instance, it is therefore evident that finding this matrix by inspection, intuition or 'trial & error' becomes preposterous. SVD holds the potential to compute such a matrix almost automatically. Let $\mathbf{P}\in\mathbb{R}^{N\times 3}$ be the matrix representing the topography. In order to apply the SVD and obtain satisfactory results, the whole point topography should be translated to $-G$ (the centroid). Following, the SVD applied to $\mathbf{P}$ provides $\mathbf{U}\in \mathbb{R}^{N\times N}$ , $\mathbf{S}\in \mathbb{R}^{N\times 3}$, and $\mathbf{V}^\top\in \mathbb{R}^{3\times 3}$.  In particular, $\mathbf{V}$ realises the change of basis. Hence, each point of $\mathbf{P}$, namely $\mathbf{p}_i$, will be rotated according to $\mathbf{V}^\top$:

$$\mathbf{p}_i \leftarrow \mathbf{V}^\top\mathbf{p}_i.$$

To perform this, just invoke:

```python
t.rotate_by_svd()
```

which wraps `rotate_about_centre`.

Since $\mathbf{V}^\top$ is orthonormal, the topography is subjected to a *rigid* rotation: neither stretching nor deformations occur. If the $\det{V^\top} \simeq -1$, the transformed topography (through SVD) may need flipping. To overcome this, just use ```flip``` ([Flip](#flip)).

# Data Regression <a name="data-regression"></a>

## Gaussian Process Regression (GPR) <a name="gpr"></a>

PyToM-3D wraps the regressors of scikit-learn, amongst which GPR. In this instance, the topography is modelled as the following regression model:

$$t(x,y) = f(x,y) + \epsilon(0, \sigma),$$

where $f(x,y)$ is a latent function modelling the topography and $\epsilon$ is Gaussian noise having null mean and $\sigma$ as the standard deviation. Next, a Gaussian Process is placed over $f(x,y)$:

$$f \sim GP(M(x,y), K(x,y)),$$

where $M(x,y)$ is the mean, and $K(x,y)$ is the kernel (covariance function). Initially, we need to define the kernel:

```python
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
kernel = ConstantKernel() * RBF([1.0, 1.0], (1e-5, 1e5)) \
                + WhiteKernel(noise_level=1e-3, noise_level_bounds=(1e-5, 1e5))
```

which represents a typical squared exponential kernel with noise:

$$K(\mathbf{x},\mathbf{x}') = C \exp{\left(\frac{\Vert \mathbf{x} - \mathbf{x}'\Vert^2}{l^2}\right)} + \sigma_{ij},$$

where:

$$\sigma_{ij} = \delta_{ij} \epsilon,\quad \mathbf{x}=\left[x,y\right]$$

and $\delta_{ij}$ is Kronecker's delta applied to any pair of points $\mathbf{x}_{i}$, $\mathbf{x}_j$.

Finally, we invoke:

```python
from sklearn.gaussian_process import GaussianProcessRegressor as gpr
t.fit(gpr(kernel=kernel))
```

and the GPR is fit. To predict data:

```python
t.pred(X)
```

where `X` is $M \times 2$ a numpy array containing the $x$ and $y$ coordinates of an evaluation grid.

## Spline Fitting <a name="spline"></a>

PyToM-3D allows user to fit data by bi-variate splines specifically wrapping `scipy.interpolate.bisplrep`. Modelling the topography as a two-variable function $f(x,y)$, we approximate it as:

$$f(x,y) \approx \sum_{i=1}^{m} \sum_{j=1}^{n} C_{ij} Q_{i,r}(x) Q_{j,s}(y), $$

where $Q_{i,r}$ and $Q_{j,s}$ are polynomials of degree $r$ and $s$ respectively. Additionally, $m$ and $n$ are the number of control points (aka knots) distributed along the $x$- and $y$-axis. Lastly, $C_{ij}$ are the trainable coefficients, which are determined upon the points of the topography.

To fit a bi-variate spline to the data, we call:

```python
from scipy.interpolate import bisplrep
t.fit(bisplrep, kx, ky, tx, ty)
```

where `kx`, `ky` represent the above-mentioned $r$ and $s$ (degree of the polynomials), and `tx` and `ty` are the control points, which are expected to be `np.ndarray`-like objects. Once the fitting is done we forecast the topography elsewhere by:

```python
t.pred(X)
```

# Data Inspection <a name="data-inspection"></a>
PyToM-3D offers afew visualisation utilities to inspect the data. Particularly, it exploits `pytom3d.Viewer.Viewer` class. So we need one istance of this class before proceeding:

```python
from pytom3d.Viewer import Viewer
v = Viewer()
```

## 2D Views <a name="2d"></a>

We can easily display the three Cartesian  views of the topography `t`, by using:

```python
v.views2D(t)
```

The method can take an indefinite number of input topographies.

## 3D Scatter <a name="3d"></a>

Similarly we can easily the 3D scatter plot of `t` with:

```python
v.scatter(t)
```

The method accepts an indefinite number of input topographies.