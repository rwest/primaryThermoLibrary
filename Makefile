
ALL = s1.out s2.out s4.out t1.out t2.out

all: $(ALL)

%.out : %.dat
	python ../CanTherm/source/CanTherm.py $< | tee $@
	mv cantherm.out $*.log
