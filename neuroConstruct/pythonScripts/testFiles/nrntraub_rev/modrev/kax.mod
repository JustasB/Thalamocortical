TITLE Potasium Type A current for RD Traub, J Neurophysiol 89:909-921, 2003

COMMENT

	Implemented by Maciej Lazarewicz 2003 (mlazarew@seas.upenn.edu)

ENDCOMMENT

INDEPENDENT { t FROM 0 TO 1 WITH 1 (ms) }

UNITS { 
	(mV) = (millivolt) 
	(mA) = (milliamp) 
} 
NEURON { 
	SUFFIX kax
	USEION k READ ek WRITE ik
	RANGE gbar, ik, m, h, alphah, betah, alpham, betam, mtau, htau
}
PARAMETER { 
	gbar = 0.0 	(mho/cm2)
	v (mV) ek 		(mV)  
	xn = 0
} 
ASSIGNED { 
	ik 		(mA/cm2) 
	minf hinf 	(1)
	mtau (ms) htau 	(ms) 
	alphah (/ms) betah	(/ms)
	alpham (/ms) betam	(/ms)
} 
STATE {
	m h
}
BREAKPOINT { 
	SOLVE states METHOD cnexp
	ik = gbar * m * m * m * m * h * ( (v-xn) - ek ) 
:	debugging:
	alphah = hinf/htau
	betah = 1/htau - alphah
	alpham = minf/mtau
	betam = 1/mtau - alpham
} 
INITIAL { 
	settables(v) 
:	m  = minf
	m  = 0
	h  = hinf
:	h = 0.208608 : from F tcr cc run
} 
DERIVATIVE states { 
	settables(v) 
	m' = ( minf - m ) / mtau 
	h' = ( hinf - h ) / htau
}

UNITSOFF 

PROCEDURE settables(v (mV)) { 
	TABLE minf, hinf, mtau, htau  FROM -120 TO 40 WITH 641

	minf  = 1 / ( 1 + exp( ( - (v-xn) - 60 ) / 8.5 ) )
	mtau = 0.185 + 0.5 / ( exp( ( (v-xn) + 35.8 ) / 19.7 ) + exp( ( - (v-xn) - 79.7 ) / 12.7 ) )
	hinf  = 1 / ( 1 + exp( ( (v-xn) + 78 ) / 6 ) )
	if( (v-xn) <= -63 ) {
		htau = 0.5 / ( exp( ( (v-xn) + 46 ) / 5 ) + exp( ( - (v-xn) - 238 ) / 37.5 ) )
	}else{
		htau = 9.5
	}
}

UNITSON
