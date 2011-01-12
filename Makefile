
ALL = s1.out s2.out s4.out t1.out t2.out
RESULTS = results.txt

$(RESULTS): $(ALL) combine.py
	python combine.py $(ALL) | tee $(RESULTS)

all: $(ALL)

%.out : %.dat
	python ../CanTherm/source/CanTherm.py $< | tee $@
	mv cantherm.out $*.log

clean:
	rm -f $(ALL) $(RESULTS)