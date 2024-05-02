# NODE
This is a simple example package. And it is an algorithm for deconvolution of spatial transcriptomic data.

NODE is a Python-based package for spatial transcriptomic data. NODE is based on an optimization search model and non-negative least squares problem to use scRNA-Seq data for deconvoluting spatial transcriptomics data and inferring spatial communications. In deconvolution, Node can infer cell number and cell type from spatial transcriptomics data by referring to single-cell data. In inference of spatial communication, NODE can infer the information flow in space.

You can use [this](https://github.com/wzdrgi/NODE) or (wangzedong23@mails.ucas.ac.cn) to contact us.

# Background
NODE is a Python-based package for spatial transcriptomic data. NODE is based on an optimization search model and non-negative least squares problem to use scRNA-Seq data for deconvoluting spatial transcriptomics data and inferring spatial communications. In deconvolution, Node can infer cell number and cell type from spatial transcriptomics data by referring to single-cell data. In inference of spatial communication, NODE can infer the information flow in space.
# Usage
NODE require users to provide four types of data for deconvolution and inferring the spatial communication.
Firstly the user needs to download and unzip it locally.
The user can then use sys (python package) to find the directory for NODE and import it, followed by using the
The specific form of the data is shown below:
## Sc_data (Single-cell data) 
Sc_data needs to carry the gene name and cell name as a square, (0, 0) can specify any name, such as 'gene' and 'name'. Sc_data rows represent genes, columns represent cells, and each column represents the expression of a gene. The genes' name of sc_data must correspond to the genes' name of st_data.

sc_data is shown below:

    name      cell1      cell2 

    gene1     5.0        3.0

    gene2     2.0        0.0

## St_data (Spatial transcriptomics data) 
St_data needs to carry the genes' name and spots' name as a square,(0,0) can specify any name, such as 'spot' and 'name'. st_data rows represent genes, columns represent spots, and each column represents the expression of a gene in a spot. The genes' name of st_data must correspond to the genes's name of sc_data.

st_data is shown below:

    spot     spot1     spot2

    gene1     4.0      8.0

    gene2     0.0      2.0

## cell_type (single-cell categorization data)
cell_type needs to carry the cell name and its cell type. celltype's first line is title information including name and cell type name. Cell_type rows represent each cell. The name column of cell_type must correspond to the first row of sc_data, and the cell names in it must be the same.

cell_type is shown below:
    
    name          celltype

    cell1         type1

    cell2         type2

## st_coordinate (coordinate data of spatial transcriptomic data)
st_coordinate needs to carry the spots' name and theirs coordinates. St_coordinate 's first line is title information including 'spot', 'x', and 'y'. St_coordinate rows represent spot. St_coordinate's spot column must correspond to the first row of st_data, where the names of the spots must be the same.

st_coordinate is shown below:

    spot    x       y

    spot1   8       20

    spot2   10      12
