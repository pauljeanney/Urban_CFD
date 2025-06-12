#!/bin/bash
##----------------------- Start job description -----------------------
#SBATCH --partition=standard
#SBATCH --job-name=fine
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=20
#SBATCH --mem-per-cpu=16GB
#SBATCH --time=130:00:00
#SBATCH --mail-user=paul.jeanney@arup.com
#SBATCH --mail-type=ALL
#SBATCH --output=out-%j.log
#SBATCH --error=err-%j.log

##------------------------ End job description ------------------------
module purge && module load OpenFOAM/8-foss-2020a
module load M4/1.4.19
source $FOAM_BASH

# rm -rf processor*

# # # # # Decompose
# decomposePar > log.decomposePar

# topoSet for the .stl pollution zone
srun --ntasks=80 --export=ALL,IBV_FORK_SAFE=1 topoSet -parallel > log.topoSet

# # # run pollutant model
mpirun -np 80 -x IBV_FORK_SAFE=1 -x UCX_IB_REG_METHODS=direct simpleConlyFoam -parallel > log.simpleConlyFoam

## Reconstruct 
reconstructPar -latestTime > log.reconstructPar

# # # # For the VTK post-processing
# foamToVTK -latestTime
# foamToVTK -time '19001:latestTime'

