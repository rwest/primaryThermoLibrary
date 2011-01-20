
ALL = s1.out s2.out s4.out t1.out t2.out \
      cyclopropene12diyl.out cyclopropynylidyne.out
LIBRARY = Library.txt
DICTIONARY = Dictionary.txt

data: $(LIBRARY) $(DICTIONARY)

$(LIBRARY): $(ALL) combine.py
	python combine.py $(ALL) | tee $(LIBRARY)

$(DICTIONARY): *.chemgraph
	cat *.chemgraph > $(DICTIONARY)

cantherm: $(ALL)

%.out : %.dat
	python ../CanTherm/source/CanTherm.py $< | tee $@
	mv cantherm.out $*.log

clean:
	rm -f $(ALL) $(LIBRARY) $(DICTIONARY)