********************************************************************************
*
*	Project: Fixed Effect Monte Carlo
*	About: DGP for FE and compare results for reg & reghdfe (without and with FE)
*	Date: Feb 26th 2022
*	
********************************************************************************

cap log close
clear all
set more off 
set maxvar 100000
set matsize 11000

*------------------------------------------------------------------------------*
* 							Prep: DGP										   *
*------------------------------------------------------------------------------*

cd "/Users/BrianChung/Dropbox/Github"

set obs 10000000
set seed 123456

local beta1 = 3
local beta2 = 4
local beta3 = 2
	
gen pid = _n

gen theta_i = 0
replace theta_i = 1 if pid <=250

tostring pid, gen(pidstr)
gen phi_j = 0
foreach last in 1 3 5 7 9{
replace phi_j = `last' if substr(pidstr, 1, 1) == "`last'"
}

gen x1 = rnormal(5,1)+3*theta_i + phi_j/2
gen x2 = rnormal(10,2)
gen x3 = rnormal(6,1)+phi_j/3

gen y = `beta1'*x1 + `beta2'*x2 + `beta3'*x3 + 5*theta_i + phi_j + rnormal(0,3)
save RegPyMat/matrix_fe, replace	
clear


*------------------------------------------------------------------------------*	
* 							Analysis										   *
*------------------------------------------------------------------------------*	
log using "./RegPyMat/matrix_fe", replace

use RegPyMat/matrix_fe
reg y x1 x2	x3

reghdfe y x1 x2 x3, a(theta_i phi_j)
	
log close	
